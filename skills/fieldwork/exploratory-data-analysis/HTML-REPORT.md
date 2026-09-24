# HTML report and retained analysis

The `Report` module in `scripts/report.py` owns the section order (header and summary, What the file contains, Data quality, Data overview, Observations when any, Analysis limitations when any), validates each addition, and escapes every text argument. Visuals are trusted HTML or inline SVG from the driver: build them with `bar_chart()`, `line_chart()`, `pie_chart()`, and `table()`. The selection criteria for overview questions and observations are in steps 3 and 4 of [SKILL.md](SKILL.md); each method's docstring states what it accepts.

## Driver script

Save the driver in the OS temporary directory, with absolute paths for the source file and the installed skill. Replace the placeholders in angle brackets, set the source selection and parsing choices, explain the mechanical conditions and coverage spans the Report derived, add the conditions the assessment found beyond them, and add the overview and any observations from the analysis. This starting point is not a complete assessment or exploration by itself.

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas>=2.0,<4", "openpyxl>=3.1.5,<4"]
# ///
from pathlib import Path
import sys

SKILL_DIR = Path(r"<absolute skill directory>")
SOURCE = Path(r"<absolute CSV or XLSX path>")
sys.dont_write_bytecode = True  # keep __pycache__ out of the skill folder
sys.path.insert(0, str(SKILL_DIR / "scripts"))
from profile_table import profile_table, blank_cells
from report import ALL_FIELDS, Report, bar_chart, line_chart, pie_chart, table, fmt, money, pct, esc

# Persist selection and interpretation choices; overrides recompute statistics.
# CSV: selection = {}. XLSX: use the exact sheet and range or Table from profiling.
# Examples: {"sheet": "Transactions", "cell_range": "B5:H800"}, {"table": "Transactions"}
selection = {}
# Example syntax: roles={"account": "identifier"}, date_formats={"date": "%d/%m/%Y"}
raw, data, profile = profile_table(SOURCE, **selection, roles={}, date_formats={})
assert len(raw) == len(data) == profile["rows"]
assert all(
    field["blank"] + field["source_errors"] + field["parse_failures"] + field["parsed"] == len(raw)
    for field in profile["columns"]
)
rows = profile["rows"]

# Invented example: service_requests.csv becomes "Service Requests", never the file stem.
r = Report(
    profile,
    "<plain-language dataset name>",
    description="<One or two sentences: what the data is and what one record represents.>",
    meanings={  # one sentence per field on what it appears to hold; every field is required
        "<field>": "<what it appears to hold>",
    },
)

# Mechanical conditions and coverage spans: the Report derived these from the profile (blanks,
# unparsed values, Excel errors, out-of-range parts, case variants, repeated identifiers, blank
# and duplicate records, and each date field's span). Explain every one; write() names any left out.
# A condition expected for its field, such as blanks in an optional note, is explained as expected.
reasons = {  # one entry per item in r.conditions (field, kind, area, observation, affected) and r.spans (field, start, end, records)
    ("<field>", "<kind>"): "<what this changes for a reader who uses the field>",
    ("<date field>", "span"): "<what the span means for the file>",
}
for item in (*r.conditions, *r.spans):
    if item.key in reasons:
        r.explain(*item.key, reasons[item.key])
# Judged conditions beyond the mechanical ones: r.quality("<area>", "<field or ALL_FIELDS>", "<observation>", <affected>, "<why it matters>"),
# such as a confirmed placeholder, or one per value shape confirmed as a second identifier scheme, counting its records only.
# Checks that found nothing: r.checked("<area>", "<what was tested>"), such as a composite key with no repeats.
# Period labels: r.coverage("<period field>", <earliest>, <latest>, <records with a valid value>, "<what the span means>");
# gaps within any span: r.quality("Coverage", ...).

# Data overview: one r.overview(question, chart, takeaway=..., context=...) per descriptive question,
# or r.no_overview(reason) when the file cannot support one (for example, headers but no records).
# Observations: one r.observation(title, visual, noticed=..., why_it_matters=..., question=...) per stakeholder question.
# Limitations: one r.limitation(note) per material constraint on interpretation.

