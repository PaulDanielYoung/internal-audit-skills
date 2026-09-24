"""Visuals for the report: bar, line, and pie charts, and tables, as values.

Each entry point validates its input, folds a long tail into Other where its chart kind has
a limit, draws inline SVG or HTML, and returns a Visual the Report accepts. The palette and
the CSS the visuals need live here, in STYLE, which the Report places in the page.

No browser, network, JavaScript, or external asset is needed to read the result.
"""
from __future__ import annotations

import math
import numbers
import textwrap
from dataclasses import dataclass

from formatting import esc, fmt, pct

# Bars are upright; past this many groups, the smallest fold into Other.
BAR_MAX_CATEGORIES = 12
# Labels wrap beneath their bars up to this many lines; longer labels tilt instead.
BAR_LABEL_MAX_LINES = 3
BAR_LABEL_TILT = 40  # degrees, as Chart.js tilts tick labels that do not fit
CHAR_WIDTH = 7.2  # approximate width of one 13px character in chart units
# A line labels every point up to this many; beyond it, only the first, last, peak, and low.
LINE_LABEL_ALL_MAX = 12
# Period labels wrap beneath their points up to this many lines; longer ones thin out.
LINE_LABEL_MAX_LINES = 2
# Slices a reader can compare; past this many parts, the smallest fold into Other.
PIE_MAX_SLICES = 5
CHART_WIDTH = 820


OTHER = "Other"
# The palette: the mark colour, and the gap drawn between pie slices and inside a hollow marker.
ACCENT = "#4f46e5"
GAP = "#ffffff"
# Pie slices in order: Okabe-Ito colors, distinguishable with common color-vision deficiencies.
SLICE_COLORS = ("#0072b2", "#e69f00", "#009e73", "#d55e00", "#cc79a7")
assert len(SLICE_COLORS) >= PIE_MAX_SLICES

STYLE = """
    figure { margin: 24px 0 0; }
    figcaption { font-weight: 600; margin-bottom: 10px; }
    .scroll-chart, .scroll-table { overflow-x: auto; }
    svg { width: 100%; min-width: 640px; display: block; }
    svg text { font: 13px system-ui, sans-serif; fill: #475569; }
""" + "".join(f"    .slice-{index} {{ fill: {color}; }}\n" for index, color in enumerate(SLICE_COLORS[:PIE_MAX_SLICES], 1))


@dataclass(frozen=True)
class Other:
    """What a chart folded into its Other group: how many of the driver's groups, their
    combined value, and whether that outweighs the largest group shown."""
    groups: int
    value: float
    outweighs_largest: bool


@dataclass(frozen=True)
class Visual:
    """One chart or table for the report. kind is "bar", "line", "pie", or "table"; html is
    the markup; labels and values are what a chart drew, after any fold; other reports a
    fold; rows counts a table's body rows."""
    kind: str
    html: str
    labels: tuple = ()
    values: tuple = ()
    other: Other | None = None
    rows: int = 0

    def __post_init__(self):
        object.__setattr__(self, "labels", tuple(self.labels))
        object.__setattr__(self, "values", tuple(self.values))

    @property
    def is_chart(self) -> bool:
        return self.kind in {"bar", "line", "pie"}


def _chart_input(labels: list, values: list, decimals: int) -> tuple[list[str], list[float]]:
    """Validate the arguments every chart shares; labels as text, values as floats."""
    if len(labels) != len(values):
        raise ValueError("Chart labels and values must have the same length.")
    if isinstance(decimals, bool) or not isinstance(decimals, numbers.Integral) or decimals < 0:
        raise ValueError("Chart decimals must be a non-negative integer.")
    values = [float(value) for value in values]
    if not values:
        raise ValueError("A chart with no values is not a chart; say why there is nothing to plot.")
    if not all(math.isfinite(value) for value in values):
        raise ValueError("Chart values must be finite; explain exclusions before plotting.")
    return [str(label) for label in labels], values


def _fold(labels: list, values: list, decimals: int, limit: int) -> tuple[list[str], list[float], Other | None]:
    """Beyond limit groups, fold the smallest into one Other group drawn last. Survivors keep
    their order; a group the driver already labeled Other joins the fold. Ties at the cut
    keep the earlier group."""
    labels, values = _chart_input(labels, values, decimals)
    own = [index for index, label in enumerate(labels) if label.strip().lower() == OTHER.lower()]
    if len(labels) <= limit and not (own and len(labels) > limit):
        return labels, values, None
    ranked = sorted((index for index in range(len(labels)) if index not in own),
                    key=lambda index: (-values[index], index))
    keep = sorted(ranked[:limit - 1])
    folded = [index for index in range(len(labels)) if index not in keep and index not in own]
    other_value = sum(values[index] for index in folded) + sum(values[index] for index in own)
    kept_labels = [labels[index] for index in keep] + [OTHER]
    kept_values = [values[index] for index in keep] + [other_value]
    largest = max(kept_values[:-1]) if keep else 0.0
    return kept_labels, kept_values, Other(len(folded), other_value, other_value > largest)


