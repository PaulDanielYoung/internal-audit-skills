"""Report derives the mechanical conditions and coverage spans; the driver explains them."""
import re

import pytest

from profiles import column, meanings, profile
from report import ALL_FIELDS, Report


def report(prof, **kwargs):
    return Report(prof, "Orders", description="One record per order line.", meanings=meanings(prof), **kwargs)


def explain_all(r, why="It changes the denominator."):
    for condition in r.conditions:
        r.explain(condition.field, condition.kind, why)
    for span in r.spans:
        r.explain(span.field, "span", why)


def page(r, tmp_path):
    return r.write(tmp_path / "report.html").read_text(encoding="utf-8")


def keys(r):
    return {(c.field, c.kind) for c in r.conditions}


# --- Deriving mechanical conditions ------------------------------------------------------

def test_clean_profile_has_no_mechanical_conditions_or_spans():
    r = report(profile([column("id", "identifier", duplicates=0), column("amount", "measure")]))
    assert r.conditions == [] and r.spans == []


def test_blank_cells_and_entirely_blank_fields_are_completeness_conditions():
    prof = profile([column("note", blank=7), column("unused", blank=100)])
    r = report(prof)
    by_key = {(c.field, c.kind): c for c in r.conditions}
    assert by_key[("note", "blank")].area == "Completeness"
    assert by_key[("note", "blank")].observation == "Blank"
    assert by_key[("note", "blank")].affected == 7
    assert by_key[("unused", "blank_field")].observation == "Entirely blank"
    assert by_key[("unused", "blank_field")].affected == 100
    assert ("unused", "blank") not in by_key


def test_unparsed_values_name_the_expected_type_in_reader_words():
    prof = profile([
        column("amount", "measure", parse_failures=3),
        column("opened", "date", parse_failures=2, start="2024-01-01", end="2024-12-31"),
        column("fiscal_year", "year", parse_failures=1),
        column("period", "month", parse_failures=1),
    ])
    observations = {c.field: c.observation for c in report(prof).conditions if c.kind == "unparsed"}
    assert observations == {
        "amount": "Does not parse as a number",
        "opened": "Does not parse as a date",
        "fiscal_year": "Does not parse as a year",
        "period": "Does not parse as a month",
    }
    assert all(c.area == "Validity" for c in report(prof).conditions if c.kind == "unparsed")


def test_excel_errors_and_out_of_range_parts_are_validity_conditions():
    prof = profile([
        column("total", "measure", source_errors=4),
        column("month", "month", expected_range=[1, 12], outside_range=2),
    ])
    by_key = {(c.field, c.kind): c for c in report(prof).conditions}
    assert by_key[("total", "source_error")].observation == "Excel error value"
    assert by_key[("total", "source_error")].affected == 4
    assert by_key[("month", "outside_range")].observation == "Outside 1 to 12"
    assert by_key[("month", "outside_range")].area == "Validity"


def test_case_variants_repeated_identifiers_and_record_conditions():
    prof = profile(
        [
            column("status", "category", case_variants={"count": 9, "groups": [[{"value": "Open", "count": 5}, {"value": "open", "count": 4}]]}),
            column("order_id", "identifier", duplicates=12),
        ],
        blank_records=2, duplicate_records=3,
    )
    by_key = {(c.field, c.kind): c for c in report(prof).conditions}
    assert by_key[("status", "case_variants")].area == "Consistency"
    assert by_key[("status", "case_variants")].affected == 9
    assert by_key[("order_id", "duplicate_id")].area == "Uniqueness"
    assert by_key[("order_id", "duplicate_id")].affected == 12
    assert by_key[(ALL_FIELDS, "blank_record")].area == "Completeness"
    assert by_key[(ALL_FIELDS, "blank_record")].affected == 2
    assert by_key[(ALL_FIELDS, "duplicate_record")].area == "Uniqueness"
    assert by_key[(ALL_FIELDS, "duplicate_record")].affected == 3


def test_empty_table_has_no_conditions():
    prof = profile([column("id", "identifier", rows=0), column("amount", "measure", rows=0)], rows=0)
    r = report(prof)
    assert r.conditions == [] and r.spans == []


