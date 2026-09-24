"""Numbers for the reader: the formatting helpers the driver interpolates into prose and tables."""
from report import esc, fmt, money, pct


def test_fmt_keeps_integers_plain_and_rounds_fractions():
    assert fmt(1912) == "1,912"
    assert fmt(1234.5678) == "1,234.57"
    assert fmt(1234.5678, decimals=1) == "1,234.6"
    assert fmt(None) == "n/a"
    assert fmt(float("nan")) == "n/a"


def test_fmt_compact_writes_millions_and_billions_for_prose():
    assert fmt(1_250_000, compact=True) == "1.25M"
    assert fmt(2_000_000_000, compact=True) == "2B"
    assert fmt(999_999, compact=True) == "999,999"


def test_money_carries_sign_and_two_decimals():
    assert money(12_500_000, compact=True) == "$12.5M"
    assert money(-1234.5) == "-$1,234.50"
    assert money(1000) == "$1,000"


def test_pct_never_reads_as_zero_or_whole_when_it_is_not():
    assert pct(0.184) == "18.4%"
    assert pct(0.0001) == "<0.1%"
    assert pct(0.9999) == ">99.9%"
    assert pct(1) == "100.0%"
    assert pct(None) == "n/a"


def test_esc_escapes_markup_and_quotes():
    assert esc('<b class="x">') == "&lt;b class=&quot;x&quot;&gt;"
