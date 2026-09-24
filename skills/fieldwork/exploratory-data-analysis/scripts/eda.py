"""What a driver imports: profiling, locating, the Report, the visuals, and the formatters.

    sys.path.insert(0, "<skill directory>/scripts")
    from eda import profile_table, locate, Report, ALL_FIELDS, bar_chart, line_chart, pie_chart, table, fmt, money, pct

profile_table(path, **choices) reads and profiles the one selected table with the choices the
profiler printed. locate(profile, record, field) names a record in the reader's words. The
Report and the visuals are documented in their own modules.
"""
from __future__ import annotations

from charts import bar_chart, line_chart, pie_chart, table  # noqa: F401
from formatting import fmt, money, pct  # noqa: F401
from profile_table import blank_cells, profile_table  # noqa: F401
from report import ALL_FIELDS, Report  # noqa: F401
from table_source import locate as _locate


def locate(profile: dict, record: int, field: str | None = None) -> str:
    """A record's place in the source for the reader: "record 12" for a CSV, and "row 14"
    or, with a field, "cell C14" for a worksheet."""
    return _locate(profile["source"], [column["name"] for column in profile["columns"]], record, field)
