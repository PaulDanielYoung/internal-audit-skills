# HTML Report Format

The report is one self-contained HTML file. Tailwind (CDN) handles layout and style. Chart.js (CDN) renders charts. Hand-built HTML and CSS handle everything simpler than a chart: completeness bars, summary numbers, badges, schema cards, small tables, small grids.

The report is **editorial**: a narrative the auditor reads from overview → structure → field profile → observations → closer examination → analysis notes. A few summary numbers at the top orient the reader; the observation cards carry the argument. The page is static, and its JavaScript is limited to Chart.js rendering.

Every visual is **question-first**: it exists because it answers a named analytical question, and the reader can see the answer without reverse-engineering it. When a number or a small table answers the question better, use that instead.

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
    <script>
      Chart.defaults.color = "#475569";
      Chart.defaults.font.family =
        'ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
      Chart.defaults.borderColor = "#e2e8f0";
    </script>

    <style>
      body { -webkit-font-smoothing: antialiased; }
      .chart-container { position: relative; width: 100%; height: 360px; }
      .numeric { font-variant-numeric: tabular-nums; }
      .scroll-table { overflow-x: auto; }
    </style>
  </head>

  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-6xl mx-auto px-6 py-12 space-y-14">

      <header id="overview">
        <h1 class="text-3xl font-semibold tracking-tight">...</h1>
      </header>

      <section id="structure">
        <h2 class="text-xl font-semibold">...</h2>
      </section>

      <section id="field-profile">
        ...
      </section>

      <section id="observations" class="space-y-10">
        <article class="rounded-xl border border-slate-200 bg-white p-6 space-y-6">
          <h3 class="text-base font-semibold">...</h3>
          <p class="text-sm text-slate-600">...</p>
        </article>
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

Field names, file names, sheet names, and literal category values render in monospace:

```html
<code class="font-mono text-sm bg-slate-100 px-1.5 py-0.5 rounded">employee_id</code>
```

Tables stay visually light, with numeric columns right-aligned and wide tables wrapped in `.scroll-table`:

```html
<table class="w-full text-sm">
  <thead class="border-b border-slate-200 text-left text-slate-500">...</thead>
  <tbody class="divide-y divide-slate-100">...</tbody>
</table>
```

## Header

Open with the facts the reader needs to orient, and go directly into the dataset:

* Dataset or analysis name
* Generation date
* Source files, sheets, tables, or objects
* Row count and field count
* Coverage period, when identifiable
* Apparent grain, when identifiable

```text
Travel & Expense Transactions

142,318 rows · 27 fields · Jan 2024–Jun 2026

Sources
expenses.xlsx / Transactions
employees.csv

Apparent grain
One row per expense line
```

When meanings, grain, or relationships are apparent rather than established, add a compact note:

> **Interpretation note:** Field meanings and dataset grain are inferred from names, values, and relationships unless otherwise stated.

A material limitation belongs here, near the top, rather than in the analysis notes alone.

## Data structure

Explain how the dataset is organized before discussing patterns within it.

For a single flat dataset, use a compact schema or grouped field summary.

For multiple sources, show each source with its apparent purpose, row and field counts, apparent key fields, and apparent relationships to the other sources. Relate sources only where the data connects them.

Simple relationships work as hand-built HTML cards and arrows, labeled with the connecting field and whether the relationship was validated or is apparent:

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

When joins were tested, show matched records, unmatched records, duplicate keys, and the apparent cardinality (one-to-one, one-to-many, many-to-many). An unmatched record is unmatched until the expected relationship has been established.

## Field profile

A compact reference for the important fields, holding the metrics that explain each field's role. Category values beyond the most common few are summarized here and explored in their own observation card.

Default table:

| Field          | Apparent role | Coverage | Distinct | Range / common values  | Note                         |
| -------------- | ------------- | -------: | -------: | ---------------------- | ---------------------------- |
| `employee_id`  | Identifier    |     100% |    4,291 | —                      | Repeats across transactions  |
| `expense_date` | Date          |    99.9% |      812 | Jan 2024–Jun 2026      | 117 missing                  |
| `amount`       | Measure       |    99.8% |        — | -420 to 18,330         | Strong right tail            |
| `expense_type` | Category      |     100% |       17 | Airfare 31%, Hotel 24% | Concentrated in 4 categories |

Show completeness visually when it helps explain the dataset. A horizontal bar in the primary accent is enough; missingness is a characteristic, and the color stays neutral until its significance is understood:

```html
<div class="w-full bg-slate-100 rounded-full h-2">
  <div class="bg-indigo-500 h-2 rounded-full" style="width: 97.4%"></div>
</div>
```

## Observation cards

The observation card is the main analytical unit. Each kept pattern is one `<article>`, ordered by how much it explains the data rather than how dramatic it looks. The visual carries the weight; prose says what the visual establishes and gives the context to read it.

Elements, used as the observation needs them:

* **Title**: states what the data shows. "Travel spend is concentrated among 14 departments", rather than "Concerning departmental concentration".
* **Observation**: what the data directly supports. "Transactions in the final three business days of each month average 1.8× the daily volume of the rest of the month."
* **Visual**: the chart, number, or table that shows the observation directly.
* **Context**: the denominator, period, population, or comparison group that keeps ordinary variation from looking meaningful. "312 of 4,291 employees account for 50% of recorded spend." "The pattern appears in 21 of 24 complete months." "Excludes 117 transactions with missing dates."
* **Interpretation**: optional, and stated as a possibility. "**Interpretation:** The concentration may reflect centralized purchasing, department size, or both."
* **Open question**: only when more information would materially change the interpretation. "**Open question:** Are these departments expected to purchase centrally on behalf of other units?"

