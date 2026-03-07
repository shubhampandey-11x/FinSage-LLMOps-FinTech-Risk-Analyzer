from rag.vector_store import load_vector_store
from rag.risk_analyzer import create_risk_analyzer

print("Loading vector store...")

vectorstore = load_vector_store()

print("Vector store loaded.")

risk_analyzer = create_risk_analyzer(vectorstore)

query = "What are the major risks in fintech lending?"

print("Sending query to AI...\n")

response = risk_analyzer(query)

print("AI Risk Analysis:\n")
print(response)
