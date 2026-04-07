import sys
import os

# Fix import path for main.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import re

from main import run_pipeline   # core pipeline
from memory import ConversationMemory  # memory

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="FinSage Dashboard", layout="wide")

# -----------------------------
# Ensure logs folder exists
# -----------------------------
os.makedirs("logs", exist_ok=True)

# -----------------------------
# Initialize Memory
# -----------------------------
if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory()

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
    risk_text = str(risk_text).upper()

    if "HIGH" in risk_text:
        return "🔴 HIGH RISK"
    elif "MEDIUM" in risk_text:
        return "🟠 MEDIUM RISK"
    else:
        return "🟢 LOW RISK"

# -----------------------------
# Logging
# -----------------------------
def log_analysis(query, risk):
    import datetime
    with open("logs/analysis_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}|{risk}|{query}\n")

# -----------------------------
# UI
# -----------------------------
st.title("FinSage AI - Financial Risk Assistant")
st.caption("Dashboard updates after each analysis")

user_input = st.text_area("Transaction or Query:")

# =============================
# PIPELINE WITH MEMORY
# =============================
if st.button("Analyze"):

    if not user_input.strip():
        st.warning("Please enter a transaction or query.")
        st.stop()

    if is_malicious(user_input):
        st.error("⚠️ Security Policy: Blocked malicious query.")
        st.stop()

    with st.spinner("Analyzing..."):

        # Get memory context
        context = st.session_state.memory.get_context()

        enhanced_input = f"""
        Previous Context:
        {context}

        Current Query:
        {user_input}
        """

        # ✅ UPDATED: receive risk_score also
        response, risk, explanation, risk_score = run_pipeline(enhanced_input)

        normalized_risk = normalize_risk_label(risk)

        # Store memory
        st.session_state.memory.add(user_input, response)

        # Log
        log_analysis(user_input, normalized_risk)

        # -----------------------------
        # CHAT UI
        # -----------------------------
        st.chat_message("user").write(user_input)
        st.chat_message("assistant").write(response)

        # -----------------------------
        # PREMIUM UI OUTPUT (DAY 16)
        # -----------------------------
        st.success("Analysis Result")

        st.markdown("## 📊 Financial Risk Report")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🔍 Risk Level")
            st.write(f"**{normalized_risk}**")

            # ✅ NEW: Risk Score
            st.markdown("### 📊 Risk Score")
            st.write(f"**{risk_score} / 100**")

        with col2:
            st.markdown("### 🤖 AI Response")
            st.write(response)

        # Risk Indicator
        st.divider()

        if "HIGH" in normalized_risk:
            st.error("🔴 HIGH RISK TRANSACTION")
        elif "MEDIUM" in normalized_risk:
            st.warning("🟠 MEDIUM RISK TRANSACTION")
        else:
            st.success("🟢 LOW RISK TRANSACTION")

        # -----------------------------
        # EXPLANATION (FIXED)
        # -----------------------------
        st.divider()

        st.markdown("## 🧠 AI Explanation")

        if isinstance(explanation, dict):
            st.markdown(explanation.get("llm_response", ""))
        else:
            st.markdown(explanation)

        # -----------------------------
        # EXPLAINABILITY (KEY FEATURE)
        # -----------------------------
        st.divider()

        st.markdown("### 🔍 Why this score?")
        st.info(
            "This risk assessment is based on financial indicators such as revenue trends, "
            "debt levels, expenses, and cash flow. The AI evaluates stability, liquidity, "
            "and potential risk signals to generate this score."
        )

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