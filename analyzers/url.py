from urllib.parse import urlparse

from analyzers.text import analyze_text
from core.idna import analyze_idna
from core.risk import calculate_risk
from core.skeleton import skeleton


def looks_like_url(value: str) -> bool:

    return (
        "://" in value
        or value.startswith("www.")
        or "." in value
    )


def extract_domain(value: str) -> str:

    candidate = value.strip()

    if "://" not in candidate:
        candidate = "http://" + candidate

    parsed = urlparse(candidate)

    return parsed.hostname or ""


def analyze_url(value: str) -> dict:

    domain = extract_domain(value)

    domain_result = analyze_text(domain)

    idna_result = analyze_idna(domain)

    domain_skeleton = skeleton(domain)

    risk = calculate_risk(
        domain_result["characters"],
        input_type="domain",
        idna=idna_result,
    )

    return {
        "input": value,
        "input_type": "url",

        "domain": domain,

        "idna": idna_result,

        "skeleton": domain_skeleton,

        "characters": domain_result["characters"],

        "risk": risk,
    }
