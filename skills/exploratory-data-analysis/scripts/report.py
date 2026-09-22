"""Emitters for the exploratory data analysis HTML report.

Standard library only. Each emitter returns an HTML fragment; `write_report`
fills `assets/template.html` with the fragments, writes a fresh file to the OS
temp directory and opens it.

Sections, in reading order:

    header(profile, title, ...)        overview facts from the profile JSON
    structure(profile, ...)            sources and apparent relationships
    field_profile(profile, ...)        per-field table from the profile JSON
    section("observations", ...)       observation cards, built with card()
    closer_examination(items)          questions grounded in the observations
    analysis_notes(notes)              choices that affect interpretation

Visuals, each answering one question:

    chart(labels, datasets, kind=...)  bar, horizontal bar, line, scatter, stacked
    table(columns, rows, ...)          record-level evidence
    completeness_bar(share)            share of a field that is populated
    reconciliation(total_label, total, parts)   how two datasets line up
    heatmap(row_labels, col_labels, values)     small two-dimensional grid

Any card body also accepts raw HTML for visuals the emitters do not cover.
"""
from __future__ import annotations

import datetime as dt
import html
import itertools
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

__all__ = [
    "analysis_notes",
    "card",
    "chart",
    "closer_examination",
    "code",
    "completeness_bar",
    "field_profile",
    "fmt",
    "header",
    "heatmap",
    "pct",
    "reconciliation",
    "section",
    "structure",
    "table",
    "write_report",
]

INDIGO = "#4f46e5"
PALETTE = [INDIGO, "#0ea5e9", "#14b8a6", "#f59e0b", "#8b5cf6", "#64748b"]
TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "template.html"

_ids = itertools.count(1)


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------


def esc(value) -> str:
    return "" if value is None else html.escape(str(value), quote=True)


def fmt(value, decimals: int | None = None, unit: str | None = None) -> str:
    """Format a number with thousands separators and sensible precision."""
    if value is None:
        return "—"
    if isinstance(value, str):
        return esc(value)
    number = float(value)
    if decimals is None:
        decimals = 0 if number.is_integer() or abs(number) >= 100 else 2
    text = f"{number:,.{decimals}f}"
    if unit:
        text = f"{unit}{text}" if len(unit) == 1 else f"{text} {unit}"
    return text


def pct(share, decimals: int = 1) -> str:
    """Format a 0–1 share as a percentage."""
    return "—" if share is None else f"{float(share) * 100:.{decimals}f}%"


def code(value) -> str:
    return f'<code class="font-mono text-sm bg-slate-100 px-1.5 py-0.5 rounded">{esc(value)}</code>'


def _paragraph(label: str | None, text: str | None, tone: str = "text-slate-600") -> str:
    if not text:
        return ""
    prefix = f"<strong class='text-slate-900'>{esc(label)}:</strong> " if label else ""
    return f'<p class="text-sm {tone}">{prefix}{text}</p>'


# ---------------------------------------------------------------------------
# Page sections
# ---------------------------------------------------------------------------


def section(section_id: str, title: str, body: str, subtitle: str | None = None) -> str:
    sub = f'<p class="text-sm text-slate-600 mt-1">{subtitle}</p>' if subtitle else ""
    return (
        f'<section id="{esc(section_id)}" class="space-y-6">'
        f'<div><h2 class="text-xl font-semibold">{esc(title)}</h2>{sub}</div>'
        f"{body}</section>"
    )


