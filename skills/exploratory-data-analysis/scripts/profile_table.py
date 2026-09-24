# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas>=2.0,<4", "openpyxl>=3.1.5,<4"]
# ///
"""Profile one CSV or selected XLSX table, without modifying it.

CLI: uv run profile_table.py FILE [--sheet NAME] [--table NAME | --range B5:H800]
     uv run profile_table.py FILE.xlsx --inspect
Library: raw, data, profile = profile_table(path, sheet=..., cell_range=...)

raw retains CSV strings or typed XLSX values; data contains interpreted values.
Both use one-based data-record indexes (not physical line numbers). Blank cells
and failed conversions are counted separately. Inferred roles cover plain numbers,
ISO dates, and whole-number year or month fields named as such. Other date formats
require an explicit format; a field whose values fit one gets a date_format_hint
listing every format that fits. Fields list possible_placeholders (values such as
R-000000, 99999, --, UNKNOWN), and entity_fields names the fields that never vary
within a repeating identifier.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import re
import tempfile
import sys
from pathlib import Path
from zipfile import BadZipFile

import pandas as pd

sys.dont_write_bytecode = True
from table_source import read_table, inspect_xlsx

# A strong majority can suggest a type without hiding the remaining bad values.
# These are profiling heuristics, not audit thresholds; explicit roles override them.
PARSE_THRESHOLD = 0.95
ROLES = {"identifier", "measure", "category", "date", "year", "month", "text"}
ID_NAME = re.compile(r"(^|[^a-z])(id|key|code|number|no|ref|reference)$", re.I)
ISO_DATE = r"\d{4}-\d{2}-\d{2}"
# Date parts are labels, not quantities: name words that suggest one, and its expected
# range. Values outside the range are counted in the profile, not rejected.
DATE_PARTS = {
    "year": ({"year", "yr", "fy"}, (1800, 2100)),
    "month": ({"month", "mon", "mo"}, (1, 12)),
}
# Non-ISO date formats offered as hints, each with the shape its values must have.
DATE_HINTS = [
    ("%m/%d/%Y", r"\d{1,2}/\d{1,2}/\d{4}"),
    ("%d/%m/%Y", r"\d{1,2}/\d{1,2}/\d{4}"),
    ("%m/%d/%y", r"\d{1,2}/\d{1,2}/\d{2}"),
    ("%d/%m/%y", r"\d{1,2}/\d{1,2}/\d{2}"),
    ("%m-%d-%Y", r"\d{1,2}-\d{1,2}-\d{4}"),
    ("%d-%m-%Y", r"\d{1,2}-\d{1,2}-\d{4}"),
    ("%d.%m.%Y", r"\d{1,2}\.\d{1,2}\.\d{4}"),
    ("%Y/%m/%d", r"\d{4}/\d{1,2}/\d{1,2}"),
]
# Values that often stand in for a missing one: runs of zeros or nines with an optional
# short prefix (R-000000, 99999), dashes, question marks, and common missing-value words.
PLACEHOLDER = re.compile(
    r"[a-z]{0,3}[-\s]?(0{3,}|9{3,})(\.0+)?|-+|\?+|#?n/?a|null|nil|unknown|unk|tbd|tba",
    re.I,
)
# An identifier describes entities when at least this share of its records repeat a key.
ENTITY_MIN_REPEATED = 0.1


def blank_cells(values: pd.Series) -> pd.Series:
    """Source blanks include absent XLSX cells and empty/whitespace text."""
    return values.map(lambda value: value is None or value is pd.NA
                      or (isinstance(value, str) and not value.strip()))


def text_values(values: pd.Series) -> pd.Series:
    """A parsing view; raw values retain their original types."""
    return values.map(lambda value: None if pd.isna(value) else str(value)).astype("string")


def native_date(value) -> bool:
    return isinstance(value, (dt.datetime, dt.date)) and not pd.isna(value)


def parse_dates(values: pd.Series, date_format: str | None) -> pd.Series:
    """Formats apply to text only; numeric cells are never guessed to be serial dates."""
    strings = text_values(values.where(values.map(lambda value: isinstance(value, str)))).str.strip()
    parsed = pd.to_datetime(strings, format=date_format or "%Y-%m-%d", errors="coerce")
    if date_format is None:
        parsed = parsed.where(strings.str.fullmatch(ISO_DATE).fillna(False))
    dates = values.map(native_date)
    if dates.any():
        parsed.loc[dates] = pd.to_datetime(values[dates], errors="coerce")
    return parsed


def numeric(values: pd.Series) -> pd.Series:
    """Parse plain decimal/scientific notation; exclude non-finite values."""
    parsed = pd.to_numeric(values, errors="coerce")
    finite = parsed.map(lambda value: pd.notna(value) and math.isfinite(float(value)))
    return parsed.where(finite)


def in_range(parsed: pd.Series, part: str) -> pd.Series:
    """Whole numbers within the date part's expected range; missing values are False."""
    low, high = DATE_PARTS[part][1]
    return (parsed.between(low, high) & parsed.eq(parsed.round())).fillna(False)


