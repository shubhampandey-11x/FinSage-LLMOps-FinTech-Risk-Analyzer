from fastapi import FastAPI
import requests
from backend.explainer import generate_risk_explanation  

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API Gateway Running"}

@app.post("/analyze-risk")
def analyze_risk(data: dict):
    try:
        # Call risk service
        response = requests.post(
            "http://127.0.0.1:8001/risk-score",
            json=data
        )

        result = response.json()

        #  Extract risk score
        risk_score = result.get("risk_score")

        # 🔹 Generate AI explanation
        explanation = generate_risk_explanation(data, risk_score)

        #  Return both
        return {
            "risk_score": risk_score,
            "explanation": explanation
        }

    except Exception as e:
        return {"error": str(e)}