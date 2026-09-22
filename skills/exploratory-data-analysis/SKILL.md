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

## Process

### 1. Orient

Read the raw structure before analyzing it. Inspect each file, workbook, sheet, or object:

* Sources provided, and the rows and columns in each
* Fields present and the data types they appear to hold
* The apparent role of each field: identifier, date, amount, category, free text, or measure
* Apparent keys and relationships between datasets or sheets
* The date range or other period covered
* Structures that are not transactional data: empty sheets, title rows, duplicated headers, subtotals, formulas, lookup tables, instructions

Read representative records and distinct values to work out what fields mean.

Call the Skill tool with `"shared-understanding"` when a field, dataset, relationship, or intended meaning is materially ambiguous and the ambiguity would change the analysis.

Orient is complete when every source has row and field counts, every field has an apparent role, and the grain of each source is stated or flagged as ambiguous.

### 2. Profile

Build a quantitative baseline before deciding what deserves deeper exploration. Profile each field according to its apparent role; the statistics that explain a category say nothing about an identifier.

* **Identifiers and keys**: completeness, distinct count, duplicates, formatting consistency, and whether apparent relationships between datasets hold
* **Numeric measures**: count, missing values, range, median and relevant percentiles, zero and negative values, spread, extreme observations, distribution shape. Show the mean only when it aids interpretation.
* **Categories**: distinct count, completeness, most common values, concentration, rare values, inconsistent labels or formatting
* **Dates and times**: earliest and latest, completeness, frequency, gaps, clustering, values outside the apparent period
* **Free text**: completeness, repeated exact values, common prefixes or patterns, formatting variation, length distribution. Summarize only when meaningful structure exists.

Choose the summaries that explain the field and omit the rest.

Preserve the original data. Record every parsing step, type conversion, filter, normalization, or other transformation so each observation stays **traceable** to the source.

Profile is complete when every field has the profile its role calls for and every transformation is recorded.

### 3. Explore

Follow the signals from orientation and profiling rather than a fixed catalog of anomaly tests. Questions that tend to open the data up:

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

### 4. Present

Compute in a script; the HTML is the presentation layer only. Aggregate, group, or bin during analysis and pass the results to the page.

Read `HTML-REPORT.md` before writing any HTML. It defines the scaffold, sections, chart patterns, and style of the report.

Write the report to the OS temporary directory under a fresh filename for each run, so the user's source files and working directory stay untouched. Open the completed report for the user when the environment permits.

Present is complete when the report passes four checks:

* Every section helps the auditor understand the dataset.
* Every observation shows its evidence.
* Every interpretation is separated from what the data establishes.
* Every adverse word rests on something exploration actually established; otherwise the observation stands and the conclusion stays open.
