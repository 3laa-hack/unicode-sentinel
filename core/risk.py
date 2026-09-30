from core.comparison import find_cross_script_confusables


IGNORED_SCRIPTS = {
    "Common",
    "Unknown",
    "Punctuation",
    "Number",
    "Separator",
    "Symbol",
    "Mark",
}


def _risk_level(score: int) -> str:
    if score == 0:
        return "SAFE"

    if score == 1:
        return "LOW"

    if score <= 3:
        return "MEDIUM"

    if score <= 5:
        return "HIGH"

    return "CRITICAL"


def calculate_risk(
    characters: list[dict],
    input_type: str = "text",
    idna: dict | None = None,
) -> dict:
    """
    Calculate heuristic Unicode security risk.

    Important distinction:

    - Raw UTS #39 mappings are informational.
    - Security risk is based on security-relevant
      cross-script comparison evidence.
    - Mixed scripts alone do not constitute a security
      finding.
    """

    # ------------------------------------------------------------
    # Script analysis
    # ------------------------------------------------------------

    scripts = {
        item["script"]
        for item in characters
        if item["script"] not in IGNORED_SCRIPTS
    }

    mixed_script = len(scripts) > 1

    # ------------------------------------------------------------
    # Security comparison evidence
    # ------------------------------------------------------------

    text = "".join(
        item.get("character", "")
        for item in characters
    )

    comparison_evidence = (
        find_cross_script_confusables(text)
    )

    suspicious_positions = sorted({
        item["position"]
        for item in comparison_evidence
    })

    # Security-relevant confusable count.
    #
    # Do NOT count every UTS #39 mapping here.
    # For example:
    #
    # Arabic ا -> Latin l
    #
    # is a raw confusable mapping but should not make
    # normal Arabic text suspicious.
    cross_script_count = len(
        comparison_evidence
    )

    cross_script_confusable = bool(
        comparison_evidence
    )

    # ------------------------------------------------------------
    # Risk scoring
    # ------------------------------------------------------------

    risk_factors = []
    score = 0

    # ------------------------------------------------------------
    # Mixed script combined with a cross-script confusable
    # is now a security-relevant finding.
    # ------------------------------------------------------------

    if mixed_script and cross_script_count > 0:
        score += 1

        risk_factors.append({
            "factor": "MIXED_SCRIPT",
            "severity": "HIGH",
            "points": 1,
            "description": (
                "Multiple Unicode scripts are present "
                "together with a security-relevant "
                "cross-script confusable"
            ),
        })

    # ------------------------------------------------------------
    # Security-relevant cross-script confusable
    # ------------------------------------------------------------

    if cross_script_count > 0:
        score += 2

        risk_factors.append({
            "factor": "CROSS_SCRIPT_CONFUSABLE",
            "severity": "HIGH",
            "points": 2,
            "description": (
                "One or more characters visually resemble "
                "characters from another Unicode script "
                "within a security-relevant script context"
            ),
        })

    # ------------------------------------------------------------
    # Multiple security-relevant confusables
    # ------------------------------------------------------------

    if cross_script_count >= 2:
        score += 1

        risk_factors.append({
            "factor": "MULTIPLE_CONFUSABLES",
            "severity": "HIGH",
            "points": 1,
            "description": (
                "Multiple security-relevant cross-script "
                "confusable characters were detected"
            ),
        })

    # ------------------------------------------------------------
    # Domain-specific evidence
    # ------------------------------------------------------------

    if input_type in {"url", "domain"}:
        if cross_script_count > 0:
            score += 1

            risk_factors.append({
                "factor": "DOMAIN_CONFUSABLE",
                "severity": "HIGH",
                "points": 1,
                "description": (
                    "A security-relevant cross-script "
                    "confusable occurs inside a URL/domain"
                ),
            })

    # ------------------------------------------------------------
    # IDNA / Punycode
    # ------------------------------------------------------------

    if idna:
        if idna.get("is_idna"):
            score += 1

            risk_factors.append({
                "factor": "IDNA_DOMAIN",
                "severity": "MEDIUM",
                "points": 1,
                "description": (
                    "The domain contains an IDNA/Punycode "
                    "representation"
                ),
            })

    # ------------------------------------------------------------
    # Final level
    # ------------------------------------------------------------

    level = _risk_level(score)

    reasons = [
        factor["description"]
        for factor in risk_factors
        if factor["points"] > 0
    ]

    return {
        "score": score,
        "level": level,
        "mixed_script": mixed_script,
        "scripts": sorted(scripts),
        "confusable_count": cross_script_count,
        "cross_script_confusable": (
            cross_script_confusable
        ),
        "suspicious_positions": suspicious_positions,
        "comparison_evidence": comparison_evidence,
        "risk_factors": risk_factors,
        "reasons": reasons,
    }