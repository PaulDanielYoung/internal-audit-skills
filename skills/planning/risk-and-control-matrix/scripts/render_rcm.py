"""Validate the supported RCM Markdown contract and write its offline HTML viewer."""

import argparse
import html
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit


FIELDS = (
    'Process ID', 'Process Title', 'Process Description',
    'Risk ID', 'Risk Title', 'Risk Description',
    'Inherent Risk Likelihood Rating', 'Inherent Risk Impact Rating',
    'Inherent Risk Score', 'Risk Band',
    'Control ID', 'Control Title', 'Control Description', 'Control Owner',
    'Frequency', 'Control Type', 'Control Nature', 'Planned Procedures',
)
LINK = re.compile(r'\[([^\[\]]+)\]\(([^\s()]+)\)')
BREAK = re.compile(r'<br\s*/?>', re.IGNORECASE)
MISSING_CONTROL = 'Control not yet identified'


class ValidationError(ValueError):
    """A named, user-correctable Markdown error."""


def fail(name, detail):
    raise ValidationError(f'{name}: {detail}')


def unknown(value):
    return (value.casefold() in ('', 'unknown', 'tbd', '?')
            or re.fullmatch(r'\[[^\[\]]+\]', value) is not None)


def cells(line, number):
    line = line.strip()
    if not line.startswith('|') or not line.endswith('|'):
        fail('TableStructure', f'line {number}: table lines need outer pipes')
    result, current = [], []
    i = 1
    while i < len(line):
        char = line[i]
        if char == '\\' and i + 1 < len(line) and line[i + 1] in '|\\':
            current.append(line[i + 1])
            i += 2
            continue
        if char == '|':
            result.append(''.join(current).strip())
            current = []
        else:
            current.append(char)
        i += 1
    if current or len(result) != len(FIELDS):
        fail('TableStructure', f'line {number}: expected {len(FIELDS)} cells')
    return result


def parse(source):
    lines = source.splitlines()
    candidates = [i for i, line in enumerate(lines) if line.lstrip().startswith('|')]
    if not candidates:
        fail('TableStructure', 'one matrix table is required')
    start = candidates[0]
    end = start
    while end < len(lines) and lines[end].strip():
        end += 1
    if any(i >= end for i in candidates):
        fail('TableStructure', 'additional table outside the matrix')
    if end - start < 3:
        fail('TableStructure', 'header, separator, and data row required')
    if tuple(cells(lines[start], start + 1)) != FIELDS:
        fail('TableStructure', 'required column names/order differ; see RENDERER.md')
    if not all(re.fullmatch(r':?-{3,}:?', cell)
               for cell in cells(lines[start + 1], start + 2)):
        fail('TableStructure', f'line {start + 2}: invalid separator')
    rows = [(i + 1, cells(lines[i], i + 1)) for i in range(start + 2, end)]
    before, after = lines[:start], lines[end:]
    # A pipe-table without outer pipes is also unsupported, even in notes.
    for line in before + after:
        if re.search(r'(?:^|\|)\s*:?-{3,}:?\s*\|', line):
            fail('TableStructure', 'additional or malformed table in surrounding prose')
    return before, rows, after


def methodology(lines):
    config = {
        'likelihood': [1, 2, 3, 4, 5], 'impact': [1, 2, 3, 4, 5],
        'bands': [('Low', 1, 4), ('Moderate', 5, 9), ('High', 10, 16), ('Critical', 17, 25)],
        'types': ['preventive', 'detective', 'corrective', 'directive', 'compensating', 'recovery'],
        'natures': ['manual', 'automated', 'IT-dependent'],
    }
    seen = set()
    for line in lines:
        if not line.strip().startswith('RCM '):
            continue
        match = re.fullmatch(r'RCM (\w+):\s*(.+)', line.strip())
        if not match or match[1] not in config or match[1] in seen:
            fail('InvalidMethodology', f'invalid or repeated directive: {line}')
        key, value = match.groups()
        seen.add(key)
        if key in ('likelihood', 'impact'):
            parts = [part.strip() for part in value.split(',')]
            if not all(re.fullmatch(r'[1-9]\d*', part) for part in parts):
                fail('InvalidMethodology', f'{key} needs positive integers')
            values = list(map(int, parts))
        elif key == 'bands':
            values = []
            for part in value.split(';'):
                band = re.fullmatch(r'\s*([^=;]+?)\s*=\s*(\d+)\.\.(\d+)\s*', part)
                if not band or unknown(band[1]):
                    fail('InvalidMethodology', 'bands need Name=min..max')
                values.append((band[1], int(band[2]), int(band[3])))
        else:
            values = [part.strip() for part in value.split(',')]
            if any(unknown(part) for part in values):
                fail('InvalidMethodology', f'{key} needs known nonempty names')
        keys = [v[0].casefold() if isinstance(v, tuple) else
                v.casefold() if isinstance(v, str) else v for v in values]
        if len(set(keys)) != len(keys):
            fail('InvalidMethodology', f'duplicate {key} values')
        config[key] = values
    expected = min(config['likelihood']) * min(config['impact'])
    for name, low, high in config['bands']:
        if low != expected or high < low:
            fail('InvalidMethodology', 'bands must be ascending and contiguous over the score range')
        expected = high + 1
    if expected != max(config['likelihood']) * max(config['impact']) + 1:
        fail('InvalidMethodology', 'bands must cover exactly the score range')
    return config


