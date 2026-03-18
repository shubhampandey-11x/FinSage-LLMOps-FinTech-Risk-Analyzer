from services.llm_service import generate_response
from services.guardrail_service import process_prompt
from services.evaluation_service import evaluate
from services.explanation_service import explain
from src.observability.logger import log_event


def run_pipeline(user_input):
    cleaned_prompt, error = process_prompt(user_input)

    if error:
        return error, None, None

    response = generate_response(cleaned_prompt)
    risk = evaluate(response)
    explanation = explain(cleaned_prompt, response)

    log_event(user_input, risk, response)

    return response, risk, explanation