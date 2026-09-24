"""Offline HTML report for one exploratory data analysis.

The driver builds a Report: construct it with the profile and the reader-facing framing,
add data quality conditions, overview items, observations, and limitations as the analysis
produces them, then write(). The Report owns section order and titles, leaves out empty
optional sections, validates each addition, and escapes every text argument. Visuals and
the bodies they contain are trusted HTML or inline SVG from the driver; build them with
bar_chart(), line_chart(), pie_chart(), and table().

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


# Bars are upright; past this many categories, combine the rest as Other.
BAR_MAX_CATEGORIES = 12
# Labels wrap beneath their bars up to this many lines; longer labels tilt instead.
BAR_LABEL_MAX_LINES = 3
BAR_LABEL_TILT = 40  # degrees, as Chart.js tilts tick labels that do not fit
CHAR_WIDTH = 7.2  # approximate width of one 13px character in chart units
# A line labels every point up to this many; beyond it, only the first, last, peak, and low.
LINE_LABEL_ALL_MAX = 12
# Period labels wrap beneath their points up to this many lines; longer ones thin out.
LINE_LABEL_MAX_LINES = 2
PIE_MAX_SLICES = 5
CHART_WIDTH = 820


def _chart_input(labels: list, values: list, decimals: int) -> list[float]:
    """Validate the arguments every chart shares and return the values as floats."""
    if len(labels) != len(values):
        raise ValueError("Chart labels and values must have the same length.")
    if isinstance(decimals, bool) or not isinstance(decimals, numbers.Integral) or decimals < 0:
        raise ValueError("Chart decimals must be a non-negative integer.")
    values = [float(value) for value in values]
    if not all(math.isfinite(value) for value in values):
        raise ValueError("Chart values must be finite; explain exclusions before plotting.")
    return values


def _figure(title: str, unit: str, height: float, marks: list[str]) -> str:
    return (
        f'<figure><figcaption>{esc(title)}{(" · " + esc(unit)) if unit else ""}</figcaption>'
        f'<div class="scroll-chart"><svg xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{esc(title)}" viewBox="0 0 {CHART_WIDTH} {height:.0f}"><title>{esc(title)}</title>'
        f'{"".join(marks)}</svg></div></figure>'
    )


def _tspans(lines: list[str], x: float, first_y: float) -> str:
    return "".join(f'<tspan x="{x:.2f}" y="{first_y + index * 16:.2f}">{esc(line)}</tspan>'
                   for index, line in enumerate(lines))


def bar_chart(labels: list, values: list, *, title: str, unit: str = "", decimals: int = 2) -> str:
    """Upright bars comparing distinct items or groups, with a zero baseline, full labels,
    and visible values.

    Supply at most BAR_MAX_CATEGORIES already aggregated, finite values, sorted in the
    driver; combine the rest as Other. Labels wrap beneath their bars when every word fits
    the bar's width in at most BAR_LABEL_MAX_LINES lines; otherwise every label tilts.
    Negative values extend below zero. An empty input returns a no-values message, which
    is not an overview chart. decimals sets display precision for non-integral values in
    labels and tooltips, without changing bar heights; integral values keep no decimal
    places, as in fmt().
    """
    values = _chart_input(labels, values, decimals)
    if not values:
        return '<p class="muted">No values to plot.</p>'
    if len(values) > BAR_MAX_CATEGORIES:
        raise ValueError(f"A bar chart shows at most {BAR_MAX_CATEGORIES} bars; combine the rest as Other.")
    labels = [str(label) for label in labels]
    low, high = min(0, min(values)), max(0, max(values))
    span = high - low or 1
    top, plot, right = 30, 260, CHART_WIDTH - 20
    slot = (right - 40) / len(values)
    chars = int(slot / CHAR_WIDTH)
    wrapped_labels = [textwrap.wrap(label, width=chars) or [""] for label in labels]
    tilted = any(len(word) > chars for label in labels for word in label.split()) or \
        max(len(lines) for lines in wrapped_labels) > BAR_LABEL_MAX_LINES
    cos, sin = math.cos(math.radians(BAR_LABEL_TILT)), math.sin(math.radians(BAR_LABEL_TILT))
    # A tilted first label runs down and to the left of its bar; leave room for it.
    left = max(40, cos * len(labels[0]) * CHAR_WIDTH - slot / 2 + 12) if tilted else 40
    slot = (right - left) / len(values)
    bar = min(64, slot * 0.7)
    def y(value):
        return top + (high - value) / span * plot
    zero = y(0)
    bottom = top + plot + (38 if low < 0 else 20)  # below the lowest bar and any value label under it
    if tilted:
        height = bottom + sin * max(len(label) for label in labels) * CHAR_WIDTH + 20
    else:
        height = bottom + max(len(lines) for lines in wrapped_labels) * 16 + 12
    marks = [f'<line x1="{left:.2f}" x2="{right}" y1="{zero:.2f}" y2="{zero:.2f}" stroke="#94a3b8"/>',
             f'<text x="{left - 8:.2f}" y="{zero + 4:.2f}" text-anchor="end">0</text>']
    for index, (label, value, lines) in enumerate(zip(labels, values, wrapped_labels)):
        display_value = esc(fmt(value, decimals=decimals))
        center = left + slot * (index + 0.5)
        value_y = y(value) - 8 if value >= 0 else y(value) + 18
        if tilted:
            axis_label = (f'<text x="{center:.2f}" y="{bottom:.2f}" text-anchor="end" '
                          f'transform="rotate(-{BAR_LABEL_TILT} {center:.2f} {bottom:.2f})">{esc(label)}</text>')
        else:
            axis_label = f'<text text-anchor="middle">{_tspans(lines, center, bottom + 4)}</text>'
        marks.append(
            f'<rect x="{center - bar / 2:.2f}" y="{min(zero, y(value)):.2f}" width="{bar:.2f}" '
            f'height="{abs(y(value) - zero):.2f}" rx="3" fill="#4f46e5"><title>{esc(label)}: {display_value}</title></rect>'
            f'<text x="{center:.2f}" y="{value_y:.2f}" text-anchor="middle">{display_value}</text>{axis_label}'
        )
    return _figure(title, unit, height, marks)


def _nice_ticks(low: float, high: float, count: int = 5) -> list[float]:
    """Round axis ticks from low to high; callers include zero in the range."""
    span = high - low or 1
    raw = span / (count - 1)
    magnitude = 10 ** math.floor(math.log10(raw))
    step = next(m * magnitude for m in (1, 2, 2.5, 5, 10) if m * magnitude >= raw)
    start, stop = math.floor(low / step) * step, math.ceil(high / step) * step
    return [start + index * step for index in range(round((stop - start) / step) + 1)]


def line_chart(labels: list, values: list, *, title: str, unit: str = "", decimals: int = 2,
               partial_last: bool = False) -> str:
    """One series changing over continuous time, left to right, on a y-axis that includes zero.

    labels are the periods in chronological order, written as labels (1940s, 2022-Q3).
    Supply every period in the range, with zero for an empty one, so the time axis stays
    even. Every point has a marker; values are labeled on every point up to
    LINE_LABEL_ALL_MAX points, and otherwise on the first, last, peak, and low. Period
    labels wrap beneath their points, or thin to every nth, counted back from the last,
    when a word is too long for its slot. partial_last draws the final segment dashed and marks its period "to date".
    decimals works as in bar_chart().
    """
    values = _chart_input(labels, values, decimals)
    if not values:
        return '<p class="muted">No values to plot.</p>'
    if len(values) < 2:
        raise ValueError("A line chart needs at least two periods; use bar_chart() for one.")
    labels = [str(label) for label in labels]
    ticks = _nice_ticks(min(0, min(values)), max(0, max(values)))
    low, high = ticks[0], ticks[-1]
    left, right, top, plot = 80, CHART_WIDTH - 40, 24, 260
    step = (right - left) / (len(values) - 1)
    def y(value):
        return top + (high - value) / (high - low or 1) * plot
    marks = []
    for tick in ticks:
        marks.append(
            f'<line x1="{left}" x2="{right}" y1="{y(tick):.2f}" y2="{y(tick):.2f}" '
            f'stroke="{"#94a3b8" if tick == 0 else "#e2e8f0"}"/>'
            f'<text x="{left - 10}" y="{y(tick) + 4:.2f}" text-anchor="end">{esc(fmt(tick, decimals, compact=True))}</text>'
        )
    points = [(left + index * step, y(value)) for index, value in enumerate(values)]
    solid = points[:-1] if partial_last else points
    marks.append('<polyline fill="none" stroke="#4f46e5" stroke-width="2.5" points="'
                 + " ".join(f"{px:.2f},{py:.2f}" for px, py in solid) + '"/>')
    if partial_last:
        (x1, y1), (x2, y2) = points[-2:]
        marks.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                     'stroke="#4f46e5" stroke-width="2.5" stroke-dasharray="6 5"/>')
    last = len(values) - 1
    if len(values) <= LINE_LABEL_ALL_MAX:
        labeled = set(range(len(values)))
    else:
        labeled = {0, last, values.index(max(values)), values.index(min(values))}
    # Every period label shows when each wraps to fit its slot in LINE_LABEL_MAX_LINES lines;
    # otherwise labels thin to every nth, counted back from the last so the spacing stays even.
    chars = max(1, int((step - 6) / CHAR_WIDTH))
    wrapped = [textwrap.wrap(label, width=chars) or [""] for label in labels]
    if all(len(word) <= chars for label in labels for word in label.split()) and \
            max(len(lines) for lines in wrapped) <= LINE_LABEL_MAX_LINES:
        shown, axis_lines = set(range(len(values))), wrapped
    else:
        every = max(1, math.ceil(max(len(label) for label in labels) * 8 / step))
        shown = {index for index in range(len(values)) if (last - index) % every == 0}
        axis_lines = [[label] for label in labels]
    axis_y = top + plot + 22
    for index, ((px, py), label, value) in enumerate(zip(points, labels, values)):
        display_value = esc(fmt(value, decimals=decimals))
        hollow = partial_last and index == last
        marks.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="4" fill="{"#fafaf9" if hollow else "#4f46e5"}" '
                     f'stroke="#4f46e5" stroke-width="2"><title>{esc(label)}: {display_value}</title></circle>')
        if index in labeled:
            anchor, label_x, label_y = "middle", px, py - 10
            if index == 0:
                # Start at the point to clear the y-axis tick labels, and sit below a rising line.
                anchor, label_x = "start", px - 4
                if values[1] > value:
                    label_y = py + 20
            marks.append(f'<text x="{label_x:.2f}" y="{label_y:.2f}" text-anchor="{anchor}">{display_value}</text>')
        if index in shown:
            lines = [*axis_lines[index], "to date"] if hollow else axis_lines[index]
            marks.append(f'<text text-anchor="middle">{_tspans(lines, px, axis_y)}</text>')
    label_lines = max(len(axis_lines[index]) for index in shown) + (1 if partial_last else 0)
    height = axis_y + label_lines * 16 + 8
    return _figure(title, unit, height, marks)


def pie_chart(labels: list, values: list, *, title: str, unit: str = "", decimals: int = 2) -> str:
    """Parts of one whole, at most PIE_MAX_SLICES slices including any Other, each labeled
    directly with its share and value. The values must be non-negative parts that add up
    to the whole the title names; combine small parts as Other before plotting. Slices
    take the report's colorblind-safe palette in order. decimals works as in bar_chart().
    """
    values = _chart_input(labels, values, decimals)
    if not values:
        return '<p class="muted">No values to plot.</p>'
    if len(values) > PIE_MAX_SLICES:
        raise ValueError(f"A pie chart shows at most {PIE_MAX_SLICES} slices; combine the rest as Other or use bar_chart().")
    if any(value < 0 for value in values):
        raise ValueError("Pie slices must be non-negative parts of one whole; use bar_chart() for negative values.")
    total = sum(values)
    if total <= 0:
        raise ValueError("A pie chart needs a positive total.")
    cx, cy, radius = CHART_WIDTH / 2, 170, 130
    marks, sides = [], {1: [], -1: []}
    angle = -math.pi / 2  # the first slice starts at twelve o'clock and runs clockwise
    for index, (label, value) in enumerate(zip(labels, values)):
        share = value / total
        sweep = share * 2 * math.pi
        detail = f"{pct(share)} ({fmt(value, decimals=decimals)})"
        tooltip = f'<title>{esc(label)}: {esc(detail)}</title>'
        css = f"slice-{index + 1}"
        if share >= 1:
            marks.append(f'<circle class="{css}" cx="{cx}" cy="{cy}" r="{radius}">{tooltip}</circle>')
        elif share > 0:
            x1, y1 = cx + radius * math.cos(angle), cy + radius * math.sin(angle)
            x2, y2 = cx + radius * math.cos(angle + sweep), cy + radius * math.sin(angle + sweep)
            marks.append(f'<path class="{css}" stroke="#fafaf9" stroke-width="2" d="M{cx},{cy} L{x1:.2f},{y1:.2f} '
                         f'A{radius},{radius} 0 {1 if sweep > math.pi else 0} 1 {x2:.2f},{y2:.2f} Z">{tooltip}</path>')
        middle = angle + sweep / 2
        side = 1 if math.cos(middle) >= 0 else -1
        sides[side].append([cy + (radius + 22) * math.sin(middle), middle, str(label), detail])
        angle += sweep
    lowest = cy + radius
    for side, items in sides.items():
        items.sort(key=lambda item: item[0])
        for previous, item in zip(items, items[1:]):
            item[0] = max(item[0], previous[0] + 38)  # two text lines per label, never overlapping
        elbow = cx + (radius + 34) * side
        text_x = elbow + 8 * side
        anchor = "start" if side == 1 else "end"
        for label_y, middle, label, detail in items:
            edge_x, edge_y = cx + radius * math.cos(middle), cy + radius * math.sin(middle)
            marks.append(
                f'<polyline fill="none" stroke="#94a3b8" points="{edge_x:.2f},{edge_y:.2f} {elbow:.2f},{label_y:.2f}"/>'
                f'<text x="{text_x:.2f}" y="{label_y:.2f}" text-anchor="{anchor}">'
                f'<tspan font-weight="600">{esc(label)}</tspan>'
                f'<tspan x="{text_x:.2f}" dy="16">{esc(detail)}</tspan></text>'
            )
            lowest = max(lowest, label_y + 16)
    return _figure(title, unit, lowest + 24, marks)


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

    profile: the dict returned by profile_table().
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
        self._checked: dict[str, list[str]] = {area: [] for area in QUALITY_AREAS}
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
        under QUALITY_MIN_SHARE are collapsed beneath the area's table by default.
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

    def checked(self, area: str, note: str) -> None:
        """A check in one area that found nothing to record, stated so the reader knows it
        was made, such as "No two records share an order number and line number"."""
        if area not in QUALITY_AREAS:
            raise ValueError(f"Area must be one of: {', '.join(QUALITY_AREAS)}; got {area!r}")
        if not str(note).strip():
            raise ValueError("A checked note needs text.")
        self._checked[area].append(str(note))

    def coverage(self, field: str, start, end, records: int, why_it_matters: str) -> None:
        """The span of one date or period field, always shown under Coverage. start and end
        are the earliest and latest values in the words the reader should see: a date, a
        year, or text such as "November 1911" or "Jan–Jun 2020". records is the count of
        records carrying a valid value in the field. Record gaps within the span with
        quality("Coverage", ...)."""
        rows = self._profile["rows"]
        if any(not str(cell).strip() for cell in (field, start, end, why_it_matters)):
            raise ValueError("A coverage row needs a field, a start, an end, and why it matters.")
        if isinstance(records, bool) or not isinstance(records, numbers.Integral) or not 0 <= records <= rows:
            raise ValueError(f"Coverage records must be a record count from 0 to {rows}; got {records!r}")
        def label(value) -> str:
            if isinstance(value, dt.date):
                return value.strftime("%d %b %Y")
            if isinstance(value, numbers.Real) and float(value).is_integer():
                return str(int(value))  # a year, without a thousands separator
            return str(value)
        share = int(records) / rows if rows else 0.0
        self._quality.append(("Coverage", int(records), True, [
            field, f"Spans {label(start)} to {label(end)}", f"{fmt(records)} with a value ({pct(share)})", why_it_matters,
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
        timestamped .html file in the OS temporary directory, named after the source stem.
        The source is never written."""
        if path is None:
            stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
            stem = Path(self._profile["path"]).stem
            with tempfile.NamedTemporaryFile(prefix=f"{stem}-exploratory-data-analysis-{stamp}-",
                                             suffix=".html", delete=False) as output:
                path = Path(output.name)
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
            f'{self._source_context()}'
            '</header>'
        )

    def _source_context(self) -> str:
        source = self._profile.get("source", {})
        if source.get("format") != "xlsx":
            return ""
        notes = [f"Source: {self._profile['file']}, worksheet {source['sheet']}, range {source['range']}."]
        if source.get("table"):
            notes.append(f"Excel Table: {source['table']}.")
        notes.append("All rows and columns in the selected data range are included, regardless of visibility or filters.")
        if source["sheet_state"] != "visible":
            notes.append("The selected worksheet is hidden.")
        if source["hidden_rows_included"] or source["hidden_columns_included"]:
            rows, columns = len(source["hidden_rows_included"]), len(source["hidden_columns_included"])
            notes.append(f"Included {rows} hidden data row{'s' if rows != 1 else ''} and "
                         f"{columns} hidden column{'s' if columns != 1 else ''}.")
        if source["filters"]:
            active = any(item["criteria_present"] for item in source["filters"])
            notes.append("Saved filter criteria overlap the selection." if active
                         else "Filter controls are present without saved criteria.")
        if source["totals_rows_excluded"]:
            rows = ", ".join(str(row) for row in source["totals_rows_excluded"])
            notes.append(f"Declared Table totals row excluded from records: {rows}.")
        if self._profile.get("blank_records"):
            count = self._profile["blank_records"]
            notes.append(f"Retained {fmt(count)} entirely blank data row{'s' if count != 1 else ''}.")
        return f'<p class="muted">{esc(" ".join(notes))}</p>'

    def _field_profile(self) -> str:
        """Every field in file order with its apparent meaning."""
        rows = [[name, meaning] for name, meaning in self._meanings.items()]
        return table(["Field", "Apparent meaning"], rows, css_class="fields")

    def _data_quality(self) -> str:
        """One subheading and table per area in QUALITY_AREAS order, rows sorted by affected
        records, most first. Conditions under QUALITY_MIN_SHARE sit in a collapsed table
        beneath; checks that found nothing follow. An area with neither conditions nor
        checked notes says it was checked with nothing to report."""
        by_area = {area: [] for area in QUALITY_AREAS}
        for area, affected, always_show, row in self._quality:
            by_area[area].append((affected, always_show, row))
        rows = self._profile["rows"]
        columns = ["Field", "Observation", "Affected records", "Why it matters"]
        def ranked(items):
            return [row for _, _, row in sorted(items, key=lambda item: item[0], reverse=True)]
        parts = []
        for area, area_rows in by_area.items():
            parts.append(f'<h3>{esc(area)}</h3>')
            visible = [always_show or (affected / rows if rows else 0.0) >= QUALITY_MIN_SHARE
                       for affected, always_show, _ in area_rows]
            shown = [item for item, show in zip(area_rows, visible) if show]
            hidden = [item for item, show in zip(area_rows, visible) if not show]
            if shown:
                # Same fixed column widths in every area, so the tables line up down the section.
                parts.append(table(columns, ranked(shown), css_class="quality"))
            if hidden:
                noun = "condition" if len(hidden) == 1 else "conditions"
                parts.append(f'<details><summary>{len(hidden)} {noun} affecting less than '
                             f'{QUALITY_MIN_SHARE:.0%} of records</summary>'
                             f'{table(columns, ranked(hidden), css_class="quality")}</details>')
            for note in self._checked[area]:
                parts.append(f'<p class="muted">Checked: {esc(note)}</p>')
            if not area_rows and not self._checked[area]:
                parts.append('<p class="muted">Checked; nothing to report.</p>')
        return "".join(parts)

    def _overview_body(self) -> str:
        if self._overview and self._no_overview:
            raise ValueError("A report has overview items or a reason there are none, not both.")
        if self._overview:
            return "".join(self._overview)
        if self._no_overview:
            return f'<p>{esc(self._no_overview)}</p>'
        raise ValueError("Build the data overview or call no_overview() with why the file cannot support one.")
