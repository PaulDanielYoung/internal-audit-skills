"""Offline HTML report for one exploratory data analysis.

The driver builds a Report: construct it with the profile and the reader-facing framing,
explain the mechanical conditions and coverage spans it derived, add judged conditions,
overview items, observations, and limitations as the analysis produces them, then write().
The Report owns section order and titles, leaves out empty optional sections, validates each
addition, and escapes every text argument. Visuals are values from the charts module.

No browser, network, JavaScript, or external asset is needed to read the result.
"""
from __future__ import annotations

import datetime as dt
import numbers
import tempfile
from dataclasses import dataclass
from pathlib import Path

from charts import STYLE, Visual, table_html
from formatting import NA, esc, fmt, money, pct  # noqa: F401  re-exported for the driver

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "template.html"
# The field name of a whole-record condition, such as an entirely blank record.
ALL_FIELDS = "All fields"
QUALITY_AREAS = ("Completeness", "Validity", "Uniqueness", "Consistency", "Coverage")
# Default display threshold; a material condition can opt in with always_show=True.
QUALITY_MIN_SHARE = 0.01
# A table supporting an observation is a sample of the evidence, not a data dump.
OBSERVATION_MAX_ROWS = 10


def _section(title: str, body: str) -> str:
    return f'<section><h2>{esc(title)}</h2>{body}</section>'


# --- Mechanical conditions and coverage spans --------------------------------------------

@dataclass(frozen=True)
class Condition:
    """One data quality condition Report derived from the profile. The driver explains it
    with Report.explain(field, kind, why_it_matters); the field, area, observation, and
    affected count are settled."""
    field: str
    kind: str
    area: str
    observation: str
    affected: int

    @property
    def key(self) -> tuple[str, str]:
        return (self.field, self.kind)


@dataclass(frozen=True)
class Span:
    """The reach of one date field, derived from the profile: its earliest and latest valid
    values and the count of records carrying one. The driver explains it with
    Report.explain(field, "span", why_it_matters)."""
    field: str
    start: str
    end: str
    records: int

    @property
    def key(self) -> tuple[str, str]:
        return (self.field, "span")


_PARSE_NOUNS = {"measure": "number", "date": "date", "year": "year", "month": "month"}


def _mechanical(profile: dict) -> tuple[list[Condition], list[Span]]:
    """Every condition and span the profile establishes without judgment, in field order."""
    rows = profile["rows"]
    conditions, spans = [], []
    for field in profile["columns"]:
        name, role = field["name"], field["role"]
        if rows and field["blank"] == rows:
            conditions.append(Condition(name, "blank_field", "Completeness", "Entirely blank", rows))
        elif field["blank"]:
            conditions.append(Condition(name, "blank", "Completeness", "Blank", field["blank"]))
        if field["parse_failures"]:
            noun = _PARSE_NOUNS.get(role, role)
            conditions.append(Condition(name, "unparsed", "Validity", f"Does not parse as a {noun}", field["parse_failures"]))
        if field["source_errors"]:
            conditions.append(Condition(name, "source_error", "Validity", "Excel error value", field["source_errors"]))
        if field.get("outside_range"):
            low, high = field["expected_range"]
            conditions.append(Condition(name, "outside_range", "Validity", f"Outside {low} to {high}", field["outside_range"]))
        if variants := field.get("case_variants"):
            conditions.append(Condition(name, "case_variants", "Consistency",
                                        "Same value in different case or spacing", variants["count"]))
        if field.get("duplicates"):
            conditions.append(Condition(name, "duplicate_id", "Uniqueness", "Repeated identifier value", field["duplicates"]))
        if role == "date" and field.get("start") and field.get("end") and field["parsed"]:
            spans.append(Span(name, field["start"], field["end"], field["parsed"]))
    if profile["blank_records"]:
        conditions.append(Condition(ALL_FIELDS, "blank_record", "Completeness", "Entirely blank record", profile["blank_records"]))
    if profile["duplicate_records"]:
        conditions.append(Condition(ALL_FIELDS, "duplicate_record", "Uniqueness", "Exact duplicate record", profile["duplicate_records"]))
    return conditions, spans


# --- The report ------------------------------------------------------------------------

