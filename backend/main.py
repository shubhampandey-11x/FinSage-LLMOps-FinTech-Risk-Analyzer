from fastapi import FastAPI

# 🔥 Initialize FastAPI FIRST (must be before any routes)
app = FastAPI()


@app.get("/")
def home():
    return {"message": "API Gateway Running"}


@app.post("/analyze-risk")
def analyze_risk(data: dict):
    try:
        # 🔹 Safe query extraction
        query = str(data.get("query", "")).lower().strip()

        # 🔥 RULE-BASED RISK ENGINE
        risk_score = 20  # base score

        if "unknown" in query:
            risk_score += 30
        if "late night" in query or "night" in query:
            risk_score += 20
        if any(word in query for word in ["50000", "100000", "large", "huge"]):
            risk_score += 20

        # 🔹 Cap score between 0–100
        risk_score = max(0, min(risk_score, 100))

        # 🔹 Risk label
        if risk_score >= 70:
            risk = "HIGH"
        elif risk_score >= 40:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        # 🧠 AI EXPLANATION (safe fallback, no dependency issues)
        explanation = (
            f"This transaction is classified as {risk} risk based on amount, timing, "
            f"and account trust indicators."
        )

        # 🤖 AI RESPONSE
        if risk == "HIGH":
            response_text = "⚠️ High-risk transaction detected. Immediate verification is strongly recommended."
        elif risk == "MEDIUM":
            response_text = "⚠️ Moderate risk detected. Please review this transaction carefully."
        else:
            response_text = "✅ Low-risk transaction. No immediate concerns detected."

        # 🔹 FINAL RESPONSE (frontend-safe)
        return {
            "risk": risk,
            "risk_score": risk_score,
            "explanation": explanation,
            "response": response_text
        }

    except Exception as e:
        return {
            "risk": "UNKNOWN",
            "risk_score": 0,
            "explanation": "Error occurred during analysis",
            "response": str(e)
        }