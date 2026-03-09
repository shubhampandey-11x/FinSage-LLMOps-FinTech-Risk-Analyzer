import re

# blocked topics for finance assistant
BLOCKED_KEYWORDS = [
    "hack bank",
    "steal money",
    "bypass kyc",
    "fraud",
    "launder money",
]


def validate_prompt(prompt: str):

    prompt_lower = prompt.lower()

    for keyword in BLOCKED_KEYWORDS:
        if keyword in prompt_lower:
            return False, "Query violates financial safety policy."

    if len(prompt) < 5:
        return False, "Query too short."

    return True, "Valid prompt"


def clean_prompt(prompt: str):
    """
    Remove suspicious characters
    """

    prompt = re.sub(r"[<>]", "", prompt)

    return prompt.strip()