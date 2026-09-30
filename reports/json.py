import json


def generate_json(
    result: dict,
    indent: int = 2,
) -> str:
    """
    Convert an analysis result into a JSON string.

    The complete analysis result is preserved, including
    Unicode, confusable, IDNA, skeleton and risk data.
    """

    return json.dumps(
        result,
        ensure_ascii=False,
        indent=indent,
    )


def save_json(
    result: dict,
    filename: str,
    indent: int = 2,
) -> None:
    """
    Save an analysis result as a UTF-8 JSON file.
    """

    data = generate_json(
        result,
        indent=indent,
    )

    with open(
        filename,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(data)
        file.write("\n")
