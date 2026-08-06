import json


def parse(text: str):

    text = text.strip()

    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0]

    return json.loads(text)