## Visualization patterns

Choose the visual from the question, so different observations look different.

### Distribution

*How is this numeric measure distributed?* A histogram-style bar chart: bin the population during analysis and pass bin labels and counts.

```text
$0–$100        4,218
$100–$250      7,914
$250–$500      3,108
$500–$1,000    1,142
$1,000+          428
```

For heavily skewed data, choose bins that make the distribution readable, show a meaningful percentile range in the primary chart with the extremes disclosed beside it, or use a logarithmic axis. Extreme values stay in the analysis; when a chart's range cuts them off, say so next to the chart.

### Ranked bars

*Which categories carry the measure?* Horizontal bars sorted descending by the measure. For high-cardinality categories, show the relevant top categories and group the remainder as **Other**, stating that categories were grouped.

### Time series

*How does this behave over time?* A line chart when continuity and direction matter, bars when periods are discrete totals. Pick the aggregation level (daily, weekly, monthly) that communicates the pattern most clearly.

### Composition over time

*How does the mix change?* Stacked bars, reserved for when the changing composition is itself the question, with a few meaningful groups aggregated first.

### Scatter

*How do two numeric measures relate?* The native Chart.js `scatter` type. A scatter shows association; causation belongs in the open question. When a relationship is summarized numerically, say what the metric represents.

### Group comparison

*How does a measure differ across groups?* Grouped bars of medians, percentile ranges, small multiples of distribution charts, or a summary table, all within core Chart.js.

### Heatmap-style grid

*How does activity spread across two dimensions?* For a small grid such as weekday × hour or field × period, a hand-built HTML/CSS grid with visible labels and scale.

### Missingness

*Where are the gaps?* Completeness bars, or a compact HTML/CSS matrix by field and period or subgroup when missing values appear concentrated.

### Reconciliation summary

*How do two datasets line up?* Plain counts, with any concentration of unmatched records visualized separately.

```text
142,318 transaction records

138,902 employee IDs matched       97.6%
  3,416 employee IDs unmatched      2.4%
```

### Record-level evidence

*Which records make the pattern?* A table of enough records to support understanding: largest values, duplicate key combinations, unusual date combinations, unmatched identifiers, representative examples. Title the table by what it shows, such as "Records contributing to the observed pattern", "Largest recorded values", "Unmatched records", or "Representative examples".

## Chart.js

Each chart sits in a fixed-height responsive container, 320–420px tall unless more height materially improves readability:

```html
<div class="chart-container">
  <canvas id="spendByDepartment"></canvas>
</div>
```

Configure each chart explicitly and locally, with a legend only when multiple series need one, and the observation title left to the card heading above:

```html
<script>
  new Chart(document.getElementById("spendByDepartment"), {
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
      plugins: { legend: { display: false } },
      scales: {
        x: { beginAtZero: true, grid: { color: "#e2e8f0" } },
        y: { grid: { display: false } }
      }
    }
  });
</script>
```

Core types cover the report: `bar`, `line`, `scatter`, and `doughnut` for a simple part-to-whole display with very few categories. Bars carry any ranking or precise comparison.

Chart data arrives pre-aggregated from the analysis: bins and counts, period totals, category sums. Record-level detail is embedded only where a table needs it.

## Areas for closer examination

The analytical portion ends with a short section titled **Areas for closer examination**: a handful of questions or hypotheses, each grounded in an observation already shown in the report, each phrased as something to understand.

> **Understand the unmatched employee IDs.**
> 3,416 transaction records contain employee IDs that do not appear in the employee file. Determine whether this reflects population timing, terminated employees, contractor activity, identifier changes, or incomplete source data.

> **Understand the month-end increase in transaction volume.**
> Transaction volume is consistently higher during the final three business days of the month. Additional process context could determine whether this reflects normal reporting cycles or another operational pattern.

## Analysis notes

Close with a compact record of the choices that affect interpretation: inferred field meanings and grain, parsing decisions, type conversions, excluded records, filters, normalization, deduplication, joins, aggregation choices, known limitations, assumptions. The purpose is traceability, so each note is one line, and the processing code stays out.

```text
Analysis notes

• `transaction_date` was parsed from MM/DD/YYYY text.
• 14 blank rows at the end of the Transactions sheet were ignored.
• Department names were trimmed for leading and trailing whitespace when calculating category counts; original values were preserved.
• Employee-to-transaction relationships were inferred using `employee_id`.
• No records were removed from the source files.
```

## Style

**Whitespace.** Sections use `space-y-10` and cards use `p-6 space-y-6`, so charts and observations have room to breathe.

**Color.** Neutral stone and slate for structure, one primary accent for data, amber for uncertainty, assumptions, and limitations:

* **Slate / stone**: structure and neutral context
* **Indigo**: primary data, including outliers, missing values, unmatched records, and rare values
* **Amber**: uncertainty, assumptions, or limitations

Additional colors appear only where they encode meaningful categories or series. Red is reserved for adverse significance that exploration has established, which in practice means it is absent.

**Numbers.** Thousands separators, currency symbols or units when known, sensible precision, and the count beside the percentage when the denominator matters: "3,416 records (2.4%)".

## Language

Prose keeps what the data establishes separate from what the analyst infers, using the observation, interpretation, and open question labels from the process.

An **outlier** is unusual relative to a defined distribution or comparison: "Five transactions fall above the 99.9th percentile of recorded amounts."

A data-quality characteristic is described before any significance is assigned: "`department` is blank for 8.7% of records, with most missing values concentrated in February and March 2025."

Sentences lead with the observation: "Transaction volume rises near month-end." Then the evidence.
