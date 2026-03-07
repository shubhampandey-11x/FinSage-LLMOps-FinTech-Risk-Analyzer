# Day 04 – RAG Risk Analysis Engine

## Objective
Integrate the FAISS vector database with a Large Language Model to enable contextual financial risk analysis.

## Work Completed
- Implemented `risk_analyzer.py`
- Connected FAISS vector retriever with the LLM
- Integrated local LLM using Ollama (Llama3)
- Built Retrieval Augmented Generation (RAG) pipeline
- Implemented prompt-based financial risk analysis
- Tested system using `test_risk_analyzer.py`

## Architecture

User Query  
↓  
Retriever (FAISS Vector Database)  
↓  
Relevant Context Retrieval  
↓  
Prompt Construction  
↓  
Ollama LLM (Llama3)  
↓  
AI Generated Financial Risk Analysis

## Key Learning
Learned how Retrieval Augmented Generation systems combine vector search with LLM reasoning to produce domain-aware responses.

## Outcome
The system can now analyze fintech risks using contextual knowledge retrieved from financial documents.
