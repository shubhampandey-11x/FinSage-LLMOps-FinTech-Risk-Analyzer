# backend/risk_service/analyzer.py

def analyze_transaction(data):
    # Simple rule-based logic (safe version)

    risk_score = 0
    reasons = []

    if data["amount"] > 100000:
        risk_score += 50
        reasons.append("High transaction amount")

    if "dealer" in data["merchant"].lower() or "crypto" in data["merchant"].lower():
        risk_score += 30
        reasons.append("Suspicious merchant")

    if data["location"].lower() not in ["delhi", "mumbai", "bangalore"]:
        risk_score += 20
        reasons.append("Unusual location")

    return {
        "risk_score": risk_score,
        "risk_level": "HIGH" if risk_score > 60 else "MEDIUM" if risk_score > 30 else "LOW",
        "reasons": reasons
    }