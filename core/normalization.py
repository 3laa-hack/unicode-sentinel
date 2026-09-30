import unicodedata


def normalize_text(text: str) -> dict:
    return {
        "NFC": unicodedata.normalize("NFC", text),
        "NFD": unicodedata.normalize("NFD", text),
        "NFKC": unicodedata.normalize("NFKC", text),
        "NFKD": unicodedata.normalize("NFKD", text),
    }


def normalized_equal(a: str, b: str) -> bool:
    return (
        unicodedata.normalize("NFKC", a)
        == unicodedata.normalize("NFKC", b)
    )