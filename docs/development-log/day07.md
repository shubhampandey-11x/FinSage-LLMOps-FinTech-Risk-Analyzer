Day 7 – Explainable AI (XAI) Integration
Overview
On Day 7, an Explainable AI (XAI) layer was integrated into the FinSage LLMOps Fraud Detection system to eliminate black-box behavior and improve transparency in risk predictions.
Objectives
Add interpretability to fraud detection outputs
Provide clear reasoning behind risk classification
Combine rule-based logic with LLM reasoning
Implementation Details
1. Explainability Engine
Created backend/explainability.py
Implemented rule-based scoring using:
Transaction amount
Time of transaction
New beneficiary detection
International transfer flag
Output:
risk_score (numeric)
reasons (list of explanations)
2. Feature Extraction
Added logic in app.py to extract structured data from user input:
Parsed amount using regex
Detected keywords like:
“midnight” → unusual time
“new account” → new beneficiary
“overseas” → international
3. LLM Integration (Hybrid Approach)
Modified LLM prompt to include:
Transaction details
Risk score
Explanation reasons
Result:
Improved contextual accuracy
Reduced hallucination
More consistent outputs
4. UI Enhancement (Streamlit)
Added Explainability section:
Displayed risk score
Displayed bullet-point reasons
Improved user trust and readability
5. Codebase Improvements
Introduced modular backend (backend/ folder)
Added __init__.py for proper package structure
Maintained separation of concerns
Output Example
Risk Level:  HIGH RISK
Risk Score: 9
Reasons:
Large transaction amount
Transaction at unusual hour
Transfer to new beneficiary
International transaction
Key Outcomes
Eliminated black-box decision making
Improved transparency and interpretability
Built hybrid AI system (rule-based + LLM)
Enhanced system reliability and user trust
