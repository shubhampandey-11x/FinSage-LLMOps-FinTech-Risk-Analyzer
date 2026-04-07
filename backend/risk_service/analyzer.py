# backend/risk_service/analyzer.py

import re

def extract_amount(text):
    """Extract amount from text if possible"""
    match = re.search(r"\b\d{4,}\b", text)
    return int(match.group()) if match else 0

def analyze_transaction(data):
    """
    Handles BOTH:
    1. Structured dict input ✅
    2. Raw text input (LLM/string) ✅
    """

    # -----------------------------
    # 🛡️ CASE 1: If data is STRING
    # -----------------------------
    if isinstance(data, str):
        text = data.lower()

        amount = extract_amount(text)

        risk_score = 0
        reasons = []

        if amount > 100000:
            risk_score += 50
            reasons.append("High transaction amount (parsed from text)")

        if "crypto" in text or "dealer" in text:
            risk_score += 30
            reasons.append("Suspicious keywords in transaction")

        if "international" in text or "unknown location" in text:
            risk_score += 20
            reasons.append("Unusual location")

    # -----------------------------
    # 🧠 CASE 2: If data is DICT
    # -----------------------------
    else:
        risk_score = 0
        reasons = []

        amount = data.get("amount", 0)
        merchant = data.get("merchant", "").lower()
        location = data.get("location", "").lower()

        if amount > 100000:
            risk_score += 50
            reasons.append("High transaction amount")

        if "dealer" in merchant or "crypto" in merchant:
            risk_score += 30
            reasons.append("Suspicious merchant")

        if location not in ["delhi", "mumbai", "bangalore"]:
            risk_score += 20
            reasons.append("Unusual location")

    # -----------------------------
    # 🎯 FINAL OUTPUT
    # -----------------------------
    return {
        "risk_score": risk_score,
        "risk_level": "HIGH" if risk_score > 60 else "MEDIUM" if risk_score > 30 else "LOW",
        "reasons": reasons
    }