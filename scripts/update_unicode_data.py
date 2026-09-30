#!/usr/bin/env python3

import json
import re
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "data"

CONFUSABLES_URL = (
    "https://www.unicode.org/Public/security/latest/confusables.txt"
)

SCRIPTS_URL = (
    "https://www.unicode.org/Public/UCD/latest/ucd/Scripts.txt"
)

def download(url):
    print(f"[+] Downloading: {url}")

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Unicode-Homoglyph-Detector/1.0"
        }
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")

def parse_codepoints(value):
    return [int(x, 16) for x in value.strip().split()]

def codepoints_to_string(values):
    return "".join(chr(x) for x in values)

def parse_confusables(text):
    mappings = {}
    sequences = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        if "#" in line:
            data, comment = line.split("#", 1)
        else:
            data = line
            comment = ""

        parts = [p.strip() for p in data.split(";")]

        if len(parts) < 2:
            continue

        source_hex = parts[0]
        target_hex = parts[1]

        try:
            source = parse_codepoints(source_hex)
            target = parse_codepoints(target_hex)
        except ValueError:
            continue

        source_text = codepoints_to_string(source)
        target_text = codepoints_to_string(target)

        entry = {
            "source": source_hex.upper(),
            "target": target_hex.upper(),
            "source_char": source_text,
            "target_char": target_text,
            "comment": comment.strip(),
        }

        # Single Unicode character mappings
        if len(source) == 1:
            cp = f"{source[0]:04X}"
            mappings[cp] = entry

        # Multi-character mappings
        else:
            sequences.append(entry)

    return {
        "mappings": mappings,
        "sequences": sequences,
    }

def parse_scripts(text):
    scripts = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        if "#" in line:
            data, comment = line.split("#", 1)
        else:
            data = line
            comment = ""

        if ";" not in data:
            continue

        range_part, script = data.split(";", 1)

        range_part = range_part.strip()
        script = script.strip()

        try:
            if ".." in range_part:
                start_hex, end_hex = range_part.split("..")
                start = int(start_hex, 16)
                end = int(end_hex, 16)
            else:
                start = int(range_part, 16)
                end = start
        except ValueError:
            continue

        scripts.append({
            "start": f"{start:04X}",
            "end": f"{end:04X}",
            "script": script,
        })

    return scripts

def main():

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Unicode Security Data Updater")
    print("=" * 60)

    # ---------------------------------------------------------
    # Confusables
    # ---------------------------------------------------------

    confusables_text = download(CONFUSABLES_URL)

    confusables = parse_confusables(confusables_text)

    confusables_output = {
        "source": CONFUSABLES_URL,
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
        "mappings_count": len(confusables["mappings"]),
        "sequences_count": len(confusables["sequences"]),
        "mappings": confusables["mappings"],
        "sequences": confusables["sequences"],
    }

    confusables_file = DATA_DIR / "confusables.json"

    with confusables_file.open("w", encoding="utf-8") as f:
        json.dump(
            confusables_output,
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(
        f"[+] Confusable mappings: "
        f"{confusables_output['mappings_count']}"
    )

    print(
        f"[+] Confusable sequences: "
        f"{confusables_output['sequences_count']}"
    )

    print(f"[+] Saved: {confusables_file}")

    # ---------------------------------------------------------
    # Scripts
    # ---------------------------------------------------------

    scripts_text = download(SCRIPTS_URL)

    scripts = parse_scripts(scripts_text)

    scripts_output = {
        "source": SCRIPTS_URL,
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
        "ranges_count": len(scripts),
        "ranges": scripts,
    }

    scripts_file = DATA_DIR / "scripts.json"

    with scripts_file.open("w", encoding="utf-8") as f:
        json.dump(
            scripts_output,
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"[+] Script ranges: {len(scripts)}")
    print(f"[+] Saved: {scripts_file}")

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    metadata = {
        "confusables_source": CONFUSABLES_URL,
        "scripts_source": SCRIPTS_URL,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    metadata_file = DATA_DIR / "unicode_data.json"

    with metadata_file.open("w", encoding="utf-8") as f:
        json.dump(
            metadata,
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"[+] Saved: {metadata_file}")

    print()
    print("[+] Unicode data update completed.")

if __name__ == "__main__":
    main()
