"""Read one source table without changing the file or reshaping its records."""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

# Cells listed per field whose type or number format differs from the field's usual one.
CELL_EXCEPTIONS_MAX = 100


@dataclass
class SourceTable:
    raw: pd.DataFrame
    source: dict
    errors: pd.DataFrame
    formats: dict
    cell_types: dict
    cell_metadata: dict = field(default_factory=dict)

    def location(self, record: int, field: str | None = None) -> dict:
        if self.source["format"] == "csv":
            return {"record": int(record)}
        from openpyxl.utils import get_column_letter

        row = self.source["header_row"] + int(record)
        result = {"record": int(record), "sheet": self.source["sheet"], "row": row}
        if field is not None:
            column = self.source["first_column"] + self.raw.columns.get_loc(field)
            result["cell"] = f"{get_column_letter(column)}{row}"
        return result


def read_csv(path: Path, encoding: str = "utf-8-sig") -> SourceTable:
    records, skipped = [], 0
    with path.open(encoding=encoding, newline="") as stream:
        reader = csv.reader(stream, strict=True)
        header = next(reader, None)
        if not header or any(not name.strip() for name in header):
            raise ValueError("The first CSV record must contain non-empty field names.")
        if len(set(header)) != len(header):
            raise ValueError("CSV field names must be unique; duplicate headers need clarification.")
        for record in reader:
            if not record:
                skipped += 1
                continue
            if len(record) != len(header):
                raise ValueError(
                    f"CSV record ending on line {reader.line_num} has {len(record)} fields; "
                    f"the header has {len(header)}. Check delimiters and quoting."
                )
            records.append(record)
    raw = pd.DataFrame(records, columns=header, dtype="string")
    raw.index = pd.RangeIndex(1, len(raw) + 1, name="record")
    return SourceTable(raw, {"format": "csv", "empty_lines_skipped": skipped},
                       pd.DataFrame(False, index=raw.index, columns=raw.columns), {}, {})


def _bounds(reference: str) -> tuple[int, int, int, int]:
    from openpyxl.utils import range_boundaries

    try:
        bounds = range_boundaries(reference.upper())
        left, top, right, bottom = bounds
        if (any(value is None for value in bounds) or not 1 <= left <= right <= 16384
                or not 1 <= top <= bottom <= 1048576):
            raise ValueError()
    except (ValueError, TypeError):
        raise ValueError("Use a bounded cell range including its header, such as B5:H800.") from None
    return bounds


def _intersects(first, second) -> bool:
    return not (first[2] < second[0] or second[2] < first[0]
                or first[3] < second[1] or second[3] < first[1])


def _reference(bounds) -> str:
    from openpyxl.utils import get_column_letter

    left, top, right, bottom = bounds
    return f"{get_column_letter(left)}{top}:{get_column_letter(right)}{bottom}"


def _open_workbook(path: Path):
    from openpyxl import load_workbook

    # Formula expressions must remain visible, including formulas without caches.
    return load_workbook(path, data_only=False, keep_links=False)


def inspect_xlsx(path: str | Path) -> dict:
    """List sheets, Tables and small value previews; make no selection."""
    workbook = _open_workbook(Path(path))
    try:
        sheets = []
        for sheet in workbook.worksheets:
            bounds = _bounds(sheet.calculate_dimension())
            left, top, right, bottom = bounds
            sheets.append({
                "sheet": sheet.title, "state": sheet.sheet_state,
                "dimensions": sheet.calculate_dimension(),
                "tables": [{"name": table.name, "range": table.ref,
                            "header_rows": table.headerRowCount,
                            "totals_rows": table.totalsRowCount or 0}
                           for table in sheet.tables.values()],
                "preview": [[str(cell.value) if cell.value is not None else None for cell in row]
                            for row in sheet.iter_rows(min_row=top, max_row=min(bottom, top + 5),
                                                       min_col=left, max_col=min(right, left + 11))],
            })
        return {"file": Path(path).name, "sheets": sheets}
    finally:
        workbook.close()


