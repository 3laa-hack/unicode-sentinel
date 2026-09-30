import unicodedata

from core.scripts import detect_script


def analyze_character(char: str, position: int) -> dict:
    cp = ord(char)

    return {
        "position": position,
        "character": char,
        "codepoint": f"U+{cp:04X}",
        "unicode_name": unicodedata.name(char, "UNKNOWN"),
        "category": unicodedata.category(char),
        "script": detect_script(char),
    }


def analyze_text_characters(text: str) -> list[dict]:
    return [
        analyze_character(char, position)
        for position, char in enumerate(text)
    ]