def date_format_hint(values: pd.Series) -> list[str]:
    """Every non-ISO format that parses a strong majority of the present values. More
    than one (such as month-first and day-first) means the order is unresolved."""
    present = values.dropna().str.strip()
    fits = []
    for date_format, shape in DATE_HINTS:
        matches = present.str.fullmatch(shape)
        if present.empty or matches.mean() < PARSE_THRESHOLD:
            continue
        parsed = pd.to_datetime(present[matches], format=date_format, errors="coerce")
        if parsed.notna().sum() / len(present) >= PARSE_THRESHOLD:
            fits.append(date_format)
    return fits


def infer_role(values: pd.Series, name: str) -> str:
    present = values.dropna()
    if present.empty:
        return "empty"
    words = re.sub(r"([a-z])([A-Z])", r"\1_\2", name)
    if ID_NAME.search(words) or present.str.fullmatch(r"0\d+").any():
        return "identifier"
    if present.str.fullmatch(ISO_DATE).mean() >= PARSE_THRESHOLD:
        return "date"
    parsed = numeric(present.str.strip())
    if parsed.notna().mean() >= PARSE_THRESHOLD:
        name_words = set(re.split(r"[^a-z0-9]+", words.lower()))
        for part, (part_words, _) in DATE_PARTS.items():
            if name_words & part_words and in_range(parsed, part).mean() >= PARSE_THRESHOLD:
                return part
        return "measure"
    # Low-cardinality text gets frequency summaries; this never changes its values.
    if present.nunique() <= 20 or present.nunique() / len(present) <= 0.1:
        return "category"
    return "text"


def possible_placeholders(values: pd.Series) -> dict | None:
    """Count and most frequent values that look like stand-ins for a missing value."""
    present = values.dropna().str.strip()
    matches = present[present.str.fullmatch(PLACEHOLDER)]
    if matches.empty:
        return None
    return {
        "count": int(len(matches)),
        "values": [{"value": str(value), "count": int(count)} for value, count in matches.value_counts().head(5).items()],
    }


def entity_fields(raw: pd.DataFrame, identifiers: list[str]) -> list[dict]:
    """For each identifier whose keys repeat, the other fields that never vary within a key.

    Such fields describe the entity, not the record: they repeat on each of its records,
    so totals across records count them once per record. Blanks count as a value, and
    fields with one value across the whole file are left out as uninformative."""
    varying = [name for name in raw.columns if raw[name].str.strip().nunique() > 1]
    results = []
    for name in identifiers:
        keys = raw[name].str.strip()
        rows = raw[keys.ne("")]
        keys = keys[keys.ne("")]
        repeated = keys.duplicated(keep=False).sum()
        if rows.empty or keys.nunique() < 2 or repeated < ENTITY_MIN_REPEATED * len(rows):
            continue
        groups = rows.groupby(keys)
        constant = [other for other in varying
                    if other != name and (groups[other].nunique(dropna=False) <= 1).all()]
        if constant:
            results.append({"identifier": name, "entities": int(keys.nunique()),
                            "records": int(len(rows)), "constant_fields": constant})
    return results


def scalar(value):
    if pd.isna(value):
        return None
    if isinstance(value, (dt.datetime, dt.date, dt.time)):
        return value.isoformat()
    if isinstance(value, dt.timedelta):
        return str(value)
    return value.item() if hasattr(value, "item") else value


