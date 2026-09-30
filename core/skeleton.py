import unicodedata

from core.confusables import get_confusables


def skeleton_char(char: str) -> str:
    """
    Convert one Unicode character into its confusable skeleton form.
    """

    confusables = get_confusables(char)

    if confusables:
        target = confusables[0]

        # Unicode confusable target can theoretically contain
        # more than one character.
        return target

    return char


def skeleton(text: str) -> str:
    """
    Generate a Unicode confusable skeleton for an entire string.
    """

    result = []

    for char in text:
        result.append(skeleton_char(char))

    return "".join(result)


def normalized_skeleton(text: str) -> str:
    """
    Normalize text first, then generate its confusable skeleton.
    """

    normalized = unicodedata.normalize("NFKC", text)

    return skeleton(normalized)


def skeleton_equal(a: str, b: str) -> bool:
    """
    Check whether two strings have the same confusable skeleton.
    """

    return normalized_skeleton(a) == normalized_skeleton(b)
