from ui.colors import (
    BRIGHT_BLUE,
    BRIGHT_CYAN,
    BRIGHT_GREEN,
    BRIGHT_MAGENTA,
    BRIGHT_RED,
    BRIGHT_WHITE,
    BRIGHT_YELLOW,
    BOLD,
    RESET,
    color,
    danger,
    dim,
    info,
    risk,
    success,
    warning,
)


def section(title):
    print()
    print(
        color("╭─ ", BRIGHT_BLUE + BOLD)
        + color(title, BRIGHT_CYAN + BOLD)
        + color(" ───────────────────────────────────────╮", BRIGHT_BLUE)
    )


def section_end():
    print(
        color("╰──────────────────────────────────────────────────────────────╯",
              BRIGHT_BLUE)
    )


def render_risk(risk_data):
    section("SECURITY RISK")

    level = risk_data.get("level", "UNKNOWN")
    score = risk_data.get("score", 0)
    mixed = risk_data.get("mixed_script", False)
    cross = risk_data.get("cross_script_confusable", False)

    print(
        f"  {color('Risk Level', BRIGHT_WHITE + BOLD):<28}: "
        f"{risk(level)}"
    )

    print(
        f"  {color('Score', BRIGHT_WHITE + BOLD):<28}: "
        f"{score}"
    )

    print(
        f"  {color('Mixed Script', BRIGHT_WHITE + BOLD):<28}: "
        f"{color('YES', BRIGHT_YELLOW) if mixed else color('NO', BRIGHT_GREEN)}"
    )

    print(
        f"  {color('Cross-Script Confusable', BRIGHT_WHITE + BOLD):<28}: "
        f"{color('YES', BRIGHT_RED) if cross else color('NO', BRIGHT_GREEN)}"
    )

    positions = risk_data.get("suspicious_positions", [])

    print(
        f"  {color('Suspicious Positions', BRIGHT_WHITE + BOLD):<28}: "
        f"{positions if positions else 'None'}"
    )

    scripts = risk_data.get("scripts", [])

    print(
        f"  {color('Scripts', BRIGHT_WHITE + BOLD):<28}: "
        f"{', '.join(scripts) if scripts else 'None'}"
    )

    print(
        f"  {color('Confusable Count', BRIGHT_WHITE + BOLD):<28}: "
        f"{risk_data.get('confusable_count', 0)}"
    )

    reasons = risk_data.get("reasons", [])

    if reasons:
        print()
        print(color("  Risk Factors:", BRIGHT_YELLOW + BOLD))

        for reason in reasons:
            print(
                color("    • ", BRIGHT_YELLOW)
                + reason
            )

    section_end()


def render_characters(characters):
    section("CHARACTER ANALYSIS")

    for item in characters:
        char = item.get("character", "")
        position = item.get("position", "?")
        codepoint = item.get("codepoint", "")
        name = item.get("unicode_name", "")
        script = item.get("script", "")

        print()
        print(
            color(f"  [{position}] ", BRIGHT_BLUE + BOLD)
            + color(
                repr(char),
                BRIGHT_MAGENTA + BOLD,
            )
        )

        print(
            f"      {color('Code Point', BRIGHT_CYAN)} : "
            f"{codepoint}"
        )

        print(
            f"      {color('Unicode Name', BRIGHT_CYAN)}: "
            f"{name}"
        )

        print(
            f"      {color('Script', BRIGHT_CYAN)}      : "
            f"{script}"
        )

        confusables = item.get("confusables", [])

        if confusables:
            print(
                color("      Confusables:", BRIGHT_YELLOW + BOLD)
            )

            for confusable in confusables:
                target = confusable.get("character", "")
                target_cp = confusable.get("codepoint", "")
                target_name = confusable.get("unicode_name", "")

                print(
                    color("        → ", BRIGHT_RED)
                    + color(
                        repr(target),
                        BRIGHT_WHITE + BOLD,
                    )
                    + f" {target_cp}"
                )

                print(
                    f"          {dim(target_name)}"
                )

    section_end()


