# HTML report and retained analysis

Write the report for an auditor who has not opened the file. Order: header, what the file contains, observation sections, analysis notes. Add areas for closer examination only when grounded in observations already shown. No section needs to manufacture a finding.

The helpers in `scripts/report.py` use embedded CSS and SVG, without JavaScript, CDNs, external fonts, or images. Text arguments are escaped. Pass HTML only to `section()` bodies and `card()` visuals, using the helper output; pass dataset values through text arguments or `table()`.

## Driver script

Save the driver in the OS temporary directory. Use absolute paths for the source CSV and the installed skill; `report_path(SOURCE)` names a fresh report file in the same temporary directory.

This runnable starting point illustrates a calculated missingness observation. Replace the placeholders in angle brackets, set the parsing choices, and adapt the observations to what exploration established. This is not a required chart or a complete exploration by itself.

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
MONEY_FIELDS = {"<fields holding dollar amounts>"}

# Persist all interpretation choices here; overrides recompute field statistics.
# Example syntax: roles={"account": "identifier"}, date_formats={"date": "%d/%m/%Y"}
raw, data, profile = profile_csv(SOURCE, roles={}, date_formats={})
assert len(raw) == len(data) == profile["rows"]
assert all(
    field["blank"] + field["parse_failures"] + field["parsed"] == len(raw)
    for field in profile["columns"]
)

cards = []
blank_fields = sorted(
    [field for field in profile["columns"] if field["blank"]],
    key=lambda field: field["blank"], reverse=True,
)
if blank_fields:
    shown = blank_fields[:15]
    # Field counts can overlap: the same record may have several blank cells.
    blank_records = int(raw.apply(lambda column: column.str.strip().eq("")).any(axis=1).sum())
    cards.append(r.card(
        "Source blanks by field",
        r.chart([field["name"] for field in shown], [field["blank"] for field in shown],
                title="How many source cells are blank in each field?", unit="cells"),
        observation=(f"{r.fmt(blank_records)} of {r.fmt(len(raw))} records "
                     f"({r.pct(blank_records / len(raw))}) have at least one blank cell."),
        context=(f"All source records. Showing {len(shown)} of {len(blank_fields)} fields with blanks. "
                 "Counts overlap across fields; conversion failures are reported separately."),
    ))

failed = sum(field["parse_failures"] for field in profile["columns"])
notes = profile["notes"] + [
    f"{profile['duplicate_records']} duplicate records beyond their first occurrences; retained.",
    "Reviewed field profiles and source blank counts; further business-context exploration is not included in this example.",
    "The source CSV was read without modification. This report is temporary; rerun the exploratory-data-analysis skill to regenerate it.",
]
if failed:
    notes.append(f"{failed} nonblank cells could not be parsed under the selected types; "
                 "they are excluded from typed summaries and retained in the source.")
sections = [
    r.header(profile, TITLE, description=DESCRIPTION),
    r.section("What the file contains",
              r.field_profile(profile, MEANINGS, money_fields=MONEY_FIELDS) + r.sample_records(profile)),
]
if cards:
    sections.append(r.section("Observations", "".join(cards)))
sections.append(r.analysis_notes(notes))
print(r.write_report(TITLE, sections, r.report_path(SOURCE)))
```

Run `uv run "<driver path>"`, or use the Python interpreter from the environment containing pandas. Keep filters, date formats, role overrides, and extra transformations in the driver, so every count, percentage, and period in the report follows from its calculations.

## Helpers and analytical choices

| Helper | Purpose |
| --- | --- |
| `header(profile, title, description=..., facts=...)` | Plain-language title and description, record and field counts plus optional key facts such as "1,668 sites", source filename, and generation date. State a reporting period only when the relevant date field is understood. |
| `field_profile(profile, meanings, money_fields=...)` | All fields with their apparent meaning in plain words, role, raw blanks, conversion failures, distinct raw strings, and a summary. Correct roles in `profile_csv()`, not in the display. |
| `sample_records(profile)` | The first five records exactly as written in the file. |
| `section(title, body)` | Group helper-produced HTML. Omit optional sections when they add nothing. |
| `card(title, visual, observation=..., context=..., interpretation=..., open_question=...)` | One supported observation. Interpretation and open question are optional. |
| `chart(labels, values, title=..., unit=...)` | Simple horizontal bars with a zero baseline and expandable values table. Aggregate or bin in the driver; pass only finite values. |
| `table(columns, rows, title=...)` | Group comparisons, distributions, or representative records. Format numeric cells with `fmt()`, `money()`, or `pct()`. |
| `fmt(value, compact=...)`, `money(value, compact=...)`, `pct(share)` | Numbers for the reader. `compact=True` writes 2.96M or $391.2M for prose; tables keep the full figure. |
| `analysis_notes(notes)` | Choices affecting interpretation, including parsing, exclusions, assumptions, dimensions explored, and limitations. Combine with the profiler's notes. |
| `report_path(csv_path)` | A fresh, timestamped `.html` path in the OS temporary directory, named after the CSV stem. |
| `write_report(title, sections, path)` | Write the complete offline report to an explicit `.html` path. |

Numbers in prose carry their units: $391.2M, 2.96M acres, 32.9% of records. Build record tables from the parsed values in `data` and format each cell; raw cell strings such as `2022.0` belong only in the sample records table. Use a number or table when it explains the observation better than a chart. For category charts, show a manageable number of groups, combining the rest as Other where appropriate and saying so. For time comparisons, retain chronological order and distinguish incomplete periods. For distributions, explain bins and any display-range exclusions; extreme values remain in the underlying analysis. Choose units from established context and state the assumption in the notes when the file does not give them.

Identify inspected records using the profiler's one-based data-record index or a source identifier. Data-record indexes exclude the header and empty lines outside quoted fields; they are not physical line numbers when cells contain line breaks.

Use neutral language. Describe missingness or an unusual value before assigning significance. Keep implementation details in the driver; the report needs only the choices that affect interpretation, written in words rather than format codes.
