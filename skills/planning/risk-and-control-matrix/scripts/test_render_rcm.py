"""Public Markdown-to-HTML/error contract; run from the skill folder."""

from contextlib import redirect_stderr, redirect_stdout
from html.parser import HTMLParser
import io
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.render_rcm import main, open_report, render, write_report, ValidationError


FIXTURE = Path(__file__).parent / 'fixtures' / 'matrix.md'


class TableReader(HTMLParser):
    def __init__(self, document):
        super().__init__()
        self.rows, self.row, self.cell = [], None, None
        self.tables = 0
        self.feed(document)

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.tables += 1
        elif tag == 'tr':
            self.row = []
        elif tag == 'td':
            self.cell = ''

    def handle_data(self, data):
        if self.cell is not None:
            self.cell += data

    def handle_endtag(self, tag):
        if tag == 'td':
            self.row.append(self.cell)
            self.cell = None
        elif tag == 'tr' and self.row:
            self.rows.append(self.row)


class RendererTests(unittest.TestCase):
    def setUp(self):
        self.source = FIXTURE.read_text(encoding='utf-8')

    def change_cell(self, source, row_number, column, value):
        # Fixture-specific split preserves escaped pipes as Markdown, not decoded cells.
        lines = source.splitlines()
        data_lines = [i for i, line in enumerate(lines) if line.startswith('| P-')]
        index = data_lines[row_number]
        parts = re.split(r'(?<!\\)\|', lines[index])[1:-1]
        parts[column] = value
        lines[index] = '| ' + ' | '.join(part.strip() for part in parts) + ' |'
        return '\n'.join(lines)

    def assert_invalid(self, source, category):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'risk-and-control-matrix.md'
            path.write_text(source, encoding='utf-8')
            output = path.with_suffix('.html')
            for existing in (False, True):
                if existing:
                    output.write_bytes(b'existing valid output')
                with self.assertRaisesRegex(ValidationError, '^' + category + ':'):
                    write_report(path)
                if existing:
                    self.assertEqual(output.read_bytes(), b'existing valid output')
                else:
                    self.assertFalse(output.exists())
            self.assertEqual(sorted(p.name for p in Path(directory).iterdir()),
                             ['risk-and-control-matrix.html', 'risk-and-control-matrix.md'])

    def test_full_fixture_order_fields_links_procedures_and_notes(self):
        document = render(self.source)
        parsed = TableReader(document)
        self.assertEqual(parsed.tables, 1)
        self.assertTrue(all(len(row) == 18 for row in parsed.rows))
        self.assertEqual([(r[0], r[3], r[10]) for r in parsed.rows], [
            ('P-01', 'R-01', 'C-01'), ('P-01', 'R-02', 'C-02'),
            ('P-01', 'R-03', ''), ('P-02', 'R-01', 'C-01')])
        self.assertEqual(parsed.rows[0][3:], parsed.rows[3][3:])
        self.assertIn('Control not yet identified', parsed.rows[2])
        self.assertEqual(parsed.rows[2][12:17], [''] * 5)
        self.assertIn('Ask the process owner', parsed.rows[2][17])
        self.assertIn('A | B &amp; &lt;limits&gt;', document)
        self.assertIn('href="../sources/policy.pdf#page=2"', document)
        self.assertIn('<li value="2">Trace a purchase', document)
        self.assertIn('Upstream snapshots:', document)
        self.assertIn('Methodology basis:', document)
        self.assertLess(document.index('</table>'), document.index('<h2>Information gaps'))
        self.assertIn('<h2>Flags</h2>', document)
        self.assertEqual(document.count('id="C-01"'), 1)
        self.assertIn('position:sticky', document)
        self.assertIn('colspan="3"', document)
        self.assertIn('colspan="7"', document)
        self.assertIn('colspan="8"', document)

    def test_structure_errors(self):
        data_row = next(line for line in self.source.splitlines() if line.startswith('| P-'))
        cases = [self.source.replace('Process Title', 'Wrong heading'),
                 self.source.replace('| --- |', '| -- |', 1),
                 self.source.replace(data_row, data_row[:-1]),
                 self.source.replace(data_row, data_row + ' extra |'),
                 self.source + '\n| Notes | Another table |\n| --- | --- |\n',
                 self.source + '\nNotes | Another table\n--- | ---\n',
                 '# No table',
                 '\n'.join(line for line in self.source.splitlines() if not line.startswith('| P-'))]
        for source in cases:
            with self.subTest(source=source[:70]):
                self.assert_invalid(source, 'TableStructure')

    def test_missing_and_invalid_ids(self):
        for column in (0, 3, 10):
            self.assert_invalid(self.change_cell(self.source, 1, column, 'Unknown'), 'MissingID')
            self.assert_invalid(self.change_cell(self.source, 1, column, 'wrong'), 'InvalidID')
        for column in (0, 3):
            self.assert_invalid(self.change_cell(self.source, 1, column, ''), 'MissingID')

    def test_missing_control_attributes_and_fabricated_identity(self):
        self.assert_invalid(self.change_cell(self.source, 3, 13, 'Manager'), 'MissingControl')
        self.assert_invalid(self.change_cell(self.source, 3, 10, 'C-99'), 'MissingControl')
        self.assert_invalid(self.change_cell(self.source, 1, 10, ''), 'MissingControl')

    def test_conflicting_shared_process_risk_control_and_procedures(self):
        for row, column in ((2, 1), (2, 4), (2, 13), (2, 17)):
            with self.subTest(column=column):
                self.assert_invalid(self.change_cell(self.source, row, column, 'Changed'), 'ConflictingEntity')

    def test_duplicate_combination(self):
        row = next(line for line in self.source.splitlines() if line.startswith('| P-'))
        self.assert_invalid(self.source.replace(row, row + '\n' + row), 'DuplicateCombination')

    def test_shared_gap_procedures_and_shared_control_across_risks(self):
        rows = [line for line in self.source.splitlines() if line.startswith('| P-')]
        gap = rows[3].replace('P-01 | Purchase ordering | Request and approve purchases.',
                              'P-02 | Invoice payment | Pay approved invoices.')
        source = self.source.replace(rows[3], rows[3] + '\n' + gap)
        self.assertEqual(len(TableReader(render(source)).rows), 5)
        self.assert_invalid(source.replace(gap, gap.replace('Ask the process owner', 'Interview management')),
                            'ConflictingEntity')
        other_risk = rows[2].replace('R-01', 'R-04')
        self.assertEqual(len(TableReader(render(self.source.replace(rows[2], rows[2] + '\n' + other_risk))).rows), 5)

    def test_internal_references_and_external_rq(self):
        for reference in ('#P-99', '#R-99', '#C-99'):
            self.assert_invalid(self.source + '\nSee [missing](' + reference + ').', 'DanglingReference')
        self.assertIn('RQ-01', render(self.source + '\n[RQ-99](../request-list.md#RQ-99)'))
        self.assert_invalid(self.change_cell(self.source, 1, 17, '1. See [missing](#C-99).'), 'DanglingReference')

    def test_ratings_and_classifications(self):
        for column, value, category in ((6, '6', 'InvalidRating'), (7, '0', 'InvalidRating'),
                (6, '1.5', 'InvalidRating'), (8, '26', 'InvalidRating'),
                (8, '7', 'InconsistentScore'), (9, 'Low', 'InconsistentBand'),
                (9, 'Severe', 'InconsistentBand'), (15, 'key', 'InvalidClassification'),
                (16, 'hybrid', 'InvalidClassification')):
            with self.subTest(column=column, value=value):
                self.assert_invalid(self.change_cell(self.source, 1, column, value), category)

    def test_unknown_values_and_no_procedure_scope_gate(self):
        source = self.source
        for column, value in ((6, '?'), (7, '[Pending]'), (8, ''), (9, 'Unknown'),
                              (15, 'TBD'), (16, '[Nature pending]'), (17, '')):
            source = self.change_cell(source, 1, column, value)
        document = render(source)
        self.assertIn('[Nature pending]', document)
        self.assertIn('[Unknown]', document)
        self.assertIn('Control not yet identified', document)

    def test_methodology_replacements(self):
        source = self.source.replace('4 | 5 | 20 | Critical', '3 | 3 | 9 | Severe')
        source = source.replace('2 | 3 | 6 | Moderate', '2 | 2 | 4 | Routine')
        source = source.replace('| automated |', '| hybrid |').replace('| detective |', '| monitoring |')
        source = ('RCM likelihood: 1, 2, 3\nRCM impact: 1, 2, 3\n'
                  'RCM bands: Routine=1..4; Severe=5..9\n'
                  'RCM types: preventive, monitoring\nRCM natures: manual, hybrid\n\n') + source
        document = render(source)
        self.assertIn('RCM bands: Routine=1..4; Severe=5..9', document)
        self.assertEqual(TableReader(document).rows[0][9], 'Severe')
        for directive in ('RCM likelihood: 1, 1', 'RCM impact: 0, 2',
                          'RCM bands: Low=1..4; High=6..25', 'RCM bands: Low=1..24',
                          'RCM types: manual,', 'RCM natures: auto, AUTO',
                          'RCM unknown: yes', 'RCM impact:',
                          'RCM impact: 1, 2\nRCM impact: 1, 2'):
            self.assert_invalid(directive + '\n\n' + self.source, 'InvalidMethodology')

    def test_secondary_sort_score_control_and_unknown_last(self):
        rows = [line for line in self.source.splitlines() if line.startswith('| P-')]
        lower = rows[2].replace('R-01', 'R-04').replace('4 | 5 | 20', '5 | 5 | 25')
        other = rows[2].replace('C-01', 'C-03')
        source = self.source.replace(rows[2], rows[2] + '\n' + lower + '\n' + other)
        parsed = TableReader(render(source))
        self.assertEqual([(r[3], r[10]) for r in parsed.rows[:5]],
                         [('R-04', 'C-01'), ('R-01', 'C-01'), ('R-01', 'C-03'),
                          ('R-02', 'C-02'), ('R-03', '')])

    def test_html_sensitive_text_and_unsafe_links(self):
        source = self.source + '\n<script>alert(1)</script> & "quote" [bad](javascript:alert) [bad](//host/x) [ok](https://example.org/p?q=1&b=2)'
        source = self.change_cell(source, 1, 17, r'1. Read A\|B.<br/>4. Read C:\\folder and <img src=x onerror=alert>.')
        document = render(source)
        self.assertNotIn('<script>', document)
        self.assertNotIn('<img', document)
        self.assertNotIn('href="javascript:', document)
        self.assertNotIn('href="//host', document)
        self.assertIn('href="https://example.org/p?q=1&amp;b=2"', document)
        self.assertIn('<li value="4">Read C:\\folder', document)
        self.assertIn('Read A|B.', document)

    def test_file_and_cli_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'risk-and-control-matrix.md'
            path.write_text(self.source, encoding='utf-8')
            original = path.read_bytes()
            result = subprocess.run([sys.executable, str(FIXTURE.parents[1] / 'render_rcm.py'), str(path), '--no-open'],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(Path(result.stdout.strip()), path.with_suffix('.html'))
            self.assertEqual(path.read_bytes(), original)
            path.write_text('Invalid', encoding='utf-8')
            output = path.with_suffix('.html').read_bytes()
            with redirect_stderr(io.StringIO()) as errors:
                self.assertEqual(main([str(path), '--no-open']), 1)
            self.assertIn('TableStructure:', errors.getvalue())
            self.assertEqual(path.with_suffix('.html').read_bytes(), output)

    def test_opener_platforms_and_launch_failure(self):
        for platform, executable in [('win32', 'powershell.exe'), ('darwin', 'open'), ('linux', 'xdg-open')]:
            with self.subTest(platform=platform), patch('scripts.render_rcm.sys.platform', platform), patch('scripts.render_rcm.subprocess.run') as run:
                open_report(Path("owner's report.html"))
                args = run.call_args.args[0]
                self.assertEqual(args[0], executable)
                if platform == 'win32':
                    self.assertIn("owner''s report.html", args[-1])
                    self.assertIn('Start-Process -FilePath', args[-1])
                else:
                    self.assertEqual(args[1], str(Path("owner's report.html").resolve()))
                self.assertTrue(run.call_args.kwargs['check'])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'matrix.md'
            path.write_text(self.source, encoding='utf-8')
            with patch('scripts.render_rcm.open_report', side_effect=OSError('no browser')), redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()) as errors:
                self.assertEqual(main([str(path)]), 2)
            self.assertIn('BrowserOpen: HTML saved', errors.getvalue())
            self.assertTrue(path.with_suffix('.html').exists())

    def test_replace_failure_preserves_existing_output_and_cleans_temporary(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'matrix.md'
            path.write_text(self.source, encoding='utf-8')
            path.with_suffix('.html').write_bytes(b'valid previous report')
            with patch('scripts.render_rcm.os.replace', side_effect=OSError('locked')), redirect_stderr(io.StringIO()) as errors:
                self.assertEqual(main([str(path), '--no-open']), 1)
            self.assertIn('FileError:', errors.getvalue())
            self.assertEqual(path.with_suffix('.html').read_bytes(), b'valid previous report')
            self.assertEqual(sorted(p.name for p in Path(directory).iterdir()), ['matrix.html', 'matrix.md'])


if __name__ == '__main__':
    unittest.main()
