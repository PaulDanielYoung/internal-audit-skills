# HTML Report Format

One self-contained HTML file in `<stem>-eda/report.html`. Tailwind and Chart.js come from CDNs; the data is inlined from `profile.json`. The page is static: the only scripts are the two CDN imports and the chart constructors.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Data profile: {{file name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
  </head>
  <body class="bg-stone-50 text-stone-900 font-sans">
    <main class="max-w-6xl mx-auto px-6 py-10 space-y-10">
      <header>...</header>
      <section id="headline">...</section>
      <section id="over-time">...</section>
      <section id="concentration">...</section>
      <section id="flags">...</section>
      <section id="fields">...</section>
    </main>
    <script>
      Chart.defaults.font.family = "system-ui, sans-serif";
      new Chart(document.getElementById("..."), {...});
    </script>
  </body>
</html>
```

## Sections, in order

**Header.** File name, path, rows × columns, when profiled. One line in monospace under the title. No introduction paragraph.

**Headline.** A row of stat tiles: rows, columns, period covered (from the primary date field), total of the primary amount field, duplicate rows, blank cells %. Each tile is a label in `text-xs uppercase tracking-wider text-stone-500` over a `text-2xl font-semibold` value.

**Over time.** Two cards side by side from `time_series`: records per month as a column chart, primary amount per month as a line. Skip the section when there is no date field.

**Concentration.** One card per entry in `crosstabs`: top ten values of a category by the primary amount, horizontal bars sorted high to low, an "Other" bar in grey at the end. Show count, sum, and share in the data table.

**Flags.** `dataset_flags` as a list, one line each, field name in monospace first, amber left border. Skip the section when the list is empty.

**Fields.** A two-column grid, one card per field in file order. Card header: field name, then `type · N distinct · N% blank`. Card body by type:

| Type | Show |
|---|---|
| number | histogram as a column chart; min, median, max, round-thousand count; first-digit vs Benford bars when `first_digit` is present |
| date | records per month as columns; records per weekday as columns with Saturday and Sunday in the second hue; range and weekend count |
| category, boolean | top values as horizontal bars |
| id | repeated values; `sequence.first` to `sequence.last` and the missing count when `sequence.contiguous`, else "not contiguous" |
| text | average and maximum length; top values |
| blank | "no values" |

Every card ends with the sample values in monospace and the field's flags, if any, as amber lines.

## Charts

- **Every chart carries its data table** in a `<details>` below it, so the numbers are readable and copyable.
- **One hue.** Bars and lines in `#2a78d6`. The second hue, `#eb6834`, marks only contrast within a chart: weekend bars, the Benford reference line. "Other" is `#c3c2b7`.
- **Bars over pies.** Categories are horizontal bars sorted by value. A donut only when the message is a share of a whole with five or fewer slices.
- **One axis per chart.** Counts and amounts get separate charts, never a second y-axis.
- Chart.js defaults give hover tooltips; keep them. Hide the legend for a single series; show it at the bottom for two.
- Rounded bar ends (`borderRadius: 4`), hairline gridlines (`#e1e0d9`) on the value axis only, muted tick labels (`#898781`).
- Heights: ~220px for the over-time and concentration charts, ~160px inside field cards, so two cards sit side by side without scrolling.

## Tone

Labels and titles use the field names as they appear in the file. Prose is sparse: a card needs no sentence if the chart and the numbers carry it. Observations belong in the conversation, not on the page.
