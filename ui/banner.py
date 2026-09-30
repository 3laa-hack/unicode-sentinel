from ui.colors import (
    BOLD,
    BRIGHT_BLUE,
    BRIGHT_CYAN,
    BRIGHT_GREEN,
    BRIGHT_MAGENTA,
    BRIGHT_RED,
    BRIGHT_WHITE,
    RESET,
    color,
)


# ============================================================
# Unicode Sentinel — Banner
# ============================================================

INNER_WIDTH = 62


def _line(content: str, shade: str) -> str:
    """
    بناء سطر داخل الإطار بعرض ثابت مع توسيط تلقائي.
    """
    return color(
        f"║{content.center(INNER_WIDTH)}║",
        shade + BOLD,
    )


def print_banner():
    """
    طباعة شعار Unicode Sentinel بشكل متوازن ومحاذى.
    """

    print()

    # --------------------------------------------------------
    # الإطار العلوي
    # --------------------------------------------------------

    print(color(
        "╔" + "═" * INNER_WIDTH + "╗",
        BRIGHT_CYAN + BOLD,
    ))

    print(_line("", BRIGHT_BLUE))

    # --------------------------------------------------------
    # شعار UNICODE
    # --------------------------------------------------------

    logo = [
        "██╗   ██╗███╗   ██╗██╗ ██████╗ ██████╗ ██████╗ ██████╗ ",
        "██║   ██║████╗  ██║██║██╔════╝██╔═══██╗██╔══██╗██╔══██╗",
        "██║   ██║██╔██╗ ██║██║██║     ██║   ██║██████╔╝██║  ██║",
        "╚██╗ ██╔╝██║╚██╗██║██║██║     ██║   ██║██╔═══╝ ██║  ██║",
        " ╚████╔╝ ██║ ╚████║██║╚██████╗╚██████╔╝██║     ██████╔╝",
        "  ╚═══╝  ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═════╝ ",
    ]

    colors = [
        BRIGHT_CYAN,
        BRIGHT_BLUE,
        BRIGHT_MAGENTA,
        BRIGHT_MAGENTA,
        BRIGHT_BLUE,
        BRIGHT_CYAN,
    ]

    for line, shade in zip(logo, colors):
        print(_line(line.strip().center(INNER_WIDTH), shade))

    print(_line("", BRIGHT_BLUE))

    # --------------------------------------------------------
    # العنوان الرئيسي
    # --------------------------------------------------------

    print(_line(
        "U N I C O D E   S E N T I N E L",
        BRIGHT_MAGENTA,
    ))

    print(_line(
        "UNICODE HOMOGLYPH DETECTOR",
        BRIGHT_WHITE,
    ))

    print(_line(
        "Unicode • Confusables • IDNA • Security",
        BRIGHT_GREEN,
    ))

    print(_line("", BRIGHT_BLUE))

    # --------------------------------------------------------
    # سطر التحذير الأمني
    # --------------------------------------------------------

    print(_line(
        "[!]  IDENTITY • SCRIPT • SPOOFING • PHISHING",
        BRIGHT_RED,
    ))

    print(_line("", BRIGHT_BLUE))

    # --------------------------------------------------------
    # الإطار السفلي
    # --------------------------------------------------------

    print(color(
        "╚" + "═" * INNER_WIDTH + "╝",
        BRIGHT_CYAN + BOLD,
    ))

    print()