def table_html(columns: list[str], rows: list[list], title: str = "", *, css_class: str = "") -> str:
    """The markup of one table; cells are escaped. The Report uses this for its own tables."""
    caption = f'<caption>{esc(title)}</caption>' if title else ""
    headings = "".join(f'<th scope="col">{esc(column)}</th>' for column in columns)
    body = "".join(
        '<tr>' + "".join(f'<td>{esc(cell)}</td>' for cell in row) + '</tr>' for row in rows
    )
    attrs = f' class="{esc(css_class)}"' if css_class else ""
    return f'<div class="scroll-table"><table{attrs}>{caption}<thead><tr>{headings}</tr></thead><tbody>{body}</tbody></table></div>'


def table(columns: list[str], rows: list[list], title: str = "") -> Visual:
    """Group comparisons, distributions, or representative records. Cells are escaped;
    format numeric cells with fmt(), money(), or pct() first. An observation's table is a
    sample of the evidence: the columns the prose cites, and a title naming the selection
    and its share of the population."""
    return Visual("table", table_html(columns, rows, title), rows=len(rows))


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


def bar_chart(labels: list, values: list, *, title: str, unit: str = "", decimals: int = 2) -> Visual:
    """Upright bars comparing distinct items or groups, with a zero baseline, full labels,
    and visible values.

    Supply aggregated, finite values in the order the reader should see. Beyond
    BAR_MAX_CATEGORIES groups, the smallest fold into one Other bar drawn last; the survivors
    keep their order, and the Visual's other reports what was folded. Labels wrap beneath
    their bars when every word fits the bar's width in at most BAR_LABEL_MAX_LINES lines;
    otherwise every label tilts. Negative values extend below zero. decimals sets display
    precision for non-integral values in labels and tooltips, without changing bar heights;
    integral values keep no decimal places, as in fmt().
    """
    labels, values, other = _fold(labels, values, decimals, BAR_MAX_CATEGORIES)
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
            f'height="{abs(y(value) - zero):.2f}" rx="3" fill="{ACCENT}"><title>{esc(label)}: {display_value}</title></rect>'
            f'<text x="{center:.2f}" y="{value_y:.2f}" text-anchor="middle">{display_value}</text>{axis_label}'
        )
    return Visual("bar", _figure(title, unit, height, marks), labels=labels, values=values, other=other)


def _nice_ticks(low: float, high: float, count: int = 5) -> list[float]:
    """Round axis ticks from low to high; callers include zero in the range."""
    span = high - low or 1
    raw = span / (count - 1)
    magnitude = 10 ** math.floor(math.log10(raw))
    step = next(m * magnitude for m in (1, 2, 2.5, 5, 10) if m * magnitude >= raw)
    start, stop = math.floor(low / step) * step, math.ceil(high / step) * step
    return [start + index * step for index in range(round((stop - start) / step) + 1)]


def line_chart(labels: list, values: list, *, title: str, unit: str = "", decimals: int = 2,
               partial_last: bool = False) -> Visual:
    """One series changing over continuous time, left to right, on a y-axis that includes zero.

    labels are the periods in chronological order, written as labels (1940s, 2022-Q3).
    Supply every period in the range, with zero for an empty one, so the time axis stays
    even. Every point has a marker; values are labeled on every point up to
    LINE_LABEL_ALL_MAX points, and otherwise on the first, last, peak, and low. Period
    labels wrap beneath their points, or thin to every nth, counted back from the last,
    when a word is too long for its slot. partial_last draws the final segment dashed and marks its period "to date".
    decimals works as in bar_chart().
    """
    labels, values = _chart_input(labels, values, decimals)
    if len(values) < 2:
        raise ValueError("A line chart needs at least two periods; use bar_chart() for one.")
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
    marks.append(f'<polyline fill="none" stroke="{ACCENT}" stroke-width="2.5" points="'
                 + " ".join(f"{px:.2f},{py:.2f}" for px, py in solid) + '"/>')
    if partial_last:
        (x1, y1), (x2, y2) = points[-2:]
        marks.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                     f'stroke="{ACCENT}" stroke-width="2.5" stroke-dasharray="6 5"/>')
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
        marks.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="4" fill="{GAP if hollow else ACCENT}" '
                     f'stroke="{ACCENT}" stroke-width="2"><title>{esc(label)}: {display_value}</title></circle>')
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
    return Visual("line", _figure(title, unit, height, marks), labels=labels, values=values)


def pie_chart(labels: list, values: list, *, title: str, unit: str = "", decimals: int = 2) -> Visual:
    """Parts of one whole, each labeled directly with its share and value. The values must
    be non-negative parts that add up to the whole the title names. Beyond PIE_MAX_SLICES
    parts, the smallest fold into one Other slice drawn last, and the Visual's other reports
    what was folded. Slices take the colorblind-safe palette in STYLE, in order. decimals
    works as in bar_chart().
    """
    labels, values, other = _fold(labels, values, decimals, PIE_MAX_SLICES)
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
            marks.append(f'<path class="{css}" stroke="{GAP}" stroke-width="2" d="M{cx},{cy} L{x1:.2f},{y1:.2f} '
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
    return Visual("pie", _figure(title, unit, lowest + 24, marks), labels=labels, values=values, other=other)


