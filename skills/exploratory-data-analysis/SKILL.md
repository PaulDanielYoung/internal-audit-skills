---
name: exploratory-data-analysis
description: Explores one CSV an auditor has received and opens a temporary offline HTML report of its contents, structure, quality, and patterns. Use for a first look at a dataset before audit testing. Supports one table with a header row.
---

# Exploratory Data Analysis

Turn an unfamiliar CSV into an understanding of what it contains and what deserves closer examination. Exploration generates observations and hypotheses, not conclusions. An unusual value or relationship is a reason to look closer.

## Scope and files

Analyze exactly one comma-delimited CSV, with one table and field names in the first record. If several files are offered, establish which one to explore. For an unsupported structure, explain what is needed rather than silently choosing a table or changing the source.

Read the existing CSV in place and leave its bytes unchanged. The report is throwaway: write the driver script, the report, and every intermediate file to the OS temporary directory. Each run writes a fresh report, named by `report_path()` in the skill's helpers. The driver may import the installed skill's helpers.

## 1. Orient and profile

Run `uv run "<skill directory>/scripts/profile_csv.py" "<CSV path>"`. Read the printed summary and temporary JSON profile. If uv is unavailable, use Python 3.10+ with `pandas>=2.0,<4` installed in a virtual environment. Script paths are relative to the skill directory, not the engagement directory; `--help` describes parsing overrides.

Review every field's apparent role against its name and raw values. The profiler preserves strings, including leading-zero identifiers and literal `NA` values. It treats whitespace-only cells as blank, infers plain numbers and ISO dates, and reports conversion failures separately from blanks. Inspect failed examples before using parsed values. Correct roles and date formats by rerunning the profiler with overrides; the driver must use the same choices.

If there are any unresolved questions about the meaning of a field or its values that would materially change a calculation or interpretation, use the `shared-understanding` skill and invoke it with the specific ambiguity and already-established context. The user must resolve the ambiguity before you can continue. If the user cannot resolve it, flag the field as unresolved and continue with the rest of the dataset.

This step is complete when row and field counts, blanks, and appropriate basic field summaries are established; every field's role has been reviewed and its apparent meaning written in plain words; and the dataset's grain is stated with its basis or flagged as unresolved. An empty table can have a complete profile without supporting further analysis.

## 2. Assess data quality

Record the observable conditions in the file that could affect how its data is interpreted or analyzed, one condition per row, in five areas:

- **Completeness:** blank cells by field, fields that are entirely blank, and fields far sparser than the rest.
- **Validity:** values that fail to parse as their apparent type, dates or numbers outside a possible range, and malformed values.
- **Uniqueness:** exact duplicate records, and repeated values in apparent identifiers or composite keys.
- **Consistency:** fields that contradict each other within a record, and values that vary within an apparent entity where they should stay constant.
- **Coverage:** earliest and latest dates and obvious gaps between them. Whether the data are current depends on the expected refresh cycle, which the file does not give; an old latest date is an open question for the user.

Each condition names its field, states the observation as a short plain-language phrase ("Blank", "Placeholder number instead of a resolution"), counts the affected records, and says why it matters: what it changes for a reader who uses the data, such as a denominator that shrinks, a join that fails, or a total that needs affected records excluded.

This step is complete when every area has been checked against the profile and the records, and each condition found is recorded with its field, observation, affected records, and why it matters, or the area is recorded as checked with nothing to report.

## 3. Explore

Follow useful signals from the profile and the data quality conditions. Examine distributions, concentrations, changes over time, relationships between columns, or concentrations of missing and repeated values when relevant. Choose comparisons that help interpret the pattern and inspect the contributing records. Keep raw values available alongside parsed values; record exclusions and transformations in the script, and state those that change a denominator in the context of the observation they affect.

Write each retained pattern with:

- **Observation:** what the data shows, with its denominator, population, period, or comparison group as needed.
- **Interpretation:** optional; a possible explanation, clearly separated from the observation.
- **Open question:** optional; additional context that would materially change the interpretation.

Exploration is complete when the basic profile has been considered for useful follow-up, each retained pattern is supported by calculations and inspected records, and material unresolved limitations are stated in the observations they affect. Require no minimum number of observations or charts; a short report is appropriate when further exploration adds little.

## 4. Present and verify

Read [HTML-REPORT.md](HTML-REPORT.md) for the driver and report helpers. Write the driver in the OS temporary directory with the source path, helper location, interpretation choices, and all calculations behind the report. Derive statements containing numbers from calculated values. Give the report a readable narrative, using tables or embedded charts where they answer a useful question. All styling and visuals must work offline.

Write for an auditor who has not opened the file:

- Name the dataset in plain words inferred from the filename and contents. Describe it in a sentence or two, including what one record represents.
- Give every field an apparent meaning in plain words.
- Carry units and scale with quantities in prose rather than leaving them implicit. Format figures in tables consistently from the parsed values.

Run the driver and check:

- Counts reconcile to the source; blanks, parsing failures, and exclusions explain the denominators used.
- Each reported number matches its calculation, and every interpretation remains distinct from what the data establishes.
- The report renders with readable labels, tables, and charts. Render it with headless Chrome or Edge and read the screenshot; the Chrome extension opens only web URLs, not local files. Use a tall window and crop the image when the page is long:

  ```text
  "<chrome or msedge executable>" --headless=new --disable-gpu --hide-scrollbars --window-size=1280,12000 --screenshot="<temp png>" "<file URL of report.html>"
  ```

  If no browser can render it, disclose that visual verification remains outstanding.

Open the report in the user's default browser: `Start-Process` on Windows, `open` on macOS, `xdg-open` on Linux. Return the report's absolute path and a short account of useful observations, the dimensions explored, and limitations. The report is temporary; rerun the skill to regenerate it.

This step is complete when the checks pass, the report is open in the browser, and the title, description, and field meanings read as plain language. Formal audit-trail packaging is outside this version's scope.
