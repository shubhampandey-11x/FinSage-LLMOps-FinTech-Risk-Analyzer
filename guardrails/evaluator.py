def evaluate_response(response: str):

    score = 0

    if len(response) > 50:
        score += 1

    if "risk" in response.lower():
        score += 1

    if "financial" in response.lower():
        score += 1

    quality = "LOW"

    if score == 3:
        quality = "HIGH"
    elif score == 2:
        quality = "MEDIUM"

    return {
        "score": score,
        "quality": quality
    }