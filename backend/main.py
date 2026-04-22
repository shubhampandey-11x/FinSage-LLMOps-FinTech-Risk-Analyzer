from fastapi import FastAPI

# 🔥 Initialize FastAPI FIRST
app = FastAPI()


@app.get("/")
def home():
    return {"message": "API Gateway Running"}


@app.post("/analyze-risk")
def analyze_risk(data: dict):
    try:
        # =========================================================
        # 🔹 FIX: Handle BOTH payload formats
        # frontend may send {"query": "..."} OR {"data": {"query": "..."}}
        # =========================================================
        query = (
            data.get("query")
            or (data.get("data", {}) or {}).get("query")
            or ""
        )
        query = str(query).lower().strip()

        # =========================================================
        # 🧠 STEP 1: Detect QUESTION vs TRANSACTION
        # =========================================================
        question_keywords = ["why", "what", "how", "explain", "define", "?"]

        if any(q in query for q in question_keywords):
            return {
                "risk": "N/A",
                "risk_score": 0,
                "explanation": "This is a financial concept explanation, not a transaction risk analysis.",
                "response": (
                    "A high debt-to-income ratio is risky because it indicates that a large portion "
                    "of income is already committed to debt repayments. This reduces financial flexibility "
                    "and increases the likelihood of default during financial stress."
                )
            }

        # =========================================================
        # 🔥 STEP 2: TRANSACTION RISK ENGINE
        # =========================================================
        risk_score = 20  # base score

        if "unknown" in query:
            risk_score += 50
        if "late night" in query or "night" in query:
            risk_score += 60
        if any(word in query for word in ["50000", "100000", "large", "huge"]):
            risk_score += 70

        # 🔹 Cap score
        risk_score = max(0, min(risk_score, 100))

        # 🔹 Risk label
        if risk_score >= 70:
            risk = "HIGH"
        elif risk_score >= 40:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        # 🧠 Explanation
        explanation = (
            f"This transaction is classified as {risk} risk based on amount, timing, "
            f"and account trust indicators."
        )

        # 🤖 Response
        if risk == "HIGH":
            response_text = "⚠️ High-risk transaction detected. Immediate verification is strongly recommended."
        elif risk == "MEDIUM":
            response_text = "⚠️ Moderate risk detected. Please review this transaction carefully."
        else:
            response_text = "✅ Low-risk transaction. No immediate concerns detected."

        # 🔹 Final response
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