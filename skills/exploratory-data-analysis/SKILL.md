---
name: exploratory-data-analysis
description: Explores one CSV an auditor has received and produces an offline HTML report of its contents, structure, quality, and patterns. Use for a first look at a dataset before audit testing. Supports one table with a header row.
---

# Exploratory Data Analysis

Turn an unfamiliar CSV into an understanding of what it contains and what deserves closer examination. Exploration generates observations and hypotheses, not audit conclusions. An unusual value or relationship is a reason to look closer; an error or control failure requires a separate testing or investigation workflow.

Two terms guide the analysis:

- **Apparent:** a meaning, field role, or grain inferred from the data, pending supporting context.
- **Characteristic:** what a field is like, such as repeated values or a long tail. Whether it is a concern depends on its meaning and use.

## Scope and files

Analyze exactly one comma-delimited CSV, with one table and field names in the first record, small enough to process in memory. If several files are offered, establish which one to explore. For an unsupported structure, explain what is needed rather than silently choosing a table or changing the source.

Read the existing CSV in place and leave its bytes unchanged. Put the retained outputs in a sibling directory named `<csv-stem> - exploratory data analysis`, where the stem is the filename without `.csv`:

```text
transactions.csv
transactions - exploratory data analysis/
    analysis.py
    report.html
```

Reuse that directory on subsequent runs. Read any existing `analysis.py` before revising it; retain relevant interpretation choices. Replace these generated outputs when rerunning this analysis, leaving unrelated files untouched. Keep intermediate files in the OS temporary directory and remove only those created for this run when finished. The retained script must regenerate the report from the CSV without a temporary profile or conversation state. It may import the installed skill's helpers.

## 1. Orient and profile

Run `uv run "<skill directory>/scripts/profile_csv.py" "<CSV path>"`. Read the printed summary and temporary JSON profile. If uv is unavailable, use Python 3.10+ with `pandas>=2.0,<4` installed in a virtual environment. Script paths are relative to the skill directory, not the engagement directory; `--help` describes parsing overrides.

Review every field's apparent role against its name and raw values. The profiler preserves strings, including leading-zero identifiers and literal `NA` values. It treats whitespace-only cells as blank, infers plain numbers and ISO dates, and reports conversion failures separately from blanks. Inspect failed examples before using parsed values. Correct roles and date formats by rerunning the profiler with overrides; the retained script must use the same choices. Do not guess locale, date order, currency, or business meaning when it would change the analysis.

Ask only when unresolved meaning would materially change a calculation or interpretation. If `shared-understanding` is available, invoke it with the specific ambiguity and already-established context; for this workflow, resolve that question without restarting a full engagement interview. Otherwise ask the specific question directly. Continue independent analysis while the affected decision remains unresolved.

This step is complete when row and field counts, blanks, and appropriate basic field summaries are established; every field's role has been reviewed; and the dataset's grain is stated with its basis or flagged as unresolved. An empty table can have a complete profile without supporting further analysis.

## 2. Explore

Follow useful signals from the profile. Examine distributions, concentrations, changes over time, relationships between columns, or concentrations of missing and repeated values when relevant. Choose comparisons that help interpret the pattern and inspect the contributing records. Keep raw values available alongside parsed values; record exclusions and transformations in the script and report notes.

Write each retained pattern with:

- **Observation:** what the data shows, with its denominator, population, period, or comparison group as needed.
- **Interpretation:** optional; a possible explanation, clearly separated from the observation.
- **Open question:** optional; additional context that would materially change the interpretation.

Exploration is complete when the basic profile has been considered for useful follow-up, each retained pattern is supported by calculations and inspected records, and material unresolved limitations are stated. Briefly record the dimensions explored and relevant limitations. Require no minimum number of observations or charts; a short report is appropriate when further exploration adds little. A quiet dataset does not establish that controls are effective.

## 3. Present and verify

Read [HTML-REPORT.md](HTML-REPORT.md) for the retained script and report helpers. Create `analysis.py` in the output directory with the source filename, helper location, interpretation choices, and all calculations needed to regenerate `report.html`. Derive statements containing numbers from calculated values. Give the report a readable narrative, using tables or embedded charts where they answer a useful question. All styling and visuals must work offline.

Run the script and check:

- Counts reconcile to the source; blanks, parsing failures, and exclusions explain the denominators used.
- Each reported number matches its calculation, and every interpretation remains distinct from what the data establishes.
- The report renders with readable labels, tables, and charts. Inspect it in a browser when a preview is available; otherwise disclose that visual verification remains outstanding.
- The script reruns from another working directory without temporary inputs, producing the report beside it and leaving the CSV unchanged.

Return links to `report.html` and `analysis.py`, a short account of useful observations or limitations, and the command for rerunning the script. Formal audit-trail packaging is outside this version's scope.
