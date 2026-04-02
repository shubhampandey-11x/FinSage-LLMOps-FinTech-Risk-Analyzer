import requests

def generate_risk_explanation(data, risk_score):
    prompt = f"""
You are a financial risk analyst.

Financial Data:
Revenue: {data['revenue']}
Debt: {data['debt']}
Expenses: {data['expenses']}
Cash Flow: {data['cash_flow']}

Risk Score: {risk_score}%

Explain:
- Why risk is high or low
- Key reasons
- Financial concerns

Keep it simple and professional.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    return result.get("response", "No explanation generated")