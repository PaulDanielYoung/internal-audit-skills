# HTML Report Format

The exploratory data analysis is rendered as a single self-contained HTML file in the OS temp directory. Tailwind comes from a CDN for layout and styling, and Chart.js comes from a CDN for charts.

The report is an **analytical narrative, not a dashboard**. It should help an auditor understand what the data contains, how it behaves, what patterns emerged, and what may deserve closer examination.

Visuals carry the weight. Prose should explain what the data shows, provide the context needed to interpret it, and clearly separate observation from interpretation.

Do not chart everything. Select the tables and visualizations that materially improve understanding of the dataset.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Exploratory data analysis — {{dataset name}}</title>

    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
      body {
        -webkit-font-smoothing: antialiased;
      }

      .chart-container {
        position: relative;
        width: 100%;
        height: 360px;
      }

      .numeric {
        font-variant-numeric: tabular-nums;
      }

      .scroll-table {
        overflow-x: auto;
      }
    </style>
  </head>

  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-6xl mx-auto px-6 py-12 space-y-14">

      <header id="overview">
        ...
      </header>

      <section id="structure">
        ...
      </section>

      <section id="field-profile">
        ...
      </section>

      <section id="observations" class="space-y-10">
        ...
      </section>

      <section id="closer-examination">
        ...
      </section>

      <section id="analysis-notes">
        ...
      </section>

    </main>
  </body>
</html>
```

Keep JavaScript limited to the code needed to render Chart.js visualizations.

The report should not behave like an application. Do not add filters, tabs, dropdowns, navigation frameworks, or other dashboard controls unless interaction is genuinely necessary to communicate the analysis.

Prefer HTML and CSS for simple displays such as completeness bars, summary statistics, badges, schema cards, and small tables. Use Chart.js when a chart materially improves understanding.

Prepare chart data during analysis rather than embedding raw populations unnecessarily. Aggregate, group, or bin the underlying data first, then pass the resulting values to Chart.js.

## Header

Start with the facts the reader needs to orient themselves.

Show:

* **Dataset or analysis name**
* **Generation date**
* **Source files, sheets, tables, or objects**
* **Row count**
* **Field count**
* **Coverage period**, when identifiable
* **Apparent grain**, when identifiable

Example:

```text
Travel & Expense Transactions

142,318 rows · 27 fields · Jan 2024–Jun 2026

Sources
expenses.xlsx / Transactions
employees.csv

Apparent grain
One row per expense line
```

Do not write a generic introduction explaining exploratory data analysis. Go directly into the dataset.

If field meanings, grain, relationships, or other important characteristics are inferred rather than established, include a compact interpretation note:

> **Interpretation note:** Field meanings and dataset grain are inferred from names, values, and relationships unless otherwise stated.

If a material limitation affects the analysis, surface it near the top rather than burying it at the end.

## Data structure

Explain how the dataset is organized before discussing patterns within it.

For a single flat dataset, use a compact schema or grouped field summary.

For multiple files, sheets, tables, or objects, show:

* each source
* its apparent purpose
* row and field counts
* apparent key fields
* apparent relationships between sources

Do not force relational structure onto unrelated datasets.

When relationships are straightforward, use hand-built HTML cards and arrows. A relationship display should make clear which fields appear to connect the datasets and whether the relationship was validated or merely inferred.

Example:

```text
employees.csv
4,291 rows
employee_id appears unique
        │
        │ employee_id
        ▼