def render_comparison_evidence(evidence):
    if not evidence:
        return

    section("SECURITY COMPARISON EVIDENCE")

    for item in evidence:
        print()
        print(
            f"  {color('Position', BRIGHT_CYAN)}     : "
            f"{item.get('position')}"
        )

        print(
            f"  {color('Character', BRIGHT_CYAN)}    : "
            f"{item.get('character')}"
        )

        print(
            f"  {color('Code Point', BRIGHT_CYAN)}   : "
            f"{item.get('codepoint')}"
        )

        print(
            f"  {color('Source Script', BRIGHT_CYAN)} : "
            f"{item.get('script')}"
        )

        confusable = item.get("confusable", {})

        print(
            f"  {color('Confusable', BRIGHT_CYAN)}   : "
            f"{confusable.get('character', '')}"
        )

        print(
            f"  {color('Target Code', BRIGHT_CYAN)}  : "
            f"{confusable.get('codepoint', '')}"
        )

        print(
            f"  {color('Target Name', BRIGHT_CYAN)}  : "
            f"{confusable.get('unicode_name', '')}"
        )

        print(
            color("  Type", BRIGHT_CYAN)
            + "           : "
            + color("CROSS-SCRIPT", BRIGHT_RED + BOLD)
        )

    section_end()


def render_idna(idna):
    if not idna:
        return

    section("IDNA / PUNYCODE")

    print(
        f"  {color('Original', BRIGHT_CYAN)} : "
        f"{idna.get('original', '')}"
    )

    print(
        f"  {color('ASCII', BRIGHT_CYAN)}    : "
        f"{idna.get('ascii', '')}"
    )

    print(
        f"  {color('Unicode', BRIGHT_CYAN)}  : "
        f"{idna.get('unicode', '')}"
    )

    print(
        f"  {color('IDNA', BRIGHT_CYAN)}     : "
        f"{idna.get('is_idna', False)}"
    )

    if idna.get("error"):
        print(
            color("  Error: ", BRIGHT_RED + BOLD)
            + idna["error"]
        )

    section_end()


def render_analysis(result):
    print()
    print(
        color("╭─ ", BRIGHT_BLUE + BOLD)
        + color("ANALYSIS RESULT", BRIGHT_CYAN + BOLD)
        + color(" ───────────────────────────────────────╮", BRIGHT_BLUE)
    )

    print(
        f"  {color('Input', BRIGHT_CYAN + BOLD)} : "
        f"{result.get('input', '')}"
    )

    print(
        f"  {color('Type', BRIGHT_CYAN + BOLD)}  : "
        f"{result.get('input_type', '')}"
    )

    print(
        color("╰──────────────────────────────────────────────────────────────╯",
              BRIGHT_BLUE)
    )

    render_risk(result.get("risk", {}))

    if result.get("idna"):
        render_idna(result["idna"])

    render_characters(result.get("characters", []))

    render_comparison_evidence(
        result.get("risk", {}).get(
            "comparison_evidence",
            [],
        )
    )


def render_normalization(result):
    section("UNICODE NORMALIZATION")

    for form, value in result.items():
        print(
            f"  {color(form, BRIGHT_CYAN + BOLD):<22} "
            f": {value}"
        )

    section_end()


def render_comparison(result):
    section("STRING COMPARISON")

    print(
        f"  {color('Original', BRIGHT_CYAN)}          : "
        f"{result.get('original')}"
    )

    print(
        f"  {color('Candidate', BRIGHT_CYAN)}         : "
        f"{result.get('candidate')}"
    )

    print(
        f"  {color('Original Skeleton', BRIGHT_CYAN)}  : "
        f"{result.get('original_skeleton')}"
    )

    print(
        f"  {color('Candidate Skeleton', BRIGHT_CYAN)} : "
        f"{result.get('candidate_skeleton')}"
    )

    same = result.get("same_skeleton")

    if same:
        print(
            "  "
            + color(
                "✓ Same Unicode skeleton",
                BRIGHT_GREEN + BOLD,
            )
        )
    else:
        print(
            "  "
            + color(
                "✖ Different Unicode skeleton",
                BRIGHT_RED + BOLD,
            )
        )

    print(
        f"  {color('Original Scripts', BRIGHT_CYAN)}  : "
        f"{', '.join(result.get('original_scripts', [])) or 'None'}"
    )

    print(
        f"  {color('Candidate Scripts', BRIGHT_CYAN)} : "
        f"{', '.join(result.get('candidate_scripts', [])) or 'None'}"
    )

    suspicious = result.get("suspicious_positions", [])

    print(
        f"  {color('Suspicious Positions', BRIGHT_CYAN)}: "
        f"{suspicious if suspicious else 'None'}"
    )

    render_comparison_evidence(
        result.get("cross_script_confusables", [])
    )

    section_end()
