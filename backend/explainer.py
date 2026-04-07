import requests

def generate_risk_explanation(data, risk_score):
    prompt = f"""
You are a financial risk analyst AI.

Analyze the given financial data and return output STRICTLY in this format:

1. Risk Score (0–10 scale)
2. Key Risk Factors (bullet points)
3. Positive Signals (bullet points)
4. AI Insight (2–3 lines)
5. Final Verdict (Low / Moderate / High Risk with reason)
6. Explanation of Score (clear reasoning)

Be concise, structured, and professional.

Financial Data:
- Revenue: {data['revenue']}
- Debt: {data['debt']}
- Expenses: {data['expenses']}
- Cash Flow: {data['cash_flow']}

Existing Risk Score: {risk_score}%
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
    