expenses.xlsx / Transactions
142,318 rows
employee_id repeats
```

Label an inferred relationship as **apparent** until supported by the data.

If joins were tested, show the resulting relationship characteristics where useful:

* matched records
* unmatched records
* duplicate keys
* apparent one-to-one, one-to-many, or many-to-many behavior

Do not describe an unmatched record as an exception unless the expected relationship has been established.

## Field profile

The field profile is a compact reference for understanding important fields. It is not a dump of every statistic calculated during analysis.

Profile fields according to their apparent role.

A useful default table is:

| Field | Apparent role | Coverage | Distinct | Range / common values | Note |
| ----- | ------------- | -------: | -------: | --------------------- | ---- |

Examples:

| Field          | Apparent role | Coverage | Distinct | Range / common values  | Note                         |
| -------------- | ------------- | -------: | -------: | ---------------------- | ---------------------------- |
| `employee_id`  | Identifier    |     100% |    4,291 | —                      | Repeats across transactions  |
| `expense_date` | Date          |    99.9% |      812 | Jan 2024–Jun 2026      | 117 missing                  |
| `amount`       | Measure       |    99.8% |        — | -420 to 18,330         | Strong right tail            |
| `expense_type` | Category      |     100% |       17 | Airfare 31%, Hotel 24% | Concentrated in 4 categories |

Use only metrics that help explain the field.

### Identifier fields

Useful characteristics may include:

* completeness
* distinct count
* duplicate count
* formatting consistency
* apparent uniqueness
* relationship to other identifiers

Do not calculate averages, medians, or numeric distributions for identifiers merely because they are stored as numbers.

### Numeric measures

Useful characteristics may include:

* count
* missing values
* minimum and maximum
* median
* relevant percentiles
* zero values
* negative values
* spread
* extreme observations
* distribution shape

Use the mean only when it helps interpretation. Do not mechanically show every conventional summary statistic.

### Categorical fields

Useful characteristics may include:

* distinct count
* completeness
* most common values
* category concentration
* rare values
* inconsistent labels or formatting

Do not display hundreds of category values in the field profile. Summarize the useful structure and explore important categories separately.

### Dates and times

Useful characteristics may include:

* earliest and latest value
* completeness
* frequency
* gaps
* unusual clustering
* values outside the apparent coverage period

### Free text

Summarize free-text fields only when meaningful structure exists.

Useful characteristics may include:

* completeness
* repeated exact values
* common prefixes or patterns
* formatting variation
* length distribution

Do not generate word clouds.

### Completeness

Show completeness visually when it materially helps explain the dataset.

A simple horizontal bar is often enough:

```html
<div class="w-full bg-slate-100 rounded-full h-2">
  <div class="bg-indigo-500 h-2 rounded-full" style="width: 97.4%"></div>
