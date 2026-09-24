"""Hand-built profiles in the shape profile_table() returns, for tests that need no file."""


def column(name, role="text", *, rows=100, blank=0, parse_failures=0, source_errors=0, **more):
    entry = {
        "name": name, "role": role, "blank": blank, "distinct": 0,
        "parsed": rows - blank - parse_failures - source_errors,
        "parse_failures": parse_failures, "source_errors": source_errors,
        "failure_examples": [], "error_examples": [],
    }
    entry.update(more)
    return entry


def profile(columns, *, rows=100, blank_records=0, duplicate_records=0, source=None, path="/data/orders.csv"):
    return {
        "file": path.rsplit("/", 1)[-1], "path": path, "generated": "2026-09-24T00:00:00",
        "rows": rows, "fields": len(columns), "duplicate_records": duplicate_records,
        "empty_lines_skipped": 0, "columns": columns,
        "source": source or {"format": "csv", "empty_lines_skipped": 0},
        "blank_records": blank_records, "entity_fields": [], "sample": [],
    }


def meanings(prof):
    return {field["name"]: f"what {field['name']} holds" for field in prof["columns"]}
