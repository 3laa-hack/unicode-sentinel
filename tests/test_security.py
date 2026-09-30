from analyzers.text import analyze_text
from analyzers.url import analyze_url
from core.idna import analyze_idna
from core.skeleton import skeleton, skeleton_equal


def test_latin_text_is_safe():

    result = analyze_text("apple")

    assert result["risk"]["level"] == "SAFE"
    assert result["risk"]["score"] == 0
    assert result["risk"]["confusable_count"] == 0


def test_cyrillic_a_is_detected():

    result = analyze_text("аpple")

    assert result["characters"][0]["script"] == "Cyrillic"
    assert result["characters"][0]["codepoint"] == "U+0430"

    assert result["risk"]["confusable_count"] == 1
    assert result["risk"]["level"] == "MEDIUM"


def test_skeleton_apple():

    assert skeleton("apple") == "apple"
    assert skeleton("аpple") == "apple"

    assert skeleton_equal(
        "apple",
        "аpple"
    )


def test_google_confusable():

    assert skeleton_equal(
        "google",
        "gοοgle"
    )


def test_paypal_confusable():

    assert skeleton_equal(
        "paypal",
        "раypal"
    )


def test_normal_domain():

    result = analyze_url(
        "https://apple.com/login"
    )

    assert result["domain"] == "apple.com"

    assert result["idna"]["valid"] is True
    assert result["idna"]["is_idna"] is False
    assert result["idna"]["contains_non_ascii"] is False

    assert result["risk"]["level"] == "SAFE"
    assert result["risk"]["score"] == 0


def test_homograph_domain():

    result = analyze_url(
        "https://аpple.com/login"
    )

    assert result["domain"] == "аpple.com"

    assert result["idna"]["valid"] is True
    assert result["idna"]["is_idna"] is True
    assert result["idna"]["contains_non_ascii"] is True

    assert result["idna"]["ascii"] == "xn--pple-43d.com"

    assert result["risk"]["level"] == "HIGH"
    assert result["risk"]["score"] == 5
    assert result["risk"]["mixed_script"] is True
    assert result["risk"]["confusable_count"] == 1


def test_punycode_domain():

    result = analyze_idna(
        "xn--pple-43d.com"
    )

    assert result["valid"] is True
    assert result["is_idna"] is True
    assert result["unicode"] == "аpple.com"


def test_suspicious_position():

    result = analyze_url(
        "https://аpple.com"
    )

    suspicious = []

    for item in result["characters"]:

        source_script = item["script"]

        for conf in item.get("confusables", []):

            target = conf["character"]

            target_scripts = set()

            from core.scripts import detect_script

            for char in target:
                target_scripts.add(
                    detect_script(char)
                )

            if any(
                script != source_script
                for script in target_scripts
            ):
                suspicious.append(
                    item["position"]
                )

    assert suspicious == [0]
