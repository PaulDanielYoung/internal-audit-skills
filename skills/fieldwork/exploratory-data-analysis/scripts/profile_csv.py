# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas>=2.0,<4", "openpyxl>=3.1.5,<4"]
# ///
"""Compatibility entry point for existing CSV drivers; new drivers use profile_table."""
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from profile_table import profile_table, main


def profile_csv(path, *, roles=None, date_formats=None, encoding="utf-8-sig"):
    if Path(path).suffix.lower() != ".csv":
        raise ValueError("Provide one .csv file; use profile_table for XLSX.")
    return profile_table(path, roles=roles, date_formats=date_formats, encoding=encoding)


if __name__ == "__main__":
    raise SystemExit(main())
