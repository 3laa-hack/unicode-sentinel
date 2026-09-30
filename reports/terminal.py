def print_header():
    print()
    print("╔══════════════════════════════════════════════╗")
    print("║       UNICODE HOMOGLYPH DETECTOR            ║")
    print("╚══════════════════════════════════════════════╝")
    print()


def _script_of_char(char: str) -> str:
    from core.scripts import detect_script
    return detect_script(char)


IGNORED_SCRIPTS = {
    "Common",
    "Unknown",
    "Punctuation",
    "Number",
    "Separator",
    "Symbol",
    "Mark",
}


def _is_cross_script_confusable(
    item: dict,
    confusable: dict,
) -> bool:

    source_script = item.get("script", "")
    target = confusable.get("character", "")

    if not source_script or not target:
        return False

    target_scripts = set()

    for char in target:

        script = _script_of_char(char)

        if script not in IGNORED_SCRIPTS:
            target_scripts.add(script)

    return any(
        script != source_script
        for script in target_scripts
    )


def _has_cross_script_confusable(item: dict) -> bool:

    return any(
        _is_cross_script_confusable(item, conf)
        for conf in item.get("confusables", [])
    )


def print_risk(risk: dict):

    print("=" * 65)
    print("RISK ASSESSMENT")
    print("=" * 65)

    print(f"Level:             {risk['level']}")
    print(f"Score:             {risk['score']}")

    print(
        "Mixed Script:      "
        + ("YES" if risk["mixed_script"] else "NO")
    )

    print(
        "Cross-Script:      "
        + (
            "YES"
            if risk.get("cross_script_confusable")
            else "NO"
        )
    )

    print(
        "Suspicious Pos:    "
        + (
            ", ".join(
                str(pos)
                for pos in risk.get(
                    "suspicious_positions",
                    []
                )
            )
            if risk.get("suspicious_positions")
            else "NONE"
        )
    )

    if risk["scripts"]:
        print(
            "Scripts:           "
            + ", ".join(risk["scripts"])
        )

    print(
        f"Confusables:       "
        f"{risk['confusable_count']}"
    )

    if risk["reasons"]:
        print()
        print("Reasons:")

        for reason in risk["reasons"]:
            print(f"[+] {reason}")

    print()


def print_characters(characters: list[dict]):

    print("=" * 100)
    print("CHARACTER ANALYSIS")
    print("=" * 100)

    print(
        f"{'Pos':<5}"
        f"{'Char':<8}"
        f"{'Code Point':<13}"
        f"{'Script':<14}"
        f"Unicode Name"
    )

    print("-" * 100)

    for item in characters:

        char = item["character"]

        if char == " ":
            display_char = "<space>"
        elif char == "\t":
            display_char = "<tab>"
        elif char == "\n":
            display_char = "<newline>"
        else:
            display_char = char

        print(
            f"{item['position']:<5}"
            f"{display_char:<8}"
            f"{item['codepoint']:<13}"
            f"{item['script']:<14}"
            f"{item['unicode_name']}"
        )

    print()


def print_confusables(characters: list[dict]):

    print("=" * 100)
    print("CONFUSABLE CHARACTERS")
    print("=" * 100)

    security_found = False
    skeleton_found = False

    for item in characters:

        confusables = item.get("confusables", [])

        cross_script = [
            conf
            for conf in confusables
            if _is_cross_script_confusable(
                item,
                conf,
            )
        ]

        if not cross_script:
            continue

        security_found = True

        print(
            f"\nPosition: {item['position']}"
        )

        print(
            f"Character: {item['character']}"
        )

        print(
            f"Code Point: {item['codepoint']}"
        )

        print(
            f"Script: {item['script']}"
        )

        print(
            f"Name: {item['unicode_name']}"
        )

        print("Security-Relevant Confusable:")

        for conf in cross_script:

            print(
                f"  -> {conf['character']} "
                f"{conf['codepoint']} "
                f"{conf['unicode_name']}"
            )

            print(
                "     Type: CROSS-SCRIPT"
            )

    if not security_found:

        print(
            "No security-relevant cross-script "
            "confusables found."
        )

    for item in characters:

        confusables = item.get("confusables", [])

        same_script = [
            conf
            for conf in confusables
            if not _is_cross_script_confusable(
                item,
                conf,
            )
        ]

        if not same_script:
            continue

        skeleton_found = True

        print(
            f"\nPosition: {item['position']}"
        )

        print(
            f"Character: {item['character']}"
        )

        print(
            f"Code Point: {item['codepoint']}"
        )

        print(
            f"Name: {item['unicode_name']}"
        )

        print("Skeleton / Informational Mapping:")

        for conf in same_script:

            print(
                f"  -> {conf['character']} "
                f"{conf['codepoint']} "
                f"{conf['unicode_name']}"
            )

            print(
                "     Type: SAME-SCRIPT / SKELETON"
            )

    if not skeleton_found and not security_found:

        print("No known confusable mappings found.")

    print()


def print_comparison(text: str, characters: list[dict]):

    suspicious_positions = []

    for item in characters:

        if _has_cross_script_confusable(item):

            suspicious_positions.append(
                item["position"]
            )

    if not suspicious_positions:
        return

    print("=" * 100)
    print("SECURITY-RELEVANT SUSPICIOUS POSITIONS")
    print("=" * 100)

    print(text)

    marker = ""

    for index in range(len(text)):

        if index in suspicious_positions:
            marker += "^"
        else:
            marker += " "

    print(marker)
    print()


def print_comparison_evidence(risk: dict):

    evidence = risk.get(
        "comparison_evidence",
        [],
    )

    if not evidence:
        return

    print("=" * 100)
    print("SECURITY COMPARISON EVIDENCE")
    print("=" * 100)

    for item in evidence:

        confusable = item["confusable"]

        print(
            f"\nPosition:       {item['position']}"
        )

        print(
            f"Character:      {item['character']}"
        )

        print(
            f"Code Point:     {item['codepoint']}"
        )

        print(
            f"Source Script:  {item['script']}"
        )

        print(
            f"Confusable:     {confusable['character']}"
        )

        print(
            f"Target Code:    {confusable['codepoint']}"
        )

        print(
            f"Target Name:    {confusable['unicode_name']}"
        )

        print(
            "Target Scripts: "
            + ", ".join(
                item["target_scripts"]
            )
        )

        print(
            "Type:           CROSS-SCRIPT"
        )

    print()