print(r.write())
```

Run `uv run "<driver path>"`, or use the Python interpreter from the environment containing the profiler's dependencies. Keep source selection, analytical filters, date formats, role overrides, and extra transformations in the driver, so every count, percentage, period, ranking ("next", "largest"), and named example in the report follows from its calculations. This includes figures and record numbers in `why_it_matters` text and limitations: interpolate them from calculated values.

`raw` preserves CSV strings or typed XLSX values. Use `blank_cells(raw[field])` to detect blanks in either format. In `data`, blanks, source errors, and failed conversions are missing values (NA/NaN/NaT depending on dtype); `.isna()` includes all three, while the profile counts them separately. For XLSX interpretation and source metadata, use [XLSX.md](XLSX.md). For a nullable boolean selection mask, use `mask.fillna(False)` before indexing to explicitly exclude unknown matches.

The Report collapses conditions below its display threshold; `always_show=True` on `explain()` or `quality()` keeps a material one visible, with its impact in `why_it_matters`. `Report.checked(area, note)` states a check that found nothing, so an area reads as tested rather than merely empty.

## Analytical choices

Numbers in prose carry their units; invented examples are $12.5M, 1.25M service hours, and 18.4% of requests. `fmt()`, `money()`, and `pct()` format them; `compact=True` writes 1.25M or $12.5M for prose while tables keep the full figure. Numeric years, months, and record numbers are labels: write them as `str(int(value))` so they carry no thousands separator (1912, not 1,912). Preserve text identifiers exactly, including leading zeros. Build record tables from the parsed values in `data` and format each cell. Use a number or table when it explains an observation better than a chart. For bar and pie charts, combine the groups beyond the chart's limit as Other and say so in the chart's context. When Other or a similar catch-all group outweighs the largest group shown, say so in the takeaway: the field is spread thinly, and how concentrated it is may answer the question better than which groups lead. For distributions, explain bins and any display-range exclusions; extreme values remain in the underlying analysis. Choose units from established context and state the assumption in the context of each observation that relies on it when the file does not give them.

`bar_chart()`, `line_chart()`, and `pie_chart()` draw the chart types that step 3 of [SKILL.md](SKILL.md) chooses between; each docstring states its limits. `bar_chart()` takes at most 12 bars; labels wrap beneath their bars, or tilt when a word is too long to fit. `line_chart()` takes every period in the range, in chronological order, with zero for an empty one, and `partial_last=True` draws an incomplete final period dashed and marked "to date". `pie_chart()` takes at most five non-negative parts of one whole and rejects more. Set `decimals` to choose display precision for non-integral value labels and tooltips (for example, `decimals=1` for service hours); the default is 2, integral values have no decimal places, and the marks use the supplied values without rounding. An observation's supporting table is a sample of the evidence: only the columns the prose cites, and a caption naming the selection and its share of the population, such as the invented "Longest 5 of 48 service requests awaiting assignment".

Date fields' spans are mechanical: explain them. A period stored as a label profiles as a category, so record its span with `r.coverage(field, start, end, records, why_it_matters)`, taking start and end from the valid values and `records` as the count of records carrying a valid value. Record gaps within any span with `r.quality("Coverage", ...)`. State a reporting period in the header facts only when the relevant date field is understood. For a label such as `FY24 JUL-DEC` or `2023-Q3`, map each label to its calendar start in the driver, order and gap-check the periods from that mapping, pass the labels to `line_chart()` in that calendar order, and state the fiscal-year convention the mapping assumes, with its basis.

Identify inspected CSV records using the profiler's one-based data-record index or a source identifier. CSV record indexes exclude the header and empty lines outside quoted fields; they are not physical line numbers when cells contain line breaks. For XLSX, use the worksheet row or cell address from source metadata; the Report automatically displays the selected worksheet/range and visibility and totals exclusions.

Use neutral language. Describe missingness or an unusual value before assigning significance. Keep implementation details in the driver; the report needs only the choices that affect interpretation, written in words rather than format codes.
