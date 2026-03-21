from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Risk service running"}

@app.post("/risk-score")
def risk_score(data: dict):
    return {
        "risk_score": 85,
        "status": "HIGH RISK",
        "input": data
    }