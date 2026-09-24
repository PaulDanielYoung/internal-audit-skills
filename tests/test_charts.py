"""Charts and tables are Visual values with their limits, folding, and styling inside."""
import pytest

from charts import BAR_MAX_CATEGORIES, PIE_MAX_SLICES, STYLE, Visual, bar_chart, line_chart, pie_chart, table


def test_each_chart_is_a_visual_holding_one_svg():
    for visual in (
        bar_chart(["a", "b"], [1, 2], title="Bars"),
        line_chart(["2023", "2024"], [1, 2], title="Line"),
        pie_chart(["a", "b"], [1, 2], title="Pie"),
    ):
        assert isinstance(visual, Visual) and visual.is_chart
        assert visual.html.count("<svg") == 1
        assert visual.rows == 0
    assert bar_chart(["a"], [1], title="t").kind == "bar"
    assert line_chart(["a", "b"], [1, 2], title="t").kind == "line"
    assert pie_chart(["a"], [1], title="t").kind == "pie"


def test_empty_input_is_rejected():
    for chart in (bar_chart, line_chart, pie_chart):
        with pytest.raises(ValueError, match="no values"):
            chart([], [], title="Nothing")


def test_shared_validation_of_lengths_decimals_and_finite_values():
    with pytest.raises(ValueError, match="same length"):
        bar_chart(["a"], [1, 2], title="t")
    with pytest.raises(ValueError, match="decimals"):
        bar_chart(["a"], [1], title="t", decimals=-1)
    with pytest.raises(ValueError, match="finite"):
        line_chart(["a", "b"], [1, float("nan")], title="t")


def test_bar_chart_folds_the_smallest_groups_into_other_keeping_the_drivers_order():
    labels = [f"g{i}" for i in range(15)]
    values = [15, 1, 14, 2, 13, 3, 12, 4, 11, 5, 10, 6, 9, 7, 8]
    visual = bar_chart(labels, values, title="Groups")
    assert visual.labels == ("g0", "g2", "g4", "g6", "g8", "g9", "g10", "g11", "g12", "g13", "g14", "Other")
    assert visual.values[-1] == 1 + 2 + 3 + 4
    assert visual.other.groups == 4
    assert visual.other.value == 10
    assert visual.other.outweighs_largest is False
    assert visual.html.count("<rect") == BAR_MAX_CATEGORIES


def test_other_that_outweighs_the_largest_group_is_flagged():
    labels = [f"g{i}" for i in range(30)]
    values = [10] + [3] * 29
    visual = bar_chart(labels, values, title="Spread thin")
    assert visual.other.groups == 19
    assert visual.other.value == 57
    assert visual.other.outweighs_largest is True


def test_no_fold_within_the_limit():
    visual = bar_chart(list("abcdefghijkl"), range(12, 0, -1), title="Twelve")
    assert visual.other is None and visual.labels == tuple("abcdefghijkl")


def test_a_drivers_own_other_joins_the_fold():
    labels = [f"g{i}" for i in range(13)] + ["Other"]
    values = [20] * 13 + [5]
    visual = bar_chart(labels, values, title="Pre-folded")
    assert visual.labels[-1] == "Other" and visual.labels.count("Other") == 1
    assert visual.values[-1] == 20 * 2 + 5
    assert visual.other.groups == 2


def test_pie_chart_folds_to_its_slice_limit_and_rejects_bad_parts():
    visual = pie_chart(list("abcdefg"), [7, 6, 5, 4, 3, 2, 1], title="Parts")
    assert visual.labels == ("a", "b", "c", "d", "Other")
    assert visual.values[-1] == 3 + 2 + 1
    assert visual.html.count("<path") == PIE_MAX_SLICES
    with pytest.raises(ValueError, match="non-negative"):
        pie_chart(["a", "b"], [1, -1], title="t")
    with pytest.raises(ValueError, match="positive total"):
        pie_chart(["a", "b"], [0, 0], title="t")


def test_marks_carry_the_palette_not_a_placeholder():
    from charts import ACCENT, GAP
    for visual in (bar_chart(["a"], [1], title="t"), line_chart(["a", "b"], [1, 2], title="t", partial_last=True),
                   pie_chart(["a", "b"], [1, 2], title="t")):
        assert "{ACCENT}" not in visual.html and "{GAP}" not in visual.html
    assert f'<polyline fill="none" stroke="{ACCENT}"' in line_chart(["a", "b"], [1, 2], title="t").html
    assert f'stroke="{GAP}"' in pie_chart(["a", "b"], [1, 2], title="t").html


def test_line_chart_needs_two_periods_and_marks_a_partial_last_period():
    with pytest.raises(ValueError, match="two periods"):
        line_chart(["2024"], [1], title="t")
    visual = line_chart(["Jan", "Feb", "Mar"], [3, 4, 1], title="t", partial_last=True)
    assert "to date" in visual.html and "stroke-dasharray" in visual.html


def test_table_is_a_visual_that_counts_its_body_rows_and_escapes_cells():
    visual = table(["Field", "Value"], [["a", "<b>"], ["c", "d"]], title="Sample")
    assert visual.kind == "table" and not visual.is_chart
    assert visual.rows == 2
    assert "&lt;b&gt;" in visual.html and "<caption>Sample</caption>" in visual.html


def test_style_block_covers_every_pie_slice():
    for index in range(1, PIE_MAX_SLICES + 1):
        assert f".slice-{index}" in STYLE
    assert "figcaption" in STYLE and "svg" in STYLE