# --- Deriving coverage spans -------------------------------------------------------------

def test_date_fields_with_values_become_spans():
    prof = profile([
        column("opened", "date", blank=10, start="2023-02-01", end="2024-11-30"),
        column("closed", "date", blank=100),
        column("fiscal_year", "year", min=2021, max=2024),
    ])
    spans = {s.field: s for s in report(prof).spans}
    assert set(spans) == {"opened"}
    assert (spans["opened"].start, spans["opened"].end, spans["opened"].records) == ("2023-02-01", "2024-11-30", 90)


# --- Explaining --------------------------------------------------------------------------

def test_write_refuses_until_every_mechanical_condition_and_span_is_explained(tmp_path):
    prof = profile([column("note", blank=5), column("opened", "date", start="2024-01-01", end="2024-06-30")])
    r = report(prof)
    r.no_overview("Nothing to chart.")
    with pytest.raises(ValueError, match=r"note.*blank") as excinfo:
        r.write(tmp_path / "report.html")
    assert "opened" in str(excinfo.value) and "span" in str(excinfo.value)
    r.explain("note", "blank", "Notes are optional; counts by note exclude these records.")
    with pytest.raises(ValueError, match="opened"):
        r.write(tmp_path / "report.html")
    r.explain("opened", "span", "The file covers the first half of 2024.")
    assert r.write(tmp_path / "report.html").exists()


def test_explain_rejects_unknown_keys_blank_reasons_and_repeats():
    r = report(profile([column("note", blank=5)]))
    with pytest.raises(ValueError, match="amount"):
        r.explain("amount", "blank", "why")
    with pytest.raises(ValueError, match="unparsed"):
        r.explain("note", "unparsed", "why")
    with pytest.raises(ValueError):
        r.explain("note", "blank", "   ")
    r.explain("note", "blank", "Optional field.")
    with pytest.raises(ValueError, match="already"):
        r.explain("note", "blank", "Again.")


def test_explained_condition_renders_with_its_reason(tmp_path):
    r = report(profile([column("note", blank=5)]))
    r.explain("note", "blank", "Notes are optional.", always_show=True)
    r.no_overview("Nothing to chart.")
    html = page(r, tmp_path)
    assert "Notes are optional." in html
    assert "5 (5.0%)" in html
    assert "<details>" not in html


# --- Driver-recorded conditions ------------------------------------------------------------

def test_quality_validates_area_field_and_count():
    r = report(profile([column("amount", "measure")]))
    with pytest.raises(ValueError, match="Area"):
        r.quality("Accuracy", "amount", "Placeholder", 1, "why")
    with pytest.raises(ValueError, match="field"):
        r.quality("Validity", "total", "Placeholder", 1, "why")
    with pytest.raises(ValueError, match="0 to 100"):
        r.quality("Validity", "amount", "Placeholder", 101, "why")
    with pytest.raises(ValueError, match="0 to 100"):
        r.quality("Validity", "amount", "Placeholder", True, "why")
    r.quality("Validity", "amount", "Placeholder number", 3, "Excluded from totals.")
    r.quality("Uniqueness", ALL_FIELDS, "Near-duplicate record", 2, "Counts overstate activity.")


def test_conditions_below_threshold_collapse_unless_always_shown(tmp_path):
    r = report(profile([column("amount", "measure")], rows=1000))
    r.quality("Validity", "amount", "Placeholder number", 5, "Small but excluded.")
    r.quality("Validity", "amount", "Negative amount", 1, "A refund in a sales file.", always_show=True)
    r.no_overview("Nothing to chart.")
    html = page(r, tmp_path)
    assert re.search(r"<details><summary>1 condition affecting less than 1% of records</summary>.*Placeholder number", html, re.S)
    assert html.index("Negative amount") < html.index("<details>")


def test_checked_notes_and_untouched_areas_read_as_tested(tmp_path):
    r = report(profile([column("amount", "measure")]))
    r.checked("Uniqueness", "No two records share an order and line number.")
    r.no_overview("Nothing to chart.")
    html = page(r, tmp_path)
    assert "Checked: No two records share an order and line number." in html
    assert html.count("Checked; nothing to report.") == 4


