import argparse
import sys

from analyzers.text import analyze_text
from analyzers.url import analyze_url, looks_like_url

from reports.json import generate_json, save_json
from reports.html import save_html

from ui.banner import print_banner

from ui.app import run_interactive

from reports.terminal import (
    print_header,
    print_risk,
    print_characters,
    print_confusables,
    print_comparison,
    print_comparison_evidence,
)


def analyze_value(value: str) -> dict:
    """
    Analyze text, URL, or domain and return the raw result.
    """

    if looks_like_url(value):
        return analyze_url(value)

    return analyze_text(value)


def print_terminal_report(result: dict):
    """
    Render the standard terminal report.
    """

    print_header()

    if result["input_type"] == "url":

        print(f"Input:   {result['input']}")
        print("Type:    URL")
        print(f"Domain:  {result['domain']}")
        print()

        idna = result["idna"]

        print("=" * 65)
        print("IDNA / PUNYCODE")
        print("=" * 65)

        print(f"Unicode Domain:   {idna['unicode']}")
        print(f"ASCII Domain:     {idna['ascii']}")

        print(
            f"IDNA/Punycode:    "
            f"{'YES' if idna['is_idna'] else 'NO'}"
        )

        print(
            f"Non-ASCII:        "
            f"{'YES' if idna['contains_non_ascii'] else 'NO'}"
        )

        print(
            f"Valid:            "
            f"{'YES' if idna['valid'] else 'NO'}"
        )

        if idna["error"]:
            print(
                f"Error:            "
                f"{idna['error']}"
            )

        print()

        print("=" * 65)
        print("UNICODE SKELETON")
        print("=" * 65)
        print(result["skeleton"])
        print()

    else:

        print(f"Input:   {result['input']}")
        print("Type:    TEXT")
        print()

    print_risk(result["risk"])

    print_characters(
        result["characters"]
    )

    print_confusables(
        result["characters"]
    )

    print_comparison(
        result["input"],
        result["characters"],
    )

    print_comparison_evidence(
        result["risk"],
    )


def analyze(value: str):
    """
    Analyze and display a value in terminal format.
    """

    result = analyze_value(value)

    print_terminal_report(result)


def build_parser():

    parser = argparse.ArgumentParser(
        description=(
            "Unicode Homoglyph Detector - "
            "Unicode, confusable, IDNA and risk analysis"
        )
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output analysis as JSON",
    )

    parser.add_argument(
        "--output",
        "-o",
        metavar="FILE",
        help="Save report to FILE",
    )

    parser.add_argument(
        "--html",
        action="store_true",
        help="Generate an HTML report",
    )

    parser.add_argument(
        "input",
        nargs="*",
        help="Text, URL, or domain to analyze",
    )

    return parser


def main():

    # =========================================================
    # Interactive UI
    # =========================================================

    if len(sys.argv) == 1:
        run_interactive()
        return

    # =========================================================
    # CLI banner
    # =========================================================

    

    parser = build_parser()

    args = parser.parse_args()

    # =========================================================
    # Validate options
    # =========================================================

    if args.html and not args.output:
        parser.error(
            "--html requires --output"
        )

    if args.html and args.json:
        parser.error(
            "--html and --json cannot be used together"
        )

    if args.output and not args.json and not args.html:
        parser.error(
            "--output requires --json or --html"
        )

    # =========================================================
    # No input
    # =========================================================

    if not args.input:

        if args.json:
            parser.error(
                "--json requires an input value"
            )

        run_interactive()
        return

    # =========================================================
    # Join command-line input
    # =========================================================

    value = " ".join(args.input)

    # =========================================================
    # HTML
    # =========================================================

    if args.html:

        result = analyze_value(value)

        save_html(
            result,
            args.output,
        )

        print(
            f"HTML report saved to: "
            f"{args.output}"
        )

        return

    # =========================================================
    # JSON
    # =========================================================

    if args.json:

        result = analyze_value(value)

        if args.output:

            save_json(
                result,
                args.output,
            )

            print(
                f"JSON report saved to: "
                f"{args.output}"
            )

        else:

            print(
                generate_json(result)
            )

        return

    # =========================================================
    # Standard CLI analysis
    # =========================================================

    analyze(value)


if __name__ == "__main__":
    main()