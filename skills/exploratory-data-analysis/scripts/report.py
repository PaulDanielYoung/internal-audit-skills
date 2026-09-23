"""Offline HTML report helpers. Text arguments are escaped; section bodies and
visuals accept trusted HTML or inline SVG from the driver. No browser or network needed.
"""
from __future__ import annotations

import datetime as dt
import html
import math
import numbers
import tempfile
import textwrap
from html.parser import HTMLParser
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "template.html"
NA = "n/a"
QUALITY_AREAS = ("Completeness", "Validity", "Uniqueness", "Consistency", "Coverage")
# Conditions affecting a smaller share of records are left out of the data quality tables.
QUALITY_MIN_SHARE = 0.01


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def _compact(number: float, decimals: int) -> str | None:
    """Millions and billions for prose; None when the number is below a million."""
    for scale, suffix in ((1e9, "B"), (1e6, "M")):
        if abs(number) >= scale:
            text = f"{number / scale:,.{decimals}f}".rstrip("0").rstrip(".")
            return f"{text}{suffix}"
    return None


def fmt(value, decimals: int = 2, *, compact: bool = False) -> str:
    """Plain number. compact=True writes 2.96M in prose; tables keep the full figure."""
    if value is None:
        return NA
    number = float(value)
    if not math.isfinite(number):
        return NA
    if compact and (short := _compact(number, decimals)):
        return short
    return f"{number:,.0f}" if number.is_integer() else f"{number:,.{decimals}f}"


def money(value, *, compact: bool = False) -> str:
    """Dollar amount. compact=True writes $391.2M in prose; tables keep the full figure."""
    if value is None:
        return NA
    number = float(value)
    if not math.isfinite(number):
        return NA
    sign = "-" if number < 0 else ""
    magnitude = abs(number)
    if compact and (short := _compact(magnitude, 1)):
        return f"{sign}${short}"
    body = f"{magnitude:,.0f}" if magnitude.is_integer() else f"{magnitude:,.2f}"
    return f"{sign}${body}"


def pct(share: float | None) -> str:
    return NA if share is None else f"{share:.1%}"


def report_path(csv_path: str | Path) -> Path:
    """A fresh, timestamped report path in the OS temporary directory, named after the CSV stem."""
    source = Path(csv_path).resolve()
    if source.suffix.lower() != ".csv":
        raise ValueError("Expected a .csv source path.")
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    return Path(tempfile.gettempdir()) / f"{source.stem}-exploratory-data-analysis-{stamp}.html"


def section(title: str, body: str) -> str:
    return f'<section><h2>{esc(title)}</h2>{body}</section>'


def header(profile: dict, title: str, *, description: str, facts: list[str] | tuple[str, ...] = ()) -> str:
    """Plain-language title and description, then record and field counts with any key facts.

    title: the dataset's name in words, never the file stem.
    description: one or two sentences on what the data is and what one record represents.
    facts: optional extra key figures beyond records and fields, e.g. "1,668 sites".
    """
    items = [f"{fmt(profile['rows'])} records", f"{fmt(profile['fields'])} fields", *facts]
    return (
        f'<header><p class="eyebrow">Exploratory data analysis</p><h1>{esc(title)}</h1>'
        f'<p class="lede">{esc(description)}</p>'
        f'<p class="facts">{" · ".join(esc(item) for item in items)}</p>'
        '</header>'
    )


def table(columns: list[str], rows: list[list], title: str = "", *, css_class: str = "") -> str:
    caption = f'<caption>{esc(title)}</caption>' if title else ""
    headings = "".join(f'<th scope="col">{esc(column)}</th>' for column in columns)
    body = "".join(
        '<tr>' + "".join(f'<td>{esc(cell)}</td>' for cell in row) + '</tr>' for row in rows
    )
    attrs = f' class="{esc(css_class)}"' if css_class else ""
    return f'<div class="scroll-table"><table{attrs}>{caption}<thead><tr>{headings}</tr></thead><tbody>{body}</tbody></table></div>'


