# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas>=2.0,<4"]
# ///
"""Profile one comma-delimited CSV with a header row, without modifying it.

CLI: uv run profile_csv.py FILE [--role FIELD=ROLE] [--date-format FIELD=FORMAT]
Library: raw, data, profile = profile_csv(path, roles=..., date_formats=...)

raw retains cell strings; data contains the interpreted values used in statistics.
Both use one-based data-record indexes (not physical line numbers). Blank cells
and failed conversions are counted separately. Only plain numbers and ISO dates
are inferred; other date formats require an explicit format.
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
ROLES = {"identifier", "measure", "category", "date", "text"}
ID_NAME = re.compile(r"(^|[^a-z])(id|key|code|number|no|ref|reference)$", re.I)
ISO_DATE = r"\d{4}-\d{2}-\d{2}"
DATE_FORMAT_NAMES = {
    "%Y-%m-%d": "year-month-day", "%m/%d/%Y": "month/day/year", "%d/%m/%Y": "day/month/year",
    "%Y/%m/%d": "year/month/day", "%d-%m-%Y": "day-month-year", "%m-%d-%Y": "month-day-year",
    "%Y%m%d": "yearmonthday", "%d.%m.%Y": "day.month.year",
}


def describe_format(date_format: str) -> str:
    return DATE_FORMAT_NAMES.get(date_format, f"the format {date_format}")


def read_csv(path: Path, encoding: str = "utf-8-sig") -> tuple[pd.DataFrame, list[str]]:
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
    notes = [
        f"Read as comma-delimited CSV using {encoding}; first record used as the header.",
        "Empty or whitespace-only cells count as blank; literal NA, NULL and similar strings are retained.",
        "Record numbers count data records after the header, not physical lines; duplicate records are retained.",
    ]
    if skipped:
        notes.append(f"Ignored {skipped} empty lines outside quoted fields; all table records are retained.")
    return raw, notes


def numeric(values: pd.Series) -> pd.Series:
    """Parse plain decimal/scientific notation; exclude non-finite values."""
    parsed = pd.to_numeric(values, errors="coerce")
    finite = parsed.map(lambda value: pd.notna(value) and math.isfinite(float(value)))
    return parsed.where(finite)


def infer_role(values: pd.Series, name: str) -> str:
    present = values.dropna()
    if present.empty:
        return "empty"
    words = re.sub(r"([a-z])([A-Z])", r"\1_\2", name)
    if ID_NAME.search(words) or present.str.fullmatch(r"0\d+").any():
        return "identifier"
    if present.str.fullmatch(ISO_DATE).mean() >= PARSE_THRESHOLD:
        return "date"
    if numeric(present).notna().mean() >= PARSE_THRESHOLD:
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
    """
    path = Path(path).resolve()
    raw, notes = read_csv(path, encoding)
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
    measures, dated, overridden = [], {}, []
    for name in raw.columns:
        original = raw[name]
        blank = original.str.strip().eq("")
        values = original.mask(blank)
        inferred = infer_role(values, name)
        role = roles.get(name, "date" if name in date_formats else inferred)
        parsed = values
        if role == "measure":
            parsed = numeric(values.str.strip())
            measures.append(name)
        elif role == "date":
            date_format = date_formats.get(name, "%Y-%m-%d")
            parsed = pd.to_datetime(values.str.strip(), format=date_format, errors="coerce")
            if name not in date_formats:
                parsed = parsed.where(values.str.fullmatch(ISO_DATE).fillna(False))
            dated.setdefault(describe_format(date_format), []).append(name)
        if name in roles or name in date_formats:
            overridden.append(f"{name} ({role}; initially {inferred})")
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
        columns.append(entry)

    if measures:
        notes.append("Parsed as plain numbers, without currency or locale rules: " + ", ".join(measures) + ".")
    for style, names in dated.items():
        notes.append(f"Parsed as dates written {style}: " + ", ".join(names) + ".")
    if overridden:
        notes.append("Roles set explicitly: " + "; ".join(overridden) + ".")

    profile = {
        "file": path.name, "path": str(path),
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "rows": len(raw), "fields": len(raw.columns),
        "duplicate_records": int(raw.duplicated().sum()),
        "notes": notes, "columns": columns,
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
    for field in profile["columns"]:
        print(f"  {field['name']}: {field['role']}; {field['blank']} blank, {field['parse_failures']} unparsed")
    print(f"Temporary profile: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
