# HTML Report Format

The report is one self-contained HTML file, built by a per-run **driver** script that imports `scripts/report.py` and calls `write_report()`, which fills `assets/template.html`, writes a fresh file to the OS temp directory and opens it. Tailwind and Chart.js load from CDNs. The emitters carry the markup, so the driver holds analysis and content only.

The report is **editorial**: a narrative the auditor reads from overview → structure → field profile → observations → closer examination → analysis notes. The observation cards carry the argument. The page is static.

Every visual is **question-first**: it exists because it answers a named analytical question, and the reader can see the answer without reverse-engineering it. When a number or a small table answers the question better, use that instead.

## Driver

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas>=2.0", "openpyxl>=3.1"]
# ///
import json, sys
import pandas as pd

sys.path.insert(0, r"<skill base directory>/scripts")
import report as r

profile = json.load(open(r"<profile json path>", encoding="utf-8"))
df = pd.read_excel(r"expenses.xlsx", sheet_name="Transactions", header=2)

# exploration: slice, inspect records, bin and aggregate for each card
by_type = df.groupby("expense_type")["amount"].sum().sort_values(ascending=False)

sections = [
    r.header(profile, "Travel & Expense Transactions", grain="One row per expense line"),
    r.structure(profile),
    r.field_profile(profile, notes={"amount": "Strong right tail"}),
    r.section("observations", "Observations", "".join([
        r.card(
            "Four expense categories account for 78% of recorded spend",
            r.chart(by_type.index.tolist(), by_type.round().tolist(), horizontal=True, unit="$"),
            observation="Four of 17 categories account for 78% of recorded spend.",
            context=f"{r.fmt(len(df))} transactions, Jan 2024 to Jun 2026.",
            interpretation="The concentration may reflect the nature of travel spend rather than anything unusual.",
        ),
    ])),
    r.closer_examination([
        ("Understand the unmatched employee IDs",
         "3,416 transaction records carry employee IDs absent from the employee file. Determine whether this reflects population timing, terminated employees, contractor activity, identifier changes, or incomplete source data."),
    ]),
    r.analysis_notes(["Two title rows above the Transactions header were excluded.", "No records were removed from the source files."]),
]
print(r.write_report("Travel & Expense Transactions", sections))
```

The header row for `read_excel` is the `header_row` the profile recorded for that source.

## Sections

**Header.** `header(profile, title, grain, note, limitation)` renders the facts from the profile. Supply the apparent grain in words. The default interpretation note states that meanings and grain are inferred; replace it with a string when something is established, or pass `False` when everything is. A material limitation goes in `limitation` so it sits near the top.

**Structure.** `structure(profile, extra_html)` renders the sources table, apparent relationships with match counts, and the profiler's structural notes. A relationship display built by hand goes in `extra_html`, labeled with the connecting field and whether the relationship was validated or is apparent. An unmatched record is unmatched until the expected relationship has been established.

**Field profile.** `field_profile(profile, notes, roles)` renders one table per tabular source with an automatic note per field. `roles` corrects apparent roles the profiler got wrong; `notes` replaces the automatic note where the field deserves a better one. Category values beyond the most common few belong in an observation card, not this table.

**Observations.** `section("observations", "Observations", cards)` where each kept pattern is one `card()`, ordered by how much it explains the data rather than how dramatic it looks. The visual carries the weight; prose says what the visual establishes and gives the context to read it. Elements, used as the observation needs them:

* **Title** states what the data shows. "Travel spend is concentrated among 14 departments", rather than "Concerning departmental concentration".
* **Observation** is what the data directly supports. "Transactions in the final three business days of each month average 1.8× the daily volume of the rest of the month."
* **Context** is the denominator, period, population, or comparison group that keeps ordinary variation from looking meaningful. "312 of 4,291 employees account for 50% of recorded spend." "The pattern appears in 21 of 24 complete months." "Excludes 117 transactions with missing dates."
* **Interpretation** is optional and stated as a possibility. "The concentration may reflect centralized purchasing, department size, or both."
* **Open question** appears only when more information would materially change the interpretation. "Are these departments expected to purchase centrally on behalf of other units?"

**Areas for closer examination.** `closer_examination(items)` takes a handful of (heading, body) pairs, each grounded in an observation already shown and each phrased as something to understand:

> **Understand the month-end increase in transaction volume.**
> Transaction volume is consistently higher during the final three business days of the month. Additional process context could determine whether this reflects normal reporting cycles or another operational pattern.

**Analysis notes.** `analysis_notes(notes)` takes one line per choice that affects interpretation: inferred meanings and grain, parsing decisions, type conversions, excluded records, filters, normalization, deduplication, joins, aggregation choices, known limitations, assumptions. The profiler's own notes are already in the structure section. Processing code stays out.

## Visualization patterns

Choose the call from the question, so different observations look different.

| Question | Call | Judgement the agent makes |
| --- | --- | --- |
| How is this measure distributed? | `chart(bin_labels, counts)` | Bin during analysis. For skewed data, choose readable bins, show a percentile range with extremes disclosed beside it, or pass `log=True`. Extreme values stay in the analysis; when a chart's range cuts them off, say so next to the chart. |
| Which categories carry the measure? | `chart(labels, values, horizontal=True)` | Sort descending. For high cardinality, show the relevant top categories and group the rest as **Other**, stating that categories were grouped. |
| How does this behave over time? | `chart(periods, values, kind="line")`, or `kind="bar"` for discrete totals | Pick the aggregation level (daily, weekly, monthly) that shows the pattern most clearly. |
| How does the mix change over time? | `chart(periods, [{"label", "data"}, ...], kind="stacked")` | Reserved for when the changing composition is itself the question, with a few meaningful groups aggregated first. |
| How do two measures relate? | `chart(None, [{"label", "data": [{"x", "y"}, ...]}], kind="scatter")` | A scatter shows association; causation belongs in the open question. Sample large populations before plotting. |
| How does a measure differ across groups? | `chart(groups, [{"label": "Median", "data"}, ...])` or `table()` | Grouped bars of medians or percentile ranges, or a summary table. |
| How does activity spread across two dimensions? | `heatmap(row_labels, col_labels, values)` | Small grids only, such as weekday × hour or field × period. |
| Where are the gaps? | `completeness_bar(share)` or `heatmap()` by field and period | Explore missingness by subgroup or time when it appears concentrated. |
| How do two datasets line up? | `reconciliation(total_label, total, parts)` | Plain counts. Visualize any concentration of unmatched records separately. |
| Which records make the pattern? | `table(columns, rows, title)` | Enough records to support understanding. Title by what it shows: "Records contributing to the observed pattern", "Largest recorded values", "Unmatched records", "Representative examples". |
| Anything else | raw HTML in the card body | Relationship diagrams and bespoke visuals, using the same Tailwind classes the emitters use. |

## Style

**Color.** The emitters use neutral stone and slate for structure, indigo for all data including outliers, missing values, unmatched records and rare values, and amber for uncertainty, assumptions and limitations. Additional series colors appear only where they encode meaningful categories. Red is reserved for adverse significance that exploration has established, which in practice means it is absent.

**Numbers.** `fmt()` and `pct()` handle separators and precision. The judgement is to show the count beside the percentage when the denominator matters, "3,416 records (2.4%)", and to pass the unit when it is known.

**Chart height.** The default is 360px. Pass `height` only when more room materially improves readability.

## Language

Prose keeps what the data establishes separate from what the analyst infers, using the observation, interpretation and open question labels from the process.

An **outlier** is unusual relative to a defined distribution or comparison: "Five transactions fall above the 99.9th percentile of recorded amounts."

A data-quality characteristic is described before any significance is assigned: "`department` is blank for 8.7% of records, with most missing values concentrated in February and March 2025."

Sentences lead with the observation: "Transaction volume rises near month-end." Then the evidence.
