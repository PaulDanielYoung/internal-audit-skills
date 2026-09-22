"""Offline HTML report helpers. Text arguments are escaped; section bodies and
card visuals accept HTML produced by these helpers. No browser or network needed.
"""
from __future__ import annotations

import html
import math
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "template.html"


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def fmt(value, decimals: int = 2) -> str:
    if value is None:
        return "—"
    if isinstance(value, int):
        return f"{value:,}"
    number = float(value)
    if not math.isfinite(number):
        return "—"
    return f"{number:,.0f}" if number.is_integer() else f"{number:,.{decimals}f}"


def pct(share: float | None) -> str:
    return "—" if share is None else f"{share:.1%}"


def output_directory(csv_path: str | Path) -> Path:
    source = Path(csv_path).resolve()
    if source.suffix.lower() != ".csv":
        raise ValueError("Expected a .csv source path.")
    return source.parent / f"{source.stem} - exploratory data analysis"


def section(title: str, body: str) -> str:
    return f'<section><h2>{esc(title)}</h2>{body}</section>'


def header(profile: dict, title: str, *, grain: str, limitation: str = "") -> str:
    limit = f'<p class="limitation">{esc(limitation)}</p>' if limitation else ""
    return (
        f'<header><p class="eyebrow">Exploratory data analysis</p><h1>{esc(title)}</h1>'
        f'<p class="facts">{fmt(profile["rows"])} records · {fmt(profile["fields"])} fields</p>'
        f'<p>Source: <code>{esc(profile["file"])}</code> · Generated {esc(profile["generated"])}</p>'
        f'<p><strong>Grain:</strong> {esc(grain)}</p>'
        '<p class="muted">Meanings are apparent unless established by supporting context. '
        'Observations guide further understanding; they are not audit conclusions.</p>'
        f'{limit}</header>'
    )


def table(columns: list[str], rows: list[list], title: str = "") -> str:
    caption = f'<caption>{esc(title)}</caption>' if title else ""
    headings = "".join(f'<th scope="col">{esc(column)}</th>' for column in columns)
    body = "".join(
        '<tr>' + "".join(f'<td>{esc(cell)}</td>' for cell in row) + '</tr>' for row in rows
    )
    return f'<div class="scroll-table"><table>{caption}<thead><tr>{headings}</tr></thead><tbody>{body}</tbody></table></div>'


def field_profile(profile: dict) -> str:
    rows = []
    for field in profile["columns"]:
        role = field["role"]
        summary = "No usable values" if not field["parsed"] else ""
        if role == "measure" and "min" in field:
            summary = (
                f"Range {fmt(field['min'])} to {fmt(field['max'])}; median {fmt(field['median'])}; "
                f"P05–P95 {fmt(field['p05'])} to {fmt(field['p95'])}; "
                f"{fmt(field['negatives'])} negative, {fmt(field['zeros'])} zero"
            )
        elif role == "date" and "start" in field:
            summary = f"{field['start']} to {field['end']}"
        elif field.get("top_values"):
            summary = "; ".join(f"{item['value']} ({fmt(item['count'])})" for item in field["top_values"])
            if role == "identifier":
                summary = f"{fmt(field['duplicates'])} repeated nonblank values; " + summary
        rows.append([
            field["name"], role, fmt(field["blank"]), fmt(field["parse_failures"]),
            fmt(field["distinct"]), summary,
        ])
    return section(
        "Field profile",
        '<p class="muted">Blank and unparsed counts are separate. Distinct counts use original '
        'nonblank strings; numerical and date summaries use successfully parsed values. '
        'Common values show counts, up to five per field.</p>'
        + table(["Field", "Apparent role", "Blank", "Unparsed", "Distinct", "Summary"], rows),
    )


def card(title: str, visual: str = "", *, observation: str, context: str,
         interpretation: str = "", open_question: str = "") -> str:
    paragraphs = "".join(
        f'<p><strong>{label}:</strong> {esc(text)}</p>'
        for label, text in [
            ("Observation", observation), ("Context", context),
            ("Interpretation", interpretation), ("Open question", open_question),
        ] if text
    )
    return f'<article><h3>{esc(title)}</h3>{paragraphs}{visual}</article>'


def chart(labels: list, values: list, *, title: str, unit: str = "") -> str:
    """Horizontal SVG bars with a zero baseline and a complete data table.

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
    left, width = 240, 430
    def x(value):
        return left + (value - low) / span * width
    zero = x(0)
    height = 48 + len(values) * 34
    marks = [f'<line x1="{zero:.2f}" x2="{zero:.2f}" y1="16" y2="{height - 28}" stroke="#94a3b8"/>']
    for index, (label, value) in enumerate(zip(labels, values)):
        y = 20 + index * 34
        label = str(label)
        short = label if len(label) <= 30 else label[:29] + "…"
        marks.append(
            f'<text x="226" y="{y + 16}" text-anchor="end">{esc(short)}</text>'
            f'<rect x="{min(zero, x(value)):.2f}" y="{y}" width="{abs(x(value) - zero):.2f}" '
            f'height="24" rx="3" fill="#4f46e5"><title>{esc(label)}: {esc(fmt(value))}</title></rect>'
            f'<text x="688" y="{y + 16}">{esc(fmt(value))}</text>'
        )
    marks.append(f'<text x="{zero:.2f}" y="{height - 7}" text-anchor="middle">0</text>')
    data_table = table(["Category", unit or "Value"], [[label, fmt(value)] for label, value in zip(labels, values)])
    return (
        f'<figure><figcaption>{esc(title)}{(" · " + esc(unit)) if unit else ""}</figcaption>'
        f'<div class="scroll-chart"><svg xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{esc(title)}" viewBox="0 0 820 {height}"><title>{esc(title)}</title>'
        f'{"".join(marks)}</svg></div><details><summary>Chart values</summary>{data_table}</details></figure>'
    )


def analysis_notes(notes: list[str]) -> str:
    return section("Analysis notes", '<ul>' + "".join(f'<li>{esc(note)}</li>' for note in notes) + '</ul>')


def write_report(title: str, sections: list[str], path: str | Path) -> Path:
    """Write to an explicit HTML path. Reruns replace that report, never the CSV."""
    path = Path(path).resolve()
    if path.suffix.lower() != ".html":
        raise ValueError("Report output must have an .html extension.")
    template = TEMPLATE.read_text(encoding="utf-8")
    page = template.replace("{{title}}", esc(title)).replace("{{body}}", "\n".join(sections))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page, encoding="utf-8")
    return path
