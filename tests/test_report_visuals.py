"""Report accepts Visual values from the chart module and nothing else."""
import pytest

from charts import STYLE, bar_chart, table
from profiles import column, meanings, profile
from report import Report


def report():
    prof = profile([column("amount", "measure")])
    return Report(prof, "Orders", description="One record per order.", meanings=meanings(prof))


def test_overview_takes_a_chart_and_nothing_else():
    r = report()
    r.overview("How much?", bar_chart(["a"], [1], title="t"), takeaway="One.", context="All records.")
    with pytest.raises(ValueError, match="chart"):
        r.overview("How much?", table(["a"], [[1]]), takeaway="One.", context="All records.")
    with pytest.raises(ValueError, match="chart"):
        r.overview("How much?", "<svg></svg>", takeaway="One.", context="All records.")


def test_observation_takes_a_chart_or_a_short_table():
    r = report()
    r.observation("A", bar_chart(["a"], [1], title="t"), noticed="x", why_it_matters="y", question="z?")
    r.observation("B", table(["a"], [[1]] * 10), noticed="x", why_it_matters="y", question="z?")
    r.observation("C", noticed="x", why_it_matters="y", question="z?")
    with pytest.raises(ValueError, match="10 rows"):
        r.observation("D", table(["a"], [[1]] * 11), noticed="x", why_it_matters="y", question="z?")
    with pytest.raises(ValueError, match="Visual"):
        r.observation("E", "<table></table>", noticed="x", why_it_matters="y", question="z?")


def test_page_carries_the_chart_style_block(tmp_path):
    r = report()
    r.overview("How much?", bar_chart(["a"], [1], title="t"), takeaway="One.", context="All records.")
    html = r.write(tmp_path / "report.html").read_text(encoding="utf-8")
    assert STYLE.strip() in html
    assert html.count("<svg") == 1
