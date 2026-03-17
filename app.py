from guardrails.guardrails import validate_prompt, clean_prompt
from guardrails.evaluator import evaluate_response
from backend.explainability import generate_explanation

import streamlit as st
import ollama
import datetime
import re
import pandas as pd
import os

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="FinSage Dashboard", layout="wide")

# -----------------------------
# Ensure logs folder exists
# -----------------------------
os.makedirs("logs", exist_ok=True)

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
    return any(word in query.lower() for word in BLOCKED_WORDS)

# -----------------------------
# Normalize Risk Labels
# -----------------------------
def normalize_risk_label(risk_text):
    risk_text = risk_text.upper()

    if "HIGH" in risk_text:
        return "🔴 HIGH RISK"
    elif "MEDIUM" in risk_text:
        return "🟠 MEDIUM RISK"
    else:
        return "🟢 LOW RISK"

# -----------------------------
# Extract Structured Data
# -----------------------------
def extract_transaction_features(text):
    text = text.lower()

    amount_match = re.search(r'\d+', text)
    amount = int(amount_match.group()) if amount_match else 0

    time = 1 if ("midnight" in text or "night" in text) else 12
    is_new_beneficiary = "new" in text or "new account" in text
    is_international = "overseas" in text or "international" in text

    return {
        "amount": amount,
        "time": time,
        "is_new_beneficiary": is_new_beneficiary,
        "is_international": is_international
    }

# -----------------------------
# Parse LLM Response
# -----------------------------
def parse_response(response):
    risk = re.search(r"Risk Level:\s*(.*)", response, re.IGNORECASE)
    confidence = re.search(r"Confidence:\s*(.*)", response, re.IGNORECASE)
    action = re.search(r"Action:\s*(.*)", response, re.IGNORECASE)

    return {
        "risk": risk.group(1).strip() if risk else "N/A",
        "confidence": confidence.group(1).strip() if confidence else "N/A",
        "action": action.group(1).strip() if action else "N/A",
        "raw": response
    }

# -----------------------------
# Logging Function
# -----------------------------
def log_analysis(query, risk):
    with open("logs/analysis_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}|{risk}|{query}\n")

# -----------------------------
# UI
# -----------------------------
st.title("FinSage AI - Financial Risk Assistant")
st.caption("🔄 Dashboard updates after each analysis")

user_input = st.text_area("Transaction or Query:")

if st.button("Analyze"):

    if not user_input.strip():
        st.warning("Please enter a transaction or query.")
        st.stop()

    if is_malicious(user_input):
        st.error("⚠️ Security Policy: Blocked malicious query.")
        st.stop()

    valid, message = validate_prompt(user_input)
    if not valid:
        st.error(message)
        st.stop()

    cleaned_prompt = clean_prompt(user_input)

    with st.spinner("Analyzing..."):

        transaction_data = extract_transaction_features(cleaned_prompt)
        explanation = generate_explanation(transaction_data)

        # -----------------------------
        # STRONG PROMPT (FIXED)
        # -----------------------------
        response = ollama.chat(
            model="mistral",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert financial fraud detection AI."
                },
                {
                    "role": "user",
                    "content": f"""
Analyze the transaction and respond STRICTLY in format.

Risk Level: (LOW / MEDIUM / HIGH)
Confidence: (0-100%)
Reasons:
- ...
- ...
Action: (ONLY one word: ALLOW or REVIEW or BLOCK)

Transaction:
{cleaned_prompt}

System Signals:
Score: {explanation['risk_score']}
Reasons: {explanation['reasons']}
"""
                }
            ]
        )

        output = response["message"]["content"]
        parsed = parse_response(output)

        normalized_risk = normalize_risk_label(parsed["risk"])

        log_analysis(user_input, normalized_risk)

        # -----------------------------
        # UI OUTPUT
        # -----------------------------
        st.success("Analysis Result")

        st.subheader("🔍 Fraud Analysis")

        st.write(f"**Risk Level:** {normalized_risk}")
        st.write(f"**Confidence:** {parsed['confidence']}")
        st.write(f"**Action:** {parsed['action']}")

        # Risk Indicator
        if "HIGH" in normalized_risk:
            st.error("🔴 HIGH RISK TRANSACTION")
        elif "MEDIUM" in normalized_risk:
            st.warning("🟠 MEDIUM RISK TRANSACTION")
        else:
            st.success("🟢 LOW RISK TRANSACTION")

        # Confidence bar
        try:
            conf_value = int(parsed["confidence"].replace('%',''))
            st.progress(conf_value)
        except:
            pass

        # Explainability
        st.subheader("🔍 Explainability")
        st.write("Risk Score:", explanation["risk_score"])

        for reason in explanation["reasons"]:
            st.write(f"- {reason}")

        # Optional raw (collapsed)
        with st.expander("📄 Full LLM Response"):
            st.write(parsed["raw"])

# -----------------------------
# DASHBOARD
# -----------------------------
st.subheader("📊 Fraud Monitoring Dashboard")

try:
    data = []

    with open("logs/analysis_log.txt", "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 3:
                data.append(parts)

    df = pd.DataFrame(data, columns=["time", "risk", "query"])
    df["time"] = pd.to_datetime(df["time"])

    if not df.empty:

        st.write("### 📊 Risk Distribution")
        st.bar_chart(df["risk"].value_counts())

        st.write("### 📈 Transactions Over Time")
        st.line_chart(df.groupby(df["time"].dt.hour).size())

        st.write("### 🎯 Risk Breakdown")

        risk_counts = df["risk"].value_counts()

        col1, col2, col3 = st.columns(3)

        col1.metric("🔴 High Risk", risk_counts.get("🔴 HIGH RISK", 0))
        col2.metric("🟠 Medium Risk", risk_counts.get("🟠 MEDIUM RISK", 0))
        col3.metric("🟢 Low Risk", risk_counts.get("🟢 LOW RISK", 0))

        st.write("### 🚨 High Risk Alerts")
        st.dataframe(df[df["risk"].str.contains("HIGH", na=False)])

except:
    st.warning("No data available yet.")