class Report:
    """One report, assembled in a fixed order when written.

    Sections, in order: header; What the file contains; Data quality; Data overview;
    Observations, only when one was added; Analysis limitations, only when one was added.

    profile: the dict returned by profile_table().
    title: the dataset's name in plain words, never the file stem.
    description: one or two sentences on what the data is and what one record represents.
    meanings: one sentence per field on what it appears to hold; every field is required.
    facts: optional key figures shown beside the record and field counts, e.g. "240 service teams".

    On construction the report derives its mechanical conditions and coverage spans from the
    profile; read them from conditions and spans, and explain every one before write().
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
        self._fields = set(names)
        self._title = str(title)
        self._description = str(description)
        self._meanings = {name: meanings[name] for name in names}
        self._facts = tuple(facts)
        self.conditions, self.spans = _mechanical(profile)
        self._explained: dict[tuple[str, str], tuple[str, bool]] = {}
        self._quality: list[tuple[str, int, bool, list]] = []
        self._spans: list[tuple[int, list]] = []
        self._checked: dict[str, list[str]] = {area: [] for area in QUALITY_AREAS}
        self._overview: list[str] = []
        self._no_overview = ""
        self._observations: list[str] = []
        self._limitations: list[str] = []

    # -- Adding content ----------------------------------------------------------------

    def _check_field(self, field: str) -> str:
        if field != ALL_FIELDS and field not in self._fields:
            raise ValueError(f"Unknown field {field!r}; name a field in the file or use ALL_FIELDS.")
        return field

    def _check_count(self, count: int, what: str) -> int:
        rows = self._profile["rows"]
        if isinstance(count, bool) or not isinstance(count, numbers.Integral) or not 0 <= count <= rows:
            raise ValueError(f"{what} must be a record count from 0 to {rows}; got {count!r}")
        return int(count)

    def explain(self, field: str, kind: str, why_it_matters: str, *, always_show: bool = False) -> None:
        """Explain one mechanical condition or coverage span, identified by its field and
        kind (a Condition's kind, or "span"). why_it_matters says what the condition changes
        for a reader who uses the data; a condition expected for the field, such as blanks in
        an optional note, is explained as expected rather than left out. always_show keeps a
        material condition visible below QUALITY_MIN_SHARE."""
        keys = {item.key for item in (*self.conditions, *self.spans)}
        if (field, kind) not in keys:
            listed = ", ".join(f"{f}/{k}" for f, k in sorted(keys)) or "none"
            raise ValueError(f"No mechanical condition or span {field!r}/{kind!r}; this report has: {listed}")
        if not str(why_it_matters).strip():
            raise ValueError(f"Explain why {field!r}/{kind!r} matters.")
        if not isinstance(always_show, bool):
            raise ValueError("always_show must be a boolean.")
        if (field, kind) in self._explained:
            raise ValueError(f"{field!r}/{kind!r} is already explained.")
        self._explained[(field, kind)] = (str(why_it_matters), always_show)

    def quality(self, area: str, field: str, observation: str, affected: int, why_it_matters: str,
                *, always_show: bool = False) -> None:
        """One data quality condition the assessment found beyond the mechanical ones. area
        is one of QUALITY_AREAS; field names the field involved, or ALL_FIELDS for whole-record
        conditions; observation is a short plain-language phrase; affected is the count of
        records the condition applies to, shown with its percentage of the file's records.
        Conditions under QUALITY_MIN_SHARE are collapsed beneath the area's table; set
        always_show=True for a material condition that merits a visible row regardless."""
        if area not in QUALITY_AREAS:
            raise ValueError(f"Area must be one of: {', '.join(QUALITY_AREAS)}; got {area!r}")
        if any(not str(cell).strip() for cell in (field, observation, why_it_matters)):
            raise ValueError(f"Every text cell of a {area} condition needs text.")
        if not isinstance(always_show, bool):
            raise ValueError("always_show must be a boolean.")
        self._check_field(field)
        affected = self._check_count(affected, "Affected records")
        self._quality.append((area, affected, always_show, [field, observation, self._share_cell(affected), why_it_matters]))

    def checked(self, area: str, note: str) -> None:
        """A check in one area that found nothing to record, stated so the reader knows it
        was made, such as "No two records share an order number and line number"."""
        if area not in QUALITY_AREAS:
            raise ValueError(f"Area must be one of: {', '.join(QUALITY_AREAS)}; got {area!r}")
        if not str(note).strip():
            raise ValueError("A checked note needs text.")
        self._checked[area].append(str(note))

    def coverage(self, field: str, start, end, records: int, why_it_matters: str) -> None:
        """The span of one period field the profile could not derive, such as labels like
        "FY24 JUL-DEC" mapped to calendar order in the driver. start and end are the earliest
        and latest values in the words the reader should see; records is the count of records
        carrying a valid value. Date fields' spans are mechanical: explain them instead.
        Record gaps within any span with quality("Coverage", ...)."""
        if any(not str(cell).strip() for cell in (field, start, end, why_it_matters)):
            raise ValueError("A coverage row needs a field, a start, an end, and why it matters.")
        self._check_field(field)
        records = self._check_count(records, "Coverage records")
        def label(value) -> str:
            if isinstance(value, dt.date):
                return value.strftime("%d %b %Y")
            if isinstance(value, numbers.Real) and float(value).is_integer():
                return str(int(value))  # a year, without a thousands separator
            return str(value)
        self._spans.append((records, [field, f"Spans {label(start)} to {label(end)}",
                                      self._records_cell(records), why_it_matters]))

    def overview(self, question: str, chart: Visual, *, takeaway: str, context: str) -> None:
        """One descriptive question answered by exactly one chart from the charts module, a
        takeaway, and the context needed to read the chart correctly."""
        if any(not str(value).strip() for value in (question, takeaway, context)):
            raise ValueError("An overview needs a question, chart, takeaway, and context.")
        if not isinstance(chart, Visual) or not chart.is_chart:
            raise ValueError("An overview's chart is a bar_chart(), line_chart(), or pie_chart() from the charts module.")
        if self._no_overview:
            raise ValueError("A report has overview items or a reason there are none, not both.")
        self._overview.append(
            f'<div class="overview"><h3>{esc(question)}</h3>{chart.html}'
            f'<p>{esc(takeaway)}</p><p class="muted">{esc(context)}</p></div>'
        )

    def no_overview(self, reason: str) -> None:
        """Why the file cannot support a meaningful overview, for example a CSV with headers
        but no records. Only for a report with no overview items."""
        if not reason.strip():
            raise ValueError("Give the reason the file supports no overview.")
        if self._overview or self._no_overview:
            raise ValueError("A report has overview items or one reason there are none; this one already has one.")
        self._no_overview = reason

    def observation(self, title: str, visual: Visual | None = None, *, noticed: str, why_it_matters: str,
                    question: str) -> None:
        """A supported pattern ending with a concrete question for the data provider. The
        optional visual, a chart or table from the charts module, follows What we noticed,
        the claim it lets the reader check. A table shows at most OBSERVATION_MAX_ROWS rows."""
        if any(not str(value).strip() for value in (title, noticed, why_it_matters, question)):
            raise ValueError("An observation needs a title, evidence, why it matters, and a stakeholder question.")
        if visual is not None and not isinstance(visual, Visual):
            raise ValueError("An observation's visual is a Visual from the charts module, or None.")
        if visual is not None and visual.rows > OBSERVATION_MAX_ROWS:
            raise ValueError(
                f"An observation table shows at most {OBSERVATION_MAX_ROWS} rows; got {visual.rows}. "
                "Show the rows that best support the observation and say how many of the total they are."
            )
        markup = visual.html if visual is not None else ""
        self._observations.append(
            f'<div class="observation"><h3>{esc(title)}</h3>'
            f'<p><strong>What we noticed:</strong> {esc(noticed)}</p>{markup}'
            f'<p><strong>Why it matters:</strong> {esc(why_it_matters)}</p>'
            f'<p><strong>Question for the data provider:</strong> {esc(question)}</p></div>'
        )

    def limitation(self, note: str) -> None:
        """A material constraint on interpretation, listed once at the end of the report.
        Refer to an observation by title when it carries the full investigation."""
        if not str(note).strip():
            raise ValueError("A limitation needs text.")
        self._limitations.append(str(note))

    # -- Writing -----------------------------------------------------------------------

    def write(self, path: str | Path | None = None) -> Path:
        """Write the complete offline report and return its path. Without a path, a fresh
        timestamped .html file in the OS temporary directory, named after the source stem.
        The source is never written. Fails while any mechanical condition or span is
        unexplained, or the overview is neither built nor declined."""
        unexplained = [item.key for item in (*self.conditions, *self.spans) if item.key not in self._explained]
        if unexplained:
            listed = ", ".join(f"{field}/{kind}" for field, kind in unexplained)
            raise ValueError(f"Explain every mechanical condition and span before writing; unexplained: {listed}")
        if not self._overview and not self._no_overview:
            raise ValueError("Build the data overview or call no_overview() with why the file cannot support one.")
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
        page = (template.replace("{{title}}", esc(self._title)).replace("{{styles}}", STYLE.strip("\n"))
                .replace("{{body}}", "\n".join(sections)))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(page, encoding="utf-8")
        return path

    def _share_cell(self, affected: int) -> str:
        rows = self._profile["rows"]
        return f"{fmt(affected)} ({pct(affected / rows if rows else 0.0)})"

    def _records_cell(self, records: int) -> str:
        rows = self._profile["rows"]
        return f"{fmt(records)} with a value ({pct(records / rows if rows else 0.0)})"

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
        return f'<p class="muted">{esc(" ".join(notes))}</p>'

    def _field_profile(self) -> str:
        """Every field in file order with its apparent meaning."""
        rows = [[name, meaning] for name, meaning in self._meanings.items()]
        return table_html(["Field", "Apparent meaning"], rows, css_class="fields")

    def _all_conditions(self) -> list[tuple[str, int, bool, list]]:
        """Mechanical conditions with their explanations, then driver-recorded ones."""
        explained = []
        for condition in self.conditions:
            why, always_show = self._explained[condition.key]
            explained.append((condition.area, condition.affected, always_show,
                              [condition.field, condition.observation, self._share_cell(condition.affected), why]))
        return explained + self._quality

    def _all_spans(self) -> list[tuple[int, list]]:
        """Mechanical spans with their explanations, then driver-recorded ones."""
        explained = []
        for span in self.spans:
            why, _ = self._explained[span.key]
            explained.append((span.records, [span.field, f"Spans {span.start} to {span.end}",
                                             self._records_cell(span.records), why]))
        return explained + self._spans

    def _data_quality(self) -> str:
        """One subheading and table per area in QUALITY_AREAS order, rows sorted by affected
        records, most first. Coverage opens with every span, most records first. Conditions
        under QUALITY_MIN_SHARE sit in a collapsed table beneath; checks that found nothing
        follow. An area with nothing at all says it was checked with nothing to report."""
        by_area = {area: [] for area in QUALITY_AREAS}
        for area, affected, always_show, row in self._all_conditions():
            by_area[area].append((affected, always_show, row))
        rows = self._profile["rows"]
        columns = ["Field", "Observation", "Affected records", "Why it matters"]
        def ranked(items):
            return [row for _, _, row in sorted(items, key=lambda item: item[0], reverse=True)]
        parts = []
        for area, area_rows in by_area.items():
            parts.append(f'<h3>{esc(area)}</h3>')
            spans = self._all_spans() if area == "Coverage" else []
            if spans:
                span_rows = [row for _, row in sorted(spans, key=lambda item: item[0], reverse=True)]
                parts.append(table_html(["Field", "Span", "Records with a value", "Why it matters"], span_rows, css_class="quality"))
            visible = [always_show or (affected / rows if rows else 0.0) >= QUALITY_MIN_SHARE
                       for affected, always_show, _ in area_rows]
            shown = [item for item, show in zip(area_rows, visible) if show]
            hidden = [item for item, show in zip(area_rows, visible) if not show]
            if shown:
                # Same fixed column widths in every area, so the tables line up down the section.
                parts.append(table_html(columns, ranked(shown), css_class="quality"))
            if hidden:
                noun = "condition" if len(hidden) == 1 else "conditions"
                parts.append(f'<details><summary>{len(hidden)} {noun} affecting less than '
                             f'{QUALITY_MIN_SHARE:.0%} of records</summary>'
                             f'{table_html(columns, ranked(hidden), css_class="quality")}</details>')
            for note in self._checked[area]:
                parts.append(f'<p class="muted">Checked: {esc(note)}</p>')
            if not area_rows and not spans and not self._checked[area]:
                parts.append('<p class="muted">Checked; nothing to report.</p>')
        return "".join(parts)

    def _overview_body(self) -> str:
        if self._overview:
            return "".join(self._overview)
        return f'<p>{esc(self._no_overview)}</p>'
