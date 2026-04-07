print("MAIN STARTED")

from services.llm_service import generate_response
from services.guardrail_service import process_prompt
from backend.risk_service.analyzer import analyze_transaction
from services.explanation_service import explain
from src.observability.logger import log_event


def run_pipeline(user_input):
    # Step 1: Guardrails
    cleaned_prompt, error = process_prompt(user_input)

    if error:
        return error, None, None

    # ✅ Step 2: Analyze ORIGINAL INPUT (FIXED)
    risk_result = analyze_transaction(user_input)
    risk = risk_result["risk_level"]
    risk_score = risk_result["risk_score"]

    # Step 3: LLM Response
    response = generate_response(cleaned_prompt)

    # Step 4: Explanation
    explanation = explain(cleaned_prompt, response)

    # Logging
    log_event(user_input, risk, response)

    return response, risk, explanation, risk_score