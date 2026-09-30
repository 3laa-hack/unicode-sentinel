from analyzers.url import analyze_url
from reports.html import generate_html, save_html


def test_html_contains_risk_information():
    result = analyze_url("https://аpple.com")

    html = generate_html(result)

    assert "HIGH" in html
    assert "U+0430" in html
    assert "Cyrillic" in html
    assert "xn--pple-43d.com" in html
    assert "а" in html


def test_html_contains_security_information():
    result = analyze_url("https://аpple.com")

    html = generate_html(result)

    assert "Risk Assessment" in html
    assert "Character Analysis" in html
    assert "Confusable Characters" in html
    assert "Risk Factors" in html


def test_html_contains_suspicious_character_row():
    result = analyze_url("https://аpple.com")

    html = generate_html(result)

    assert 'class="suspicious"' in html


def test_save_html(tmp_path):
    result = analyze_url("https://аpple.com")

    output_file = tmp_path / "report.html"

    save_html(
        result,
        str(output_file),
    )

    assert output_file.exists()

    content = output_file.read_text(
        encoding="utf-8"
    )

    assert "<!DOCTYPE html>" in content
    assert "Unicode Homoglyph Detector" in content
    assert "HIGH" in content