def ratings(row, config, where):
    numbers = []
    for index, key in ((6, 'likelihood'), (7, 'impact'), (8, 'score')):
        value = row[index]
        if unknown(value):
            numbers.append(None)
            continue
        if not re.fullmatch(r'[1-9]\d*', value):
            fail('InvalidRating', f'{where}: {FIELDS[index]} must be an integer or unknown')
        number = int(value)
        if key != 'score' and number not in config[key]:
            fail('InvalidRating', f'{where}: {key} {number} is outside the scale')
        if key == 'score' and not config['bands'][0][1] <= number <= config['bands'][-1][2]:
            fail('InvalidRating', f'{where}: score {number} is outside the scale')
        numbers.append(number)
    likelihood, impact, score = numbers
    product = likelihood * impact if likelihood is not None and impact is not None else None
    if product is not None and score is not None and score != product:
        fail('InconsistentScore', f'{where}: score must equal likelihood times impact')
    band_names = [b[0].casefold() for b in config['bands']]
    band = row[9].casefold()
    if not unknown(row[9]):
        if band not in band_names:
            fail('InconsistentBand', f'{where}: unsupported band {row[9]}')
        basis = score if score is not None else product
        _, low, high = config['bands'][band_names.index(band)]
        if basis is not None and not low <= basis <= high:
            fail('InconsistentBand', f'{where}: band does not match score')
    complete = all(n is not None for n in numbers) and not unknown(row[9])
    return (row[0], not complete, -band_names.index(band) if complete else 0,
            -score if complete else 0, row[10])


def validate(before, rows, after, config):
    entities = {'P': {}, 'R': {}, 'C': {}, 'gap': {}}
    combinations, order = set(), {}
    for line, row in rows:
        where = f'line {line}'
        for prefix, index in (('P', 0), ('R', 3), ('C', 10)):
            value = row[index]
            if prefix == 'C' and not value:
                continue
            if unknown(value):
                fail('MissingID', f'{where}: {FIELDS[index]} is required')
            if not re.fullmatch(prefix + r'-\d+', value):
                fail('InvalidID', f'{where}: invalid {FIELDS[index]} {value}')
        if not row[10] and (row[11] != MISSING_CONTROL or any(row[12:17])):
            fail('MissingControl', f'{where}: blank Control ID requires the missing-control title and empty attributes')
        if row[10] and row[11] == MISSING_CONTROL:
            fail('MissingControl', f'{where}: missing-control row must have no Control ID')
        combination = row[0], row[3], row[10]
        if combination in combinations:
            fail('DuplicateCombination', f'{where}: {combination}')
        combinations.add(combination)
        groups = [('P', row[0], row[:3]), ('R', row[3], row[3:10])]
        groups.append(('C', row[10], row[10:]) if row[10] else ('gap', row[3], row[17:]))
        for kind, identity, content in groups:
            previous = entities[kind].setdefault(identity, content)
            if previous != content:
                fail('ConflictingEntity', f'{where}: {identity} has conflicting {kind} content')
        order[line] = ratings(row, config, where)
        for index, key in ((15, 'types'), (16, 'natures')):
            if not unknown(row[index]) and row[index].casefold() not in [v.casefold() for v in config[key]]:
                fail('InvalidClassification', f'{where}: unsupported {FIELDS[index]} {row[index]}')
    ids = set().union(*(set(entities[kind]) for kind in ('P', 'R', 'C')))
    texts = before + [cell for _, row in rows for cell in row] + after
    for text in texts:
        for match in LINK.finditer(text):
            target = match[2]
            if target.startswith(('#P-', '#R-', '#C-')) and target[1:] not in ids:
                fail('DanglingReference', f'{target} has no matrix entity')
    return sorted(rows, key=lambda entry: order[entry[0]])


def safe_link(destination):
    if any(ord(char) < 32 or char == '\\' for char in destination):
        return False
    try:
        parts = urlsplit(destination)
    except ValueError:
        return False
    return not destination.startswith('//') and parts.scheme.lower() in ('', 'http', 'https', 'mailto')


def inline(text):
    result, start = [], 0
    for match in LINK.finditer(text):
        result.append(html.escape(text[start:match.start()]))
        label, target = match.groups()
        if safe_link(target):
            result.append(f'<a href="{html.escape(target, quote=True)}">{html.escape(label)}</a>')
        else:
            result.append(html.escape(match[0]))
        start = match.end()
    result.append(html.escape(text[start:]))
    return ''.join(result)


def rich_text(text):
    parts = BREAK.split(text)
    numbered = [re.fullmatch(r'\s*(\d+)\.\s+(.+)', part) for part in parts]
    if all(numbered):
        return '<ol>' + ''.join(f'<li value="{int(m[1])}">{inline(m[2])}</li>' for m in numbered) + '</ol>'
    return '<br>'.join(inline(part) for part in parts)


