# Selecting and interpreting XLSX data

## Select one table

Inspect the workbook with `uv run "<skill directory>/scripts/profile_table.py" "<source.xlsx>" --inspect`. Use its worksheet inventory, Excel Table definitions, dimensions, and previews to identify the requested data. Previews are bounded samples; inspect additional cells when necessary to establish the table's boundaries. A worksheet's dimensions alone do not establish a table.

Honor a sheet, Table, or range the user already supplied. Otherwise select a single unambiguous rectangular table with one header row; ask the user when several plausible selections remain. Pass the selection explicitly when profiling and repeat it in the driver:

- `--table "Transactions"` selects a named Excel Table; `--sheet` may also constrain its worksheet.
- `--sheet "Transactions" --range B5:H800` selects a bounded range including its header row.
- `--sheet "Transactions"` discovers the occupied rectangle when the layout is simple. Multiple Tables, content outside a Table, blank separator rows, or repeated headers require an explicit selection. Large worksheet extents also require a Table or range.

Header names must be unique, nonblank text. Merged cells intersecting the selection and Tables without a header row are unsupported. Explain the specific obstruction and request a suitable range or values-only table. Reconstructing headers, joining blocks, and reshaping layouts are outside this version's scope.

An explicit range retains every data row inside it, including entirely blank rows. Automatic discovery trims unused space around the table. An Excel Table's declared totals row is excluded from record counts and disclosed in the report. Clarify suspected subtotal rows in ordinary ranges before choosing boundaries; a label such as “Total” alone is insufficient to remove a record.

Include hidden rows and columns and rows concealed by filters. The profile records visibility, overlapping filter ranges, and saved criteria; the Report discloses them. If the user requests only visible records, resolve a supported explicit data selection before proceeding.

## Enforce values-only scope

Formula cells inside the selected range stop profiling. For an Excel Table, this check includes its header and declared totals row, even though totals are excluded from analysis. Array and data-table formula ranges intersecting the selection also stop profiling, including when the formula anchor is outside it. Formulas elsewhere in the workbook do not prevent exploration of values-only data.

Identify the affected selection/cells and request values-only data or another selection. Reading saved formula results, recalculating formulas, and generating a values-only copy are outside this version's scope.

## Interpret cells

`raw` retains typed XLSX values, including text, numbers, booleans, dates, times, durations, missing cells, and error codes. Each profile field summarizes Excel cell types and non-General number formats with counts and examples. `raw.attrs["cells"]` lists the exceptions: the addresses of non-empty cells whose type or number format differs from their field's most common one, up to 100 per field. Review these alongside raw values before deciding roles.

- Preserve text identifiers exactly, including leading zeros. Analyze numeric values at their stored precision. Formatting such as `00000`, percentages, or currency is interpretation evidence; it does not authorize rounding, padding, or scaling. Resolve formatting that materially changes a field's meaning before calculating with it, and retain any agreed transformation in the driver.
- Native dates use the workbook's date system, recorded in `profile["source"]["date_epoch"]`. A date-format override applies to text cells; native dates retain their meaning. Numeric cells are not guessed to be date serials. Time-only values and durations remain distinct from calendar dates; establish their role and units before deriving measures from them.
- Typed Excel errors are invalid source values, distinct from blank cells and literal text such as `"#N/A"`. The profile counts `source_errors` separately, retains codes and cell addresses in `error_examples`, and masks errors in `data` for every role. Report these under Validity and explain their exclusion from calculations requiring valid values. Literal error-looking text follows the ordinary placeholder assessment.

For every field, `blank + source_errors + parse_failures + parsed == rows`. Entirely blank data rows remain in that denominator. Source record indexes begin at one after the header; worksheet row is `header_row + record`. The profile's `source`, samples, and failure/error examples retain worksheet coordinates. Use worksheet rows or cell addresses when identifying Excel records to the reader.
