# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas>=2.0,<4"]
# ///
"""Profile one comma-delimited CSV with a header row, without modifying it.

CLI: uv run profile_csv.py FILE [--role FIELD=ROLE] [--date-format FIELD=FORMAT]
Library: raw, data, profile = profile_csv(path, roles=..., date_formats=...)

raw retains cell strings; data contains the interpreted values used in statistics.
Both use one-based data-record indexes (not physical line numbers). Blank cells
and failed conversions are counted separately. Inferred roles cover plain numbers,
ISO dates, and whole-number year or month fields named as such. Other date formats
require an explicit format; a field whose values fit one gets a date_format_hint
listing every format that fits.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import re
import tempfile
from pathlib import Path

import pandas as pd

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


def read_csv(path: Path, encoding: str = "utf-8-sig") -> tuple[pd.DataFrame, int]:
    """Read strings exactly; reject missing/duplicate headers and ragged records."""
    path = Path(path)
    if path.suffix.lower() != ".csv":
        raise ValueError("Provide exactly one .csv file containing one table with a header row.")
    records = []
    skipped = 0
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
    raw.index = pd.RangeIndex(1, len(raw) + 1, name="csv_record")
    return raw, skipped


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


def scalar(value):
    if pd.isna(value):
        return None
    if isinstance(value, (dt.datetime, dt.date)):
        return value.isoformat()
    return value.item() if hasattr(value, "item") else value


def profile_csv(
    path: str | Path,
    *,
    roles: dict[str, str] | None = None,
    date_formats: dict[str, str] | None = None,
    encoding: str = "utf-8-sig",
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Read and recompute the whole profile using the supplied interpretation.

    Date formats use strptime syntax, e.g. %d/%m/%Y. Supplying a date format also
    assigns the date role. Numeric parsing does not infer currency or locale rules.

    raw retains strings, including empty strings and whitespace-only cells; detect
    blanks with raw[field].str.strip().eq(""). data masks those blanks and failed
    conversions as missing (NA/NaN/NaT depending on dtype), so data[field].isna()
    includes both. The profile counts blanks and parse failures separately.
    """
    path = Path(path).resolve()
    raw, skipped = read_csv(path, encoding)
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
        blank = original.str.strip().eq("")
        values = original.mask(blank)
        inferred = infer_role(values, name)
        role = roles.get(name, "date" if name in date_formats else inferred)
        parsed = values
        if role in {"measure", *DATE_PARTS}:
            parsed = numeric(values.str.strip())
        elif role == "date":
            date_format = date_formats.get(name, "%Y-%m-%d")
            parsed = pd.to_datetime(values.str.strip(), format=date_format, errors="coerce")
            if name not in date_formats:
                parsed = parsed.where(values.str.fullmatch(ISO_DATE).fillna(False))
        failed = ~blank & parsed.isna()
        data[name] = parsed
        present = parsed.dropna()
        entry = {
            "name": name, "role": role, "blank": int(blank.sum()),
            "distinct": int(values.nunique()), "parsed": int(parsed.notna().sum()),
            "parse_failures": int(failed.sum()),
            "failure_examples": [
                {"record": int(index), "value": value}
                for index, value in original[failed].head(5).items()
            ],
        }
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
        if role != "date" and (hint := date_format_hint(values)):
            entry["date_format_hint"] = hint
        columns.append(entry)

    profile = {
        "file": path.name, "path": str(path),
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "rows": len(raw), "fields": len(raw.columns),
        "duplicate_records": int(raw.duplicated().sum()),
        "empty_lines_skipped": skipped, "columns": columns,
        "sample": [
            {"record": int(index), "values": row.to_dict()}
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
    parser.add_argument("file", help="One CSV file; first record must be a header")
    parser.add_argument("--role", action="append", type=assignment, default=[], metavar="FIELD=ROLE")
    parser.add_argument("--date-format", action="append", type=assignment, default=[], metavar="FIELD=FORMAT")
    parser.add_argument("--encoding", default="utf-8-sig", help="Explicit input encoding (default: utf-8-sig)")
    args = parser.parse_args(argv)
    try:
        _, _, profile = profile_csv(
            args.file, roles=dict(args.role), date_formats=dict(args.date_format), encoding=args.encoding,
        )
    except (OSError, ValueError, LookupError, csv.Error) as exc:
        parser.error(str(exc))
    with tempfile.NamedTemporaryFile(mode="w", prefix="eda-profile-", suffix=".json", encoding="utf-8", delete=False) as output:
        json.dump(profile, output, ensure_ascii=False, indent=2, allow_nan=False)
        output_path = output.name
    print(f"{profile['file']}: {profile['rows']:,} records, {profile['fields']} fields")
    if profile["empty_lines_skipped"]:
        print(f"  {profile['empty_lines_skipped']} empty lines outside quoted fields skipped")
    for field in profile["columns"]:
        extra = ""
        if "outside_range" in field:
            low, high = field["expected_range"]
            extra = f", {field['outside_range']} outside {low}-{high}"
        print(f"  {field['name']}: {field['role']}; {field['blank']} blank, {field['parse_failures']} unparsed{extra}")
        hint = field.get("date_format_hint", [])
        if len(hint) == 1:
            print(f"    looks like dates in {hint[0]}: check the raw values, then set --date-format {field['name']}={hint[0]}")
        elif hint:
            print(f"    looks like dates, fitting {' and '.join(hint)}: resolve the order before setting --date-format")
    print(f"Temporary profile: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
