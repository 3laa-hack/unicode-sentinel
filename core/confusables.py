import json
import unicodedata
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "confusables.json"


def load_confusables():
    """
    Load Unicode UTS #39 confusable mappings.
    """

    if not DATA_FILE.exists():
        return {}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return data.get("mappings", {})

    except (OSError, json.JSONDecodeError):
        return {}


CONFUSABLES = load_confusables()


def get_confusables(char: str) -> list[str]:
    """
    Return Unicode confusable targets.

    A Unicode mapping may contain one character or
    multiple characters.
    """

    if not char:
        return []

    codepoint = f"{ord(char):04X}"

    entry = CONFUSABLES.get(codepoint)

    if not entry:
        return []

    target = entry.get("target_char", "")

    if not target:
        return []

    return [target]


def get_confusable_details(char: str) -> list[dict]:
    """
    Return detailed information about confusable targets.

    Supports targets containing multiple Unicode characters.
    """

    results = []

    for target in get_confusables(char):

        target_codepoints = [
            f"U+{ord(c):04X}"
            for c in target
        ]

        target_names = [
            unicodedata.name(c, "UNKNOWN")
            for c in target
        ]

        results.append({
            "character": target,
            "codepoint": " ".join(target_codepoints),
            "unicode_name": " + ".join(target_names),
            "length": len(target),
        })

    return results


def is_confusable(char: str) -> bool:
    return bool(get_confusables(char))


def get_confusable_mapping(char: str) -> dict | None:
    """
    Return the original Unicode mapping entry.
    """

    if not char:
        return None

    codepoint = f"{ord(char):04X}"

    return CONFUSABLES.get(codepoint)
