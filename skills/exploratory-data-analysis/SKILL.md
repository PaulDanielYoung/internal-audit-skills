---
name: exploratory-data-analysis
description: Explores one CSV an auditor has received and opens a temporary offline HTML report of its contents, structure, quality, and patterns. Use for a first look at a dataset before audit testing. Supports one table with a header row.
---

# Exploratory Data Analysis

Turn an unfamiliar CSV into an understanding of what it contains and what deserves closer examination. Exploration generates observations and hypotheses, not conclusions. An unusual value or relationship is a reason to look closer.

## Scope and files

Analyze exactly one comma-delimited CSV, with one table and field names in the first record. If several files are offered, establish which one to explore. For an unsupported structure, explain what is needed rather than silently choosing a table or changing the source.

Read the CSV in place and leave its bytes unchanged. The report is throwaway: the driver, the report, and every intermediate file go in the OS temporary directory, and each run writes a fresh report.

## 1. Orient and profile

Run `uv run "<skill directory>/scripts/profile_csv.py" "<CSV path>"` and read the printed summary and the temporary JSON profile. Without uv, use Python 3.10+ with `pandas>=2.0,<4` in a virtual environment. Script paths are relative to the skill directory, not the working directory; `--help` describes the parsing overrides.

Review every field's apparent role against its name and raw values, and inspect the failure examples before using parsed values. A `date_format_hint` lists the non-ISO date formats a field's values fit; confirm one against the raw values, and treat a hint that fits both month-first and day-first as an unresolved question about the field. Correct roles and date formats by rerunning the profiler with overrides; the driver must repeat the same choices.

When an unresolved question about a field's meaning or values would materially change a calculation or interpretation, call the Skill tool with "shared-understanding", giving it the specific ambiguity and the context already established. The user resolves it before you continue; if they cannot, flag the field as unresolved and continue with the rest of the dataset.

This step is complete when row and field counts, blanks, and appropriate basic field summaries are established; every field's role has been reviewed and its apparent meaning written in plain words; and the dataset's grain is stated with its basis or flagged as unresolved. An empty table can have a complete profile without supporting further analysis.

## 2. Assess data quality

Record the observable conditions in the file that could affect how its data is interpreted or analyzed, one condition each, in five areas:

- **Completeness:** blank cells by field, fields that are entirely blank, and fields far sparser than the rest.
- **Validity:** values that fail to parse as their apparent type, dates or numbers outside a possible range, and malformed values.
- **Uniqueness:** exact duplicate records, and repeated values in apparent identifiers or composite keys.
- **Consistency:** fields that contradict each other within a record, and values that vary within an apparent entity where they should stay constant.
- **Coverage:** earliest and latest dates and obvious gaps between them. Whether the data are current depends on the expected refresh cycle, which the file does not give; an old latest date is an open question for the user.

State each observation as a short plain-language phrase ("Blank", "Placeholder number instead of a resolution"), and say why it matters: what it changes for a reader who uses the data, such as a denominator that shrinks, a join that fails, or a total that needs affected records excluded.

Record every condition found with `Report.quality()`. For a condition whose impact merits attention despite affecting few records, set `always_show=True` and explain that impact in `why_it_matters`; the report otherwise summarizes conditions below its display threshold in a count.

This step is complete when every area has been checked against the profile and the records, and each condition found is recorded, or the area is recorded as checked with nothing to report.

## 3. Build the data overview

Help the reader understand their dataset through useful descriptive questions, using important fields as the starting point. Use judgment to select questions about composition, distributions, changes over time, or relationships that the data can meaningfully answer. Choose measures at the appropriate grain: counts of records and counts of distinct entities answer different questions, and repeated entity-level values may not be additive.

Each retained question gets one chart suited to it, a descriptive takeaway, and the context needed to read the chart correctly: the measure, population, period, units, denominators, or a limitation that applies to it, without inventing a caveat. Ordinary descriptive patterns, such as peaks over time or a category's share, belong here beside their charts. Include only questions the data supports answering with a meaningful chart.

Record exclusions and transformations in the driver, and apply unresolved limitations to the choice of measures and calculations.

This step is complete when the important fields have been considered for useful descriptive questions, each retained question has a rendered chart supported by calculations, and its chart and prose agree. If the file supports no meaningful overview, say why instead.

## 4. Develop observations when warranted

Follow patterns from the profile, data quality assessment, and overview that raise meaningful questions an auditor could take to the data provider. These may concern business activity, unusual relationships, or the meaning and reliability of the data. Inspect the contributing records and useful comparisons before retaining an observation.

- **What we noticed:** the supported pattern, with its denominator, population, period, or comparison group as needed. A supporting chart or table lets the reader check the claim.
- **Why it matters:** how the pattern could affect interpretation or what it prompts the auditor to explore. Include possible explanations only when useful and clearly label them as hypotheses.
- **Question for the data provider:** a specific question that would help explain or resolve the pattern.

For example, the distribution of service-request resolution times belongs in the overview; requests marked resolved before their recorded opening dates may warrant asking how those dates are defined or populated. Retain an observation only when its evidence supports a meaningful stakeholder question.

When an observation also limits analysis, apply the limitation to all affected calculations and visuals, including those earlier in the report, and keep the full evidence and stakeholder question in the observation. Describe an uncertain meaning as unresolved, without treating a suspected explanation as an established error.

This step is complete when useful follow-up signals have been examined, each retained observation is supported by calculations and inspected records and ends with a concrete stakeholder question, and any resulting limitations are reflected throughout the report.

## 5. Present and verify

Read [HTML-REPORT.md](HTML-REPORT.md) for the driver and the `Report` module. The driver holds the source path, skill location, interpretation choices, and every calculation behind the report, so each number in the report derives from a calculated value.

Add a limitation for each material constraint on interpretation, referring to an observation by title when it carries the full investigation. Routine calculation choices, such as counting distinct sites, belong in chart context rather than in limitations.

Write for an auditor who has not opened the file: name the dataset in plain words inferred from the filename and contents, describe it in a sentence or two including what one record represents, and give every field an apparent meaning in plain words.

Run the driver and check:

- Counts reconcile to the source; blanks, parsing failures, and exclusions explain the denominators used.
- Each reported number, ranking, comparison, and named example matches its calculation, and every interpretation remains distinct from what the data establishes. Read each takeaway against its rendered chart or table.
- The report renders with readable labels, tables, and charts. Render it with headless Chrome or Edge and read the screenshot; the Chrome extension opens only web URLs, not local files. Use a tall window and crop the image when the page is long:

  ```text
  "<chrome or msedge executable>" --headless=new --disable-gpu --hide-scrollbars --window-size=1280,12000 --screenshot="<temp png>" "<file URL of report.html>"
  ```

  The height above is a starting point. Check that the screenshot includes the complete final section and the page's bottom padding; if content is cut off, increase the height and render again until the whole report fits, or use a full-page capture. Inspect readable crops covering the entire page, including its bottom. If no browser can render it, disclose that visual verification remains outstanding.

Open the report in the user's default browser: `Start-Process` on Windows, `open` on macOS, `xdg-open` on Linux. Return the report's absolute path and a short account of the dimensions explored, any stakeholder questions, and limitations. The report is temporary; rerun the skill to regenerate it.

This step is complete when the checks pass, the report is open in the browser, and the title, description, and field meanings read as plain language. Formal audit-trail packaging is outside this version's scope.