def profile_table(
    path: str | Path,
    *,
    roles: dict[str, str] | None = None,
    date_formats: dict[str, str] | None = None,
    encoding: str = "utf-8-sig",
    sheet: str | None = None,
    table: str | None = None,
    cell_range: str | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Read and recompute the whole profile using the supplied interpretation.

    Date formats use strptime syntax, e.g. %d/%m/%Y. Supplying a date format also
    assigns the date role. Numeric parsing does not infer currency or locale rules.

    raw retains source values; detect blanks with blank_cells(raw[field]).
    data masks those blanks, typed Excel errors and failed
    conversions as missing (NA/NaN/NaT depending on dtype), so data[field].isna()
    includes all three. The profile counts them separately. XLSX cell metadata
    is retained in raw.attrs['cells']; addresses follow profile['source'].
    """
    path = Path(path).resolve()
    loaded = read_table(path, encoding=encoding, sheet=sheet, table=table, cell_range=cell_range)
    raw = loaded.raw
    roles, date_formats = roles or {}, date_formats or {}
    unknown = (set(roles) | set(date_formats)) - set(raw.columns)
    if unknown:
        raise ValueError(f"Unknown fields in overrides: {', '.join(sorted(unknown))}")
    if set(roles.values()) - ROLES:
        raise ValueError(f"Roles must be one of: {', '.join(sorted(ROLES))}")
    if any(roles.get(name, "date") != "date" for name in date_formats):
        raise ValueError("A field with a date format must have the date role.")

    data = raw.copy()
    columns = []
    for name in raw.columns:
        original = raw[name]
        blank = blank_cells(original)
        errors = loaded.errors[name]
        values = original.mask(blank | errors)
        strings = text_values(values)
        inferred = infer_role(strings, name)
        present_values = values.dropna()
        if not present_values.empty and inferred != "identifier":
            date_matches = values.map(native_date) | strings.str.fullmatch(ISO_DATE).fillna(False)
            if date_matches.sum() / len(present_values) >= PARSE_THRESHOLD:
                inferred = "date"
        role = roles.get(name, "date" if name in date_formats else inferred)
        parsed = values
        if role in {"measure", *DATE_PARTS}:
            parsed = numeric(strings.str.strip())
        elif role == "date":
            parsed = parse_dates(values, date_formats.get(name))
        failed = ~blank & ~errors & parsed.isna()
        data[name] = parsed
        present = parsed.dropna()
        entry = {
            "name": name, "role": role, "blank": int(blank.sum()),
            "distinct": int(values.nunique()), "parsed": int(parsed.notna().sum()),
            "parse_failures": int(failed.sum()),
            "source_errors": int(errors.sum()),
            "failure_examples": [
                {**loaded.location(index, name), "value": scalar(value)}
                for index, value in original[failed].head(5).items()
            ],
            "error_examples": [{**loaded.location(index, name), "value": scalar(value)}
                               for index, value in original[errors].head(5).items()],
        }
        if loaded.source["format"] == "xlsx":
            entry["number_formats"] = loaded.formats[name]
            entry["cell_types"] = loaded.cell_types[name]
        if role == "measure" and not present.empty:
            entry.update({key: scalar(value) for key, value in {
                "min": present.min(), "p05": present.quantile(0.05),
                "median": present.median(), "p95": present.quantile(0.95),
                "max": present.max(), "mean": present.mean(),
            }.items()})
            entry.update(zeros=int(present.eq(0).sum()), negatives=int(present.lt(0).sum()))
        elif role in DATE_PARTS and not present.empty:
            entry.update(min=scalar(present.min()), max=scalar(present.max()),
                         expected_range=list(DATE_PARTS[role][1]),
                         outside_range=int((~in_range(present, role)).sum()))
        elif role == "date" and not present.empty:
            style = "%Y-%m-%d" if (present.dt.normalize() == present).all() else "%Y-%m-%d %H:%M:%S"
            entry.update(start=present.min().strftime(style), end=present.max().strftime(style))
        elif role in {"identifier", "category", "text"}:
            counts = present.value_counts()
            entry["top_values"] = [
                {"value": str(value), "count": int(count)}
                for value, count in counts.head(5).items()
            ]
            if role == "identifier":
                entry["duplicates"] = int(len(present) - present.nunique())
        if role != "date" and (hint := date_format_hint(strings)):
            entry["date_format_hint"] = hint
        if placeholders := possible_placeholders(strings):
            entry["possible_placeholders"] = placeholders
        columns.append(entry)

    # Cell errors and literal error-looking text are distinct source records.
    if loaded.source["format"] == "csv":
        duplicates = int(raw.duplicated().sum())
        entity_values = raw
    else:
        record_keys = [tuple((type(value).__name__, scalar(value), bool(error))
                            for value, error in zip(row, errors))
                       for row, errors in zip(raw.itertuples(index=False, name=None),
                                              loaded.errors.itertuples(index=False, name=None))]
        duplicates = len(record_keys) - len(set(record_keys))
        entity_values = raw.apply(text_values).fillna("")
    profile = {
        "file": path.name, "path": str(path),
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "rows": len(raw), "fields": len(raw.columns),
        "duplicate_records": duplicates,
        "empty_lines_skipped": loaded.source.get("empty_lines_skipped", 0), "columns": columns,
        "source": loaded.source,
        "blank_records": int(raw.apply(blank_cells).all(axis=1).sum()),
        "entity_fields": entity_fields(entity_values,
                                       [c["name"] for c in columns if c["role"] == "identifier"
                                        and not c["source_errors"]]),
        "sample": [
            {**loaded.location(index), "values": {name: scalar(value) for name, value in row.items()}}
            for index, row in raw.head(5).iterrows()
        ],
    }
    # Attach evidence after calculations so pandas does not repeatedly deep-copy
    # per-cell metadata while slicing/parsing the frame.
    if loaded.source["format"] == "xlsx":
        raw.attrs["cells"] = loaded.cell_metadata
    return raw, data, profile


def assignment(value: str) -> tuple[str, str]:
    name, separator, setting = value.partition("=")
    if not separator or not name or not setting:
        raise argparse.ArgumentTypeError("Use FIELD=VALUE.")
    return name, setting


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="One CSV or XLSX file")
    parser.add_argument("--inspect", action="store_true", help="List XLSX worksheets, Tables and previews without profiling")
    parser.add_argument("--sheet", help="Exact worksheet name")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--table", help="Exact Excel Table name")
    selection.add_argument("--range", dest="cell_range", help="Bounded range including its header, e.g. B5:H800")
    parser.add_argument("--role", action="append", type=assignment, default=[], metavar="FIELD=ROLE")
    parser.add_argument("--date-format", action="append", type=assignment, default=[], metavar="FIELD=FORMAT")
    parser.add_argument("--encoding", default="utf-8-sig", help="Explicit input encoding (default: utf-8-sig)")
    args = parser.parse_args(argv)
    try:
        if args.inspect:
            if Path(args.file).suffix.lower() != ".xlsx":
                raise ValueError("--inspect applies to XLSX workbooks.")
            print(json.dumps(inspect_xlsx(args.file), ensure_ascii=False, indent=2))
            return 0
        _, _, profile = profile_table(
            args.file, roles=dict(args.role), date_formats=dict(args.date_format), encoding=args.encoding,
            sheet=args.sheet, table=args.table, cell_range=args.cell_range,
        )
    except (OSError, ValueError, LookupError, csv.Error, BadZipFile) as exc:
        parser.error(str(exc))
    with tempfile.NamedTemporaryFile(mode="w", prefix="eda-profile-", suffix=".json", encoding="utf-8", delete=False) as output:
        json.dump(profile, output, ensure_ascii=False, indent=2, allow_nan=False)
        output_path = output.name
    print(f"{profile['file']}: {profile['rows']:,} records, {profile['fields']} fields")
    if profile["source"]["format"] == "xlsx":
        print("  Source selection: " + json.dumps(profile["source"], ensure_ascii=False))
    if profile["empty_lines_skipped"]:
        print(f"  {profile['empty_lines_skipped']} empty lines outside quoted fields skipped")
    for field in profile["columns"]:
        extra = ""
        if "outside_range" in field:
            low, high = field["expected_range"]
            extra = f", {field['outside_range']} outside {low}-{high}"
        print(f"  {field['name']}: {field['role']}; {field['blank']} blank, {field['parse_failures']} unparsed, "
              f"{field['source_errors']} Excel errors{extra}")
        hint = field.get("date_format_hint", [])
        if len(hint) == 1:
            print(f"    looks like dates in {hint[0]}: check the raw values, then set --date-format {field['name']}={hint[0]}")
        elif hint:
            print(f"    looks like dates, fitting {' and '.join(hint)}: resolve the order before setting --date-format")
        if placeholders := field.get("possible_placeholders"):
            listed = ", ".join(f"{item['value']} ({item['count']:,})" for item in placeholders["values"])
            print(f"    possible placeholders in {placeholders['count']:,} records: {listed}")
    for group in profile["entity_fields"]:
        print(f"  {group['identifier']} groups {group['records']:,} records into {group['entities']:,} entities; "
              f"constant within each: {', '.join(group['constant_fields'])}")
    print(f"Temporary profile: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
