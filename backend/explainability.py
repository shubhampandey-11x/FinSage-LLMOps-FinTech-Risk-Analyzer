def generate_explanation(prompt, response):
    
    
    transaction = {
        "amount": 0,
        "time": 12,
        "is_new_beneficiary": False,
        "is_international": False
    }

    # simple parsing (safe)
    if "₹" in prompt:
        import re
        amt = re.findall(r"\d+", prompt.replace(",", ""))
        if amt:
            transaction["amount"] = int(amt[0])

    if "AM" in prompt:
        if "12 AM" in prompt or "1 AM" in prompt or "2 AM" in prompt or "3 AM" in prompt:
            transaction["time"] = 2

    if "New" in prompt:
        transaction["is_new_beneficiary"] = True

    if "International" in prompt or "Dubai" in prompt:
        transaction["is_international"] = True

    # ---- your original logic ----
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
        "reasons": reasons,
        "llm_response": response
    }
