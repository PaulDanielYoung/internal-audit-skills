# HTML report and retained analysis

The `Report` module in `scripts/report.py` owns the section order (header and summary, What the file contains, Data quality, Data overview, Observations when any, Analysis limitations when any), validates each addition, and escapes every text argument. Visuals are trusted HTML or inline SVG from the driver: build them with `chart()` and `table()`, or escape labels with `esc()` when generating custom SVG. The selection criteria for overview questions and observations are in steps 3 and 4 of [SKILL.md](SKILL.md); each method's docstring states what it accepts.

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
from report import Report, chart, table, fmt, money, pct, esc

# Persist all interpretation choices here; overrides recompute field statistics.
# Example syntax: roles={"account": "identifier"}, date_formats={"date": "%d/%m/%Y"}
raw, data, profile = profile_csv(SOURCE, roles={}, date_formats={})
assert len(raw) == len(data) == profile["rows"]
assert all(
    field["blank"] + field["parse_failures"] + field["parsed"] == len(raw)
    for field in profile["columns"]
)
rows = profile["rows"]

# city_property_details_datasd.csv becomes "San Diego City Property Details", never the file stem.
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

# Data overview: one r.overview(question, chart, takeaway=..., context=...) per descriptive question,
# or r.no_overview(reason) when the file cannot support one (for example, headers but no records).
# Observations: one r.observation(title, visual, noticed=..., why_it_matters=..., question=...) per stakeholder question.
# Limitations: one r.limitation(note) per material constraint on interpretation.

print(r.write())
```

Run `uv run "<driver path>"`, or use the Python interpreter from the environment containing pandas. Keep filters, date formats, role overrides, and extra transformations in the driver, so every count, percentage, and period in the report follows from its calculations.

## Analytical choices

Numbers in prose carry their units: $391.2M, 2.96M acres, 32.9% of records. `fmt()`, `money()`, and `pct()` format them; `compact=True` writes 2.96M or $391.2M for prose while tables keep the full figure. Build record tables from the parsed values in `data` and format each cell; raw cell strings such as `2022.0` stay out of the report. Use a number or table when it explains an observation better than a chart. For category charts, show a manageable number of groups, combining the rest as Other where appropriate and saying so. For time comparisons, retain chronological order and distinguish incomplete periods. For distributions, explain bins and any display-range exclusions; extreme values remain in the underlying analysis. Choose units from established context and state the assumption in the context of each observation that relies on it when the file does not give them.

`chart()` supplies horizontal bars; it does not restrict the choice of chart. When another chart type better answers the question, generate self-contained inline SVG in the driver, with an accessible title, readable full labels, units, and values where useful, keeping the same offline and escaping guarantees. An observation's supporting table is a sample of the evidence: only the columns the prose cites, and a caption naming the selection and its share of the population, such as "Largest 8 of 192 groups sharing a grantor, year, and land cost".

For a coverage condition, count the records carrying the relevant date. State a reporting period in the header facts only when the relevant date field is understood.

Identify inspected records using the profiler's one-based data-record index or a source identifier. Data-record indexes exclude the header and empty lines outside quoted fields; they are not physical line numbers when cells contain line breaks.

Use neutral language. Describe missingness or an unusual value before assigning significance. Keep implementation details in the driver; the report needs only the choices that affect interpretation, written in words rather than format codes.
