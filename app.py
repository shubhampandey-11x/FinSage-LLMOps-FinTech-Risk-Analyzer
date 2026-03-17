from guardrails.guardrails import validate_prompt, clean_prompt
from guardrails.evaluator import evaluate_response
from backend.explainability import generate_explanation  # ✅ NEW

import streamlit as st
import ollama
import datetime
import re  # ✅ for extracting numbers

# -----------------------------
# Security Guardrail
# -----------------------------

BLOCKED_WORDS = [
    "hack", "hacking", "exploit", "bypass",
    "malware", "steal", "attack", "breach"
]

def is_malicious(query: str) -> bool:
    if not query:
        return False
    q = query.lower()
    return any(word in q for word in BLOCKED_WORDS)


# -----------------------------
# Risk Classification
# -----------------------------

def classify_risk(text):

    text = text.lower()

    high_risk_keywords = [
        "fraud", "suspicious", "money laundering",
        "offshore", "unusual", "large transfer",
        "overseas", "new account"
    ]

    for word in high_risk_keywords:
        if word in text:
            return "🔴 HIGH RISK"

    medium_keywords = ["monitor", "review", "verify"]

    for word in medium_keywords:
        if word in text:
            return "🟠 MEDIUM RISK"

    return "🟢 LOW RISK"


# -----------------------------
# Extract Structured Data (NEW)
# -----------------------------

def extract_transaction_features(text):
    text = text.lower()

    # Extract amount
    amount_match = re.search(r'\d+', text)
    amount = int(amount_match.group()) if amount_match else 0

    # Detect time (simple logic)
    if "midnight" in text or "night" in text:
        time = 1
    else:
        time = 12

    # Detect flags
    is_new_beneficiary = "new" in text or "new account" in text
    is_international = "overseas" in text or "international" in text

    return {
        "amount": amount,
        "time": time,
        "is_new_beneficiary": is_new_beneficiary,
        "is_international": is_international
    }


# -----------------------------
# Logging Function
# -----------------------------

def log_analysis(query, response, risk):

    with open("logs/analysis_log.txt", "a") as f:
        f.write("\n----------------------------\n")
        f.write(f"Time: {datetime.datetime.now()}\n")
        f.write(f"Query: {query}\n")
        f.write(f"Risk Level: {risk}\n")
        f.write(f"Response: {response}\n")


# -----------------------------
# Streamlit UI
# -----------------------------

st.title("FinSage AI - Financial Risk Assistant")
st.write("Enter a financial transaction to analyze.")

user_input = st.text_area("Transaction or Query:")

if st.button("Analyze"):

    if not user_input or not user_input.strip():
        st.warning("Please enter a transaction or query.")
        st.stop()

    # Guardrail check
    if is_malicious(user_input):
        st.error("⚠️ Security Policy: This system cannot answer hacking or exploitation questions.")
        st.stop()

    valid, message = validate_prompt(user_input)

    if not valid:
        st.error(message)
        st.stop()

    cleaned_prompt = clean_prompt(user_input)

    with st.spinner("Analyzing..."):

        # 🔥 Extract structured features
        transaction_data = extract_transaction_features(cleaned_prompt)

        # 🔥 Generate explainability BEFORE LLM
        explanation = generate_explanation(transaction_data)

        response = ollama.chat(
            model="mistral",
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial fraud analyst. Analyze financial transactions and detect suspicious activity."
                },
                {
                    "role": "user",
                    "content": f"""
Transaction Details:
{cleaned_prompt}

System Risk Signals:
Score: {explanation['risk_score']}
Reasons: {explanation['reasons']}

Now give final fraud analysis and conclusion.
"""
                }
            ]
        )

        output = response["message"]["content"]

        evaluation = evaluate_response(output)

        # Risk classification
        risk = classify_risk(output)

        # Logging
        log_analysis(user_input, output, risk)

        # -----------------------------
        # UI OUTPUT
        # -----------------------------

        st.success("Analysis Result")

        st.write(output)

        st.subheader("Risk Level")
        st.write(risk)

        # 🔥 NEW SECTION (DAY 7 CORE)
        st.subheader("🔍 Explainability")

        st.write("Risk Score:", explanation["risk_score"])

        for reason in explanation["reasons"]:
            st.write(f"- {reason}")

        st.info(f"Response Quality: {evaluation['quality']}")