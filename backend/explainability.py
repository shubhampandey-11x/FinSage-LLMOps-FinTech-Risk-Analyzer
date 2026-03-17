def generate_explanation(transaction):
    reasons = []
    score = 0

    if transaction["amount"] > 100000:
        reasons.append("Large transaction amount")
        score += 2

    if 0 <= transaction["time"] <= 5:
        reasons.append("Transaction at unusual hour")
        score += 2

    if transaction.get("is_new_beneficiary", False):
        reasons.append("Transfer to new beneficiary")
        score += 2

    if transaction.get("is_international", False):
        reasons.append("International transaction")
        score += 3

    return {
        "risk_score": score,
        "reasons": reasons
    }
