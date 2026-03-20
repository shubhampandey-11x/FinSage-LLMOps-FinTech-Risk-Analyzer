from fastapi import FastAPI
from pydantic import BaseModel
from backend.risk_service.analyzer import analyze_transaction

app = FastAPI()

class TransactionRequest(BaseModel):
    amount: float
    location: str
    merchant: str
    timestamp: str

@app.post("/analyze")
def analyze(request: TransactionRequest):
    data = request.dict()

    try:
        risk_result = analyze_transaction(data)
    except Exception as e:
        return {
            "error": str(e)
        }

    return {
        "input": data,
        "risk_analysis": risk_result
    }