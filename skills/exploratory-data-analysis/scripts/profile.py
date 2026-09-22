#!/usr/bin/env python3
"""Profile a tabular dataset and write <stem>-eda/profile.json beside it.

Standard library only. Reads CSV/TSV/TXT (delimiter sniffed), JSON (an array
of objects) and XLSX (needs openpyxl; otherwise export the sheet to CSV).

Usage:
    python3 profile.py <path> [--sheet NAME] [--delimiter ,] [--encoding utf-8]
                       [--out DIR] [--max-rows N]

The JSON carries aggregates only: counts, totals, distributions, at most five
sample values per field. Fields that look like personal data are masked.
Raw rows are never written.
"""
import argparse
import csv
import json
import math
import os
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import date, datetime

NUM_RE = re.compile(r"^\(?[-+]?[$€£¥]?\s?\d{1,3}(?:[,\s]\d{3})*(?:\.\d+)?\)?%?$|^\(?[-+]?[$€£¥]?\s?\d+(?:\.\d+)?\)?%?$")
NUM_EU_RE = re.compile(r"^\(?[-+]?[$€£¥]?\s?\d{1,3}(?:\.\d{3})*(?:,\d+)?\)?%?$")
DATE_FORMATS = [
    "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%d %H:%M", "%d/%m/%Y", "%m/%d/%Y", "%d.%m.%Y", "%Y/%m/%d", "%d-%m-%Y",
    "%d/%m/%Y %H:%M", "%m/%d/%Y %H:%M", "%d/%m/%Y %H:%M:%S", "%m/%d/%Y %H:%M:%S",
    "%d-%b-%Y", "%d %b %Y", "%b %d, %Y", "%d %B %Y", "%Y%m%d",
]
BOOL_VALUES = {"true", "false", "yes", "no", "y", "n", "t", "f"}
# Personal data by field name. Business names (vendor, company, product) stay visible.
PII_NAME_RE = re.compile(
    r"(email|e-mail|phone|mobile|\btel\b|address|street|iban|\bbic\b|swift|bank|acct|"
    r"\bssn\b|social|national|passport|\bdob\b|birth|salary|\bcard\b|tax.?id|\btin\b|\bnino\b|\bsin\b|"
    r"account.?(no|num|number|id)|(first|last|full|employee|person|customer|contact|holder|payee|beneficiary).?name|^name$)",
    re.I)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
LONG_DIGITS_RE = re.compile(r"\d{8,}")


# ---------------------------------------------------------------- parsing

def parse_number(s):
    t = s.strip()
    if not t:
        return None
    neg = t.startswith("(") and t.endswith(")")
    t = t.strip("()")
    for sym in "$€£¥%":
        t = t.replace(sym, "")
    t = t.strip()
    if NUM_EU_RE.match(s.strip()) and not NUM_RE.match(s.strip()):
        t = t.replace(".", "").replace(",", ".")
    else:
        t = t.replace(",", "").replace(" ", "")
    try:
        v = float(t)
    except ValueError:
        return None
    return -v if neg else v


def parse_date(s, fmt_hint=None):
    t = s.strip()
    if not t:
        return None
    fmts = [fmt_hint] + DATE_FORMATS if fmt_hint else DATE_FORMATS
    for f in fmts:
        try:
            return datetime.strptime(t, f), f
        except ValueError:
            continue
    return None


def looks_numeric(s):
    t = s.strip()
    return bool(NUM_RE.match(t) or NUM_EU_RE.match(t))


# ---------------------------------------------------------------- loading