def header(
    profile: dict,
    title: str,
    grain: str | None = None,
    note: str | bool = True,
    limitation: str | None = None,
    period: str | None = None,
) -> str:
    """Overview facts. `grain` is the apparent grain in words; `note` is the
    interpretation note (True for the default wording, a string to replace it,
    False to omit); `limitation` surfaces a material limitation near the top;
    `period` replaces the coverage period, which defaults to that of the
    largest tabular source."""
    tabular = [s for s in profile["sources"] if s.get("tabular")]
    rows = sum(s["rows"] for s in tabular)
    fields = sum(s["fields"] for s in tabular)
    facts = [f"{fmt(rows)} rows", f"{fmt(fields)} fields"]
    if period is None:
        largest = max(tabular, key=lambda s: s["rows"], default=None)
        if largest and largest.get("period"):
            period = f"{largest['period']['start'][:10]} to {largest['period']['end'][:10]}"
    if period:
        facts.append(esc(period))
    sources = "".join(
        f"<li>{code(s['id'])}{' <span class=\"text-amber-700\">hidden</span>' if s.get('hidden') else ''}"
        f"{' <span class=\"text-amber-700\">non-tabular</span>' if not s.get('tabular') else ''}</li>"
        for s in profile["sources"]
    )
    grain_html = (
        f'<div><div class="text-xs uppercase tracking-wider text-slate-500">Apparent grain</div>'
        f'<div class="text-sm">{esc(grain)}</div></div>'
        if grain
        else ""
    )
    if note is True:
        note = (
            "Field meanings and dataset grain are inferred from names, values, and "
            "relationships unless otherwise stated."
        )
    note_html = (
        f'<p class="text-sm text-slate-600 border-l-2 border-amber-400 pl-3">'
        f"<strong>Interpretation note:</strong> {esc(note)}</p>"
        if note
        else ""
    )
    limitation_html = (
        f'<p class="text-sm text-amber-800 bg-amber-50 border border-amber-200 rounded-lg p-3">'
        f"<strong>Limitation:</strong> {esc(limitation)}</p>"
        if limitation
        else ""
    )
    generated = profile.get("generated", dt.datetime.now().isoformat())[:10]
    return (
        f'<header id="overview" class="space-y-5">'
        f'<div><h1 class="text-3xl font-semibold tracking-tight">{esc(title)}</h1>'
        f'<p class="text-sm text-slate-500 mt-1">Exploratory data analysis · generated {esc(generated)}</p></div>'
        f'<p class="text-lg text-slate-700 numeric">{" · ".join(facts)}</p>'
        f'<div class="grid gap-6 sm:grid-cols-2">'
        f'<div><div class="text-xs uppercase tracking-wider text-slate-500">Sources</div>'
        f'<ul class="text-sm space-y-1 mt-1">{sources}</ul></div>{grain_html}</div>'
        f"{limitation_html}{note_html}</header>"
    )


def structure(profile: dict, extra_html: str = "", subtitle: str | None = None) -> str:
    """Sources table plus apparent relationships. `extra_html` is a slot for a
    hand-built relationship diagram or any other structural visual."""
    rows = []
    for s in profile["sources"]:
        keys = ", ".join(s.get("candidate_keys") or []) or "—"
        kind = "non-tabular" if not s.get("tabular") else ("hidden" if s.get("hidden") else "")
        rows.append([code(s["id"]), fmt(s["rows"]), fmt(s["fields"]), esc(keys), esc(kind)])
    body = table(["Source", "Rows", "Fields", "Candidate keys", ""], rows, numeric=[1, 2], raw=True)

    rels = profile.get("relationships") or []
    if rels:
        items = []
        for r in rels:
            share = r["from_rows_matched"] / r["from_rows"] if r["from_rows"] else 0
            items.append(
                f"<li>{code(r['field'])}: {code(r['from'])} → {code(r['to'])}, apparent {esc(r['cardinality'])}. "
                f"<span class='numeric'>{fmt(r['from_rows_matched'])} of {fmt(r['from_rows'])} rows matched "
                f"({pct(share)}), {fmt(r['from_rows_unmatched'])} unmatched.</span></li>"
            )
        body += (
            '<div><h3 class="text-base font-semibold mb-2">Apparent relationships</h3>'
            f'<ul class="text-sm text-slate-700 space-y-2">{"".join(items)}</ul></div>'
        )
    notes = [(s["id"], n) for s in profile["sources"] for n in s.get("notes", [])]
    if notes:
        body += (
            '<div><h3 class="text-base font-semibold mb-2">Structural notes</h3>'
            f'<ul class="text-sm text-slate-600 list-disc pl-5 space-y-1">'
            f'{"".join(f"<li>{code(source_id)}: {esc(n)}</li>" for source_id, n in notes)}</ul></div>'
        )
    return section("structure", "Data structure", body + extra_html, subtitle)


