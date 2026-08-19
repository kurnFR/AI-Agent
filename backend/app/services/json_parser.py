import json
import re
from typing import Any, Dict


def extract_json(text: str) -> Dict[str, Any]:
    """
    Extract a JSON object from text, handling markdown code fences,
    leading/trailing conversational preamble, and raw JSON.
    """
    if not text or not isinstance(text, str):
        return {}

    cleaned = text.strip()

    # If wrapped in markdown code block
    if "```" in cleaned:
        # Match ```json ... ``` or ``` ... ```
        pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
        matches = re.findall(pattern, cleaned, re.DOTALL | re.IGNORECASE)
        for match in matches:
            try:
                parsed = json.loads(match.strip())
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                continue

    # Try direct parse
    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass

    # Try finding the first '{' and last '}'
    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")
    if first_brace != -1 and last_brace > first_brace:
        candidate = cleaned[first_brace:last_brace + 1]
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

    return {}
