from ui.colors import BRIGHT_CYAN, BRIGHT_RED, BOLD, color


def ask(prompt):
    return input(
        color(f"\n  ❯ {prompt}: ", BRIGHT_CYAN + BOLD)
    )


def pause():
    input(
        color(
            "\n  Press ENTER to continue...",
            BRIGHT_CYAN,
        )
    )


def error(message):
    print(
        color(
            f"\n  ✖ {message}",
            BRIGHT_RED + BOLD,
        )
    )
