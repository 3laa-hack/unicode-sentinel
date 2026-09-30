from analyzers.text import analyze_text
from analyzers.url import analyze_url


def test_risk_contains_comparison_information():

    result = analyze_text("аpple")

    risk = result["risk"]

    assert risk["cross_script_confusable"] is True

    assert risk["suspicious_positions"] == [0]

    assert len(
        risk["comparison_evidence"]
    ) >= 1


def test_normal_text_has_no_cross_script_risk():

    result = analyze_text("apple")

    risk = result["risk"]

    assert risk["cross_script_confusable"] is False

    assert risk["suspicious_positions"] == []

    assert risk["comparison_evidence"] == []

    assert risk["level"] == "SAFE"


def test_url_keeps_high_risk_detection():

    result = analyze_url(
        "https://аpple.com"
    )

    risk = result["risk"]

    assert risk["cross_script_confusable"] is True

    assert 0 in risk["suspicious_positions"]

    assert risk["level"] == "HIGH"

    assert risk["score"] == 5


def test_skeleton_mapping_alone_does_not_raise_risk():

    result = analyze_text("m")

    risk = result["risk"]

    assert risk["cross_script_confusable"] is False

    assert risk["suspicious_positions"] == []

    assert risk["level"] == "SAFE"
