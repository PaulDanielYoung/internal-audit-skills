---
name: exploratory-data-analysis
description: Explore data an auditor has received and present what it is in a visual HTML report. Use when the user shares or names a data file (CSV, XLSX, JSON) and wants to understand, summarize, or profile it.
---

# Exploratory Data Analysis

Turn an unfamiliar dataset into an understanding of what it contains, how it is structured, and what deserves closer examination. The aim is to understand the data before testing. That includes its shape, fields, quality, distributions, relationships, and notable patterns.

Exploration generates observations and hypotheses, not audit conclusions. An unusual value, pattern, or relationship is a reason to investigate further, not evidence by itself of an error, control failure, or other exception.

## Process

### 1. Orient

Start by understanding what you received before analyzing it. Do not jump straight to visualizations, anomalies, or audit tests.

Inspect each file, workbook, sheet, or object and establish its basic structure:

* What data sources were provided?
* How many rows and columns does each contain?
* What fields are present, and what data types do they appear to contain?
* Which fields look like identifiers, dates, amounts, categories, free text, or measures?
* Are there obvious keys or relationships between datasets or sheets within a dataset?
* What date range or other period does the data cover?
* Are there empty sheets, duplicated headers, title rows, subtotals, formulas, lookup tables, instructions, or other structures that should not be treated as transactional data?

Read representative records and inspect distinct values where useful to understand what fields appear to mean. Treat inferred meanings as hypotheses unless they are established by the data, accompanying documentation, or the user.

If a field, dataset, relationship, or intended meaning is materially ambiguous and that ambiguity would affect the analysis, call the Skill tool with `"shared-understanding"` rather than silently guessing.

### 2. Profile

Build a quantitative baseline for the data before deciding what deserves deeper exploration.

Profile fields according to what they contain rather than applying the same statistics to every column. At minimum, establish where relevant:

* **Completeness**: null, blank, or otherwise missing values
* **Uniqueness**: distinct values, repeated values, and apparent duplicate records
* **Cardinality**: how concentrated or varied categorical and identifier fields are
* **Numeric distributions**: range, center, spread, zero and negative values, and extreme observations
* **Categorical distributions**: common values, rare values, and concentration
* **Dates and times**: coverage, gaps, frequency, clustering, and values outside the apparent period
* **Identifiers and keys**: uniqueness, formatting consistency, and whether apparent relationships between datasets hold
* **Text fields**: recurring values, formatting variation, and other structure that can be meaningfully summarized

Do not mechanically calculate every possible statistic. Choose summaries that help explain the field and omit metrics that would be meaningless or misleading for its apparent role.

Distinguish **data characteristics** from **data quality concerns**. A field with many nulls, repeated values, extreme amounts, or an unexpected distribution is noteworthy, but whether it represents a problem depends on what the field means and how the data is used.

Preserve the original data while profiling. Record any parsing, type conversion, filtering, normalization, or other transformation needed to analyze it so the resulting observations can be traced back to the source.

### 3. Explore

Follow the signals that emerge from orientation and profiling. Explore organically rather than running a fixed catalog of anomaly tests.

Look for patterns that help explain how the data behaves and where closer examination may be useful:

* How do important measures vary across categories, entities, locations, or time?
* Are apparent outliers isolated observations or part of a broader pattern?
* Do unusual values cluster around particular people, vendors, departments, accounts, dates, or other dimensions?
* Are there discontinuities, spikes, gaps, seasonality, or changes in behavior over time?
* Do fields that appear related behave consistently with one another?
* Do subsets of the data behave materially differently from the overall population?
* Are duplicates, missing values, rare categories, or other quality characteristics concentrated somewhere specific?
* Do relationships between datasets reveal unmatched, one-to-many, or otherwise unexpected records?

Let one observation lead to the next. When a pattern looks interesting, slice it along relevant dimensions, inspect the underlying records, and determine whether the pattern persists or disappears under closer examination.

Prefer explanations supported directly by the data over speculation about why a pattern exists. Clearly distinguish:

* **Observation** — what the data shows
* **Interpretation** — what that pattern may mean
* **Open question** — what would need additional context or evidence to understand it

Do not turn exploration into audit testing. Avoid declaring exceptions, control failures, root causes, fraud indicators, or other audit conclusions unless the user explicitly moves into a separate testing or investigation workflow.

### 4. Present

Present the exploration as a self-contained visual HTML report that helps the auditor understand the dataset and decide what, if anything, deserves further examination.

Write the report to the OS temporary directory so the analysis does not modify the user's source files or working directory. Use a fresh filename for each run and open the completed report for the user when the environment permits it.

Make the report **visual first**. Use charts, tables, distributions, timelines, relationship diagrams, and concise annotations where they communicate the data better than prose. Choose each visualization because it answers a question; do not generate charts merely because a field can be charted.

Structure the report around the story of the data rather than reproducing every statistic collected during profiling. Include:

* **Data overview**: sources, rows, fields, apparent grain, coverage period, and relationships between datasets
* **Field profile**: the characteristics needed to understand important fields and material data-quality observations
* **Key observations**: the patterns, distributions, relationships, and unusual characteristics that emerged during exploration
* **Visual evidence**: charts or tables showing the observations directly
* **Questions and hypotheses**: matters that may warrant context, validation, or subsequent audit work
* **Analysis notes**: material assumptions, inferred meanings, transformations, and limitations that affect interpretation

For every notable observation, make it possible to understand **what was observed and why it was surfaced**. Show enough supporting context to avoid making ordinary variation look anomalous.

Prioritize findings by their usefulness for understanding the data, not by how dramatic they appear. Do not assign audit severity, risk ratings, or exception status during exploratory analysis.

End the report with **Areas for closer examination**: a short set of evidence-backed questions or hypotheses that naturally follow from the exploration. These are possible directions for subsequent work, not findings or recommended audit conclusions.
