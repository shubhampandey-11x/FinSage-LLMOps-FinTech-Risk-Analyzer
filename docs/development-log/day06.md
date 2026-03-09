## Day 6 — Guardrails & Response Evaluation

### Objective

Introduce safety and governance mechanisms in the FinSage AI pipeline to prevent unsafe prompts and evaluate the quality of LLM responses.

### Work Completed

1. **Prompt Guardrails Implementation**

   * Created a new module `guardrails/guardrails.py`.
   * Implemented prompt validation to detect unsafe or malicious financial queries.
   * Added keyword-based filtering for sensitive topics such as fraud, hacking, or bypassing financial security systems.
   * Added a prompt sanitization function to remove suspicious characters.

2. **Response Evaluation System**

   * Created `guardrails/evaluator.py`.
   * Implemented a basic response scoring mechanism.
   * Evaluates responses based on:

     * Response length
     * Presence of financial context
     * Mention of risk-related terminology.
   * Generates a quality score: **LOW / MEDIUM / HIGH**.

3. **Integration with Streamlit App**

   * Updated `app.py` to integrate guardrails before sending prompts to the LLM.
   * Implemented a validation step that blocks unsafe queries.
   * Added response quality indicator to the UI.

### Impact

* Prevents unsafe or malicious prompts.
* Introduces basic **LLM governance mechanisms**.
* Improves reliability of financial risk analysis outputs.

### Files Added

* `guardrails/guardrails.py`
* `guardrails/evaluator.py`

### Files Modified

* `app.py`

### System Architecture Update

User Input → Guardrails → LLM (Mistral via Ollama) → Response Evaluation → Streamlit Output

### Notes

This step introduces foundational **LLM**
