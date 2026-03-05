from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

# Sample financial risk documents
documents = [
    "Fintech lending platforms face borrower default risk.",
    "Regulatory changes can impact fintech companies.",
    "Cybersecurity threats are a major risk in digital finance.",
    "Liquidity risk is common in peer-to-peer lending platforms.",
    "Data privacy regulations affect fintech data handling."
]

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert documents to embeddings
embeddings = model.encode(documents)
embeddings = np.array(embeddings)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Create vector_store folder in project root
os.makedirs("vector_store", exist_ok=True)

# Save FAISS index
faiss.write_index(index, "vector_store/faiss_index.bin")

# Save documents
with open("vector_store/documents.pkl", "wb") as f:
    pickle.dump(documents, f)

print("Vector database created successfully!")