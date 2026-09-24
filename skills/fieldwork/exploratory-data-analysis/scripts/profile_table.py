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
R-000000, 99999, --, UNKNOWN); identifiers with mixed character patterns list
value_shapes, each less common shape noting any grouping value (a category or a
date's year) its records are concentrated_in, and categories with values differing only in case or spacing list
case_variants. entity_fields names the fields that never vary within a repeating
identifier. The CLI also writes a temporary pickle of (raw, data, profile) for
exploration scripts.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import pickle
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
ROLES = {"identifier", "measure", "category", "date", "year", "month", "text", "empty"}
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
# Shapes and case-variant groups listed per field, most records first.
SHAPES_MAX = 10
VARIANT_GROUPS_MAX = 5
# A less common identifier shape is concentrated when at least this share of its records
# share one value of a grouping field (a category with few values, or a date's year) that
# holds at most CONCENTRATION_MAX_BASE of all records. Shapes rarer than
# CONCENTRATION_MIN_RECORDS are left out, since a handful of records always concentrates.
CONCENTRATION_MIN_SHARE = 0.9
CONCENTRATION_MAX_BASE = 0.25
CONCENTRATION_MIN_RECORDS = 5
GROUPING_MAX_VALUES = 50


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


def value_counts(values: pd.Series) -> tuple[pd.Series, pd.Series]:
    """Record counts per distinct present value, and those values as a string Series
    aligned with them. Checks run once per distinct value and weight by these counts."""
    counts = values.dropna().value_counts()
    return counts, counts.index.to_series().astype("string")


def share(counts: pd.Series, matches: pd.Series) -> float:
    """Share of the counted records whose distinct value matches."""
    total = counts.sum()
    return counts[matches.to_numpy(dtype=bool)].sum() / total if total else 0.0


def date_format_hint(values: pd.Series) -> list[str]:
    """Every non-ISO format that parses a strong majority of the present values. More
    than one (such as month-first and day-first) means the order is unresolved."""
    counts, distinct = value_counts(values.str.strip())
    fits = []
    for date_format, shape in DATE_HINTS:
        matches = distinct.str.fullmatch(shape)
        if counts.empty or share(counts, matches) < PARSE_THRESHOLD:
            continue
        parsed = pd.to_datetime(distinct, format=date_format, errors="coerce").notna() & matches
        if share(counts, parsed) >= PARSE_THRESHOLD:
            fits.append(date_format)
    return fits


def infer_role(values: pd.Series, name: str) -> str:
    counts, distinct = value_counts(values)
    if counts.empty:
        return "empty"
    words = re.sub(r"([a-z])([A-Z])", r"\1_\2", name)
    if ID_NAME.search(words) or distinct.str.fullmatch(r"0\d+").any():
        return "identifier"
    if share(counts, distinct.str.fullmatch(ISO_DATE)) >= PARSE_THRESHOLD:
        return "date"
    parsed = numeric(distinct.str.strip())
    if share(counts, parsed.notna()) >= PARSE_THRESHOLD:
        name_words = set(re.split(r"[^a-z0-9]+", words.lower()))
        for part, (part_words, _) in DATE_PARTS.items():
            if name_words & part_words and share(counts, in_range(parsed, part)) >= PARSE_THRESHOLD:
                return part
        return "measure"
    # Low-cardinality text gets frequency summaries; this never changes its values.
    if len(counts) <= 20 or len(counts) / counts.sum() <= 0.1:
        return "category"
    return "text"


def possible_placeholders(values: pd.Series) -> dict | None:
    """Count and most frequent values that look like stand-ins for a missing value."""
    counts, distinct = value_counts(values.str.strip())
    matches = counts[distinct.str.fullmatch(PLACEHOLDER).to_numpy(dtype=bool)]
    if matches.empty:
        return None
    return {
        "count": int(matches.sum()),
        "values": [{"value": str(value), "count": int(count)} for value, count in matches.head(5).items()],
    }


def shape_of(value: str) -> str:
    """9 for a digit, A for a letter, other characters kept."""
    return re.sub(r"[^\W\d_]", "A", re.sub(r"\d", "9", value))


def value_shapes(values: pd.Series) -> dict | None:
    """Character patterns of an identifier's values when there is more than one: mixed
    shapes can mean mixed schemes."""
    counts, distinct = value_counts(values.str.strip())
    shapes = distinct.map(shape_of).to_numpy()
    by_shape = counts.groupby(shapes, sort=False).sum().sort_values(ascending=False, kind="stable")
    if len(by_shape) < 2:
        return None
    # counts is most frequent first, so the first value of each shape is its commonest.
    examples = pd.Series(counts.index, index=shapes).groupby(level=0, sort=False).first()
    return {
        "count": int(len(by_shape)),
        "shapes": [{"shape": shape, "records": int(records), "example": str(examples[shape])}
                   for shape, records in by_shape.head(SHAPES_MAX).items()],
    }


def shape_concentrations(values: pd.Series, shapes: dict, groupings: dict[str, pd.Series]) -> None:
    """Add concentrated_in to each less common shape whose records gather in one value of
    a grouping field, such as a period, source system, or year: evidence of where a scheme
    change or second source begins. Picks the grouping with the highest share, then the
    smallest base."""
    stripped = values.str.strip()
    distinct = stripped.dropna().unique()
    record_shapes = stripped.map(dict(zip(distinct, map(shape_of, distinct))))
    for item in shapes["shapes"][1:]:
        in_shape = record_shapes.eq(item["shape"]).fillna(False)
        if item["records"] < CONCENTRATION_MIN_RECORDS:
            continue
        best = None
        for name, grouping in groupings.items():
            counts = grouping[in_shape].value_counts()
            if counts.empty:
                continue
            value, records = counts.index[0], int(counts.iloc[0])
            share_of_shape = records / item["records"]
            share_of_all = float(grouping.eq(value).mean())
            candidate = (share_of_shape, -share_of_all)
            if (share_of_shape >= CONCENTRATION_MIN_SHARE and share_of_all <= CONCENTRATION_MAX_BASE
                    and (best is None or candidate > best[0])):
                best = (candidate, {"field": name, "value": str(value), "share_of_shape": round(share_of_shape, 4),
                                    "share_of_all": round(share_of_all, 4)})
        if best:
            item["concentrated_in"] = best[1]


def case_variants(values: pd.Series) -> dict | None:
    """Groups of values that differ only in letter case or spacing, which split counts."""
    counts, distinct = value_counts(values)
    keys = distinct.map(lambda value: " ".join(value.split()).casefold()).to_numpy()
    grouped = counts.groupby(keys, sort=False)
    sizes = grouped.size()
    variant_keys = sizes[sizes > 1].index
    if variant_keys.empty:
        return None
    totals = grouped.sum()[variant_keys].sort_values(ascending=False, kind="stable")
    members = pd.Series(keys, index=counts.index)
    return {
        "count": int(totals.sum()),
        "groups": [[{"value": str(value), "count": int(counts[value])} for value in members[members == key].index]
                   for key in totals.head(VARIANT_GROUPS_MAX).index],
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
    encoding: str | None = None,
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
    includes all three. The profile counts them separately, records the choices this
    call applied under "choices", and carries the source's reader disclosures under
    source["disclosures"].
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
    all_texts = loaded.texts()
    columns, blanks, texts = [], {}, {}
    shaped, groupings = {}, {}  # identifiers with mixed shapes; fields to locate those shapes by
    for name in raw.columns:
        original = raw[name]
        blank = blanks[name] = blank_cells(original)
        errors = loaded.errors[name]
        values = original.mask(blank | errors)
        texts[name] = all_texts[name]
        strings = texts[name].mask(blank | errors)
        inferred = infer_role(strings, name)
        present_values = values.dropna()
        if not present_values.empty and inferred != "identifier":
            iso = {value for value in strings.dropna().unique() if re.fullmatch(ISO_DATE, value)}
            date_matches = values.map(native_date) | strings.isin(iso)
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
        entry.update(loaded.field_facts(name))
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
                if shapes := value_shapes(strings):
                    entry["value_shapes"] = shapes
                    shaped[name] = (strings, shapes)
            elif role == "category":
                if variants := case_variants(strings):
                    entry["case_variants"] = variants
                if 1 < entry["distinct"] <= GROUPING_MAX_VALUES:
                    groupings[name] = strings
        if role == "date" and not present.empty:
            groupings[name] = parsed.dt.year.astype("Int64").astype("string")
        elif role == "year" and not present.empty:
            groupings[name] = parsed.where(in_range(parsed, "year")).astype("Int64").astype("string")
        if role != "date" and (hint := date_format_hint(strings)):
            entry["date_format_hint"] = hint
        if placeholders := possible_placeholders(strings):
            entry["possible_placeholders"] = placeholders
        columns.append(entry)
    for name, (strings, shapes) in shaped.items():
        shape_concentrations(strings, shapes, {other: values for other, values in groupings.items() if other != name})

    choices = {key: value for key, value in (("sheet", sheet), ("table", table), ("cell_range", cell_range))
               if value is not None}
    choices.update(roles=dict(roles), date_formats=dict(date_formats))
    if "encoding" in loaded.source:
        choices["encoding"] = loaded.source["encoding"]
    profile = {
        "file": path.name, "path": str(path),
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "rows": len(raw), "fields": len(raw.columns),
        "duplicate_records": loaded.duplicate_records(),
        "columns": columns,
        "source": loaded.source,
        "choices": choices,
        "blank_records": int(pd.DataFrame(blanks).all(axis=1).sum()) if blanks else 0,
        "entity_fields": entity_fields(loaded.entity_values(),
                                       [c["name"] for c in columns if c["role"] == "identifier"
                                        and not c["source_errors"]]),
        "sample": [
            {**loaded.location(index), "values": {name: scalar(value) for name, value in row.items()}}
            for index, row in raw.head(5).iterrows()
        ],
    }
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
    parser.add_argument("--encoding", help="CSV input encoding (default: utf-8-sig)")
    args = parser.parse_args(argv)
    try:
        if args.inspect:
            if Path(args.file).suffix.lower() != ".xlsx":
                raise ValueError("--inspect applies to XLSX workbooks.")
            print(json.dumps(inspect_xlsx(args.file), ensure_ascii=False, indent=2))
            return 0
        raw, data, profile = profile_table(
            args.file, roles=dict(args.role), date_formats=dict(args.date_format), encoding=args.encoding,
            sheet=args.sheet, table=args.table, cell_range=args.cell_range,
        )
    except (OSError, ValueError, LookupError, csv.Error, BadZipFile) as exc:
        parser.error(str(exc))
    with tempfile.NamedTemporaryFile(mode="w", prefix="eda-profile-", suffix=".json", encoding="utf-8", delete=False) as output:
        json.dump(profile, output, ensure_ascii=False, indent=2, allow_nan=False)
        output_path = output.name
    with tempfile.NamedTemporaryFile(prefix="eda-profile-", suffix=".pkl", delete=False) as cache:
        pickle.dump((raw, data, profile), cache)
        cache_path = cache.name
    print(f"{profile['file']}: {profile['rows']:,} records, {profile['fields']} fields")
    for note in profile["source"]["disclosures"]:
        print(f"  {note}")
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
        if shapes := field.get("value_shapes"):
            listed = ", ".join(f"{item['shape']} ({item['records']:,}, e.g. {item['example']})" for item in shapes["shapes"])
            print(f"    {shapes['count']} value shapes: {listed}")
            for item in shapes["shapes"]:
                if where := item.get("concentrated_in"):
                    print(f"      {item['shape']}: {where['share_of_shape']:.0%} of its records have "
                          f"{where['field']} = {json.dumps(where['value'], ensure_ascii=False)} "
                          f"({where['share_of_all']:.0%} of all records)")
        if variants := field.get("case_variants"):
            listed = "; ".join(" / ".join(json.dumps(item["value"], ensure_ascii=False) for item in group)
                               for group in variants["groups"])
            print(f"    values differing only in case or spacing, in {variants['count']:,} records: {listed}")
    for group in profile["entity_fields"]:
        print(f"  {group['identifier']} groups {group['records']:,} records into {group['entities']:,} entities; "
              f"constant within each: {', '.join(group['constant_fields'])}")
    print(f"Temporary profile: {output_path}")
    print(f"Exploration cache: {cache_path} (pandas.read_pickle gives raw, data, profile)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
