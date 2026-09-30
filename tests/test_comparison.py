from core.comparison import (
    compare_strings,
    find_cross_script_confusables,
)


def test_apple_vs_cyrillic_apple():

    result = compare_strings(
        "apple",
        "аpple",
    )

    assert result["same_skeleton"] is True

    assert result["different_scripts"] is True

    assert result["suspicious_positions"] == [0]


def test_cross_script_confusable_detection():

    result = find_cross_script_confusables(
        "аpple"
    )

    assert len(result) >= 1

    item = result[0]

    assert item["position"] == 0

    assert item["character"] == "а"

    assert item["codepoint"] == "U+0430"

    assert item["script"] == "Cyrillic"

    assert "Latin" in item["target_scripts"]


def test_normal_apple_has_no_cross_script_confusable():

    result = find_cross_script_confusables(
        "apple"
    )

    assert result == []


def test_google_cyrillic_or_greek_confusable():

    result = compare_strings(
        "google",
        "gοοgle",
    )

    assert result["same_skeleton"] is True

    assert result["different_scripts"] is True

    assert len(
        result["suspicious_positions"]
    ) >= 1
