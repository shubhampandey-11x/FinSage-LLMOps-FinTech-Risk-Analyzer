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
# Page Config (NEW)
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
# Extract Structured Data
# -----------------------------

def extract_transaction_features(text):
    text = text.lower()

    amount_match = re.search(r'\d+', text)
    amount = int(amount_match.group()) if amount_match else 0

    if "midnight" in text or "night" in text:
        time = 1
    else:
        time = 12

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
        f.write(f"{datetime.datetime.now()}|{risk}|{query}\n")


# -----------------------------
# Streamlit UI
# -----------------------------

st.title("FinSage AI - Financial Risk Assistant")
st.caption("🔄 Dashboard updates after each analysis")

user_input = st.text_area("Transaction or Query:")

if st.button("Analyze"):

    if not user_input or not user_input.strip():
        st.warning("Please enter a transaction or query.")
        st.stop()

    if is_malicious(user_input):
        st.error("⚠️ Security Policy: This system cannot answer hacking or exploitation questions.")
        st.stop()

    valid, message = validate_prompt(user_input)

    if not valid:
        st.error(message)
        st.stop()

    cleaned_prompt = clean_prompt(user_input)

    with st.spinner("Analyzing..."):

        transaction_data = extract_transaction_features(cleaned_prompt)
        explanation = generate_explanation(transaction_data)

        response = ollama.chat(
            model="mistral",
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial fraud analyst."
                },
                {
                    "role": "user",
                    "content": f"""
Transaction Details:
{cleaned_prompt}

System Risk Signals:
Score: {explanation['risk_score']}
Reasons: {explanation['reasons']}

Give final fraud analysis.
"""
                }
            ]
        )

        output = response["message"]["content"]
        evaluation = evaluate_response(output)
        risk = classify_risk(output)

        log_analysis(user_input, output, risk)

        st.success("Analysis Result")
        st.write(output)

        st.subheader("Risk Level")
        st.write(risk)

        st.subheader("🔍 Explainability")
        st.write("Risk Score:", explanation["risk_score"])

        for reason in explanation["reasons"]:
            st.write(f"- {reason}")

        st.info(f"Response Quality: {evaluation['quality']}")


# -----------------------------
# 📊 DAY 8 ADVANCED DASHBOARD
# -----------------------------

with st.container():

    st.subheader("📊 Fraud Monitoring Dashboard")

    try:
        data = []

        with open("logs/analysis_log.txt", "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    data.append(parts)

        df = pd.DataFrame(data, columns=["time", "risk", "query"])

        # ✅ STEP 1: Convert time
        df["time"] = pd.to_datetime(df["time"])

        if not df.empty:

            # 📊 Risk Distribution
            st.write("### 📊 Risk Distribution")
            st.bar_chart(df["risk"].value_counts())

            # 📈 Time Series
            st.write("### 📈 Transactions Over Time")
            time_series = df.groupby(df["time"].dt.hour).size()
            st.line_chart(time_series)

            # 🎯 Risk Metrics
            st.write("### 🎯 Risk Breakdown")

            risk_counts = df["risk"].value_counts()

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("🔴 High Risk", risk_counts.get("🔴 HIGH RISK", 0))

            with col2:
                st.metric("🟠 Medium Risk", risk_counts.get("🟠 MEDIUM RISK", 0))

            with col3:
                st.metric("🟢 Low Risk", risk_counts.get("🟢 LOW RISK", 0))

            # 🚨 High Risk Table
            st.write("### 🚨 High Risk Alerts")
            high_risk_df = df[df["risk"].str.contains("HIGH")]
            st.dataframe(high_risk_df)

    except:
        st.warning("No data available yet.")