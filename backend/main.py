from fastapi import FastAPI
import requests
import os
from backend.explainer import generate_risk_explanation  

app = FastAPI()

# 🔥 Use ENV for service URL (important for deployment)
RISK_SERVICE_URL = os.getenv("RISK_SERVICE_URL", "http://127.0.0.1:8001/risk-score")


@app.get("/")
def home():
    return {"message": "API Gateway Running"}


@app.post("/analyze-risk")
def analyze_risk(data: dict):
    try:
        # 🔹 Call risk service
        response = requests.post(
            RISK_SERVICE_URL,
            json=data,
            timeout=10
        )

        result = response.json()

        # 🔹 Extract risk score (safe fallback)
        risk_score = result.get("risk_score", 50)

        # 🔹 Derive risk label
        if risk_score >= 70:
            risk = "HIGH"
        elif risk_score >= 40:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        # 🔹 Generate AI explanation
        explanation = generate_risk_explanation(data, risk_score)

        # 🔹 Final response (FULL payload for frontend)
        return {
            "risk": risk,
            "risk_score": risk_score,
            "explanation": explanation,
            "response": "Risk analysis completed successfully"
        }

    except Exception as e:
        return {
            "risk": "UNKNOWN",
            "risk_score": 0,
            "explanation": "Error occurred during analysis",
            "response": str(e)
        }