def field_profile(profile: dict, meanings: dict[str, str]) -> str:
    """Every field in file order with its apparent meaning in plain words.

    meanings: one sentence per field on what it appears to hold; required for every field.
    """
    names = [field["name"] for field in profile["columns"]]
    missing = [name for name in names if not str(meanings.get(name, "")).strip()]
    if missing:
        raise ValueError(f"Write an apparent meaning for every field; missing: {', '.join(missing)}")
    unknown = set(meanings) - set(names)
    if unknown:
        raise ValueError(f"Meanings name fields not in the file: {', '.join(sorted(unknown))}")
    return table(["Field", "Apparent meaning"], [[name, meanings[name]] for name in names], css_class="fields")


def data_quality(conditions: list[tuple[str, str, str, int, str]], rows: int) -> str:
    """One subheading and table per area in QUALITY_AREAS order.

    conditions: one (area, field, observation, affected, why_it_matters) per condition.
    field names the field or fields involved, or "All fields"; observation is a short
    plain-language phrase; affected is the count of records the condition applies to,
    shown as a percentage of rows. Conditions affecting less than QUALITY_MIN_SHARE of rows are
    not shown, and a note gives how many were left out. Rows within an area are sorted by affected
    records, most first; ties keep their given order. An area with no condition says so under its heading.
    """
    by_area = {area: [] for area in QUALITY_AREAS}
    for condition in conditions:
        if len(condition) != 5:
            raise ValueError("Each condition needs area, field, observation, affected records, and why it matters.")
        area, field, observation, affected, why = condition
        if area not in by_area:
            raise ValueError(f"Area must be one of: {', '.join(QUALITY_AREAS)}; got {area!r}")
        if any(not str(cell).strip() for cell in (field, observation, why)):
            raise ValueError(f"Every text cell of a {area} condition needs text.")
        if isinstance(affected, bool) or not isinstance(affected, numbers.Integral) or not 0 <= affected <= rows:
            raise ValueError(f"Affected records must be a record count from 0 to {rows}; got {affected!r}")
        share = int(affected) / rows if rows else 0.0
        by_area[area].append((int(affected), share, [field, observation, pct(share), why]))
    parts = []
    for area, area_rows in by_area.items():
        parts.append(f'<h3>{esc(area)}</h3>')
        shown = [item for item in area_rows if item[1] >= QUALITY_MIN_SHARE]
        hidden = len(area_rows) - len(shown)
        if shown:
            ranked = [row for _, _, row in sorted(shown, key=lambda item: item[0], reverse=True)]
            # Same fixed column widths in every area, so the tables line up down the section.
            parts.append(table(["Field", "Observation", "Affected records", "Why it matters"], ranked, css_class="quality"))
        elif not hidden:
            parts.append('<p class="muted">Checked; nothing to report.</p>')
        if hidden:
            noun = "condition" if hidden == 1 else "conditions"
            parts.append(f'<p class="muted">{hidden} {noun} affecting less than {QUALITY_MIN_SHARE:.0%} of records not shown.</p>')
    return "".join(parts)


def analysis_limitations(notes: list[str] | tuple[str, ...]) -> str:
    """One optional final section containing material limitations as a concise list."""
    items = "".join(f'<li>{esc(note)}</li>' for note in notes if note.strip())
    return section("Analysis limitations", f'<ul>{items}</ul>') if items else ""


class _MarkupTags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)


def overview(question: str, visual: str, *, takeaway: str, context: str) -> str:
    """A question, one SVG chart, a takeaway, and a brief context paragraph; no tables."""
    if any(not value.strip() for value in (question, visual, takeaway, context)):
        raise ValueError("An overview needs a question, chart, takeaway, and context.")
    markup = _MarkupTags()
    markup.feed(visual)
    if markup.tags.count("svg") != 1 or {"table", "details", "summary"}.intersection(markup.tags):
        raise ValueError("Each overview needs one SVG chart, without tables or dropdowns.")
    return (
        f'<div class="overview"><h3>{esc(question)}</h3>{visual}'
        f'<p>{esc(takeaway)}</p><p class="muted">{esc(context)}</p></div>'
    )