</div>
```

Do not use red simply because a field contains missing values. Missingness is a data characteristic until its significance is understood.

## Observation cards

The observation card is the main analytical unit of the report.

The visual carries the weight. Prose explains what the visual establishes and provides the context needed to interpret it.

Each material observation is one `<article>`.

Include, as appropriate:

* **Title**
* **Observation**
* **Visual**
* **Context**
* **Interpretation**
* **Open question**

Not every observation needs every element.

### Title

Use a short, descriptive title that states what the data shows.

Prefer:

> Travel spend is concentrated among 14 departments

Over:

> Concerning departmental concentration

Prefer:

> Transaction volume rises sharply at month-end

Over:

> Potential month-end control issue

Prefer:

> 7.2% of employee IDs do not match the employee file

Over:

> Employee master data exceptions

Titles should describe the evidence, not imply an audit conclusion.

### Observation

State what is directly supported by the data.

Good:

> Four expense categories account for 78% of recorded spend.

Good:

> Transactions recorded during the final three business days of each month average 1.8× the daily volume observed during the rest of the month.

Avoid:

> Employees appear to rush submissions at month-end.

The latter is an explanation, not an observation.

### Visual

Use the visualization that most directly communicates the observation.

The chart should make the observation visible without requiring the reader to reverse-engineer it.

Do not add a chart when a number or small table communicates the point better.

### Context

Include the denominator, time period, population, comparison group, or other context necessary to interpret the observation.

Examples:

> 312 of 4,291 employees account for 50% of recorded spend.

> This comparison excludes 117 transactions with missing transaction dates.

> The pattern appears in 21 of 24 complete months in the dataset.

Context prevents ordinary variation from being presented as more meaningful than it is.

### Interpretation

Interpretation is optional.

When useful, explain what the observation **may** indicate, while keeping it distinct from what the data directly establishes.

Example:

> **Interpretation:** The concentration may reflect centralized purchasing responsibilities, differences in department size, or both.

Do not present a plausible explanation as established fact.

### Open question

Use an open question when additional information would materially change interpretation.

Example:

> **Open question:** Are these departments expected to purchase centrally on behalf of other units?

Open questions should follow naturally from the evidence. Do not create generic audit questions merely to fill space.

## Visualization patterns

Choose the visualization based on the analytical question.

Do not make every observation look the same.

Chart.js provides the rendering layer. The analysis should prepare whatever grouped, aggregated, or binned data the chart needs before generating the HTML.

### Distribution

Use a histogram-style bar chart when the question is:

> How is this numeric measure distributed?

Chart.js does not require raw values for this. Bin the numeric population during analysis, then pass the bin labels and counts to a bar chart.

Good for:

* transaction amounts
* reimbursement values
* elapsed days
* invoice totals
* quantities

Example analytical result:

```text
$0–$100        4,218
$100–$250      7,914
$250–$500      3,108
$500–$1,000    1,142
$1,000+          428
```

For heavily skewed data, consider:

* selecting bins that make the distribution interpretable
* showing a meaningful percentile range in the primary chart and separately disclosing extreme values
* using logarithmic axes where appropriate

Never silently remove extreme observations to improve the appearance of a chart.

### Ranked bars

Use horizontal bar charts for category concentration and ranked comparisons.

Good for:

* spend by department
* transactions by vendor
* cases by type
* activity by location

Sort meaningfully, usually descending by the measure being discussed.

For high-cardinality categories, show the relevant top categories and aggregate the remainder as **Other** when doing so does not obscure the observation.

State explicitly when categories were grouped.

Horizontal bars are generally preferable when category labels are long.

### Time series

Use a line chart for patterns over time when continuity and direction matter.

Good for:

* monthly spend
* daily transaction volume
* case openings
* processing-time trends
* missingness over time

Use a bar chart instead when the periods are better understood as discrete totals.

Choose the aggregation level based on the dataset and analytical question.

Do not use daily granularity merely because daily dates exist if weekly or monthly aggregation communicates the pattern more clearly.

### Composition over time

Use stacked bar charts only when the changing composition of a total is itself the analytical question.

Avoid stacked charts when the reader needs to compare individual categories precisely.

Do not create large stacks containing many categories. Aggregate or select meaningful groups first.

### Scatter plot

Use a scatter chart to explore relationships between two numeric measures.

Good for:

* amount vs. processing time
* quantity vs. unit price
* employee volume vs. employee spend

Use the native Chart.js `scatter` chart.

Do not imply causality from association.

If a relationship is summarized numerically, explain what the metric represents rather than relying on a correlation coefficient alone.

### Group comparison

When comparing the distribution of a numeric measure across groups, use a chart that the available evidence and Chart.js can communicate directly.

Useful alternatives include:

* grouped bars of medians
* percentile ranges
* small distribution charts
* multiple histogram-style charts
* summary tables

Do not introduce a box-plot dependency merely because box plots are conventional. Add another library only if the visualization materially improves the report and the skill explicitly permits it.

### Heatmap-style displays

For a small two-dimensional grid such as weekday × hour or field × period, prefer a hand-built HTML/CSS grid when it communicates the pattern clearly.

Do not add a Chart.js plugin merely to create a heatmap.

Good for:

* activity by weekday and hour
* completeness by field and period
* counts by month and category

Keep labels and the scale visible.

### Missingness

Use completeness bars or a compact HTML/CSS missingness matrix when patterns of missing values matter.

Explore missingness by subgroup or time when missing values appear concentrated.

Avoid giant field-by-record missingness displays that communicate little beyond visual noise.

### Relationship / reconciliation summary

When comparing datasets, simple counts often work better than charts.

Example:

```text
142,318 transaction records

138,902 employee IDs matched       97.6%
  3,416 employee IDs unmatched      2.4%
```

If unmatched records are concentrated by time, source, category, or entity, visualize that concentration separately.

### Record-level evidence

Use a table when the important evidence is contained in individual records.

Examples:

* largest observed amounts
* duplicate key combinations
* records with unusual date combinations
* unmatched identifiers
* representative records behind a pattern

Do not label a table **Exceptions** unless an expectation has already been established.

Use titles such as:

* Records contributing to the observed pattern
* Largest recorded values
* Unmatched records
* Representative examples

Limit tables to enough records to support understanding. Do not dump thousands of rows into the HTML report.

## Chart.js guidance

Each chart should sit inside a fixed-height responsive container:

```html
<div class="chart-container">
  <canvas id="spendByDepartment"></canvas>
</div>
```

Create the chart with a small, explicit configuration:

```html
<script>
  new Chart(
    document.getElementById("spendByDepartment"),
    {
      type: "bar",
      data: {
        labels: ["Department A", "Department B", "Department C"],
        datasets: [{
          label: "Recorded spend",
          data: [482000, 361000, 294000],
          backgroundColor: "#4f46e5"
        }]
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            grid: {
              color: "#e2e8f0"
            }
          },
          y: {
            grid: {
              display: false
            }
          }
        }
      }
    }
  );
