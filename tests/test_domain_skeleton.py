from core.domain_skeleton import (
    security_domain_skeleton,
    analyze_domain_skeleton,
)


def test_domain_skeleton_preserves_labels():
    result = security_domain_skeleton(
        "apple.com"
    )

    assert result.count(".") == 1


def test_domain_skeleton_detects_cyrillic_a():
    result = security_domain_skeleton(
        "аpple.com"
    )

    assert result == "apple.corn"


def test_domain_skeleton_returns_label_details():
    result = analyze_domain_skeleton(
        "аpple.com"
    )

    assert result["original"] == "аpple.com"

    assert len(result["labels"]) == 2

    assert result["labels"][0]["original"] == "аpple"

    assert result["labels"][0]["skeleton"] == "apple"

    assert result["labels"][1]["original"] == "com"

    assert result["labels"][1]["skeleton"] == "corn"
