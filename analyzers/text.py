from core.characters import analyze_text_characters
from core.confusables import get_confusable_details
from core.risk import calculate_risk


def analyze_text(text: str) -> dict:

    characters = analyze_text_characters(text)

    for item in characters:

        item["confusables"] = get_confusable_details(
            item["character"]
        )

    risk = calculate_risk(
        characters,
        input_type="text"
    )

    return {
        "input": text,
        "input_type": "text",
        "characters": characters,
        "risk": risk,
    }