def card(title: str, visual: str = "", *, observation: str, why_it_matters: str,
         question: str) -> str:
    """A supported observation ending with a concrete question for the data provider."""
    if any(not value.strip() for value in (title, observation, why_it_matters, question)):
        raise ValueError("An observation needs a title, evidence, why it matters, and a stakeholder question.")
    paragraphs = "".join(
        f'<p><strong>{label}:</strong> {esc(text)}</p>'
        for label, text in [
            ("What we noticed", observation), ("Why it matters", why_it_matters),
        ]
    )
    return (
        f'<article><h3>{esc(title)}</h3>{paragraphs}{visual}'
        f'<p><strong>Question for the data provider:</strong> {esc(question)}</p></article>'
    )


def chart(labels: list, values: list, *, title: str, unit: str = "") -> str:
    """Horizontal SVG bars with a zero baseline, full labels, and visible values.

    Supply already aggregated values; sort categories or keep chronological order
    in the driver. Negative values extend to the left of zero. No remote assets.
    """
    if len(labels) != len(values):
        raise ValueError("Chart labels and values must have the same length.")
    if not values:
        return '<p class="muted">No values to plot.</p>'
    values = [float(value) for value in values]
    if not all(math.isfinite(value) for value in values):
        raise ValueError("Chart values must be finite; explain exclusions before plotting.")
    low, high = min(0, min(values)), max(0, max(values))
    span = high - low or 1
    left, width = 330, 380
    def x(value):
        return left + (value - low) / span * width
    zero = x(0)
    wrapped_labels = [textwrap.wrap(str(label), width=44) or [""] for label in labels]
    row_heights = [max(34, len(lines) * 16 + 10) for lines in wrapped_labels]
    height = 48 + sum(row_heights)
    marks = [f'<line x1="{zero:.2f}" x2="{zero:.2f}" y1="16" y2="{height - 28}" stroke="#94a3b8"/>']
    y = 20
    for label, value, lines, row_height in zip(labels, values, wrapped_labels, row_heights):
        center = y + row_height / 2
        label_y = center + 4 - (len(lines) - 1) * 8
        label_text = "".join(
            f'<tspan x="{left - 14}" y="{label_y + index * 16:.2f}">{esc(line)}</tspan>'
            for index, line in enumerate(lines)
        )
        marks.append(
            f'<text text-anchor="end">{label_text}</text>'
            f'<rect x="{min(zero, x(value)):.2f}" y="{center - 12:.2f}" width="{abs(x(value) - zero):.2f}" '
            f'height="24" rx="3" fill="#4f46e5"><title>{esc(label)}: {esc(fmt(value))}</title></rect>'
            f'<text x="{left + width + 18}" y="{center + 4:.2f}">{esc(fmt(value))}</text>'
        )
        y += row_height
    marks.append(f'<text x="{zero:.2f}" y="{height - 7}" text-anchor="middle">0</text>')
    return (
        f'<figure><figcaption>{esc(title)}{(" · " + esc(unit)) if unit else ""}</figcaption>'
        f'<div class="scroll-chart"><svg xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{esc(title)}" viewBox="0 0 820 {height}"><title>{esc(title)}</title>'
        f'{"".join(marks)}</svg></div></figure>'
    )


def write_report(title: str, sections: list[str], path: str | Path) -> Path:
    """Write the page to an explicit HTML path. The CSV is never written."""
    path = Path(path).resolve()
    if path.suffix.lower() != ".html":
        raise ValueError("Report output must have an .html extension.")
    template = TEMPLATE.read_text(encoding="utf-8")
    page = template.replace("{{title}}", esc(title)).replace("{{body}}", "\n".join(sections))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page, encoding="utf-8")
    return path
