from ui.colors import (
    BRIGHT_BLUE,
    BRIGHT_CYAN,
    BRIGHT_GREEN,
    BRIGHT_MAGENTA,
    BRIGHT_RED,
    BRIGHT_WHITE,
    BOLD,
    RESET,
    color,
)


# ============================================================
# Unicode Sentinel — Main Menu
# ============================================================

INNER_WIDTH = 62


def _row(content: str) -> str:
    """
    سطر داخل الإطار بعرض ثابت 62 حرفًا.
    """
    return (
        color("│  ", BRIGHT_BLUE)
        + content.ljust(INNER_WIDTH - 2)
        + color("│", BRIGHT_BLUE)
    )


def print_menu():
    """
    طباعة القائمة الرئيسية بشكل متوازن ومحاذى.
    """

    print()

    # --------------------------------------------------------
    # السطر العلوي
    # --------------------------------------------------------

    title = " MAIN MENU "
    dashes = "─" * (INNER_WIDTH - len(title) - 1)

    print(
        color("╭─", BRIGHT_BLUE + BOLD)
        + color(title, BRIGHT_CYAN + BOLD)
        + color(dashes + "╮", BRIGHT_BLUE)
    )

    # --------------------------------------------------------
    # فراغ
    # --------------------------------------------------------

    print(_row(""))

    # --------------------------------------------------------
    # الخيارات
    # --------------------------------------------------------

    options = [
        ("1", "Analyze Text",            BRIGHT_CYAN),
        ("2", "Analyze URL / Domain",    BRIGHT_BLUE),
        ("3", "Compare Two Strings",     BRIGHT_MAGENTA),
        ("4", "Unicode Normalization",   BRIGHT_GREEN),
        ("5", "Analyze Character",       BRIGHT_CYAN),
        ("6", "Export JSON",             BRIGHT_WHITE),
        ("7", "Export HTML",             BRIGHT_WHITE),
        ("0", "Exit",                    BRIGHT_RED),
    ]

    for number, label, shade in options:
        content = (
            color(f"[{number}]", shade + BOLD)
            + f" {label}"
        )

        # حساب طول النص بدون ANSI للحفاظ على المحاذاة
        visible_length = len(f"[{number}] {label}")
        padding = " " * (INNER_WIDTH - 2 - visible_length)

        print(
            color("│  ", BRIGHT_BLUE)
            + content
            + padding
            + color("│", BRIGHT_BLUE)
        )

    # --------------------------------------------------------
    # فراغ
    # --------------------------------------------------------

    print(_row(""))

    # --------------------------------------------------------
    # السطر السفلي
    # --------------------------------------------------------

    print(
        color(
            "╰" + "─" * INNER_WIDTH + "╯",
            BRIGHT_BLUE + BOLD,
        )
    )


def ask_choice():
    """
    طلب اختيار من المستخدم.
    """
    return input(
        color("\n  > Select option: ", BRIGHT_CYAN + BOLD)
    ).strip()