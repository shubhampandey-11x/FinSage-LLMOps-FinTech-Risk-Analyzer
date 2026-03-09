from guardrails.guardrails import validate_prompt, clean_prompt
from guardrails.evaluator import evaluate_response
import streamlit as st
import ollama

st.title("FinSage AI - Financial Risk Assistant")

st.write("Enter a financial transaction to analyze.")

user_input = st.text_area("Transaction or Query:")

if st.button("Analyze"):

    valid, message = validate_prompt(user_input)

    if not valid:
        st.error(message)

    else:
        cleaned_prompt = clean_prompt(user_input)

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
                        "content": cleaned_prompt
                    }
                ]
            )

            output = response["message"]["content"]

            evaluation = evaluate_response(output)

            st.success("Analysis Result")

            st.write(output)

            st.info(f"Response Quality: {evaluation['quality']}")