"""The source table adapter: CSV and XLSX differ behind it, not in front of it."""
import csv

import pytest
from openpyxl import Workbook

from profile_table import ROLES, profile_table
from table_source import SourceTable, locate, read_table


@pytest.fixture
def csv_path(tmp_path):
    path = tmp_path / "orders.csv"
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["id", "amount", "note"])
        writer.writerow(["A1", "10", "x"])
        writer.writerow([])
        writer.writerow(["A2", "20", ""])
        writer.writerow(["A1", "10", "x"])
    return path


@pytest.fixture
def xlsx_path(tmp_path):
    path = tmp_path / "orders.xlsx"
    book = Workbook()
    sheet = book.active
    sheet.title = "Data"
    sheet["B2"], sheet["C2"], sheet["D2"] = "id", "amount", "note"
    rows = [("A1", 10, "x"), ("A2", "10", "y"), ("A1", 10, "x"), ("A4", 0.5, "#N/A"), ("A5", 12, "z")]
    for offset, row in enumerate(rows, start=3):
        sheet.cell(row=offset, column=2, value=row[0])
        sheet.cell(row=offset, column=3, value=row[1])
        sheet.cell(row=offset, column=4, value=row[2])
    sheet["C6"].number_format = "0.00%"
    sheet.row_dimensions[5].hidden = True
    book.save(path)
    return path


def names(loaded):
    return list(loaded.raw.columns)


# --- CSV adapter ---------------------------------------------------------------------------

def test_csv_adapter_locates_records_counts_duplicates_and_discloses_skipped_lines(csv_path):
    loaded = read_table(csv_path)
    assert isinstance(loaded, SourceTable)
    assert loaded.source["format"] == "csv"
    assert loaded.duplicate_records() == 1
    assert locate(loaded.source, names(loaded), 2) == "record 2"
    assert locate(loaded.source, names(loaded), 2, "amount") == "record 2"
    assert loaded.location(2, "amount") == {"record": 2}
    assert loaded.source["disclosures"] == ["1 empty line outside quoted fields was skipped."]
    assert loaded.field_facts("amount") == {}


def test_csv_rejects_xlsx_selections(csv_path):
    with pytest.raises(ValueError, match="only to XLSX"):
        read_table(csv_path, sheet="Data")


# --- XLSX adapter --------------------------------------------------------------------------

def test_xlsx_adapter_locates_by_row_and_cell(xlsx_path):
    loaded = read_table(xlsx_path, sheet="Data", cell_range="B2:D7")
    assert locate(loaded.source, names(loaded), 1) == "row 3"
    assert locate(loaded.source, names(loaded), 4, "note") == "cell D6"
    assert loaded.location(4, "note") == {"record": 4, "sheet": "Data", "row": 6, "cell": "D6"}


def test_xlsx_duplicates_respect_cell_types(xlsx_path):
    loaded = read_table(xlsx_path, sheet="Data", cell_range="B2:D7")
    assert loaded.duplicate_records() == 1  # A1/10/x twice; A2 holds the text "10", so it is distinct


def test_xlsx_disclosures_describe_the_selection_in_reader_words(xlsx_path):
    loaded = read_table(xlsx_path, sheet="Data", cell_range="B2:D7")
    text = " ".join(loaded.source["disclosures"])
    assert "worksheet Data, range B2:D7" in text
    assert "1 hidden data row" in text
    assert "regardless of visibility or filters" in text


def test_xlsx_field_facts_carry_cell_exceptions_into_the_profile(xlsx_path):
    loaded = read_table(xlsx_path, sheet="Data", cell_range="B2:D7")
    facts = loaded.field_facts("amount")
    assert facts["cell_exceptions"]["count"] == 2
    assert {item["cell"] for item in facts["cell_exceptions"]["examples"]} == {"C4", "C6"}
    assert "number_formats" in facts and "cell_types" in facts
    raw, data, profile = profile_table(xlsx_path, sheet="Data", cell_range="B2:D7")
    assert "cells" not in raw.attrs
    amount = next(field for field in profile["columns"] if field["name"] == "amount")
    assert amount["cell_exceptions"]["count"] == 2


def test_xlsx_rejects_an_encoding(xlsx_path):
    with pytest.raises(ValueError, match="encoding"):
        read_table(xlsx_path, sheet="Data", encoding="latin-1")
    with pytest.raises(ValueError, match="encoding"):
        profile_table(xlsx_path, sheet="Data", encoding="latin-1")


def test_xlsx_errors_are_source_errors_not_text(xlsx_path):
    raw, data, profile = profile_table(xlsx_path, sheet="Data", cell_range="B2:D7")
    note = next(field for field in profile["columns"] if field["name"] == "note")
    assert note["source_errors"] == 1
    assert note["error_examples"][0]["cell"] == "D6"


# --- Profile: choices and disclosures ---------------------------------------------------------

def test_profile_records_the_choices_it_applied(csv_path, xlsx_path):
    raw, data, profile = profile_table(csv_path, roles={"id": "identifier"})
    assert profile["choices"] == {"roles": {"id": "identifier"}, "date_formats": {}, "encoding": "utf-8-sig"}
    raw, data, profile = profile_table(xlsx_path, sheet="Data", cell_range="B2:D7", date_formats={})
    assert profile["choices"] == {"sheet": "Data", "cell_range": "B2:D7", "roles": {}, "date_formats": {}}
    assert profile["source"]["disclosures"]


def test_empty_is_a_role_the_driver_can_repeat(tmp_path):
    path = tmp_path / "blank.csv"
    path.write_text("id,unused\nA1,\nA2,\n", encoding="utf-8")
    assert "empty" in ROLES
    raw, data, profile = profile_table(path)
    assert profile["columns"][1]["role"] == "empty"
    raw, data, profile = profile_table(path, roles={"unused": "empty"})
    assert profile["columns"][1]["role"] == "empty"


def test_profile_has_no_format_specific_top_level_keys(csv_path):
    raw, data, profile = profile_table(csv_path)
    assert "empty_lines_skipped" not in profile
    assert profile["duplicate_records"] == 1
    assert profile["source"]["disclosures"] == ["1 empty line outside quoted fields was skipped."]


def test_iso_dates_profile_as_dates_with_a_span(tmp_path):
    path = tmp_path / "dated.csv"
    path.write_text("id,opened\nA1,2024-01-05\nA2,2024-03-09\nA3,\n", encoding="utf-8")
    raw, data, profile = profile_table(path)
    opened = profile["columns"][1]
    assert (opened["role"], opened["start"], opened["end"], opened["blank"]) == ("date", "2024-01-05", "2024-03-09", 1)
    raw, data, profile = profile_table(path, date_formats={"opened": "%Y-%m-%d"})
    assert profile["choices"]["date_formats"] == {"opened": "%Y-%m-%d"}
