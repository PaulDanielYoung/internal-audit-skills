---
name: exploratory-data-analysis
description: Explore data an auditor has received and present what it contains in a visual HTML report. Use when the user shares or names a data file (CSV, XLSX, JSON) and wants a first look at what is in it, before any audit testing.
---

# Exploratory Data Analysis

Turn an unfamiliar dataset into an understanding of what it contains, how it is structured, and what deserves closer examination: its shape, fields, quality, distributions, relationships, and notable patterns. Exploration comes before testing.

Exploration generates observations and hypotheses, not audit conclusions. An unusual value, pattern, or relationship is a reason to look closer, not evidence of an error, control failure, or other exception. Language that names an audit conclusion waits for a separate testing or investigation workflow that the user opens explicitly.

Two words carry the analytical stance throughout:

* **Apparent**: inferred from names, values, or relationships in the data. A meaning, grain, or relationship stays *apparent* until the data, accompanying documentation, or the user establishes it.
* **Characteristic**: what a field is like (many nulls, repeated values, a long tail). Whether a characteristic is a **concern** depends on what the field means and how the data is used, so describe the characteristic first.

## Scripts

Two scripts live in `scripts/` under this skill's base directory, with the page template in `assets/`. Run them with `uv run`, which installs the dependencies they declare inline. Without uv, run `python -m pip install pandas openpyxl` once and use `python` instead.

* `profile.py FILE...` loads every file and every sheet, profiles each field by apparent role, tests apparent relationships between sources, writes the full profile as JSON to the OS temp directory and prints a summary. `--help` lists what it records.
* `report.py` is a library the per-run driver script imports: one emitter per section and visual, and `write_report()`, which fills the template, writes a fresh file to the OS temp directory and opens it.

Per-run code goes in the scratchpad or temp directory. The skill folder and the user's files stay untouched.

## Process

### 1. Orient and profile

Run `profile.py` against every file received. Read the printed summary, then the JSON: the structural notes for each source, its sample records, each field's apparent role and statistics, and the apparent relationships between sources. A hidden sheet, a title row, a duplicated header, or a field stored as text appears in the notes. A non-tabular source carries a raw sample instead of a profile; decide what it is from the sample.

Check every apparent role against the sample values and the field's name, and note the ones to correct. Note the characteristics that deserve exploration.

Call the Skill tool with `"shared-understanding"` when a field, dataset, relationship, or intended meaning is materially ambiguous and the ambiguity would change the analysis.

Preserve the original data. Record every transformation the analysis needs beyond the profiler's own notes so each observation stays **traceable** to the source.

Orient and profile is complete when every source has row and field counts and is classified as tabular or not, every field's role is confirmed or corrected, the grain of each source is stated or flagged as ambiguous, and every transformation is recorded.

### 2. Explore

Follow the signals from the profile rather than a fixed catalog of anomaly tests. Questions that tend to open the data up:

* How do important measures vary across categories, entities, locations, or time?
* Are apparent outliers isolated or part of a broader pattern?
* Do unusual values cluster around particular people, vendors, departments, accounts, or dates?
* Are there discontinuities, spikes, gaps, seasonality, or changes in behavior over time?
* Do fields that appear related behave consistently with one another?
* Do subsets behave materially differently from the whole population?
* Are duplicates, missing values, or rare categories concentrated somewhere specific?
* Do relationships between datasets reveal unmatched, one-to-many, or otherwise unexpected records?

Let one observation lead to the next. When a pattern looks interesting, slice it along relevant dimensions and inspect the underlying records; keep the patterns that persist and drop those that dissolve.

Write up every kept pattern in three separated parts:

* **Observation**: what the data shows. "Four expense categories account for 78% of recorded spend."
* **Interpretation**: what the pattern may mean, offered only when useful and stated as a possibility. "The concentration may reflect centralized purchasing, department size, or both."
* **Open question**: what additional context or evidence would change the interpretation. "Are these departments expected to purchase on behalf of other units?"

Explore is complete when every surfaced pattern has been sliced along at least one dimension and its records inspected, then either dropped or written up with an observation and the context (denominator, period, population, comparison group) needed to read it.

### 3. Present

Read `HTML-REPORT.md` before writing the driver. It shows the driver's shape, what each section takes, and which visual answers which question.

Write the driver script in the scratchpad or temp directory. Compute there: bin, group, and aggregate the data behind each card, then pass the results to the emitters. Run it with `uv run` (or `python`) and give the user the path it prints.

Present is complete when the report passes four checks:

* Every section helps the auditor understand the dataset.
* Every observation shows its evidence.
* Every interpretation is separated from what the data establishes.
* Every adverse word rests on something exploration actually established; otherwise the observation stands and the conclusion stays open.