def load_rows(path, sheet=None, delimiter=None, encoding="utf-8", max_rows=None):
    ext = os.path.splitext(path)[1].lower()
    meta = {"path": os.path.abspath(path), "file": os.path.basename(path),
            "format": ext.lstrip(".") or "csv", "bytes": os.path.getsize(path)}
    if ext in (".xlsx", ".xlsm"):
        try:
            import openpyxl
        except ImportError:
            sys.exit("openpyxl is not installed: run `pip install openpyxl` or export the sheet to CSV.")
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        ws = wb[sheet] if sheet else wb[wb.sheetnames[0]]
        meta["sheet"], meta["sheets"] = ws.title, wb.sheetnames
        it = ws.iter_rows(values_only=True)
        header = [str(h).strip() if h is not None else f"column_{i+1}" for i, h in enumerate(next(it))]
        rows = []
        for r in it:
            if max_rows and len(rows) >= max_rows:
                break
            if not any(v not in (None, "") for v in r):
                continue
            cells = ["" if v is None else (v.isoformat() if isinstance(v, (datetime, date)) else str(v)) for v in r]
            rows.append(cells[:len(header)] + [""] * (len(header) - len(cells)))
        return header, rows, meta
    if ext == ".json":
        with open(path, encoding=encoding) as f:
            data = json.load(f)
        if isinstance(data, dict):
            data = next((v for v in data.values() if isinstance(v, list)), [])
        header = []
        for rec in data:
            for k in rec.keys():
                if k not in header:
                    header.append(k)
        rows = [["" if rec.get(h) is None else str(rec.get(h)) for h in header] for rec in data[:max_rows or None]]
        return header, rows, meta
    with open(path, encoding=encoding, errors="replace", newline="") as f:
        head = f.read(65536)
        f.seek(0)
        if delimiter is None:
            try:
                delimiter = csv.Sniffer().sniff(head, delimiters=",;\t|").delimiter
            except csv.Error:
                delimiter = "\t" if ext in (".tsv", ".txt") else ","
        meta["delimiter"], meta["encoding"] = delimiter, encoding
        reader = csv.reader(f, delimiter=delimiter)
        header = [h.strip().lstrip("﻿") or f"column_{i+1}" for i, h in enumerate(next(reader))]
        rows = []
        for r in reader:
            if not any(c.strip() for c in r):
                continue
            if max_rows and len(rows) >= max_rows:
                break
            rows.append(r[:len(header)] + [""] * (len(header) - len(r)))
    return header, rows, meta


# ---------------------------------------------------------------- masking

def mask(v):
    v = str(v)
    if EMAIL_RE.match(v):
        local, _, dom = v.partition("@")
        return local[:1] + "***@" + dom
    if LONG_DIGITS_RE.search(v):
        return LONG_DIGITS_RE.sub(lambda m: "*" * (len(m.group()) - 4) + m.group()[-4:], v)
    return " ".join(w[:1] + "*" * max(len(w) - 1, 1) for w in v.split()) if v.split() else v


def is_pii(name, values):
    if PII_NAME_RE.search(name):
        return True
    sample = values[:200]
    if not sample:
        return False
    if sum(1 for v in sample if EMAIL_RE.match(v)) / len(sample) > 0.5:
        return True
    if sum(1 for v in sample if LONG_DIGITS_RE.search(v)) / len(sample) > 0.5 and not re.search(r"(id|no|number|ref)$", name, re.I):
        return True
    return False


# ---------------------------------------------------------------- profiling

def histogram(values, bins=12):
    lo, hi = min(values), max(values)
    if lo == hi:
        return [{"from": lo, "to": hi, "count": len(values)}]
    width = (hi - lo) / bins
    counts = [0] * bins
    for v in values:
        counts[min(int((v - lo) / width), bins - 1)] += 1
    return [{"from": round(lo + i * width, 2), "to": round(lo + (i + 1) * width, 2), "count": c} for i, c in enumerate(counts)]


