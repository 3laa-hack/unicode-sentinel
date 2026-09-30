# 🛡️ Unicode Sentinel

> **Unicode Homoglyph Detector** — Offensive Unicode Security Analysis

A security tool that detects **Unicode homoglyph attacks** (confusable characters),
**IDN spoofing**, and **mixed-script phishing** attempts in text, URLs, and domains.

---

## ✨ Features

- 🔍 **Character-level analysis** with Unicode names and scripts
- 🎯 **Cross-script confusable detection** (e.g., Cyrillic `а` vs Latin `a`)
- 🌐 **IDNA / Punycode** inspection
- 🕸️ **Unicode skeleton** generation
- ⚠️ **Heuristic risk scoring** (SAFE → CRITICAL)
- 📊 **Terminal / JSON / HTML** reports
- 🎨 **Colored terminal output** with banner and menu

---

## 🚀 Installation

```bash
git clone https://github.com/3laa-hack/unicode-sentinel.git
cd unicode-sentinel
pip install -r requirements.txt
```

---

## 🎮 Usage

### Analyze a URL

```bash
python3 main.py "https://аpple.com"
```

### Analyze text

```bash
python3 main.py "раypal"
```

### Interactive mode

```bash
python3 main.py
```

### JSON output

```bash
python3 main.py --json "https://аpple.com"
```

### HTML report

```bash
python3 main.py --html -o report.html "https://аpple.com"
```

---

## 🧪 Tests

```bash
pytest
```

---

## 📂 Project Structure

```
unicode-sentinel/
├── main.py                 # CLI entry point
├── analyzers/              # Text / URL analyzers
├── core/                   # Detection logic
│   ├── comparison.py       # Cross-script confusables
│   ├── confusables.py      # UTS #39 mappings
│   ├── idna.py             # IDNA / Punycode
│   ├── risk.py             # Risk scoring
│   ├── scripts.py          # Script detection
│   └── skeleton.py         # Unicode skeleton
├── data/                   # Unicode data files
├── reports/                # Output generators
│   ├── html.py
│   ├── json.py
│   └── terminal.py
├── ui/                     # Terminal UI
│   ├── banner.py
│   ├── colors.py
│   └── menu.py
└── tests/                  # Test suite
```

---

## 🛡️ License

MIT License — see [LICENSE](LICENSE).

---

## ⚠️ Disclaimer

This tool is intended for **defensive security research** and **educational purposes** only.
Do not use it for malicious activities.
