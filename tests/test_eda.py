"""The driver's one entry point, the choices it copies, and what the report discloses."""
import ast
from pathlib import Path

import eda
from profiles import column, meanings, profile

SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "fieldwork" / "exploratory-data-analysis" / "scripts"


def test_eda_exposes_everything_the_driver_uses():
    for name in ("profile_table", "blank_cells", "locate", "Report", "ALL_FIELDS",
                 "bar_chart", "line_chart", "pie_chart", "table", "fmt", "money", "pct"):
        assert hasattr(eda, name), name


def test_locate_works_from_the_profile_alone(tmp_path):
    path = tmp_path / "orders.csv"
    path.write_text("id,amount\nA1,1\nA2,2\n", encoding="utf-8")
    raw, data, prof = eda.profile_table(path)
    assert eda.locate(prof, 2) == "record 2"
    assert eda.locate(prof, 2, "amount") == "record 2"
    prof["source"] = {"format": "xlsx", "sheet": "Data", "header_row": 2, "first_column": 2}
    assert eda.locate(prof, 3) == "row 5"
    assert eda.locate(prof, 3, "amount") == "cell C5"


def test_profiler_prints_the_choices_line_the_driver_pastes(tmp_path, capsys):
    from profile_table import main
    path = tmp_path / "orders.csv"
    path.write_text("id,opened\nA1,05/01/2024\n", encoding="utf-8")
    main([str(path), "--role", "id=identifier", "--date-format", "opened=%d/%m/%Y"])
    line = next(line for line in capsys.readouterr().out.splitlines() if line.startswith("choices = "))
    choices = ast.literal_eval(line.removeprefix("choices = "))
    assert choices == {"roles": {"id": "identifier"}, "date_formats": {"opened": "%d/%m/%Y"}, "encoding": "utf-8-sig"}
    raw, data, prof = eda.profile_table(path, **choices)
    assert prof["choices"] == choices


def test_report_discloses_role_and_date_format_overrides(tmp_path):
    prof = profile([column("account", "identifier"), column("opened", "date", start="2024-01-05", end="2024-01-05")])
    prof["choices"] = {"roles": {"account": "identifier"}, "date_formats": {"opened": "%d/%m/%Y"}, "encoding": "utf-8-sig"}
    r = eda.Report(prof, "Orders", description="One record per order.", meanings=meanings(prof))
    r.explain("opened", "span", "One day.")
    r.no_overview("Nothing to chart.")
    html = r.write(tmp_path / "report.html").read_text(encoding="utf-8")
    assert "account read as an identifier" in html
    assert "opened read as dates written day/month/year" in html
    prof["choices"] = {"roles": {}, "date_formats": {}, "encoding": "utf-8-sig"}
    r = eda.Report(prof, "Orders", description="One record per order.", meanings=meanings(prof))
    r.explain("opened", "span", "One day.")
    r.no_overview("Nothing to chart.")
    assert "read as" not in r.write(tmp_path / "report.html").read_text(encoding="utf-8")


def test_the_csv_compatibility_script_is_gone():
    assert not (SCRIPTS / "profile_csv.py").exists()