def field_profile(
    profile: dict,
    notes: dict[str, str] | None = None,
    roles: dict[str, str] | None = None,
    sources: list[str] | None = None,
) -> str:
    """One table per tabular source. `notes` maps field name to a note that
    replaces the automatic one; `roles` maps field name to a corrected role;
    `sources` limits the output to the named source ids."""
    notes = notes or {}
    roles = roles or {}
    blocks = []
    for s in profile["sources"]:
        if not s.get("tabular") or (sources and s["id"] not in sources):
            continue
        rows = []
        for c in s["columns"]:
            role = roles.get(c["name"], c["role"])
            coverage = (
                f'<div class="flex items-center gap-2"><span class="numeric w-14 text-right">{pct(c["coverage"])}</span>'
                f'<div class="w-24">{completeness_bar(c["coverage"])}</div></div>'
            )
            rows.append(
                [
                    code(c["name"]),
                    esc(role),
                    coverage,
                    fmt(c["distinct"]) if c["distinct"] else "—",
                    esc(_range_or_common(c)),
                    esc(notes.get(c["name"], _auto_note(c))),
                ]
            )
        heading = f'<h3 class="text-base font-semibold">{code(s["id"])}</h3>' if len(profile["sources"]) > 1 else ""
        blocks.append(
            heading
            + table(
                ["Field", "Apparent role", "Coverage", "Distinct", "Range / common values", "Note"],
                rows,
                numeric=[3],
                raw=True,
            )
        )
    return section("field-profile", "Field profile", "".join(blocks))


def _range_or_common(c: dict) -> str:
    role = c["role"]
    if role == "measure":
        return f"{fmt(c['min'])} to {fmt(c['max'])}"
    if role == "date":
        return f"{c['start'][:10]} to {c['end'][:10]}"
    if role == "category":
        return ", ".join(f"{v['value'][:24]} {pct(v['pct'], 0)}" for v in c["top_values"][:3])
    if role == "identifier" and c.get("formats"):
        return c["formats"][0]["pattern"]
    return "—"


def _auto_note(c: dict) -> str:
    parts = []
    if c.get("stored_as") == "text":
        parts.append("stored as text")
    if c["role"] == "identifier":
        parts.append("appears unique" if c["unique"] else f"{fmt(c['duplicates'])} duplicates")
    if c["role"] == "measure":
        if c["negatives"]:
            parts.append(f"{fmt(c['negatives'])} negative")
        if c["zeros"]:
            parts.append(f"{fmt(c['zeros'])} zero")
    if c["role"] == "category" and c.get("label_variants"):
        parts.append(f"{len(c['label_variants'])} label variants")
    if c["role"] == "date" and c.get("far_values"):
        parts.append(f"{fmt(c['far_values'])} far from the period")
    if c["missing"]:
        parts.append(f"{fmt(c['missing'])} missing")
    if c["role"] == "empty":
        parts.append("no values")
    return "; ".join(parts)


def closer_examination(items: list[tuple[str, str]]) -> str:
    """`items` are (heading, body) pairs, each grounded in an observation shown."""
    body = "".join(
        f'<div class="rounded-xl border border-slate-200 bg-white p-5">'
        f'<h3 class="text-base font-semibold">{esc(heading)}</h3>'
        f'<p class="text-sm text-slate-600 mt-1">{text}</p></div>'
        for heading, text in items
    )
    return section("closer-examination", "Areas for closer examination", f'<div class="space-y-4">{body}</div>')


def analysis_notes(notes: list[str]) -> str:
    body = f'<ul class="text-sm text-slate-600 list-disc pl-5 space-y-1">{"".join(f"<li>{n}</li>" for n in notes)}</ul>'
    return section("analysis-notes", "Analysis notes", body)


