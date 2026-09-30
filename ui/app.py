from analyzers.text import analyze_text
from analyzers.url import analyze_url
from core.comparison import compare_strings
from core.normalization import normalize_text
from core.characters import analyze_character

from reports.json import save_json
from reports.html import save_html

from ui.banner import print_banner
from ui.colors import clear_screen, success, info
from ui.menu import print_menu, ask_choice
from ui.prompts import ask, pause, error
from ui.renderer import (
    render_analysis,
    render_comparison,
    render_normalization,
)


def interactive_text():
    value = ask("Enter text")

    if not value:
        error("Input cannot be empty.")
        pause()
        return

    result = analyze_text(value)
    render_analysis(result)
    pause()


def interactive_url():
    value = ask("Enter URL or domain")

    if not value:
        error("Input cannot be empty.")
        pause()
        return

    result = analyze_url(value)
    render_analysis(result)
    pause()


def interactive_compare():
    original = ask("Original string")
    candidate = ask("Candidate string")

    if not original or not candidate:
        error("Both strings are required.")
        pause()
        return

    result = compare_strings(
        original,
        candidate,
    )

    render_comparison(result)
    pause()


def interactive_normalization():
    value = ask("Enter text")

    if not value:
        error("Input cannot be empty.")
        pause()
        return

    result = normalize_text(value)
    render_normalization(result)
    pause()


def interactive_character():
    value = ask("Enter one Unicode character")

    if not value:
        error("Character cannot be empty.")
        pause()
        return

    if len(value) != 1:
        error("Enter exactly one Unicode character.")
        pause()
        return

    result = analyze_character(
        value,
        0,
    )

    render_analysis({
        "input": value,
        "input_type": "character",
        "characters": [result],
        "risk": analyze_text(value)["risk"],
    })

    pause()


def interactive_export_json():
    value = ask("Enter text or URL")

    if not value:
        error("Input cannot be empty.")
        pause()
        return

    filename = ask("Output filename")

    if not filename:
        filename = "unicode-report.json"

    if "://" in value or value.startswith("www."):
        result = analyze_url(value)
    else:
        result = analyze_text(value)

    try:
        save_json(result, filename)
        print(success(f"JSON report saved: {filename}"))
    except OSError as exc:
        error(str(exc))

    pause()


def interactive_export_html():
    value = ask("Enter URL or domain")

    if not value:
        error("Input cannot be empty.")
        pause()
        return

    filename = ask("Output filename")

    if not filename:
        filename = "unicode-report.html"

    result = analyze_url(value)

    try:
        save_html(result, filename)
        print(success(f"HTML report saved: {filename}"))
    except OSError as exc:
        error(str(exc))

    pause()


def run_interactive():
    while True:
        clear_screen()
        print_banner()
        print_menu()

        choice = ask_choice()

        if choice == "1":
            interactive_text()

        elif choice == "2":
            interactive_url()

        elif choice == "3":
            interactive_compare()

        elif choice == "4":
            interactive_normalization()

        elif choice == "5":
            interactive_character()

        elif choice == "6":
            interactive_export_json()

        elif choice == "7":
            interactive_export_html()

        elif choice == "0":
            clear_screen()
            print_banner()
            print(info("Unicode Sentinel terminated."))
            print()
            break

        else:
            error("Invalid option.")
            pause()
