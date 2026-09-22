# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas>=2.0", "openpyxl>=3.1"]
# ///
"""Profile data files an auditor has received.

Usage:
    uv run profile.py FILE [FILE ...] [--out PATH]

Reads CSV, XLSX/XLSM and JSON. Every sheet of a workbook is a separate source.
For each source the profile records:

  * structure: header row, title rows above it, blank rows and columns dropped,
    duplicated or unnamed headers, hidden sheets, and whether the sheet is
    tabular at all (non-tabular sheets get a raw sample instead of a profile)
  * one entry per field with an apparent role (identifier, measure, category,
    date, text, empty) and the statistics that role calls for
  * the apparent coverage period, candidate keys, and a sample of records

Fields sharing a name across sources are tested as apparent relationships:
matched and unmatched rows on each side and the apparent cardinality.

The full profile is written as JSON (default: a fresh file in the OS temp
directory) and a compact summary is printed. Roles are apparent: inferred from
names and values, and open to correction.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import re
import sys
import tempfile
import warnings
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

TOP_N = 20
SAMPLE_RECORDS = 5
RAW_SAMPLE_ROWS = 10
HEADER_SCAN_ROWS = 20
PARSE_THRESHOLD = 0.95
MAX_MONTH_BUCKETS = 120

ID_NAME = re.compile(r"(^|[^a-z])(id|ids|key|code|no|num|number|ref|reference)$", re.I)
DATE_LIKE = re.compile(
    r"\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4}|\d{1,2}\s*[A-Za-z]{3}|[A-Za-z]{3,9}\s+\d{1,2}|\d{4}-\d{2}"
)
NUMERIC_JUNK = re.compile(r"[,$£€\s]")
PAREN_NEGATIVE = re.compile(r"^\((.*)\)$")

ROLE_ORDER = ["identifier", "date", "measure", "category", "text", "empty"]


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------


def load_file(path: Path) -> list[tuple[dict, pd.DataFrame | None]]:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xlsm", ".xls"}:
        return load_workbook(path)
    if suffix == ".json":
        return [load_json(path)]
    return [load_csv(path)]


def load_workbook(path: Path) -> list[tuple[dict, pd.DataFrame | None]]:
    xl = pd.ExcelFile(path)
    out = []
    for name in xl.sheet_names:
        raw = xl.parse(name, header=None)
        hidden = False
        try:
            hidden = xl.book[name].sheet_state != "visible"
        except Exception:  # noqa: BLE001 - engine without sheet state
            pass
        out.append(build_source(f"{path.name}/{name}", path, name, hidden, raw))
    return out


def load_csv(path: Path) -> tuple[dict, pd.DataFrame | None]:
    last_error: Exception | None = None
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            raw = pd.read_csv(
                path,
                header=None,
                sep=None,
                engine="python",
                encoding=encoding,
                dtype=object,
                skip_blank_lines=False,
            )
            src, df = build_source(path.name, path, None, False, raw)
            if encoding != "utf-8":
                src["notes"].append(f"Read with {encoding} encoding")
            return src, df
        except (UnicodeDecodeError, pd.errors.ParserError) as exc:
            last_error = exc
    raise SystemExit(f"Could not read {path}: {last_error}")


def load_json(path: Path) -> tuple[dict, pd.DataFrame | None]:
    data = json.loads(path.read_text(encoding="utf-8"))
    notes = []
    if isinstance(data, dict):
        lists = {k: v for k, v in data.items() if isinstance(v, list)}
        if lists:
            key = max(lists, key=lambda k: len(lists[k]))
            notes.append(f"Records taken from top-level key '{key}'")
            data = lists[key]
        else:
            notes.append("Single object treated as one record")
            data = [data]
    df = pd.json_normalize(data)
    src = new_source(path.name, path, None, False)
    src["notes"].extend(notes)
    src["header_row"] = None
    return finish_source(src, df)


def new_source(source_id: str, path: Path, sheet: str | None, hidden: bool) -> dict:
    return {
        "id": source_id,
        "file": path.name,
        "path": str(path.resolve()),
        "sheet": sheet,
        "hidden": hidden,
        "notes": [],
    }


def build_source(
    source_id: str, path: Path, sheet: str | None, hidden: bool, raw: pd.DataFrame
) -> tuple[dict, pd.DataFrame | None]:
    src = new_source(source_id, path, sheet, hidden)
    if hidden:
        src["notes"].append("Sheet is hidden in the workbook")

    raw = raw.dropna(how="all", axis=1)
    if raw.empty or raw.dropna(how="all").empty:
        src.update(tabular=False, rows=0, fields=0, raw_sample=[])
        src["notes"].append("Sheet is empty")
        return src, None

    header = detect_header(raw)
    if header is None:
        src.update(
            tabular=False,
            rows=int(len(raw)),
            fields=int(raw.shape[1]),
            raw_sample=rows_as_lists(raw.head(RAW_SAMPLE_ROWS)),
        )
        src["notes"].append(
            f"No header row found in the first {HEADER_SCAN_ROWS} rows; treated as non-tabular"
        )
        return src, None

    title_rows = [i for i in range(header) if raw.iloc[i].notna().any()]
    if title_rows:
        preview = "; ".join(
            " ".join(str(v) for v in raw.iloc[i].dropna().tolist())[:80] for i in title_rows[:3]
        )
        src["notes"].append(
            f"{len(title_rows)} row(s) above the header contain content and were excluded: {preview}"
        )

    columns, column_notes = make_columns(raw.iloc[header])
    src["notes"].extend(column_notes)
    df = raw.iloc[header + 1 :].reset_index(drop=True)
    df.columns = columns
    src["header_row"] = int(header)
    return finish_source(src, df)


def detect_header(raw: pd.DataFrame) -> int | None:
    limit = min(HEADER_SCAN_ROWS, len(raw) - 1)
    if limit < 1:
        return None
    counts = [int(raw.iloc[i].notna().sum()) for i in range(limit)]
    widest = max(counts) if counts else 0
    for i in range(limit):
        row = raw.iloc[i]
        values = row.dropna().tolist()
        nonnull = len(values)
        if nonnull < 2 or nonnull < 0.6 * widest:
            continue
        strings = sum(isinstance(v, str) for v in values)
        if strings < 0.8 * nonnull:
            continue
        labels = [str(v).strip().lower() for v in values]
        if len(set(labels)) < 0.8 * nonnull:
            continue
        if raw.iloc[i + 1 :].dropna(how="all").empty:
            continue
        return i
    return None


def make_columns(header_row: pd.Series) -> tuple[list[str], list[str]]:
    names: list[str] = []
    notes: list[str] = []
    seen: Counter = Counter()
    unnamed = 0
    for i, value in enumerate(header_row.tolist()):
        name = "" if value is None or (isinstance(value, float) and math.isnan(value)) else str(value).strip()
        if not name:
            unnamed += 1
            name = f"column_{i + 1}"
        seen[name] += 1
        if seen[name] > 1:
            name = f"{name}_{seen[name]}"
        names.append(name)
    duplicates = [n for n, c in seen.items() if c > 1]
    if duplicates:
        notes.append(f"Duplicated header(s) suffixed: {', '.join(duplicates[:5])}")
    if unnamed:
        notes.append(f"{unnamed} unnamed column(s) named column_<position>")
    return names, notes


def finish_source(src: dict, df: pd.DataFrame) -> tuple[dict, pd.DataFrame | None]:
    before = len(df)
    df = df.dropna(how="all").reset_index(drop=True)
    blank = before - len(df)
    if blank:
        src["notes"].append(f"{blank} fully blank row(s) dropped")

    df = coerce(df, src["notes"])
    stored_as_text = set(df.attrs.get("stored_as_text", []))
    columns = [profile_column(df[c], str(c), str(c) in stored_as_text) for c in df.columns]

    src.update(tabular=True, rows=int(len(df)), fields=int(df.shape[1]))
    src["candidate_keys"] = [
        c["name"] for c in columns if c["role"] == "identifier" and c.get("unique") and c["missing"] == 0
    ]
    src["period"] = coverage_period(columns)
    src["columns"] = columns
    src["sample"] = records(df.head(SAMPLE_RECORDS))
    return src, df


# ---------------------------------------------------------------------------
# Type coercion
# ---------------------------------------------------------------------------


def coerce(df: pd.DataFrame, notes: list[str]) -> pd.DataFrame:
    df = df.infer_objects()
    for name in df.columns:
        s = df[name]
        if is_numeric(s) or is_datetime(s) or is_bool(s):
            continue
        nonnull = s.dropna()
        if nonnull.empty:
            continue

        python_types = Counter(type(v).__name__ for v in nonnull.head(500))
        mostly = python_types.most_common(1)[0][0]
        text_values = int(nonnull.map(lambda v: isinstance(v, str)).sum())

        if mostly in {"int", "float", "Decimal"}:
            df[name] = numeric_from_mixed(s)
            if text_values:
                df.attrs.setdefault("stored_as_text", []).append(str(name))
                notes.append(f"'{name}': {text_values} value(s) stored as text parsed to numeric")
            continue
        if mostly in {"datetime", "Timestamp", "date"}:
            df[name] = to_datetime(s)
            continue
        if mostly != "str":
            continue

        text = nonnull.astype(str).str.strip()
        if not ID_NAME.search(str(name)):
            numeric = numeric_from_mixed(nonnull)
            if numeric.notna().mean() >= PARSE_THRESHOLD and not text.str.fullmatch(r"0\d+").any():
                df[name] = numeric_from_mixed(s)
                df.attrs.setdefault("stored_as_text", []).append(str(name))
                notes.append(f"'{name}' parsed from text to numeric")
                continue

        sample = text.head(200)
        if sample.str.contains(DATE_LIKE, regex=True).mean() >= 0.9:
            parsed = to_datetime(s)
            if parsed.notna().sum() >= PARSE_THRESHOLD * len(nonnull):
                df[name] = parsed
                df.attrs.setdefault("stored_as_text", []).append(str(name))
                notes.append(f"'{name}' parsed from text to datetime")
    return df


def numeric_from_mixed(s: pd.Series) -> pd.Series:
    """Parse a column holding numbers, or numbers stored as text with separators,
    currency symbols or accounting parentheses, into a numeric series."""

    def clean_value(v):
        if isinstance(v, str):
            v = PAREN_NEGATIVE.sub(r"-\1", NUMERIC_JUNK.sub("", v.strip()))
        return v

    return pd.to_numeric(s.map(clean_value), errors="coerce")


def to_datetime(s: pd.Series) -> pd.Series:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            return pd.to_datetime(s, errors="coerce", format="mixed")
        except (TypeError, ValueError):
            return pd.to_datetime(s, errors="coerce")


def is_numeric(s: pd.Series) -> bool:
    return pd.api.types.is_numeric_dtype(s) and not is_bool(s)


def is_datetime(s: pd.Series) -> bool:
    return pd.api.types.is_datetime64_any_dtype(s)


def is_bool(s: pd.Series) -> bool:
    return pd.api.types.is_bool_dtype(s)


# ---------------------------------------------------------------------------
# Column profiles
# ---------------------------------------------------------------------------


def profile_column(s: pd.Series, name: str, stored_as_text: bool = False) -> dict:
    n = int(len(s))
    missing = int(s.isna().sum())
    count = n - missing
    nonnull = s.dropna()
    entry: dict = {
        "name": name,
        "dtype": str(s.dtype),
        "count": count,
        "missing": missing,
        "coverage": round(count / n, 4) if n else 0.0,
    }
    if stored_as_text:
        entry["stored_as"] = "text"
    if count == 0:
        entry.update(role="empty", distinct=0)
        return entry

    distinct = int(nonnull.nunique())
    role = infer_role(s, nonnull, name, distinct)
    entry.update(role=role, distinct=distinct)
    entry.update(STATS[role](nonnull, distinct))
    return entry


def infer_role(s: pd.Series, nonnull: pd.Series, name: str, distinct: int) -> str:
    count = len(nonnull)
    if is_datetime(s):
        return "date"
    if is_bool(s):
        return "category"
    if ID_NAME.search(name):
        return "identifier"
    if is_numeric(s):
        values = nonnull.to_numpy(dtype="float64")
        finite = values[np.isfinite(values)]
        integral = finite.size > 0 and np.all(np.mod(finite, 1) == 0)
        if integral and count > 20 and distinct / count > 0.95:
            return "identifier"
        return "measure"

    text = nonnull.astype(str)
    spaced = text.str.contains(r"\s", regex=True).mean()
    mean_length = text.str.len().mean()
    if distinct == count and count > 20 and spaced < 0.5 and mean_length <= 24:
        return "identifier"
    if distinct <= 50 or distinct / count <= 0.05:
        return "category"
    return "text"


def stats_identifier(nonnull: pd.Series, distinct: int) -> dict:
    text = nonnull.astype(str).str.strip()
    duplicates = int(len(text) - distinct)
    counts = text.value_counts()
    sigs = Counter(signature(v) for v in text.head(5000))
    return {
        "unique": duplicates == 0,
        "duplicates": duplicates,
        "duplicated_values": top_values(counts[counts > 1].head(5)),
        "formats": [{"pattern": p, "count": c} for p, c in sigs.most_common(5)],
        "format_count": len(sigs),
        "sample": text.head(5).tolist(),
    }


def stats_measure(nonnull: pd.Series, distinct: int) -> dict:
    values = pd.to_numeric(nonnull, errors="coerce").dropna()
    q = values.quantile([0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
    finite = values[np.isfinite(values)]
    return {
        "min": num(values.min()),
        "p01": num(q[0.01]),
        "p05": num(q[0.05]),
        "p25": num(q[0.25]),
        "median": num(q[0.5]),
        "p75": num(q[0.75]),
        "p95": num(q[0.95]),
        "p99": num(q[0.99]),
        "max": num(values.max()),
        "mean": num(values.mean()),
        "std": num(values.std()),
        "zeros": int((values == 0).sum()),
        "negatives": int((values < 0).sum()),
        "integral": bool(finite.size and np.all(np.mod(finite, 1) == 0)),
        "largest": [num(v) for v in values.nlargest(5)],
        "smallest": [num(v) for v in values.nsmallest(5)],
    }


def stats_category(nonnull: pd.Series, distinct: int) -> dict:
    text = nonnull.astype(str)
    counts = text.value_counts()
    total = int(counts.sum())
    normalized = text.str.strip().str.lower().str.replace(r"\s+", " ", regex=True)
    variants = []
    for norm, group in text.groupby(normalized):
        forms = sorted(group.unique().tolist())
        if len(forms) > 1:
            variants.append({"normalized": norm, "forms": forms[:6]})
        if len(variants) >= 10:
            break
    return {
        "top_values": top_values(counts.head(TOP_N), total),
        "top1_share": round(float(counts.iloc[0] / total), 4),
        "top5_share": round(float(counts.head(5).sum() / total), 4),
        "singletons": int((counts == 1).sum()),
        "label_variants": variants,
    }


def stats_date(nonnull: pd.Series, distinct: int) -> dict:
    dates = pd.to_datetime(nonnull, errors="coerce").dropna()
    if getattr(dates.dt, "tz", None) is not None:
        dates = dates.dt.tz_localize(None)
    start, end = dates.min(), dates.max()
    months = dates.dt.to_period("M")
    by_month = months.value_counts().sort_index()
    if len(by_month) > MAX_MONTH_BUCKETS:
        by_period = dates.dt.year.value_counts().sort_index()
        buckets = {str(k): int(v) for k, v in by_period.items()}
        bucket_kind = "year"
    else:
        buckets = {str(k): int(v) for k, v in by_month.items()}
        bucket_kind = "month"
    full_range = pd.period_range(start, end, freq="M") if len(dates) else []
    empty_months = [str(p) for p in full_range if p not in set(months)]
    weekday_counts = dates.dt.day_name().value_counts()
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = pd.Timestamp.today().normalize()
    far = int(((dates < pd.Timestamp("1990-01-01")) | (dates > today + pd.Timedelta(days=365))).sum())
    return {
        "start": start.isoformat(),
        "end": end.isoformat(),
        "has_time": bool((dates.dt.normalize() != dates).any()),
        "bucket": bucket_kind,
        "counts_by_bucket": buckets,
        "empty_months": empty_months[:24],
        "empty_month_count": len(empty_months),
        "weekday_counts": {d: int(weekday_counts.get(d, 0)) for d in order},
        "far_values": far,
    }


def stats_text(nonnull: pd.Series, distinct: int) -> dict:
    text = nonnull.astype(str)
    counts = text.value_counts()
    lengths = text.str.len()
    sigs = Counter(signature(v) for v in text.head(2000))
    return {
        "repeated_values": top_values(counts[counts > 1].head(10)),
        "length_min": int(lengths.min()),
        "length_median": num(lengths.median()),
        "length_max": int(lengths.max()),
        "formats": [{"pattern": p, "count": c} for p, c in sigs.most_common(3)],
        "sample": text.head(3).tolist(),
    }


STATS = {
    "identifier": stats_identifier,
    "measure": stats_measure,
    "category": stats_category,
    "date": stats_date,
    "text": stats_text,
}


def coverage_period(columns: list[dict]) -> dict | None:
    dates = [c for c in columns if c["role"] == "date"]
    if not dates:
        return None
    best = max(dates, key=lambda c: c["coverage"])
    return {
        "field": best["name"],
        "start": best["start"],
        "end": best["end"],
        "date_fields": [c["name"] for c in dates],
    }


# ---------------------------------------------------------------------------
# Relationships
# ---------------------------------------------------------------------------


def relationships(loaded: list[tuple[dict, pd.DataFrame | None]]) -> list[dict]:
    tabular = [(src, df) for src, df in loaded if df is not None]
    out = []
    for i in range(len(tabular)):
        for j in range(i + 1, len(tabular)):
            src_a, df_a = tabular[i]
            src_b, df_b = tabular[j]
            roles_a = {normalize(c["name"]): c for c in src_a["columns"]}
            roles_b = {normalize(c["name"]): c for c in src_b["columns"]}
            for key in sorted(set(roles_a) & set(roles_b)):
                col_a, col_b = roles_a[key], roles_b[key]
                if col_a["role"] not in {"identifier", "category"} or col_b["role"] not in {
                    "identifier",
                    "category",
                }:
                    continue
                if col_a["distinct"] < 2 or col_b["distinct"] < 2:
                    continue
                out.append(relationship(src_a, df_a[col_a["name"]], src_b, df_b[col_b["name"]]))
    return out


def relationship(src_a: dict, a: pd.Series, src_b: dict, b: pd.Series) -> dict:
    a_vals = a.dropna().astype(str).str.strip()
    b_vals = b.dropna().astype(str).str.strip()
    a_unique, b_unique = a_vals.is_unique, b_vals.is_unique
    if a_unique and not b_unique:
        src_a, src_b, a_vals, b_vals, a_unique, b_unique = src_b, src_a, b_vals, a_vals, b_unique, a_unique
    a_set, b_set = set(a_vals), set(b_vals)
    a_matched = int(a_vals.isin(b_set).sum())
    b_matched = int(b_vals.isin(a_set).sum())
    if a_unique and b_unique:
        cardinality = "one-to-one"
    elif b_unique:
        cardinality = "many-to-one"
    else:
        cardinality = "many-to-many"
    return {
        "field": a.name if a.name == b.name else f"{a.name} / {b.name}",
        "from": src_a["id"],
        "to": src_b["id"],
        "cardinality": cardinality,
        "from_rows": int(len(a_vals)),
        "from_rows_matched": a_matched,
        "from_rows_unmatched": int(len(a_vals) - a_matched),
        "to_rows": int(len(b_vals)),
        "to_rows_matched": b_matched,
        "to_rows_unmatched": int(len(b_vals) - b_matched),
        "shared_values": len(a_set & b_set),
        "from_only_values": len(a_set - b_set),
        "to_only_values": len(b_set - a_set),
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def signature(value: str) -> str:
    sig = re.sub(r"[A-Za-z]", "A", str(value))
    sig = re.sub(r"\d", "9", sig)
    return sig[:30]


def top_values(counts: pd.Series, total: int | None = None) -> list[dict]:
    out = []
    for value, count in counts.items():
        item = {"value": str(value), "count": int(count)}
        if total:
            item["pct"] = round(float(count) / total, 4)
        out.append(item)
    return out


def num(value):
    if value is None:
        return None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(f) or math.isinf(f):
        return None
    return int(f) if f.is_integer() and abs(f) < 1e15 else round(f, 6)


def records(df: pd.DataFrame) -> list[dict]:
    return [{str(k): clean(v) for k, v in row.items()} for row in df.to_dict(orient="records")]


def rows_as_lists(df: pd.DataFrame) -> list[list]:
    return [[clean(v) for v in row] for row in df.itertuples(index=False, name=None)]


def clean(value):
    if value is None:
        return None
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    if isinstance(value, (int, np.integer)):
        return int(value)
    if isinstance(value, (float, np.floating)):
        f = float(value)
        return None if math.isnan(f) or math.isinf(f) else f
    if isinstance(value, (pd.Timestamp, dt.datetime, dt.date)):
        return value.isoformat()
    if value is pd.NaT or (isinstance(value, float) and math.isnan(value)):
        return None
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, np.ndarray, pd.Series)):
        return [clean(v) for v in list(value)]
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    return value if isinstance(value, str) else str(value)


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


def print_summary(profile: dict, out: Path) -> None:
    for src in profile["sources"]:
        flags = []
        if src.get("hidden"):
            flags.append("hidden")
        if not src.get("tabular"):
            flags.append("non-tabular")
        flag_text = f"  [{', '.join(flags)}]" if flags else ""
        print(f"\n== {src['id']}{flag_text}")
        print(f"   {src['rows']:,} rows x {src['fields']} fields")
        if not src.get("tabular"):
            for row in src.get("raw_sample", [])[:5]:
                print("   | " + " | ".join("" if v is None else str(v)[:20] for v in row))
            for note in src["notes"]:
                print(f"   note: {note}")
            continue
        if src.get("period"):
            p = src["period"]
            print(f"   period: {p['start'][:10]} to {p['end'][:10]} ({p['field']})")
        if src.get("candidate_keys"):
            print(f"   candidate keys: {', '.join(src['candidate_keys'])}")
        for note in src["notes"]:
            print(f"   note: {note}")
        print(f"\n   {'field':<28} {'role':<11} {'cover':>6} {'distinct':>9}  summary")
        for c in src["columns"]:
            print(
                f"   {c['name'][:28]:<28} {c['role']:<11} {c['coverage']:>6.1%} "
                f"{c['distinct']:>9,}  {column_summary(c)}"
            )
    if profile["relationships"]:
        print("\n== Apparent relationships")
        for r in profile["relationships"]:
            share = r["from_rows_matched"] / r["from_rows"] if r["from_rows"] else 0
            print(
                f"   {r['field']}: {r['from']} -> {r['to']} ({r['cardinality']}); "
                f"{r['from_rows_matched']:,} of {r['from_rows']:,} rows matched ({share:.1%})"
            )
    print(f"\nProfile written to {out}")


def column_summary(c: dict) -> str:
    role = c["role"]
    if role == "measure":
        return f"{fmt(c['min'])} to {fmt(c['max'])}, median {fmt(c['median'])}"
    if role == "date":
        return f"{c['start'][:10]} to {c['end'][:10]}"
    if role == "category":
        return ", ".join(f"{v['value'][:18]} {v['pct']:.0%}" for v in c["top_values"][:3])
    if role == "identifier":
        return "unique" if c["unique"] else f"{c['duplicates']:,} duplicates"
    if role == "text":
        return f"length {c['length_min']} to {c['length_max']}"
    return ""


def fmt(value) -> str:
    if value is None:
        return "—"
    if isinstance(value, int) or float(value).is_integer():
        return f"{int(value):,}"
    return f"{value:,.2f}"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("files", nargs="+", help="CSV, XLSX/XLSM or JSON files to profile")
    parser.add_argument("--out", help="Path for the JSON profile (default: fresh file in the OS temp directory)")
    args = parser.parse_args(argv)

    loaded: list[tuple[dict, pd.DataFrame | None]] = []
    for name in args.files:
        path = Path(name)
        if not path.exists():
            parser.error(f"{path} does not exist")
        loaded.extend(load_file(path))

    profile = {
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "files": [str(Path(f).resolve()) for f in args.files],
        "sources": [src for src, _ in loaded],
        "relationships": relationships(loaded),
    }

    out = (
        Path(args.out)
        if args.out
        else Path(tempfile.gettempdir()) / f"eda-profile-{dt.datetime.now():%Y%m%d-%H%M%S}.json"
    )
    out.write_text(json.dumps(clean(profile), indent=2), encoding="utf-8")
    print_summary(profile, out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
