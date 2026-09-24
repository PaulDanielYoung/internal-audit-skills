"""Offline HTML report for one exploratory data analysis.

The driver builds a Report: construct it with the profile and the reader-facing framing,
add data quality conditions, overview items, observations, and limitations as the analysis
produces them, then write(). The Report owns section order and titles, leaves out empty
optional sections, validates each addition, and escapes every text argument. Visuals and
the bodies they contain are trusted HTML or inline SVG from the driver; build them with
chart() and table(), or escape labels with esc() when generating custom SVG.

No browser, network, JavaScript, or external asset is needed to read the result.
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
# Default display threshold; a material condition can opt in with always_show=True.
QUALITY_MIN_SHARE = 0.01
# A table supporting an observation is a sample of the evidence, not a data dump.
OBSERVATION_MAX_ROWS = 10


# --- Numbers and text for the reader -------------------------------------------------

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
    """Plain number. compact=True writes 1.25M in prose; tables keep the full figure."""
    if value is None:
        return NA
    number = float(value)
    if not math.isfinite(number):
        return NA
    if compact and (short := _compact(number, decimals)):
        return short
    return f"{number:,.0f}" if number.is_integer() else f"{number:,.{decimals}f}"


def money(value, *, compact: bool = False) -> str:
    """Dollar amount. compact=True writes $12.5M in prose; tables keep the full figure."""
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
    """Share to one decimal place; a non-zero share never reads as 0.0% or 100.0%."""
    if share is None:
        return NA
    if 0 < share < 0.0005:
        return "<0.1%"
    if 0.9995 <= share < 1:
        return ">99.9%"
    return f"{share:.1%}"


# --- Visual vocabulary -----------------------------------------------------------------

def table(columns: list[str], rows: list[list], title: str = "", *, css_class: str = "") -> str:
    """Group comparisons, distributions, or representative records. Cells are escaped;
    format numeric cells with fmt(), money(), or pct() first."""
    caption = f'<caption>{esc(title)}</caption>' if title else ""
    headings = "".join(f'<th scope="col">{esc(column)}</th>' for column in columns)
    body = "".join(
        '<tr>' + "".join(f'<td>{esc(cell)}</td>' for cell in row) + '</tr>' for row in rows
    )
    attrs = f' class="{esc(css_class)}"' if css_class else ""
    return f'<div class="scroll-table"><table{attrs}>{caption}<thead><tr>{headings}</tr></thead><tbody>{body}</tbody></table></div>'


def chart(labels: list, values: list, *, title: str, unit: str = "", decimals: int = 2) -> str:
    """Horizontal SVG bars with a zero baseline, full labels, and visible values.

    Supply already aggregated, finite values; sort categories or keep chronological order
    in the driver. Negative values extend to the left of zero. An empty input returns a
    no-values message, which is not an overview chart. decimals sets display precision
    for non-integral values in labels and tooltips, without changing bar lengths;
    integral values keep no decimal places, as in fmt().
    """
    if len(labels) != len(values):
        raise ValueError("Chart labels and values must have the same length.")
    if isinstance(decimals, bool) or not isinstance(decimals, numbers.Integral) or decimals < 0:
        raise ValueError("Chart decimals must be a non-negative integer.")
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
        display_value = esc(fmt(value, decimals=decimals))
        center = y + row_height / 2
        label_y = center + 4 - (len(lines) - 1) * 8
        label_text = "".join(
            f'<tspan x="{left - 14}" y="{label_y + index * 16:.2f}">{esc(line)}</tspan>'
            for index, line in enumerate(lines)
        )
        marks.append(
            f'<text text-anchor="end">{label_text}</text>'
            f'<rect x="{min(zero, x(value)):.2f}" y="{center - 12:.2f}" width="{abs(x(value) - zero):.2f}" '
            f'height="24" rx="3" fill="#4f46e5"><title>{esc(label)}: {display_value}</title></rect>'
            f'<text x="{left + width + 18}" y="{center + 4:.2f}">{display_value}</text>'
        )
        y += row_height
    marks.append(f'<text x="{zero:.2f}" y="{height - 7}" text-anchor="middle">0</text>')
    return (
        f'<figure><figcaption>{esc(title)}{(" · " + esc(unit)) if unit else ""}</figcaption>'
        f'<div class="scroll-chart"><svg xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{esc(title)}" viewBox="0 0 820 {height}"><title>{esc(title)}</title>'
        f'{"".join(marks)}</svg></div></figure>'
    )


# --- The report ------------------------------------------------------------------------

class _MarkupTags(HTMLParser):
    """Tag names in a visual, plus the number of table rows outside any thead."""

    def __init__(self):
        super().__init__()
        self.tags = []
        self.body_rows = 0
        self._in_thead = 0

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag == "thead":
            self._in_thead += 1
        elif tag == "tr" and not self._in_thead:
            self.body_rows += 1

    def handle_endtag(self, tag):
        if tag == "thead" and self._in_thead:
            self._in_thead -= 1


def _section(title: str, body: str) -> str:
    return f'<section><h2>{esc(title)}</h2>{body}</section>'


class Report:
    """One report, assembled in a fixed order when written.

    Sections, in order: header; What the file contains; Data quality; Data overview;
    Observations, only when one was added; Analysis limitations, only when one was added.

    profile: the dict returned by profile_csv().
    title: the dataset's name in plain words, never the file stem.
    description: one or two sentences on what the data is and what one record represents.
    meanings: one sentence per field on what it appears to hold; every field is required.
    facts: optional key figures shown beside the record and field counts, e.g. "240 service teams".
    """

    def __init__(self, profile: dict, title: str, *, description: str,
                 meanings: dict[str, str], facts: list[str] | tuple[str, ...] = ()):
        if not str(title).strip() or not str(description).strip():
            raise ValueError("A report needs a plain-language title and a description.")
        names = [field["name"] for field in profile["columns"]]
        missing = [name for name in names if not str(meanings.get(name, "")).strip()]
        if missing:
            raise ValueError(f"Write an apparent meaning for every field; missing: {', '.join(missing)}")
        unknown = set(meanings) - set(names)
        if unknown:
            raise ValueError(f"Meanings name fields not in the file: {', '.join(sorted(unknown))}")
        self._profile = profile
        self._title = str(title)
        self._description = str(description)
        self._meanings = {name: meanings[name] for name in names}
        self._facts = tuple(facts)
        self._quality: list[tuple[str, int, bool, list]] = []
        self._overview: list[str] = []
        self._no_overview = ""
        self._observations: list[str] = []
        self._limitations: list[str] = []

    # -- Adding content ----------------------------------------------------------------

    def quality(self, area: str, field: str, observation: str, affected: int, why_it_matters: str,
                *, always_show: bool = False) -> None:
        """One data quality condition. area is one of QUALITY_AREAS; field names the field
        or fields involved, or "All fields" for whole-record conditions; observation is a
        short plain-language phrase; affected is the count of records the condition applies
        to, shown with its percentage of the file's records. Add every condition found: those
        under QUALITY_MIN_SHARE are counted in a note rather than listed by default.
        Set always_show=True for a material condition that merits a visible row even
        below that display threshold, explaining its impact in why_it_matters."""
        rows = self._profile["rows"]
        if area not in QUALITY_AREAS:
            raise ValueError(f"Area must be one of: {', '.join(QUALITY_AREAS)}; got {area!r}")
        if any(not str(cell).strip() for cell in (field, observation, why_it_matters)):
            raise ValueError(f"Every text cell of a {area} condition needs text.")
        if isinstance(affected, bool) or not isinstance(affected, numbers.Integral) or not 0 <= affected <= rows:
            raise ValueError(f"Affected records must be a record count from 0 to {rows}; got {affected!r}")
        if not isinstance(always_show, bool):
            raise ValueError("always_show must be a boolean.")
        share = int(affected) / rows if rows else 0.0
        affected_cell = f"{fmt(affected)} ({pct(share)})"
        self._quality.append((area, int(affected), always_show, [field, observation, affected_cell, why_it_matters]))

    def coverage(self, field: str, start, end, dated: int, why_it_matters: str) -> None:
        """The period one date field spans, always shown under Coverage. start and end are
        the earliest and latest values in the words the reader should see: a date, a year,
        or text such as "November 1911". dated is the count of records carrying the date.
        Record gaps within the period with quality("Coverage", ...)."""
        rows = self._profile["rows"]
        if any(not str(cell).strip() for cell in (field, start, end, why_it_matters)):
            raise ValueError("A coverage row needs a field, a start, an end, and why it matters.")
        if isinstance(dated, bool) or not isinstance(dated, numbers.Integral) or not 0 <= dated <= rows:
            raise ValueError(f"Dated records must be a record count from 0 to {rows}; got {dated!r}")
        def label(value) -> str:
            if isinstance(value, dt.date):
                return value.strftime("%d %b %Y")
            if isinstance(value, numbers.Real) and float(value).is_integer():
                return str(int(value))  # a year, without a thousands separator
            return str(value)
        share = int(dated) / rows if rows else 0.0
        self._quality.append(("Coverage", int(dated), True, [
            field, f"Dated {label(start)} to {label(end)}", f"{fmt(dated)} dated ({pct(share)})", why_it_matters,
        ]))

    def overview(self, question: str, chart: str, *, takeaway: str, context: str) -> None:
        """One descriptive question answered by exactly one SVG chart, a takeaway, and the
        context needed to read the chart correctly. Tables and dropdowns are rejected."""
        if any(not value.strip() for value in (question, chart, takeaway, context)):
            raise ValueError("An overview needs a question, chart, takeaway, and context.")
        markup = _MarkupTags()
        markup.feed(chart)
        if markup.tags.count("svg") != 1 or {"table", "details", "summary"}.intersection(markup.tags):
            raise ValueError("Each overview needs one SVG chart, without tables or dropdowns.")
        self._overview.append(
            f'<div class="overview"><h3>{esc(question)}</h3>{chart}'
            f'<p>{esc(takeaway)}</p><p class="muted">{esc(context)}</p></div>'
        )

    def no_overview(self, reason: str) -> None:
        """Why the file cannot support a meaningful overview, for example a CSV with headers
        but no records. Only for a report with no overview items."""
        if not reason.strip():
            raise ValueError("Give the reason the file supports no overview.")
        self._no_overview = reason

    def observation(self, title: str, visual: str = "", *, noticed: str, why_it_matters: str,
                    question: str) -> None:
        """A supported pattern ending with a concrete question for the data provider. The
        optional visual follows What we noticed, the claim it lets the reader check. A table
        in the visual shows at most OBSERVATION_MAX_ROWS body rows."""
        if any(not value.strip() for value in (title, noticed, why_it_matters, question)):
            raise ValueError("An observation needs a title, evidence, why it matters, and a stakeholder question.")
        markup = _MarkupTags()
        markup.feed(visual)
        if markup.body_rows > OBSERVATION_MAX_ROWS:
            raise ValueError(
                f"An observation table shows at most {OBSERVATION_MAX_ROWS} rows; got {markup.body_rows}. "
                "Show the rows that best support the observation and say how many of the total they are."
            )
        self._observations.append(
            f'<div class="observation"><h3>{esc(title)}</h3>'
            f'<p><strong>What we noticed:</strong> {esc(noticed)}</p>{visual}'
            f'<p><strong>Why it matters:</strong> {esc(why_it_matters)}</p>'
            f'<p><strong>Question for the data provider:</strong> {esc(question)}</p></div>'
        )

    def limitation(self, note: str) -> None:
        """A material constraint on interpretation, listed once at the end of the report.
        Refer to an observation by title when it carries the full investigation."""
        if note.strip():
            self._limitations.append(note)

    # -- Writing -----------------------------------------------------------------------

    def write(self, path: str | Path | None = None) -> Path:
        """Write the complete offline report and return its path. Without a path, a fresh
        timestamped .html file in the OS temporary directory, named after the CSV stem.
        The CSV is never written."""
        if path is None:
            stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
            stem = Path(self._profile["path"]).stem
            path = Path(tempfile.gettempdir()) / f"{stem}-exploratory-data-analysis-{stamp}.html"
        path = Path(path).resolve()
        if path.suffix.lower() != ".html":
            raise ValueError("Report output must have an .html extension.")
        sections = [
            self._header(),
            _section("What the file contains", self._field_profile()),
            _section("Data quality", self._data_quality()),
            _section("Data overview", self._overview_body()),
        ]
        if self._observations:
            sections.append(_section("Observations", "".join(self._observations)))
        if self._limitations:
            items = "".join(f'<li>{esc(note)}</li>' for note in self._limitations)
            sections.append(_section("Analysis limitations", f'<ul>{items}</ul>'))
        template = TEMPLATE.read_text(encoding="utf-8")
        page = template.replace("{{title}}", esc(self._title)).replace("{{body}}", "\n".join(sections))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(page, encoding="utf-8")
        return path

    def _header(self) -> str:
        profile = self._profile
        items = [f"{fmt(profile['rows'])} records", f"{fmt(profile['fields'])} fields", *self._facts]
        return (
            f'<header><p class="eyebrow">Exploratory data analysis</p><h1>{esc(self._title)}</h1>'
            f'<p class="lede">{esc(self._description)}</p>'
            f'<p class="facts">{" · ".join(esc(item) for item in items)}</p>'
            '</header>'
        )

    def _field_profile(self) -> str:
        """Every field in file order with its apparent meaning."""
        rows = [[name, meaning] for name, meaning in self._meanings.items()]
        return table(["Field", "Apparent meaning"], rows, css_class="fields")

    def _data_quality(self) -> str:
        """One subheading and table per area in QUALITY_AREAS order, rows sorted by affected
        records, most first. An area with no condition says so under its heading."""
        by_area = {area: [] for area in QUALITY_AREAS}
        for area, affected, always_show, row in self._quality:
            by_area[area].append((affected, always_show, row))
        rows = self._profile["rows"]
        parts = []
        for area, area_rows in by_area.items():
            parts.append(f'<h3>{esc(area)}</h3>')
            shown = [item for item in area_rows
                     if item[1] or (item[0] / rows if rows else 0.0) >= QUALITY_MIN_SHARE]
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

    def _overview_body(self) -> str:
        if self._overview and self._no_overview:
            raise ValueError("A report has overview items or a reason there are none, not both.")
        if self._overview:
            return "".join(self._overview)
        if self._no_overview:
            return f'<p>{esc(self._no_overview)}</p>'
        raise ValueError("Build the data overview or call no_overview() with why the file cannot support one.")
