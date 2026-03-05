# FinSage — LLMOps FinTech Risk Analyzer

FinSage is an AI-powered financial risk analysis system being built using Retrieval-Augmented Generation (RAG) and Large Language Models.

The goal of this project is to explore how modern AI systems can assist in financial risk assessment using semantic search and LLM reasoning.

---

## Tech Stack

Python  
FAISS (Vector Database)  
Sentence Transformers (Embeddings)  
HuggingFace Transformers  
Streamlit  

---

## Current Architecture (Day 3)

User → Query  
↓  
Embedding Model  
↓  
Vector Database (FAISS)  
↓  
Retrieve Financial Risk Knowledge  

LLM reasoning layer will be added in upcoming development stages.

---

## Development Log

### Day 1 — Project Setup

Today I started building FinSage AI, a FinTech risk analysis system using LLMOps.

Tasks completed:
- Set up project environment
- Installed required Python libraries
- Integrated local LLM using Ollama
- Built basic Streamlit interface

Next step: Implement Retrieval Augmented Generation (RAG).

---

### Day 2–3 — Vector Database & Retrieval Pipeline

Implemented semantic search using FAISS vector database and embedding models.

System can now retrieve relevant financial risk documents based on user queries.