# ---------------------------------------------------------------------------
# Observation cards and visuals
# ---------------------------------------------------------------------------


def card(
    title: str,
    visual: str = "",
    observation: str | None = None,
    context: str | None = None,
    interpretation: str | None = None,
    open_question: str | None = None,
) -> str:
    """One observation. `visual` is any fragment: chart(), table(),
    reconciliation(), heatmap(), or raw HTML."""
    return (
        '<article class="rounded-xl border border-slate-200 bg-white p-6 space-y-5">'
        f'<h3 class="text-base font-semibold">{esc(title)}</h3>'
        f"{_paragraph('Observation', observation, 'text-slate-700')}"
        f"{visual}"
        f"{_paragraph('Context', context)}"
        f"{_paragraph('Interpretation', interpretation)}"
        f"{_paragraph('Open question', open_question)}"
        "</article>"
    )


def chart(
    labels: list | None,
    datasets,
    kind: str = "bar",
    *,
    horizontal: bool = False,
    stacked: bool = False,
    log: bool = False,
    unit: str | None = None,
    value_label: str | None = None,
    category_label: str | None = None,
    height: int = 360,
) -> str:
    """Chart.js chart. `datasets` is a list of numbers, or a list of
    {"label", "data"} dicts for several series. For `kind="scatter"` pass
    data as [{"x":..,"y":..}, ...]. Bin and aggregate before calling."""
    if datasets and not isinstance(datasets[0], dict):
        datasets = [{"data": list(datasets)}]
    series = []
    for i, d in enumerate(datasets):
        color = PALETTE[i % len(PALETTE)]
        entry = {"label": d.get("label", ""), "data": d["data"], "backgroundColor": color, "borderColor": color}
        if kind == "line":
            entry.update(fill=False, tension=0.2, pointRadius=2)
        if kind == "scatter":
            entry["pointRadius"] = 3
        series.append(entry)

    value_axis, category_axis = ("x", "y") if horizontal else ("y", "x")
    axis_value = {"grid": {"color": "#e2e8f0"}, "stacked": stacked}
    if log:
        axis_value["type"] = "logarithmic"
    else:
        axis_value["beginAtZero"] = True
    axis_category = {"grid": {"display": False}, "stacked": stacked}
    if value_label or unit:
        axis_value["title"] = {"display": True, "text": value_label or unit}
    if category_label:
        axis_category["title"] = {"display": True, "text": category_label}
    if kind == "scatter":
        scales = {"x": dict(axis_category, grid={"color": "#e2e8f0"}), "y": axis_value}
    else:
        scales = {value_axis: axis_value, category_axis: axis_category}

    config = {
        "type": "bar" if kind == "stacked" else kind,
        "data": {"labels": labels, "datasets": series},
        "options": {
            "indexAxis": "y" if horizontal else "x",
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {"legend": {"display": len(series) > 1}},
            "scales": scales,
        },
    }
    if kind == "stacked":
        for axis in scales.values():
            axis["stacked"] = True
    chart_id = f"chart{next(_ids)}"
    return (
        f'<div class="chart-container" style="height:{int(height)}px"><canvas id="{chart_id}"></canvas></div>'
        f'<script>new Chart(document.getElementById("{chart_id}"), {json.dumps(config)});</script>'
    )


