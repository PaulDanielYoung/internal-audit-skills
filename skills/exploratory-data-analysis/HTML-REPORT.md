# HTML report and retained analysis

Write the report for an auditor who has not opened the file. Order: header, what the file contains, data quality, observation sections. Add areas for closer examination only when grounded in observations already shown. No section needs to manufacture a finding.

The helpers in `scripts/report.py` use embedded CSS and SVG, without JavaScript, CDNs, external fonts, or images. Text arguments are escaped. Pass HTML only to `section()` bodies and `card()` visuals, using the helper output; pass dataset values through text arguments or `table()`.

## Driver script

Save the driver in the OS temporary directory. Use absolute paths for the source CSV and the installed skill; `report_path(SOURCE)` names a fresh report file in the same temporary directory.

This runnable starting point illustrates data quality conditions calculated from the profile. Replace the placeholders in angle brackets, set the parsing choices, add the conditions the assessment found beyond the profile, and adapt the observations to what exploration established. This is not a complete assessment or exploration by itself.

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
import report as r

# The dataset in the reader's words, inferred from the filename and contents.
# city_property_details_datasd.csv becomes "San Diego City Property Details", never the file stem.
TITLE = "<plain-language dataset name>"
DESCRIPTION = "<One or two sentences: what the data is and what one record represents.>"
# One sentence per field on what it appears to hold. field_profile() requires every field.
MEANINGS = {
    "<field>": "<what it appears to hold>",
}
# Persist all interpretation choices here; overrides recompute field statistics.
# Example syntax: roles={"account": "identifier"}, date_formats={"date": "%d/%m/%Y"}
raw, data, profile = profile_csv(SOURCE, roles={}, date_formats={})
assert len(raw) == len(data) == profile["rows"]
assert all(
    field["blank"] + field["parse_failures"] + field["parsed"] == len(raw)
    for field in profile["columns"]
)

rows = profile["rows"]
# One (area, field, observation, affected records, why it matters) per condition; area from r.QUALITY_AREAS.
# Observations are short plain-language phrases. Consistency and coverage conditions come from the assessment, not the profile.
quality = []
for field in sorted(profile["columns"], key=lambda field: field["blank"], reverse=True):
    if field["blank"] == rows:
        quality.append(("Completeness", field["name"], "Entirely blank", rows,
                        "<what a reader loses without this field>"))
    elif field["blank"]:
        quality.append(("Completeness", field["name"], "Blank", field["blank"],
                        "<what the blanks change for calculations on this field>"))
for field in profile["columns"]:
    if field["parse_failures"]:
        quality.append(("Validity", field["name"], f"Does not parse as a {field['role']}", field["parse_failures"],
                        "<what the unparsed values are excluded from>"))
if profile["duplicate_records"]:
    quality.append(("Uniqueness", "All fields", "Exact duplicate record", profile["duplicate_records"],
                    "<what the duplicates change for counts and totals>"))

cards = []  # One r.card() per retained pattern from exploration, with r.chart() or r.table() as its visual.

sections = [
    r.header(profile, TITLE, description=DESCRIPTION),
    r.section("What the file contains", r.field_profile(profile, MEANINGS)),
    r.section("Data quality", r.data_quality(quality, rows)),
]
if cards:
    sections.append(r.section("Observations", "".join(cards)))
print(r.write_report(TITLE, sections, r.report_path(SOURCE)))
```

Run `uv run "<driver path>"`, or use the Python interpreter from the environment containing pandas. Keep filters, date formats, role overrides, and extra transformations in the driver, so every count, percentage, and period in the report follows from its calculations.

## Helpers and analytical choices

| Helper | Purpose |
| --- | --- |
| `header(profile, title, description=..., facts=...)` | Plain-language title and description, record and field counts plus optional key facts such as "1,668 sites". State a reporting period only when the relevant date field is understood. |
| `field_profile(profile, meanings)` | All fields in file order with their apparent meaning in plain words. Blanks, conversion failures, roles, and distributions belong in data quality or observations, not here. |
| `data_quality(conditions, rows)` | A subheading and table per area, in `QUALITY_AREAS` order: Completeness, Validity, Uniqueness, Consistency, Coverage. Columns are Field, Observation, Affected records, Why it matters; rows within each area are sorted by affected records, most first. Pass the affected record count; the helper shows it as a percentage of `rows` to one decimal place and leaves out conditions affecting less than `QUALITY_MIN_SHARE` (1%) of records, noting how many under the area. Still pass every condition found. Name every field involved, or "All fields" for whole-record conditions. For a coverage date range, count the records carrying that date. An area with no condition reads as checked with nothing to report. |
| `section(title, body)` | Group helper-produced HTML. Omit optional sections when they add nothing. |
| `card(title, visual, observation=..., context=..., interpretation=..., open_question=...)` | One supported observation. Interpretation and open question are optional. |
| `chart(labels, values, title=..., unit=...)` | Simple horizontal bars with a zero baseline and expandable values table. Aggregate or bin in the driver; pass only finite values. |
| `table(columns, rows, title=...)` | Group comparisons, distributions, or representative records. Format numeric cells with `fmt()`, `money()`, or `pct()`. |
| `fmt(value, compact=...)`, `money(value, compact=...)`, `pct(share)` | Numbers for the reader. `compact=True` writes 2.96M or $391.2M for prose; tables keep the full figure. |
| `report_path(csv_path)` | A fresh, timestamped `.html` path in the OS temporary directory, named after the CSV stem. |
| `write_report(title, sections, path)` | Write the complete offline report to an explicit `.html` path. |

Numbers in prose carry their units: $391.2M, 2.96M acres, 32.9% of records. Build record tables from the parsed values in `data` and format each cell; raw cell strings such as `2022.0` stay out of the report. Use a number or table when it explains the observation better than a chart. For category charts, show a manageable number of groups, combining the rest as Other where appropriate and saying so. For time comparisons, retain chronological order and distinguish incomplete periods. For distributions, explain bins and any display-range exclusions; extreme values remain in the underlying analysis. Choose units from established context and state the assumption in the context of each observation that relies on it when the file does not give them.

Identify inspected records using the profiler's one-based data-record index or a source identifier. Data-record indexes exclude the header and empty lines outside quoted fields; they are not physical line numbers when cells contain line breaks.

Use neutral language. Describe missingness or an unusual value before assigning significance. Keep implementation details in the driver; the report needs only the choices that affect interpretation, written in words rather than format codes.