</script>
```

Keep configuration minimal.

Charts should have:

* meaningful labels
* clear units
* readable tick labels
* restrained gridlines
* useful tooltips
* legends only when multiple series require them

Do not repeat the observation title inside the chart when it already appears immediately above it.

### Preferred chart types

Use the core Chart.js types when possible:

* `bar`
* `line`
* `scatter`
* `doughnut` only for simple part-to-whole displays with very few categories

Prefer bars over doughnuts when ranking or precise comparison matters.

Do not add plugins simply to increase chart variety.

### Preparing chart data

Perform calculations before rendering the HTML.

For example, do not embed 150,000 transaction amounts into the page just to create a distribution.

Instead:

1. calculate appropriate bins during analysis
2. count the observations in each bin
3. pass the bin labels and counts to Chart.js

Likewise, aggregate time-series, category, and subgroup data before embedding it when record-level detail is not necessary.

The HTML report is the presentation layer, not the analytical engine.

### Shared defaults

Where useful, define restrained defaults once:

```html
<script>
  Chart.defaults.color = "#475569";
  Chart.defaults.font.family =
    'ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
  Chart.defaults.borderColor = "#e2e8f0";
</script>
```

Keep report-specific chart options close to the individual chart.

Do not build an elaborate chart abstraction framework inside the generated report.

## Areas for closer examination

End the analytical portion of the report with a short section titled:

# Areas for closer examination

This section synthesizes the questions or hypotheses that naturally follow from the exploration.

Each item should be grounded in an observation already shown in the report.

Good:

> **Understand the unmatched employee IDs.**
> 3,416 transaction records contain employee IDs that do not appear in the employee file. Determine whether this reflects population timing, terminated employees, contractor activity, identifier changes, or incomplete source data.

Good:

> **Understand the month-end increase in transaction volume.**
> Transaction volume is consistently higher during the final three business days of the month. Additional process context could determine whether this reflects normal reporting cycles or another operational pattern.

Avoid:

> Investigate employee fraud.

Avoid:

> Test whether management controls are ineffective.

Avoid:

> Audit high-risk departments.

The report has not established those conclusions.

Keep this section short. Prefer a handful of meaningful questions over a long list of every possible follow-up.

Do not assign risk ratings or recommendation strength.

## Analysis notes

End with a compact record of analytical choices that materially affect interpretation.

Include only relevant items such as:

* inferred field meanings
* inferred dataset grain
* parsing decisions
* type conversions
* excluded records
* filters
* normalization
* deduplication used for analytical purposes
* joins
* aggregation choices
* known data limitations
* assumptions

Example:

```text
Analysis notes

• `transaction_date` was parsed from MM/DD/YYYY text.
• 14 blank rows at the end of the Transactions sheet were ignored.
• Department names were trimmed for leading and trailing whitespace when calculating category counts; original values were preserved.
• Employee-to-transaction relationships were inferred using `employee_id`.
• No records were removed from the source files.
```

Do not clutter this section with every line of data-processing code.

The purpose is analytical traceability, not implementation documentation.

## Style guidance

### Analytical report, not dashboard

Use a lean editorial style.

The reader should naturally move through:

**overview → structure → profile → observations → closer examination**

Do not create a grid of KPI tiles followed by dozens of disconnected charts.

A few summary numbers at the top are useful. A dashboard aesthetic is not.

### Generous whitespace

Give charts and observations room to breathe.

Prefer:

```html
<section class="space-y-10">
```

and:

```html
<article class="rounded-xl border border-slate-200 bg-white p-6 space-y-6">
```

Avoid dense walls of cards.

### Restrained color

Use neutral stone/slate tones with one primary analytical accent such as indigo.

Suggested roles:

* **Slate / stone** — structure and neutral context
* **Indigo** — primary data
* **Amber** — uncertainty, assumptions, or limitations

Do not use red as the default color for:

* outliers
* missing values
* unmatched records
* rare values
* unusual distributions

Red implies adverse significance that exploratory analysis may not have established.

Use additional colors only when they encode meaningful categories or series.

### Typography

Use clear hierarchy.

Suggested pattern:

```html
<h1 class="text-3xl font-semibold tracking-tight">
<h2 class="text-xl font-semibold">
<h3 class="text-base font-semibold">
<p class="text-sm text-slate-600">
```

Use monospaced text for:

* field names
* file names
* sheet names
* literal category values where useful

Example:

```html
<code class="font-mono text-sm bg-slate-100 px-1.5 py-0.5 rounded">
  employee_id
