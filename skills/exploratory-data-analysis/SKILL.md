---
name: exploratory-data-analysis
description: Explores one CSV an auditor has received and opens a temporary offline HTML report of its contents, structure, quality, and patterns. Use for a first look at a dataset before audit testing. Supports one table with a header row.
---

# Exploratory Data Analysis

Turn an unfamiliar CSV into an understanding of what it contains and what deserves closer examination. Exploration generates observations and hypotheses, not conclusions. An unusual value or relationship is a reason to look closer.

## Scope and files

Analyze exactly one comma-delimited CSV, with one table and field names in the first record. If several files are offered, establish which one to explore. For an unsupported structure, explain what is needed rather than silently choosing a table or changing the source.

Read the existing CSV in place and leave its bytes unchanged. The report is throwaway: write the driver script, the report, and every intermediate file to the OS temporary directory. Each run writes a fresh, timestamped report; `Report.write()` in the skill's `scripts/report.py` names it. The driver imports the installed skill's scripts.

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

## 3. Build the data overview

Help the reader understand their dataset through useful descriptive questions, using important fields as the starting point. Use judgment to select questions about composition, distributions, changes over time, or relationships that the data can meaningfully answer. Choose measures at the appropriate grain: counts of records and counts of distinct entities answer different questions, and repeated entity-level values may not be additive.

Present each retained question as a heading, one suitable chart, and two short prose paragraphs: a descriptive takeaway, then context needed to read the chart correctly. The context explains the measure, population, or relevant limitation; it need not invent a caveat. Keep ordinary descriptive patterns, such as peaks over time or a category's share, beside their charts. Choose chart types to suit the questions; no fixed number of charts, field-by-field chart inventory, or mix of chart types is required. Include only questions the data supports answering with a meaningful chart. This section has no tables or chart-values dropdowns.

Keep raw values available alongside parsed values. Record exclusions and transformations in the script and explain choices that affect interpretation alongside the affected visual, including units, population, period, and denominators as needed. Apply unresolved limitations to the choice of measures and calculations.

This step is complete when the important fields have been considered for useful descriptive questions, each retained question has a rendered chart supported by calculations, and its chart and two prose paragraphs agree. If the file supports no meaningful overview, state why briefly in this section.

## 4. Develop observations when warranted

Follow patterns from the profile, data quality assessment, and overview that raise meaningful questions an auditor could take to the data provider. These may concern business activity, unusual relationships, or the meaning and reliability of the data. Inspect the contributing records and useful comparisons before retaining an observation.

Write each observation with:

- **What we noticed:** the supported pattern, with its denominator, population, period, or comparison group as needed. Any supporting chart or table follows this directly, so the reader can check the claim before reading on.
- **Why it matters:** how the pattern could affect interpretation or what it prompts the auditor to explore. Include possible explanations only when useful and clearly label them as hypotheses.
- **Question for the data provider:** a specific question that would help explain or resolve the pattern.

For example, peaks in recorded acquisitions belong in the overview; identical costs across related acquisition records may warrant asking whether the cost is allocated per record or repeated from a shared purchase price. Retain an observation only when its evidence supports a meaningful stakeholder question. Omit the Observations section when nothing warrants it.

When an observation also limits analysis, apply the limitation to all affected calculations and visuals, including those earlier in the report. Keep the full evidence and stakeholder question in Observations. Describe an uncertain meaning as unresolved, without treating a suspected explanation as an established error.

This step is complete when useful follow-up signals have been examined, each retained observation is supported by calculations and inspected records and ends with a concrete stakeholder question, and any resulting limitations are reflected throughout the report.

## 5. Present and verify

Read [HTML-REPORT.md](HTML-REPORT.md) for the driver and the `Report` module. Write the driver in the OS temporary directory with the source path, skill location, interpretation choices, and all calculations behind the report. Derive statements containing numbers from calculated values. Give the report a readable narrative, using tables or embedded charts where they answer a useful question. All styling and visuals must work offline.

Consolidate material constraints on interpretation into one optional **Analysis limitations** section at the end, after Observations when present. Use a concise list, referring to an observation by title when it carries the full investigation. Keep chart-specific context in the second paragraph beneath the affected chart so it can be read on its own. Routine calculation choices, such as counting distinct sites, belong in chart context and are not automatically report-wide limitations. Data quality retains its condition tables without an introductory limitations block.

Write for an auditor who has not opened the file:

- Name the dataset in plain words inferred from the filename and contents. Describe it in a sentence or two, including what one record represents.
- Give every field an apparent meaning in plain words.
- Carry units and scale with quantities in prose rather than leaving them implicit. Format figures in tables consistently from the parsed values.

Run the driver and check:

- Counts reconcile to the source; blanks, parsing failures, and exclusions explain the denominators used.
- Each reported number matches its calculation, and every interpretation remains distinct from what the data establishes.
- Each Data overview question has a chart followed by a takeaway and context, with no tables or dropdowns. Optional Observations raise concrete questions for the data provider. Consolidated limitations appear once at the end, with essential context also beneath affected charts.
- The report renders with readable labels, tables, and charts. Render it with headless Chrome or Edge and read the screenshot; the Chrome extension opens only web URLs, not local files. Use a tall window and crop the image when the page is long:

  ```text
  "<chrome or msedge executable>" --headless=new --disable-gpu --hide-scrollbars --window-size=1280,12000 --screenshot="<temp png>" "<file URL of report.html>"
  ```

  If no browser can render it, disclose that visual verification remains outstanding.

Open the report in the user's default browser: `Start-Process` on Windows, `open` on macOS, `xdg-open` on Linux. Return the report's absolute path and a short account of the dimensions explored, any stakeholder questions, and limitations. The report is temporary; rerun the skill to regenerate it.

This step is complete when the checks pass, the report is open in the browser, and the title, description, and field meanings read as plain language. Formal audit-trail packaging is outside this version's scope.