def percentile(sorted_vals, p):
    k = (len(sorted_vals) - 1) * p
    f, c = math.floor(k), math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def profile_field(name, position, values, n_rows):
    non_blank = [v for v in values if v.strip() != ""]
    non_null = len(non_blank)
    field = {"name": name, "position": position, "non_null": non_null,
             "null_count": n_rows - non_null, "null_pct": round(100 * (n_rows - non_null) / n_rows, 1) if n_rows else 0}
    flags = []
    if non_null == 0:
        field.update({"inferred_type": "blank", "distinct": 0})
        return field
    stripped = [v.strip() for v in non_blank]
    if any(v != s for v, s in zip(non_blank, stripped)):
        flags.append("leading or trailing whitespace")
    counter = Counter(stripped)
    distinct = len(counter)
    field["distinct"] = distinct
    field["distinct_pct"] = round(100 * distinct / non_null, 1)
    pii = is_pii(name, stripped)
    field["pii"] = pii
    fmt = mask if pii else (lambda v: v)

    sample = stripped[:2000]
    total = len(sample)
    n_num = sum(1 for v in sample if looks_numeric(v))
    n_bool = sum(1 for v in sample if v.lower() in BOOL_VALUES)
    date_hint, n_date = None, 0
    for v in sample:
        r = parse_date(v, date_hint)
        if r:
            n_date += 1
            date_hint = r[1]

    if n_bool / total > 0.95:
        field["inferred_type"] = "boolean"
        field["top_values"] = [{"value": fmt(k), "count": c} for k, c in counter.most_common(5)]
    elif n_date / total > 0.9 and n_num / total < 0.9:
        field["inferred_type"] = "date"
        parsed, unparsed = [], 0
        for v in stripped:
            r = parse_date(v, date_hint)
            if r:
                parsed.append(r[0])
            else:
                unparsed += 1
        if unparsed:
            flags.append(f"{unparsed} values do not parse as dates")
        field["date_format"] = date_hint
        field["min"], field["max"] = min(parsed).isoformat(), max(parsed).isoformat()
        field["span_days"] = (max(parsed) - min(parsed)).days
        has_time = any(d.hour or d.minute or d.second for d in parsed)
        field["has_time"] = has_time
        by_month = Counter(d.strftime("%Y-%m") for d in parsed)
        field["by_month"] = [{"period": k, "count": by_month[k]} for k in sorted(by_month)]
        by_dow = Counter(d.strftime("%a") for d in parsed)
        field["by_weekday"] = [{"day": d, "count": by_dow.get(d, 0)} for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]]
        field["weekend_count"] = by_dow.get("Sat", 0) + by_dow.get("Sun", 0)
        if has_time:
            by_hour = Counter(d.hour for d in parsed)
            field["by_hour"] = [{"hour": h, "count": by_hour.get(h, 0)} for h in range(24)]
        future = sum(1 for d in parsed if d > datetime.now())
        old = sum(1 for d in parsed if d.year < 1990)
        if future:
            flags.append(f"{future} dates in the future")
        if old:
            flags.append(f"{old} dates before 1990")
    elif n_num / total > 0.9:
        nums, unparsed = [], 0
        for v in stripped:
            x = parse_number(v)
            if x is None:
                unparsed += 1
            else:
                nums.append(x)
        if unparsed:
            flags.append(f"{unparsed} values do not parse as numbers")
        if any(c in v for v in sample[:200] for c in "$€£¥,"):
            flags.append("numbers stored as text with symbols or separators")
        all_int = all(float(x).is_integer() for x in nums)
        id_like = all_int and distinct / non_null > 0.9 and non_null > 20 and len({len(v) for v in sample}) <= 2
        if id_like:
            field["inferred_type"] = "id"
        else:
            field["inferred_type"] = "number"
            s = sorted(nums)
            field.update({
                "min": s[0], "max": s[-1], "sum": round(sum(s), 2),
                "mean": round(statistics.fmean(s), 4), "median": percentile(s, 0.5),
                "p05": round(percentile(s, 0.05), 4), "p95": round(percentile(s, 0.95), 4),
                "std": round(statistics.pstdev(s), 4) if len(s) > 1 else 0,
                "zeros": sum(1 for x in s if x == 0), "negatives": sum(1 for x in s if x < 0),
                "integers_only": all_int,
                "round_hundreds": sum(1 for x in s if x != 0 and x % 100 == 0),
                "round_thousands": sum(1 for x in s if x != 0 and x % 1000 == 0),
                "histogram": histogram(s),
            })
            if len(s) >= 300 and s[0] >= 0 and s[-1] / max(s[len(s) // 2], 1e-9) > 10:
                first = Counter(str(abs(x)).lstrip("0.")[:1] for x in s if x != 0)
                tot = sum(first.values())
                field["first_digit"] = [{"digit": str(d), "share": round(first.get(str(d), 0) / tot, 4),
                                         "benford": round(math.log10(1 + 1 / d), 4)} for d in range(1, 10)]
            if distinct <= 20:
                field["top_values"] = [{"value": k, "count": c} for k, c in counter.most_common(10)]
    else:
        avg_len = sum(len(v) for v in sample) / total
        lens = {len(v) for v in sample}
        if distinct / non_null > 0.95 and non_null > 20 and (len(lens) <= 3 or avg_len < 24):
            field["inferred_type"] = "id"
        elif distinct <= 50 or distinct / non_null <= 0.05:
            field["inferred_type"] = "category"
        else:
            field["inferred_type"] = "text"
        field["avg_length"] = round(avg_len, 1)
        field["max_length"] = max(len(v) for v in stripped)
        lower = defaultdict(set)
        for k in counter:
            lower[k.lower()].add(k)
        variants = [sorted(v) for v in lower.values() if len(v) > 1]
        if variants:
            flags.append(f"{len(variants)} values differ only by case, e.g. {' / '.join(fmt(x) for x in variants[0][:3])}")
        if field["inferred_type"] != "id":
            top = counter.most_common(10)
            field["top_values"] = [{"value": fmt(k), "count": c} for k, c in top]
            field["top10_pct"] = round(100 * sum(c for _, c in top) / non_null, 1)
    if field.get("inferred_type") == "id":
        dup = sum(c - 1 for c in counter.values() if c > 1)
        field["duplicate_values"] = dup
        if dup:
            flags.append(f"{dup} repeated values in an id field")
        m = [re.match(r"^(.*?)(\d+)$", v) for v in stripped]
        if all(m) and len({x.group(1) for x in m}) <= 3:
            by_num = {int(x.group(2)): x.group(0) for x in m}
            nums = sorted(by_num)
            span = nums[-1] - nums[0] + 1
            gaps = span - len(nums)
            contiguous = len(nums) / span >= 0.5
            field["sequence"] = {"first": by_num[nums[0]], "last": by_num[nums[-1]], "missing": gaps,
                                 "contiguous": contiguous, "prefixes": sorted({x.group(1) for x in m})}
            if contiguous and gaps:
                flags.append(f"{gaps} gaps in the number sequence")
    field["samples"] = [fmt(v) for v in list(dict.fromkeys(stripped))[:5]]
    if distinct == 1 and non_null > 1:
        flags.append("constant: a single value")
    if field["null_pct"] > 50:
        flags.append("more than half blank")
    if flags:
        field["flags"] = flags
    return field


def amount_field(fields):
    nums = [f for f in fields if f.get("inferred_type") == "number"]
    if not nums:
        return None
    pref = [f for f in nums if re.search(r"amount|total|value|net|gross|debit|credit|price|cost|sum|balance", f["name"], re.I)]
    return max(pref or nums, key=lambda f: abs(f.get("sum") or 0))


def date_field(fields):
    dates = [f for f in fields if f.get("inferred_type") == "date"]
    if not dates:
        return None
    pref = [f for f in dates if re.search(r"post|entry|created|trans|booking|doc", f["name"], re.I)]
    return max(pref or dates, key=lambda f: f["non_null"])


def dataset_flags(header, rows, fields):
    flags = []
    n = len(rows)
    tup = Counter(tuple(c.strip() for c in r) for r in rows)
    dups = sum(c - 1 for c in tup.values() if c > 1)
    if dups:
        flags.append({"flag": "exact duplicate rows", "count": dups})
    repeats = tup.get(tuple(h.strip() for h in header), 0)
    if repeats:
        flags.append({"flag": "header row repeated inside the data", "count": repeats})
    for f in fields:
        for fl in f.get("flags", []):
            flags.append({"flag": fl, "field": f["name"]})
    keys = [f["name"] for f in fields if f.get("distinct") == n and f["non_null"] == n]
    return flags, keys, dups


def crosstabs(header, rows, fields, amt, limit_fields=4):
    if not amt:
        return []
    ai = header.index(amt["name"])
    cats = [f for f in fields if f.get("inferred_type") in ("category", "boolean") and not f.get("pii")]
    cats = sorted(cats, key=lambda f: f["distinct"], reverse=True)[:limit_fields]
    out = []
    for f in cats:
        ci = header.index(f["name"])
        sums, counts = Counter(), Counter()
        for r in rows:
            k = r[ci].strip() or "(blank)"
            counts[k] += 1
            v = parse_number(r[ai]) if r[ai].strip() else None
            if v is not None:
                sums[k] += v
        total = sum(sums.values()) or 1
        top = sums.most_common(10)
        out.append({"field": f["name"], "amount_field": amt["name"], "distinct": f["distinct"],
                    "rows": [{"value": k, "count": counts[k], "sum": round(v, 2), "share": round(v / total, 4)} for k, v in top],
                    "other_sum": round(total - sum(v for _, v in top), 2)})
    return out


def time_series(header, rows, dt, amt):
    if not dt:
        return None
    di = header.index(dt["name"])
    ai = header.index(amt["name"]) if amt else None
    by = defaultdict(lambda: {"count": 0, "sum": 0.0})
    for r in rows:
        p = parse_date(r[di], dt.get("date_format")) if r[di].strip() else None
        if not p:
            continue
        k = p[0].strftime("%Y-%m")
        by[k]["count"] += 1
        if ai is not None and r[ai].strip():
            v = parse_number(r[ai])
            if v is not None:
                by[k]["sum"] += v
    return {"date_field": dt["name"], "amount_field": amt["name"] if amt else None, "granularity": "month",
            "series": [{"period": k, "count": by[k]["count"], "sum": round(by[k]["sum"], 2)} for k in sorted(by)]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--sheet", help="worksheet name (XLSX); default is the first sheet")
    ap.add_argument("--delimiter", help="field delimiter; default is sniffed")
    ap.add_argument("--encoding", default="utf-8")
    ap.add_argument("--out", help="output directory (default: <stem>-eda beside the file)")
    ap.add_argument("--max-rows", type=int, help="profile only the first N rows")
    a = ap.parse_args()

    header, rows, meta = load_rows(a.path, a.sheet, a.delimiter, a.encoding, a.max_rows)
    n = len(rows)
    meta.update({"rows": n, "columns": len(header), "profiled_at": datetime.now().isoformat(timespec="seconds"),
                 "truncated_to": a.max_rows})
    cols = list(zip(*rows)) if rows else [[] for _ in header]
    fields = [profile_field(h, i, list(cols[i]), n) for i, h in enumerate(header)]
    flags, keys, dups = dataset_flags(header, rows, fields)
    amt, dt = amount_field(fields), date_field(fields)
    profile = {
        "source": meta,
        "fields": fields,
        "key_candidates": keys,
        "primary_amount_field": amt["name"] if amt else None,
        "primary_date_field": dt["name"] if dt else None,
        "time_series": time_series(header, rows, dt, amt),
        "crosstabs": crosstabs(header, rows, fields, amt),
        "dataset_flags": flags,
        "duplicate_rows": dups,
        "blank_cells_pct": round(100 * sum(f["null_count"] for f in fields) / (n * len(header)), 1) if n and header else 0,
    }
    stem = os.path.splitext(os.path.basename(a.path))[0]
    out_dir = a.out or os.path.join(os.path.dirname(os.path.abspath(a.path)), f"{stem}-eda")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "profile.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=1, default=str)

    print(f"profile: {out}")
    print(f"rows {n}  columns {len(header)}  duplicate rows {dups}  blank cells {profile['blank_cells_pct']}%")
    print(f"primary date: {profile['primary_date_field']}  primary amount: {profile['primary_amount_field']}  key candidates: {keys or 'none'}")
    print(f"{'field':<28}{'type':<10}{'null%':>7}{'distinct':>10}  notes")
    for f in fields:
        note = "; ".join(f.get("flags", []))
        if f.get("pii"):
            note = ("masked as personal data; " + note).rstrip("; ")
        print(f"{f['name'][:27]:<28}{f.get('inferred_type', '?'):<10}{f['null_pct']:>7}{f.get('distinct', 0):>10}  {note}")


if __name__ == "__main__":
    main()
