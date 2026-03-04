import streamlit as st
import ollama

st.title("FinSage AI - Financial Risk Assistant")

st.write("Enter a financial transaction to analyze.")

user_input = st.text_area("Transaction or Query:")

if st.button("Analyze"):
    if user_input.strip() == "":
        st.warning("Please enter a query.")
    else:
        with st.spinner("Analyzing..."):
            response = ollama.chat(
                model="mistral",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a financial fraud analyst. Detect suspicious patterns in transactions."
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            )

            st.success("Analysis Result")
            st.write(response["message"]["content"])