def test_checked_rejects_unknown_area_and_blank_note():
    r = report(profile([column("amount", "measure")]))
    with pytest.raises(ValueError):
        r.checked("Accuracy", "note")
    with pytest.raises(ValueError):
        r.checked("Validity", " ")


# --- Coverage --------------------------------------------------------------------------------

def test_coverage_spans_render_before_gap_conditions(tmp_path):
    prof = profile([column("opened", "date", blank=10, start="2023-02-01", end="2024-11-30"), column("period", "category")])
    r = report(prof)
    r.explain("opened", "span", "Two years of orders.")
    r.explain("opened", "blank", "Undated orders drop out of the timeline.")
    r.coverage("period", "FY23 Q1", "FY24 Q4", 100, "Eight fiscal quarters.")
    r.quality("Coverage", "opened", "No records in March 2024", 0, "A month is missing.", always_show=True)
    r.no_overview("Nothing to chart.")
    html = page(r, tmp_path)
    coverage = html[html.index("<h3>Coverage</h3>"):]
    assert coverage.index("Spans 2023-02-01 to 2024-11-30") < coverage.index("No records in March 2024")
    assert "Spans FY23 Q1 to FY24 Q4" in coverage
    assert "90 with a value (90.0%)" in coverage
    assert "Records with a value" in coverage


def test_coverage_validates_records_and_text():
    r = report(profile([column("period", "category")]))
    with pytest.raises(ValueError):
        r.coverage("period", "FY23", "FY24", 101, "why")
    with pytest.raises(ValueError, match="field"):
        r.coverage("opened", "2023", "2024", 10, "why")
    with pytest.raises(ValueError):
        r.coverage("period", "", "FY24", 10, "why")


# --- Sections and validation timing ----------------------------------------------------------

def test_sections_appear_in_order_and_optional_ones_only_when_used(tmp_path):
    r = report(profile([column("amount", "measure")]))
    r.no_overview("Nothing to chart.")
    html = page(r, tmp_path)
    headings = re.findall(r"<h2>(.*?)</h2>", html)
    assert headings == ["What the file contains", "Data quality", "Data overview"]
    r.limitation("Amounts lack a currency.")
    html = page(r, tmp_path)
    assert re.findall(r"<h2>(.*?)</h2>", html)[-1] == "Analysis limitations"


def test_limitation_rejects_blank_text():
    r = report(profile([column("amount", "measure")]))
    with pytest.raises(ValueError):
        r.limitation("  ")


def test_overview_and_no_overview_conflict_is_rejected_when_added():
    r = report(profile([column("amount", "measure")]))
    r.no_overview("Nothing to chart.")
    with pytest.raises(ValueError, match="already"):
        r.no_overview("Still nothing.")


def test_write_needs_an_overview_or_a_reason(tmp_path):
    r = report(profile([column("amount", "measure")]))
    with pytest.raises(ValueError, match="overview"):
        r.write(tmp_path / "report.html")


def test_header_shows_counts_facts_and_xlsx_source_context(tmp_path):
    source = {
        "format": "xlsx", "sheet": "Data", "sheet_state": "visible", "range": "A1:C101", "table": "Orders",
        "header_row": 1, "first_column": 1, "last_data_row": 101, "totals_rows_excluded": [102],
        "hidden_rows_included": [5], "hidden_columns_included": [], "filters": [], "date_epoch": "1899-12-30T00:00:00",
    }
    prof = profile([column("amount", "measure")], source=source, path="/data/orders.xlsx", blank_records=1)
    r = report(prof, facts=["12 customers"])
    r.explain(ALL_FIELDS, "blank_record", "One blank row inside the selected range.")
    r.no_overview("Nothing to chart.")
    html = page(r, tmp_path)
    assert "100 records · 1 fields · 12 customers" in html
    assert "worksheet Data, range A1:C101" in html
    assert "Excel Table: Orders." in html
    assert "Included 1 hidden data row and 0 hidden columns." in html
    assert "totals row excluded from records: 102." in html
    assert "Retained" not in html  # the blank-record condition carries this now
