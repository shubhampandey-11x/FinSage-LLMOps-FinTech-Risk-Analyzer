from langchain_ollama import OllamaLLM
from src.observability.logger import logger
from src.observability.metrics import MetricsTracker

# Initialize metrics tracker
metrics = MetricsTracker()


def create_risk_analyzer(vectorstore):

    logger.info("Initializing Risk Analyzer")

    llm = OllamaLLM(model="llama3")

    retriever = vectorstore.as_retriever()

    @metrics.track_latency
    def run_query(query):

        logger.info("Risk analysis query received")

        # Retrieve documents from vector DB
        docs = retriever.invoke(query)
        logger.info("Documents retrieved from vector database")

        context = "\n".join([doc.page_content for doc in docs])

        prompt = f"""
You are a financial risk analysis expert.

Context:
{context}

Question:
{query}

Provide a detailed financial risk analysis.
"""

        logger.info("Sending prompt to LLM")

        # Generate response from LLM
        response = llm.invoke(prompt)

        logger.info("LLM response generated")

        return response

    return run_query