from collections import Counter

from core.confusables import get_confusable_details
from core.scripts import detect_script
from core.skeleton import normalized_skeleton


IGNORED_SCRIPTS = {
    "Common",
    "Unknown",
    "Punctuation",
    "Number",
    "Separator",
    "Symbol",
    "Mark",
}


def _significant_script(char: str) -> str:
    """
    Return the security-relevant Unicode script
    for a character.
    """

    script = detect_script(char)

    if script in IGNORED_SCRIPTS:
        return ""

    return script


def _target_scripts(target: str) -> set[str]:
    """
    Return significant scripts used by a confusable target.
    """

    scripts = set()

    for char in target:
        script = _significant_script(char)

        if script:
            scripts.add(script)

    return scripts


def get_script_counts(text: str) -> dict[str, int]:
    """
    Count significant Unicode scripts in a string.

    Common characters such as punctuation, spaces and
    symbols are ignored.
    """

    counts = Counter()

    for char in text:
        script = _significant_script(char)

        if script:
            counts[script] += 1

    return dict(counts)


def get_dominant_script(text: str) -> str | None:
    """
    Return the dominant significant Unicode script.

    The dominant script is the script with the highest
    number of characters.

    If there are no significant scripts, return None.

    If multiple scripts have the same highest count,
    return None because there is no unique dominant script.
    """

    counts = get_script_counts(text)

    if not counts:
        return None

    highest = max(counts.values())

    dominant = [
        script
        for script, count in counts.items()
        if count == highest
    ]

    if len(dominant) != 1:
        return None

    return dominant[0]


def find_cross_script_confusables(
    text: str,
) -> list[dict]:
    """
    Find security-relevant cross-script confusables.

    A raw UTS #39 mapping is not automatically considered
    a security finding.

    A finding is reported when:

    1. The source character belongs to a significant script.
    2. Its confusable target belongs to another script.
    3. The target script matches the dominant script of
       the surrounding text.

    This reduces false positives for normal multilingual
    text such as:

        Hello مرحبا
        مرحبا بالعالم

    while preserving cases such as:

        аpple
        раypal
        gοοgle
    """

    results = []

    dominant_script = get_dominant_script(text)

    for position, char in enumerate(text):

        source_script = _significant_script(char)

        if not source_script:
            continue

        for confusable in get_confusable_details(char):

            target = confusable["character"]

            target_scripts = _target_scripts(target)

            if not target_scripts:
                continue

            cross_script = any(
                script != source_script
                for script in target_scripts
            )

            if not cross_script:
                continue

            # Without a unique dominant script there is
            # insufficient context to call this a
            # security-relevant finding.
            if dominant_script is None:
                continue

            # The confusable target must correspond to
            # the dominant script of the surrounding text.
            if dominant_script not in target_scripts:
                continue

            results.append({
                "position": position,
                "character": char,
                "codepoint": f"U+{ord(char):04X}",
                "script": source_script,
                "confusable": confusable,
                "target_scripts": sorted(
                    target_scripts
                ),
                "dominant_script": dominant_script,
            })

    return results


def compare_strings(
    original: str,
    candidate: str,
) -> dict:
    """
    Compare two strings from a Unicode security perspective.

    The comparison combines:

    - normalized UTS #39 skeleton equality
    - script differences
    - dominant-script analysis
    - security-relevant cross-script confusables
    """

    original_skeleton = normalized_skeleton(
        original
    )

    candidate_skeleton = normalized_skeleton(
        candidate
    )

    same_skeleton = (
        original_skeleton
        == candidate_skeleton
    )

    original_scripts = {
        script
        for char in original
        if (
            script := _significant_script(char)
        )
    }

    candidate_scripts = {
        script
        for char in candidate
        if (
            script := _significant_script(char)
        )
    }

    different_scripts = (
        original_scripts != candidate_scripts
    )

    original_dominant_script = (
        get_dominant_script(original)
    )

    candidate_dominant_script = (
        get_dominant_script(candidate)
    )

    suspicious_positions = []

    for position, (original_char, candidate_char) in enumerate(
        zip(original, candidate)
    ):

        original_script = _significant_script(
            original_char
        )

        candidate_script = _significant_script(
            candidate_char
        )

        if (
            original_script
            and candidate_script
            and original_script != candidate_script
        ):
            suspicious_positions.append(
                position
            )

    cross_script_evidence = (
        find_cross_script_confusables(candidate)
    )

    return {
        "original": original,
        "candidate": candidate,
        "original_skeleton": original_skeleton,
        "candidate_skeleton": candidate_skeleton,
        "same_skeleton": same_skeleton,
        "original_scripts": sorted(
            original_scripts
        ),
        "candidate_scripts": sorted(
            candidate_scripts
        ),
        "original_dominant_script": (
            original_dominant_script
        ),
        "candidate_dominant_script": (
            candidate_dominant_script
        ),
        "different_scripts": different_scripts,
        "suspicious_positions": suspicious_positions,
        "cross_script_confusables": (
            cross_script_evidence
        ),
    }