def table(
    columns: list[str],
    rows: list[list],
    title: str | None = None,
    numeric: list[int] | None = None,
    raw: bool = False,
) -> str:
    """Light table. `numeric` lists column indexes to right-align. Cell values
    are escaped unless `raw=True` (for cells already built with code(), fmt())."""
    numeric = set(numeric or [])
    head = "".join(
        f'<th class="py-2 pr-4 font-medium{" text-right" if i in numeric else ""}">{esc(c)}</th>'
        for i, c in enumerate(columns)
    )
    body = "".join(
        "<tr>"
        + "".join(
            f'<td class="py-2 pr-4 align-top{" text-right numeric" if i in numeric else ""}">'
            f"{cell if raw else (fmt(cell) if isinstance(cell, (int, float)) and i in numeric else esc(cell))}</td>"
            for i, cell in enumerate(row)
        )
        + "</tr>"
        for row in rows
    )
    caption = f'<h4 class="text-sm font-semibold text-slate-700 mb-2">{esc(title)}</h4>' if title else ""
    return (
        f'<div class="scroll-table">{caption}<table class="w-full text-sm">'
        f'<thead class="border-b border-slate-200 text-left text-slate-500"><tr>{head}</tr></thead>'
        f'<tbody class="divide-y divide-slate-100">{body}</tbody></table></div>'
    )


def completeness_bar(share: float) -> str:
    width = max(0.0, min(100.0, float(share) * 100))
    return (
        '<div class="w-full bg-slate-100 rounded-full h-2">'
        f'<div class="bg-indigo-500 h-2 rounded-full" style="width: {width:.1f}%"></div></div>'
    )


def reconciliation(total_label: str, total: int, parts: list[tuple[str, int]]) -> str:
    """Plain counts: a total line, then each part with its share of the total."""
    lines = "".join(
        f'<div class="flex justify-between gap-6"><span>{esc(label)}</span>'
        f'<span class="numeric">{fmt(count)} <span class="text-slate-500">({pct(count / total if total else 0)})</span></span></div>'
        for label, count in parts
    )
    return (
        '<div class="rounded-lg bg-slate-50 p-4 text-sm space-y-1 max-w-md">'
        f'<div class="flex justify-between gap-6 font-semibold"><span>{esc(total_label)}</span>'
        f'<span class="numeric">{fmt(total)}</span></div>{lines}</div>'
    )


def heatmap(row_labels: list, col_labels: list, values: list[list], decimals: int = 0) -> str:
    """Small grid colored by intensity, with labels and values visible."""
    flat = [v for row in values for v in row if v is not None]
    peak = max(flat) if flat else 1
    head = "".join(f'<div class="text-xs text-slate-500 text-center">{esc(c)}</div>' for c in col_labels)
    cells = []
    for label, row in zip(row_labels, values):
        cells.append(f'<div class="text-xs text-slate-500 pr-2 text-right self-center">{esc(label)}</div>')
        for v in row:
            alpha = 0.06 + 0.84 * (float(v) / peak if peak and v is not None else 0)
            text_color = "#fff" if alpha > 0.55 else "#1e293b"
            cells.append(
                f'<div class="rounded text-xs text-center py-1.5 numeric" '
                f'style="background: rgba(79,70,229,{alpha:.2f}); color: {text_color}">'
                f"{fmt(v, decimals) if v is not None else ''}</div>"
            )
    columns = f"auto repeat({len(col_labels)}, minmax(0, 1fr))"
    return (
        f'<div class="grid gap-1" style="grid-template-columns: {columns}">'
        f"<div></div>{head}{''.join(cells)}</div>"
    )


# ---------------------------------------------------------------------------
# Writing the page
# ---------------------------------------------------------------------------


def write_report(
    title: str,
    sections: list[str],
    path: str | os.PathLike | None = None,
    open_report: bool = True,
) -> Path:
    """Fill the template, write a fresh file to the OS temp directory (or
    `path`), open it for the user, and return the path."""
    template = TEMPLATE.read_text(encoding="utf-8")
    page = template.replace("{{title}}", esc(title)).replace("{{body}}", "\n".join(sections))
    if path is None:
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40] or "report"
        path = Path(tempfile.gettempdir()) / f"eda-{slug}-{dt.datetime.now():%Y%m%d-%H%M%S}.html"
    path = Path(path)
    path.write_text(page, encoding="utf-8")
    if open_report:
        _open(path)
    return path


def _open(path: Path) -> None:
    try:
        if sys.platform.startswith("win"):
            os.startfile(str(path))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except OSError:
        pass
