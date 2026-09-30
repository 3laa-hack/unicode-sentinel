import unicodedata

from core.skeleton import skeleton


def normalize_domain_label(label: str) -> str:
    """
    Normalize a single domain label.

    Unlike the full UTS #39 skeleton, this function
    preserves the label boundaries and performs
    NFC normalization only.
    """

    return unicodedata.normalize(
        "NFC",
        label,
    )


def security_domain_skeleton(domain: str) -> str:
    """
    Generate a security-oriented skeleton for a domain.

    Each DNS label is processed independently.

    This preserves the domain structure:

        example.com

    instead of allowing mappings from one label to
    visually alter the interpretation of another part
    of the domain.

    The official UTS #39 skeleton remains available
    through core.skeleton.
    """

    domain = domain.strip()

    if domain.endswith("."):
        domain = domain[:-1]

    labels = domain.split(".")

    normalized_labels = []

    for label in labels:

        normalized = normalize_domain_label(label)

        normalized_labels.append(
            skeleton(normalized)
        )

    return ".".join(normalized_labels)


def analyze_domain_skeleton(domain: str) -> dict:
    """
    Return both the original domain and its
    security-oriented skeleton.
    """

    normalized = unicodedata.normalize(
        "NFC",
        domain.strip().rstrip("."),
    )

    return {
        "original": normalized,
        "skeleton": security_domain_skeleton(normalized),
        "labels": [
            {
                "original": label,
                "skeleton": skeleton(
                    normalize_domain_label(label)
                ),
            }
            for label in normalized.split(".")
        ],
    }
