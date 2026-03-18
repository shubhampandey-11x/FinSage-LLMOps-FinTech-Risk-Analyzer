from guardrails.guardrails import validate_prompt, clean_prompt

def process_prompt(prompt):
    if not validate_prompt(prompt):
        return None, "Invalid prompt"

    cleaned = clean_prompt(prompt)
    return cleaned, None