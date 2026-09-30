from analyzers.text import analyze_text
from analyzers.url import analyze_url
from core.skeleton import skeleton, skeleton_equal


def test_mixed_script():

    result = analyze_text("аpple")

    assert result["risk"]["mixed_script"] is True

    assert (
        result["characters"][0]["script"]
        == "Cyrillic"
    )


def test_url_idna():

    result = analyze_url(
        "https://аpple.com/login"
    )

    assert result["domain"] == "аpple.com"

    assert result["idna"]["ascii"] == (
        "xn--pple-43d.com"
    )

    assert result["idna"]["is_idna"] is True


def test_skeleton():

    assert skeleton("аpple") == "apple"


def test_skeleton_equal():

    assert skeleton_equal(
        "apple",
        "аpple"
    )


def test_normal_domain_is_safe():

    result = analyze_url(
        "https://apple.com/login"
    )

    assert result["risk"]["level"] == "SAFE"
    assert result["risk"]["score"] == 0


def test_homograph_domain_is_high_risk():

    result = analyze_url(
        "https://аpple.com/login"
    )

    assert result["risk"]["level"] == "HIGH"
    assert result["risk"]["score"] == 5

    assert (
        result["risk"]["confusable_count"]
        == 1
    )


def test_suspicious_character_is_cyrillic_a():

    result = analyze_url(
        "https://аpple.com"
    )

    first = result["characters"][0]

    assert first["character"] == "а"
    assert first["codepoint"] == "U+0430"
    assert first["script"] == "Cyrillic"

    assert any(
        conf["character"] == "a"
        for conf in first["confusables"]
    )
