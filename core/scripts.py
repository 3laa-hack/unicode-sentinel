import unicodedata


SCRIPT_RANGES = {
    "Latin": [
        (0x0041, 0x005A),
        (0x0061, 0x007A),
        (0x00C0, 0x02AF),
        (0x1E00, 0x1EFF),
    ],
    "Greek": [
        (0x0370, 0x03FF),
        (0x1F00, 0x1FFF),
    ],
    "Cyrillic": [
        (0x0400, 0x052F),
        (0x2DE0, 0x2DFF),
        (0xA640, 0xA69F),
    ],
    "Arabic": [
        (0x0600, 0x06FF),
        (0x0750, 0x077F),
        (0x08A0, 0x08FF),
        (0xFB50, 0xFDFF),
        (0xFE70, 0xFEFF),
    ],
    "Hebrew": [
        (0x0590, 0x05FF),
    ],
    "Armenian": [
        (0x0530, 0x058F),
    ],
    "Georgian": [
        (0x10A0, 0x10FF),
        (0x2D00, 0x2D2F),
    ],
    "Devanagari": [
        (0x0900, 0x097F),
    ],
    "Bengali": [
        (0x0980, 0x09FF),
    ],
    "Thai": [
        (0x0E00, 0x0E7F),
    ],
    "Hangul": [
        (0x1100, 0x11FF),
        (0xAC00, 0xD7AF),
    ],
    "Hiragana": [
        (0x3040, 0x309F),
    ],
    "Katakana": [
        (0x30A0, 0x30FF),
    ],
    "CJK": [
        (0x3400, 0x4DBF),
        (0x4E00, 0x9FFF),
    ],
}


def detect_script(char: str) -> str:
    if not char:
        return "Unknown"

    cp = ord(char)

    for script, ranges in SCRIPT_RANGES.items():
        for start, end in ranges:
            if start <= cp <= end:
                return script

    name = unicodedata.name(char, "")

    for script in SCRIPT_RANGES:
        if script.upper() in name:
            return script

    category = unicodedata.category(char)

    if category.startswith("P"):
        return "Punctuation"

    if category.startswith("N"):
        return "Number"

    if category.startswith("S"):
        return "Symbol"

    if category.startswith("Z"):
        return "Separator"

    if category.startswith("M"):
        return "Mark"

    return "Common"