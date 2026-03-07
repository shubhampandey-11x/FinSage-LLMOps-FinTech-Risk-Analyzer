# Day 04 – RAG Risk Analysis Engine

## Objective
Integrate the vector database with a Large Language Model to enable contextual financial risk analysis.

## Work Completed
- Built `risk_analyzer.py` module
- Integrated FAISS vector database retriever
- Implemented Retrieval-Augmented Generation (RAG) pipeline
- Connected local LLM using Ollama (Llama3)
- Constructed contextual prompts using retrieved financial documents
- Tested end-to-end pipeline using `test_risk_analyzer.py`

## Architecture

User Query  
↓  
Retriever (FAISS Vector DB)  
↓  
Relevant Financial Context  
↓  
Prompt Construction  
↓  
Ollama LLM (Llama3)  
↓  
AI Generated Financial Risk Analysis

## Key Learning
Understanding how RAG systems combine vector search with LLM reasoning to generate domain-aware responses.

## Outcome
The system can now analyze financial risks using retrieved contextual knowledge from stored financial documents.
