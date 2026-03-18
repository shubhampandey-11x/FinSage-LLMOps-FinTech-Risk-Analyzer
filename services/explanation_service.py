from backend.explainability import generate_explanation

def explain(prompt, response):
    return generate_explanation(prompt, response)