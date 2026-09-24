# HTML report and retained analysis

The `Report` module in `scripts/report.py` owns the section order (header and summary, What the file contains, Data quality, Data overview, Observations when any, Analysis limitations when any), validates each addition, and escapes every text argument. Visuals are trusted HTML or inline SVG from the driver: build them with `bar_chart()`, `line_chart()`, `pie_chart()`, and `table()`. The selection criteria for overview questions and observations are in steps 3 and 4 of [SKILL.md](SKILL.md); each method's docstring states what it accepts.

## Driver script

Save the driver in the OS temporary directory, with absolute paths for the source CSV and the installed skill. This starting point adds the data quality conditions the profile can compute. Replace the placeholders in angle brackets, set the parsing choices, add the conditions the assessment found beyond the profile, and add the overview and any observations from the analysis. It is not a complete assessment or exploration by itself.

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas>=2.0,<4"]
# ///
from pathlib import Path
import sys

SKILL_DIR = Path(r"<absolute skill directory>")
SOURCE = Path(r"<absolute CSV path>")
sys.dont_write_bytecode = True  # keep __pycache__ out of the skill folder
sys.path.insert(0, str(SKILL_DIR / "scripts"))
from profile_csv import profile_csv
from report import Report, bar_chart, line_chart, pie_chart, table, fmt, money, pct, esc

# Persist all interpretation choices here; overrides recompute field statistics.
# Example syntax: roles={"account": "identifier"}, date_formats={"date": "%d/%m/%Y"}
raw, data, profile = profile_csv(SOURCE, roles={}, date_formats={})
assert len(raw) == len(data) == profile["rows"]
assert all(
    field["blank"] + field["parse_failures"] + field["parsed"] == len(raw)
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

# Data quality: one call per condition found. Consistency and coverage come from the assessment, not the profile.
for field in profile["columns"]:
    if field["blank"] == rows:
        r.quality("Completeness", field["name"], "Entirely blank", rows, "<what a reader loses without this field>")
    elif field["blank"]:
        r.quality("Completeness", field["name"], "Blank", field["blank"], "<what the blanks change for calculations on this field>")
    if field["parse_failures"]:
        r.quality("Validity", field["name"], f"Does not parse as a {field['role']}", field["parse_failures"],
                  "<what the unparsed values are excluded from>")
if profile["duplicate_records"]:
    r.quality("Uniqueness", "All fields", "Exact duplicate record", profile["duplicate_records"],
              "<what the duplicates change for counts and totals>")
# Coverage: one r.coverage("<date field>", <earliest valid>, <latest valid>, <records dated>, "<what the span means>") per date field.

# Data overview: one r.overview(question, chart, takeaway=..., context=...) per descriptive question,
# or r.no_overview(reason) when the file cannot support one (for example, headers but no records).
# Observations: one r.observation(title, visual, noticed=..., why_it_matters=..., question=...) per stakeholder question.
# Limitations: one r.limitation(note) per material constraint on interpretation.

print(r.write())
```

Run `uv run "<driver path>"`, or use the Python interpreter from the environment containing pandas. Keep filters, date formats, role overrides, and extra transformations in the driver, so every count, percentage, period, ranking ("next", "largest"), and named example in the report follows from its calculations. This includes figures and record numbers in `why_it_matters` text and limitations: interpolate them from calculated values.

`raw` preserves cell strings: empty and whitespace-only cells are blanks, detected with `raw[field].str.strip().eq("")`, not `.isna()`. In `data`, blanks and failed conversions are missing values (NA/NaN/NaT depending on dtype); `.isna()` includes both, while the profile counts them separately. For a nullable boolean selection mask, use `mask.fillna(False)` before indexing to explicitly exclude unknown matches.

`Report.quality(..., always_show=True)` keeps a material condition visible even below the default 1% display threshold. Explain its impact in `why_it_matters`; it then appears in the appropriate quality table and is excluded from the hidden-condition count.

## Analytical choices

Numbers in prose carry their units; invented examples are $12.5M, 1.25M service hours, and 18.4% of requests. `fmt()`, `money()`, and `pct()` format them; `compact=True` writes 1.25M or $12.5M for prose while tables keep the full figure. Years, months, codes, and record numbers are labels: write them as `str(int(value))` so they carry no thousands separator (1912, not 1,912). Build record tables from the parsed values in `data` and format each cell; raw cell strings such as `2022.0` stay out of the report. Use a number or table when it explains an observation better than a chart. For bar and pie charts, combine the groups beyond the chart's limit as Other and say so in the chart's context. For distributions, explain bins and any display-range exclusions; extreme values remain in the underlying analysis. Choose units from established context and state the assumption in the context of each observation that relies on it when the file does not give them.

`bar_chart()`, `line_chart()`, and `pie_chart()` draw the chart types that step 3 of [SKILL.md](SKILL.md) chooses between; each docstring states its limits. `bar_chart()` takes at most 12 bars; labels wrap beneath their bars, or tilt when a word is too long to fit. `line_chart()` takes every period in the range, in chronological order, with zero for an empty one, and `partial_last=True` draws an incomplete final period dashed and marked "to date". `pie_chart()` takes at most five non-negative parts of one whole and rejects more. Set `decimals` to choose display precision for non-integral value labels and tooltips (for example, `decimals=1` for service hours); the default is 2, integral values have no decimal places, and the marks use the supplied values without rounding. An observation's supporting table is a sample of the evidence: only the columns the prose cites, and a caption naming the selection and its share of the population, such as the invented "Longest 5 of 48 service requests awaiting assignment".

Record each date field's span with `r.coverage(field, start, end, dated, why_it_matters)`, taking start and end from the valid values and `dated` as the count of records carrying the date; record gaps within the span with `r.quality("Coverage", ...)`. State a reporting period in the header facts only when the relevant date field is understood.

Identify inspected records using the profiler's one-based data-record index or a source identifier. Data-record indexes exclude the header and empty lines outside quoted fields; they are not physical line numbers when cells contain line breaks.

Use neutral language. Describe missingness or an unusual value before assigning significance. Keep implementation details in the driver; the report needs only the choices that affect interpretation, written in words rather than format codes.