</code>
```

### Numbers

Use consistent formatting.

* Include thousands separators.
* Use percentages when proportions are easier to understand than counts.
* Show the count alongside the percentage when the denominator matters.
* Use sensible decimal precision.
* Include currency symbols or units when known.
* Avoid false precision.

Prefer:

> 3,416 records (2.4%)

Over:

> 2.399786%

### Tables

Use tables when precise values matter.

Keep them visually light:

```html
<table class="w-full text-sm">
  <thead class="border-b border-slate-200 text-left text-slate-500">
  ...
  </thead>
  <tbody class="divide-y divide-slate-100">
  ...
  </tbody>
</table>
```

Right-align numeric values where practical.

Use horizontal scrolling for wide tables rather than shrinking text until it becomes unreadable.

### Chart height

Most charts should be approximately 320–420px tall.

Use more height only when additional vertical space materially improves readability.

Do not make charts enormous merely to fill the page.

## Analytical language

Maintain a strict distinction between what the data establishes and what the analyst infers.

### Use

Prefer analytical terms such as:

* observation
* pattern
* distribution
* relationship
* concentration
* variation
* outlier
* unusual value
* apparent
* hypothesis
* interpretation
* open question
* data characteristic
* data quality concern
* closer examination

### Avoid unless established

Do not casually use:

* finding
* exception
* violation
* deficiency
* failure
* control failure
* fraud
* fraud indicator
* root cause
* high risk
* noncompliance
* problematic
* suspicious

These terms imply conclusions beyond exploratory analysis.

### Observation vs. interpretation

Write:

> **Observation:** 61% of recorded spend is associated with 8% of employees.

Then, if useful:

> **Interpretation:** The concentration may reflect differences in job responsibilities or purchasing authority.

Do not collapse the two into:

> A small group of employees is responsible for excessive spending.

### Outliers

An outlier is an observation that is unusual relative to a defined distribution or comparison.

Do not use **outlier** as a synonym for error.

Prefer:

> Five transactions fall above the 99.9th percentile of recorded amounts.

Not:

> Five erroneous transactions were identified.

### Data quality

Describe the characteristic before assigning significance.

Prefer:

> `department` is blank for 8.7% of records, with most missing values concentrated in February and March 2025.

Not:

> Department data quality is poor.

The latter may eventually be justified, but the distribution alone does not establish it.

## Visualization anti-patterns

Do not use:

* pie or doughnut charts for high-cardinality categories
* word clouds
* 3D charts
* decorative gauges
* speedometers
* traffic-light indicators
* giant correlation matrices without a specific analytical purpose
* charts for identifiers
* charts merely because a field exists
* truncated axes that exaggerate differences without clearly indicating the truncation
* unexplained dual axes
* dozens of colors where a few will do
* red to make an observation look adverse
* anomaly scores without explaining what makes the records unusual
* arbitrary “top 10 anomalies” lists
* meaningless averages of identifiers or codes
* chart plugins added solely for novelty

Do not generate every possible chart and then choose among them.

Decide what question needs answering, then create the visual that answers it.

## Phrasings that fit the style

* “Recorded amounts are strongly right-skewed.”
* “Four categories account for 78% of total spend.”
* “Missing values are concentrated in two reporting periods.”
* “The apparent relationship is one employee to many transactions.”
* “Seven employee IDs appear in the transaction file but not the employee file.”
* “The largest recorded values occur primarily within two expense categories.”
* “Transaction volume rises near month-end.”
* “The pattern persists across 21 of 24 complete months.”
* “This may reflect normal process timing; additional context is needed.”
* “The data does not establish why the pattern occurs.”
* “This observation warrants closer examination, not an audit conclusion.”

Avoid throat-clearing.

Do not write:

> It is important to note that there appears to potentially be an interesting pattern in the data.

Write:

> Transaction volume rises near month-end.

Then explain the evidence.

## Final test

Before writing the report, ask of every section:

**Does this help the auditor understand the dataset?**

Before surfacing an observation:

**Can the reader see the evidence for it?**

Before offering an interpretation:

**Have I clearly separated it from what the data directly establishes?**

Before using adverse language:

**Has exploratory analysis actually established that conclusion?**

If not, describe the observation and leave the conclusion open.
