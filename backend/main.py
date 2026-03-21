from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API Gateway Running"}

@app.post("/analyze-risk")
def analyze_risk(data: dict):
    try:
        response = requests.post(
            "http://127.0.0.1:8001/risk-score",
            json=data
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}