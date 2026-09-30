import unicodedata


def normalize_domain(domain: str) -> str:
    """
    Normalize a domain before IDNA processing.
    """

    domain = domain.strip()

    # Remove URL-style trailing dot only for processing.
    if domain.endswith("."):
        domain = domain[:-1]

    return unicodedata.normalize("NFC", domain)


def domain_to_ascii(domain: str) -> str:
    """
    Convert a Unicode domain to ASCII using IDNA.
    """

    domain = normalize_domain(domain)

    if not domain:
        return ""

    labels = domain.split(".")

    ascii_labels = []

    for label in labels:
        if not label:
            continue

        ascii_label = label.encode("idna").decode("ascii")
        ascii_labels.append(ascii_label)

    return ".".join(ascii_labels)


def domain_to_unicode(domain: str) -> str:
    """
    Convert an ASCII/IDNA domain back to Unicode.
    """

    domain = normalize_domain(domain)

    if not domain:
        return ""

    labels = domain.split(".")

    unicode_labels = []

    for label in labels:
        if not label:
            continue

        unicode_label = label.encode("ascii").decode("idna")
        unicode_labels.append(unicode_label)

    return ".".join(unicode_labels)


def is_idna_domain(domain: str) -> bool:
    """
    Return True if the domain contains IDNA/Punycode labels.
    """

    return any(
        label.lower().startswith("xn--")
        for label in normalize_domain(domain).split(".")
    )


def contains_non_ascii(domain: str) -> bool:
    """
    Check whether a domain contains non-ASCII characters.
    """

    return any(ord(char) > 127 for char in domain)


def analyze_idna(domain: str) -> dict:
    """
    Perform complete IDNA analysis on a domain.
    """

    domain = normalize_domain(domain)

    result = {
        "original": domain,
        "ascii": "",
        "unicode": "",
        "is_idna": False,
        "contains_non_ascii": contains_non_ascii(domain),
        "valid": False,
        "error": None,
    }

    try:
        ascii_domain = domain_to_ascii(domain)
        unicode_domain = domain_to_unicode(ascii_domain)

        result["ascii"] = ascii_domain
        result["unicode"] = unicode_domain
        result["is_idna"] = is_idna_domain(ascii_domain)
        result["valid"] = True

    except (UnicodeError, UnicodeEncodeError, ValueError) as exc:
        result["error"] = str(exc)

    return result
