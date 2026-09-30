from html import escape


def _risk_class(level: str) -> str:
    return level.lower()


def generate_html(result: dict) -> str:
    risk = result["risk"]
    characters = result["characters"]

    rows = []

    for item in characters:
        char = item["character"]

        if char == " ":
            display_char = "&lt;space&gt;"
        elif char == "\t":
            display_char = "&lt;tab&gt;"
        elif char == "\n":
            display_char = "&lt;newline&gt;"
        else:
            display_char = escape(char)

        cross_script = False

        source_script = item.get("script", "")

        for confusable in item.get("confusables", []):
            target = confusable.get("character", "")

            target_scripts = set()

            for target_char in target:
                from core.scripts import detect_script

                script = detect_script(target_char)

                if script not in {
                    "Common",
                    "Unknown",
                    "Punctuation",
                    "Number",
                    "Separator",
                    "Symbol",
                    "Mark",
                }:
                    target_scripts.add(script)

            if any(
                script != source_script
                for script in target_scripts
            ):
                cross_script = True
                break

        row_class = "suspicious" if cross_script else ""

        rows.append(
            f"""
            <tr class="{row_class}">
                <td>{item["position"]}</td>
                <td class="character">{display_char}</td>
                <td>{escape(item["codepoint"])}</td>
                <td>{escape(item["script"])}</td>
                <td>{escape(item["unicode_name"])}</td>
            </tr>
            """
        )

    reasons = ""

    for reason in risk.get("reasons", []):
        reasons += f"<li>{escape(reason)}</li>"

    if not reasons:
        reasons = "<li>No security risk factors detected.</li>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Unicode Homoglyph Detector</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 30px;
    background: #0B1120;
    color: #E2E8F0;
    font-family:
        Inter,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}}

.container {{
    max-width: 1200px;
    margin: auto;
}}

h1 {{
    color: #22D3EE;
    margin-bottom: 5px;
}}

.subtitle {{
    color: #94A3B8;
    margin-bottom: 30px;
}}

.card {{
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
}}

.input-value {{
    font-family: monospace;
    font-size: 18px;
    word-break: break-all;
}}

.risk {{
    font-size: 28px;
    font-weight: bold;
}}

.risk.safe {{
    color: #10B981;
}}

.risk.low {{
    color: #22D3EE;
}}

.risk.medium {{
    color: #F59E0B;
}}

.risk.high {{
    color: #F97316;
}}

.risk.critical {{
    color: #EF4444;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th {{
    text-align: left;
    background: #0F172A;
    color: #22D3EE;
    padding: 12px;
}}

td {{
    padding: 10px 12px;
    border-bottom: 1px solid #334155;
}}

.character {{
    font-size: 20px;
    font-family: monospace;
}}

tr.suspicious {{
    background: rgba(239, 68, 68, 0.15);
}}

tr.suspicious td {{
    border-bottom-color: #7F1D1D;
}}

code {{
    background: #0F172A;
    padding: 3px 7px;
    border-radius: 5px;
}}

ul {{
    line-height: 1.8;
}}

.badge {{
    display: inline-block;
    padding: 5px 10px;
    border-radius: 6px;
    background: #0F172A;
    color: #CBD5E1;
}}

pre {{
    white-space: pre-wrap;
    word-break: break-all;
    background: #0F172A;
    padding: 15px;
    border-radius: 8px;
}}

</style>
</head>

<body>

<div class="container">

<h1>Unicode Homoglyph Detector</h1>

<div class="subtitle">
Unicode Security Analysis Report
</div>

<div class="card">

<h2>Input</h2>

<div class="input-value">
{escape(result["input"])}
</div>

<p>
Type:
<span class="badge">
{escape(result["input_type"])}
</span>
</p>

</div>

<div class="card">

<h2>Risk Assessment</h2>

<div class="risk {_risk_class(risk["level"])}">
{escape(risk["level"])}
</div>

