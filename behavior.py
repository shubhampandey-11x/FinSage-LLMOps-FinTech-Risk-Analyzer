def analyze_behavior(history):
    insights = []

    if not history:
        return "No past behavior available."

    high_risk_count = sum(1 for h in history if "HIGH" in h.get("risk", ""))

    if high_risk_count >= 2:
        insights.append(" Frequent high-risk transactions detected")

    if len(history) >= 3:
        insights.append(" Active transaction behavior observed")

    if not insights:
        return " No unusual behavior patterns detected"

    return " | ".join(insights)