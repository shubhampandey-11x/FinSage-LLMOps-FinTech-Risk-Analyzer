from sentence_transformers import SentenceTransformer
import faiss
import pickle

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("vector_store/faiss_index.bin")

# Load stored documents
with open("vector_store/documents.pkl", "rb") as f:
    documents = pickle.load(f)


def retrieve_documents(query, k=3):
    
    # Convert query into embedding
    query_vector = model.encode([query])
    
    # Search similar documents
    distances, indices = index.search(query_vector, k)
    
    results = [documents[i] for i in indices[0]]
    
    return results
if __name__ == "__main__":

    query = "What are risks in fintech lending platforms?"

    results = retrieve_documents(query)

    print("\nRetrieved Documents:\n")

    for doc in results:
        print("-", doc)