<p>
Score: <strong>{risk["score"]}</strong>
</p>

<p>
Mixed Script:
<strong>
{"YES" if risk["mixed_script"] else "NO"}
</strong>
</p>

<p>
Confusable Characters:
<strong>
{risk["confusable_count"]}
</strong>
</p>

</div>

<div class="card">

<h2>Risk Factors</h2>

<ul>
{reasons}
</ul>

</div>
"""

    if result["input_type"] == "url":

        idna = result["idna"]

        html += f"""
<div class="card">

<h2>IDNA / Punycode</h2>

<p>
Unicode Domain:
<br>
<code>{escape(idna["unicode"])}</code>
</p>

<p>
ASCII Domain:
<br>
<code>{escape(idna["ascii"])}</code>
</p>

<p>
IDNA/Punycode:
<strong>
{"YES" if idna["is_idna"] else "NO"}
</strong>
</p>

<p>
Non-ASCII:
<strong>
{"YES" if idna["contains_non_ascii"] else "NO"}
</strong>
</p>

<p>
Valid:
<strong>
{"YES" if idna["valid"] else "NO"}
</strong>
</p>

</div>

<div class="card">

<h2>Unicode Skeleton</h2>

<pre>{escape(result["skeleton"])}</pre>

</div>
"""

    # ------------------------------------------------------------------
    # NEW: Security Comparison Evidence
    # ------------------------------------------------------------------
    comparison_evidence = risk.get(
        "comparison_evidence",
        []
    )

    if comparison_evidence:

        html += """
<div class="card">

<h2>Security Comparison Evidence</h2>

"""

        for evidence in comparison_evidence:

            confusable = evidence["confusable"]

            html += f"""
<div class="card">

<p>
<strong>Position:</strong>
{evidence["position"]}
</p>

<p>
<strong>Character:</strong>
<code>{escape(evidence["character"])}</code>
</p>

<p>
<strong>Code Point:</strong>
<code>{escape(evidence["codepoint"])}</code>
</p>

<p>
<strong>Source Script:</strong>
<span class="badge">
{escape(evidence["script"])}
</span>
</p>

<p>
<strong>Confusable:</strong>
<code>{escape(confusable["character"])}</code>
</p>

<p>
<strong>Target Code Point:</strong>
<code>{escape(confusable["codepoint"])}</code>
</p>

<p>
<strong>Target Script:</strong>
<span class="badge">
{", ".join(
    escape(script)
    for script in evidence["target_scripts"]
)}
</span>
</p>

<p>
<strong>Type:</strong>
<span class="badge">
CROSS-SCRIPT
</span>
</p>

</div>
"""

        html += """
</div>
"""

    # ------------------------------------------------------------------
    # Character Analysis
    # ------------------------------------------------------------------
    html += f"""
<div class="card">

<h2>Character Analysis</h2>

<table>

<thead>
<tr>
<th>Position</th>
<th>Character</th>
<th>Code Point</th>
<th>Script</th>
<th>Unicode Name</th>
</tr>
</thead>

<tbody>

{"".join(rows)}

</tbody>

</table>

</div>

<div class="card">

<h2>Confusable Characters</h2>
"""

    found = False

    for item in characters:

        for confusable in item.get("confusables", []):

            target = confusable.get("character", "")

            if not target:
                continue

            found = True

            html += f"""
<p>
<strong>
Position {item["position"]}
</strong>
<br>

<code>
{escape(item["character"])}
{escape(item["codepoint"])}
</code>

→

<code>
{escape(target)}
{escape(confusable["codepoint"])}
</code>

<br>

{escape(confusable["unicode_name"])}

</p>
"""

    if not found:
        html += "<p>No known confusable mappings found.</p>"

    html += """
</div>

</div>

</body>
</html>
"""

    return html


def save_html(
    result: dict,
    filename: str,
) -> None:

    html = generate_html(result)

    with open(
        filename,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(html)