def read_xlsx(path: Path, *, sheet: str | None, table: str | None,
              cell_range: str | None) -> SourceTable:
    if table and cell_range:
        raise ValueError("Select an Excel Table or a cell range, not both.")
    workbook = _open_workbook(path)
    try:
        if sheet and sheet not in workbook.sheetnames:
            raise ValueError(f"Unknown worksheet {sheet!r}; use --inspect to list worksheets.")
        selected_table = None
        if table:
            matches = [(ws, ws.tables[table]) for ws in workbook.worksheets
                       if (not sheet or ws.title == sheet) and table in ws.tables]
            if len(matches) != 1:
                raise ValueError(f"Table {table!r} is not uniquely available; use --inspect.")
            worksheet, selected_table = matches[0]
        elif sheet:
            worksheet = workbook[sheet]
        elif len(workbook.worksheets) == 1:
            worksheet = workbook.worksheets[0]
        else:
            raise ValueError("Several worksheets are available; select --sheet or --table after --inspect.")

        automatic = not table and not cell_range
        if automatic and len(worksheet.tables) > 1:
            raise ValueError("Several Tables are available; select --table or --range after --inspect.")
        if selected_table:
            bounds = _bounds(selected_table.ref)
        elif cell_range:
            bounds = _bounds(cell_range)
        else:
            extent = _bounds(worksheet.calculate_dimension())
            if (extent[2] - extent[0] + 1) * (extent[3] - extent[1] + 1) > 2_000_000:
                raise ValueError("Worksheet extent is too large for automatic discovery; select --table or --range.")
            occupied = [cell for row in worksheet.iter_rows() for cell in row if cell.value is not None]
            if not occupied:
                raise ValueError("The worksheet is empty; a header row is required.")
            bounds = (min(c.column for c in occupied), min(c.row for c in occupied),
                      max(c.column for c in occupied), max(c.row for c in occupied))
            if worksheet.tables:
                candidate = next(iter(worksheet.tables.values()))
                if _bounds(candidate.ref) != bounds:
                    raise ValueError("Content exists outside the Excel Table; select --table or --range explicitly.")
                selected_table = candidate

        left, top, right, bottom = bounds
        totals = 0
        if selected_table:
            if selected_table.headerRowCount != 1:
                raise ValueError("The selected Table must have exactly one header row.")
            totals = selected_table.totalsRowCount or 0
            if totals not in (0, 1) or bottom - totals < top:
                raise ValueError("The selected Table has unsupported totals-row metadata.")
        for merged in worksheet.merged_cells.ranges:
            if _intersects(bounds, merged.bounds):
                raise ValueError(f"Merged cells {merged} intersect the selection; select a rectangular table with one header row.")

        # Array/data-table formula anchors can be outside the selected range.
        formula_ranges = dict(worksheet.array_formulae)
        # openpyxl exposes array_formulae but not data-table formula ranges. Its
        # sparse cell store avoids scanning a million styled-but-empty rows here.
        for cell in worksheet._cells.values():
            if cell.data_type == "f" and hasattr(cell.value, "ref"):
                formula_ranges[cell.coordinate] = cell.value.ref
        for address, reference in formula_ranges.items():
            if _intersects(bounds, _bounds(reference)):
                raise ValueError(f"Formula range {reference} (anchor {address}) intersects the selection; formulas are out of scope.")
        cells = list(worksheet.iter_rows(min_row=top, max_row=bottom, min_col=left, max_col=right))
        body = cells[1:len(cells) - totals] if totals else cells[1:]
        # One pass over the body reads each cell's value, type and number format once.
        width = right - left + 1
        values, error_flags, body_formulas = [], [], []
        types = [{} for _ in range(width)]
        formats = [{} for _ in range(width)]
        styles = [{} for _ in range(width)]  # (type, number format) counts of non-empty cells
        for row in body:
            row_values, row_errors = [], []
            for offset, cell in enumerate(row):
                kind, value, number_format = cell.data_type, cell.value, cell.number_format
                if kind == "f":
                    body_formulas.append(cell.coordinate)
                row_values.append(value)
                row_errors.append(kind == "e")
                types[offset][kind] = types[offset].get(kind, 0) + 1
                if value is not None:
                    style = styles[offset]
                    style[kind, number_format] = style.get((kind, number_format), 0) + 1
                    if number_format != "General":
                        group = formats[offset].setdefault(number_format, {"count": 0, "examples": []})
                        group["count"] += 1
                        if len(group["examples"]) < 5:
                            group["examples"].append({"cell": cell.coordinate, "value": str(value)})
            values.append(row_values)
            error_flags.append(row_errors)
        edge_rows = [cells[0], *cells[len(cells) - totals:]] if totals else [cells[0]]
        formulas = [cell.coordinate for row in edge_rows for cell in row if cell.data_type == "f"] + body_formulas
        if formulas:
            raise ValueError(f"Formulas are out of scope in {worksheet.title!r}: {', '.join(formulas[:10])}. Provide values-only data.")
        if selected_table and any(column.calculatedColumnFormula is not None or column.totalsRowFormula is not None
                                  for column in selected_table.tableColumns):
            raise ValueError("The selected Table declares formulas; provide values-only data.")
        header = [cell.value for cell in cells[0]]
        if (any(not isinstance(name, str) or not name.strip() for name in header)
                or len({name.strip() for name in header}) != len(header)
                or any(cell.data_type == "e" for cell in cells[0])):
            raise ValueError("The selected header must contain unique, nonblank text field names.")
        if automatic and selected_table is None:
            if any(all(value is None for value in row) for row in values):
                raise ValueError("Blank rows make table boundaries ambiguous; confirm an explicit --range.")
            if any(row == header for row in values):
                raise ValueError("Repeated headers suggest multiple blocks; select one table with --range.")
        raw = pd.DataFrame(values, columns=header, dtype=object)
        raw.index = pd.RangeIndex(1, len(raw) + 1, name="record")
        errors = pd.DataFrame(error_flags, index=raw.index, columns=header, dtype=bool)
        # Keep addresses only for non-empty cells whose type or number format differs from
        # their column's most common one; the per-field summaries cover the rest.
        cell_metadata = {}
        for offset, style in enumerate(styles):
            if len(style) < 2:
                continue
            usual = max(style, key=style.get)
            listed = 0
            for row in body:
                cell = row[offset]
                if cell.value is not None and (cell.data_type, cell.number_format) != usual:
                    cell_metadata[cell.coordinate] = {"type": cell.data_type, "number_format": cell.number_format}
                    listed += 1
                    if listed == CELL_EXCEPTIONS_MAX:
                        break
        formats = dict(zip(header, formats))
        types = dict(zip(header, types))
        hidden_rows = [row for row in range(top + 1, bottom - totals + 1)
                       if worksheet.row_dimensions.get(row) and worksheet.row_dimensions[row].hidden]
        hidden_columns = []
        for dimension in worksheet.column_dimensions.values():
            if dimension.hidden:
                hidden_columns.extend(range(max(left, dimension.min or left),
                                            min(right, dimension.max or right) + 1))
        filters = []
        for autofilter in [worksheet.auto_filter, *[item.autoFilter for item in worksheet.tables.values()]]:
            if autofilter and autofilter.ref and _intersects(bounds, _bounds(autofilter.ref)):
                filters.append({"range": autofilter.ref, "criteria_present": bool(autofilter.filterColumn)})
        source = {
            "format": "xlsx", "sheet": worksheet.title, "sheet_state": worksheet.sheet_state,
            "range": _reference(bounds), "table": selected_table.name if selected_table else None,
            "header_row": top, "first_column": left, "last_data_row": bottom - totals,
            "totals_rows_excluded": list(range(bottom - totals + 1, bottom + 1)),
            "hidden_rows_included": hidden_rows, "hidden_columns_included": sorted(set(hidden_columns)),
            "filters": filters, "date_epoch": workbook.epoch.isoformat(),
        }
        return SourceTable(raw, source, errors, formats, types, cell_metadata)
    finally:
        workbook.close()


def read_table(path: Path, *, encoding: str = "utf-8-sig", sheet: str | None = None,
               table: str | None = None, cell_range: str | None = None) -> SourceTable:
    if path.suffix.lower() == ".csv":
        if sheet or table or cell_range:
            raise ValueError("Worksheet, Table and range selections apply only to XLSX files.")
        return read_csv(path, encoding)
    if path.suffix.lower() == ".xlsx":
        return read_xlsx(path, sheet=sheet, table=table, cell_range=cell_range)
    raise ValueError("Provide one .csv or .xlsx file.")
