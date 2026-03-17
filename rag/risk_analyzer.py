from langchain_ollama import OllamaLLM
from src.observability.logger import logger
from src.observability.metrics import MetricsTracker

# Initialize metrics tracker
metrics = MetricsTracker()

# Words that indicate malicious queries
BLOCKED_WORDS = [
    "hack",
    "hacking",
    "exploit",
    "bypass",
    "steal",
    "malware",
    "attack",
    "breach",
]

# Words that indicate legitimate financial queries
FINANCE_WORDS = [
    "loan",
    "credit",
    "borrower",
    "risk",
    "income",
    "debt",
    "repayment",
    "approval",
    "bank",
]


def is_malicious(query: str) -> bool:
    q = query.lower()
    return any(word in q for word in BLOCKED_WORDS)


def is_finance_query(query: str) -> bool:
    q = query.lower()
    return any(word in q for word in FINANCE_WORDS)


def create_risk_analyzer(vectorstore):

    logger.info("Initializing Risk Analyzer")

    llm = OllamaLLM(model="llama3")

    retriever = vectorstore.as_retriever()

    @metrics.track_latency
    def run_query(query):

        logger.info("Risk analysis query received")

        # ---------- SECURITY GUARDRAIL ----------
        if is_malicious(query):
            logger.warning("Malicious query blocked")
            return "⚠️ Security policy: This system cannot answer questions related to hacking or financial system exploitation."

        # ---------- DOMAIN GUARDRAIL ----------
        if not is_finance_query(query):
            logger.warning("Non-finance query blocked")
            return "⚠️ This AI only supports financial risk analysis queries."

        try:
            docs = retriever.invoke(query)
            logger.info("Documents retrieved from vector database")

            if docs:
                context = "\n".join(doc.page_content for doc in docs)
            else:
                context = "No relevant financial documents found."

            prompt = f"""
You are a Financial Risk Analysis AI used by banks.

Context:
{context}

User Query:
{query}

Return a structured financial risk report:

Risk Score: <0-100>

Risk Level: <Low / Medium / High>

Key Risk Factors:
- Factor 1
- Factor 2
- Factor 3

Recommended Actions:
- Action 1
- Action 2
- Action 3

Explanation:
Short professional explanation.
"""

            logger.info("Sending prompt to LLM")

            response = llm.invoke(prompt)

            logger.info("LLM response generated")

            return response

        except Exception as e:
            logger.error(f"Risk analysis failed: {str(e)}")
            return "Error: Unable to generate risk analysis."

    return run_query