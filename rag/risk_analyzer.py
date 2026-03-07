from langchain_ollama import OllamaLLM


def create_risk_analyzer(vectorstore):

    llm = OllamaLLM(model="llama3")

    retriever = vectorstore.as_retriever()

    def run_query(query):
        docs = retriever.invoke(query)

        context = "\n".join([doc.page_content for doc in docs])

        prompt = f"""
You are a financial risk analysis expert.

Context:
{context}

Question:
{query}

Provide a detailed financial risk analysis.
"""

        response = llm.invoke(prompt)

        return response

    return run_query