def prose(lines):
    result, paragraph = [], []

    def flush():
        if paragraph:
            result.append('<p>' + rich_text(' '.join(paragraph)) + '</p>')
            paragraph.clear()

    for line in lines:
        heading = re.fullmatch(r'(#{1,6})\s+(.+)', line)
        if not line.strip():
            flush()
        elif heading:
            flush()
            level = len(heading[1])
            result.append(f'<h{level}>{inline(heading[2])}</h{level}>')
        elif line.startswith('- ') or re.match(r'\d+\. ', line):
            flush()
            result.append('<p class="note">' + rich_text(line) + '</p>')
        else:
            paragraph.append(line)
    flush()
    return '\n'.join(result)


STYLE = """
body{font:15px/1.5 system-ui,sans-serif;color:#172b3a;background:#fafbfc;margin:24px}
a{color:#145d96}p{max-width:100ch}.viewer{color:#42586b}
.matrix{overflow:auto;max-height:78vh;border:1px solid #a9b8c5;background:white}
table{border-collapse:separate;border-spacing:0;min-width:3400px;width:100%}
th,td{padding:10px 12px;text-align:left;vertical-align:top;border-right:1px solid #ccd6de;border-bottom:1px solid #ccd6de}
thead{position:sticky;top:0;z-index:2;background:#173b54;color:white}
thead tr:first-child th{text-align:center;background:#102c40}th{font-weight:600}
td{min-width:95px;max-width:420px;overflow-wrap:anywhere}td:nth-child(3),td:nth-child(6),td:nth-child(13),td:nth-child(18){min-width:330px}
tbody tr:nth-child(even){background:#f1f5f8}ol{padding-left:24px;margin:0}li+li{margin-top:8px}
.unknown{color:#785009;font-style:italic}.note{margin:6px 0}
@media print{.matrix{max-height:none;overflow:visible}thead{position:static}body{margin:0}}
"""


def render(source):
    before, rows, after = parse(source)
    config = methodology(before + after)
    rows = validate(before, rows, after, config)
    body, anchors = [], set()
    for _, row in rows:
        columns = []
        for index, value in enumerate(row):
            anchor = ''
            if index in (0, 3, 10) and value and value not in anchors:
                anchors.add(value)
                anchor = f' id="{value}"'
            absent_control = not row[10] and index in (10, 12, 13, 14, 15, 16)
            css = ' class="unknown"' if unknown(value) and not absent_control else ''
            display = value if absent_control else value or '[Unknown]'
            columns.append(f'<td{anchor}{css}>{rich_text(display)}</td>')
        body.append('<tr>' + ''.join(columns) + '</tr>')
    headings = ''.join(f'<th scope="col">{field}</th>' for field in FIELDS)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Preliminary risk and control matrix</title><style>' + STYLE + '</style></head><body>'
            '<p class="viewer">Markdown governs. Edit the Markdown and regenerate this viewer.</p>'
            + prose(before) + '<div class="matrix"><table aria-label="Risk and control matrix">'
            '<colgroup span="3"></colgroup><colgroup span="7"></colgroup><colgroup span="8"></colgroup>'
            '<thead><tr><th colspan="3" scope="colgroup">Process</th>'
            '<th colspan="7" scope="colgroup">Risk</th><th colspan="8" scope="colgroup">Control</th></tr>'
            '<tr>' + headings + '</tr></thead><tbody>' + ''.join(body)
            + '</tbody></table></div>' + prose(after) + '</body></html>')


def write_report(source_path):
    source_path = Path(source_path).resolve()
    if source_path.suffix.lower() != '.md':
        fail('TableStructure', 'source must be a Markdown (.md) file')
    document = render(source_path.read_text(encoding='utf-8-sig'))
    output = source_path.with_suffix('.html')
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=output.parent,
                                         prefix='.rcm-', suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(document)
        os.replace(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return output


def open_report(path):
    path = str(Path(path).resolve())
    if sys.platform == 'win32':
        literal = "'" + path.replace("'", "''") + "'"
        command = ['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
                   f'Start-Process -FilePath {literal} -ErrorAction Stop']
    elif sys.platform == 'darwin':
        command = ['open', path]
    else:
        command = ['xdg-open', path]
    subprocess.run(command, check=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', nargs='?', default='planning/risk-and-control-matrix.md')
    parser.add_argument('--no-open', action='store_true', help='write HTML without opening a browser')
    args = parser.parse_args(argv)
    try:
        output = write_report(args.source)
    except (ValidationError, OSError, UnicodeError) as error:
        name = '' if isinstance(error, ValidationError) else 'FileError: '
        print(name + str(error), file=sys.stderr)
        return 1
    print(output)
    if not args.no_open:
        try:
            open_report(output)
        except (OSError, subprocess.SubprocessError) as error:
            print(f'BrowserOpen: HTML saved at {output}; {error}', file=sys.stderr)
            return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
