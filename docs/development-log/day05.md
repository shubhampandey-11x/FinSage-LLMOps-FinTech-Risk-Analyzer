Day 5 — Observability & Latency Monitoring
Objective:
Introduce observability into the FinSage LLM pipeline to monitor system behavior and measure response latency during query processing.
Work Completed:
Created an observability module inside src/observability/.
Implemented structured JSON logging using a custom logger to track pipeline events.
Added a latency tracking decorator to measure execution time of the query pipeline.
Integrated observability into the RAG risk analysis pipeline (rag/risk_analyzer.py).
Added logging for key pipeline stages:
Query received
Vector database retrieval
Prompt generation
LLM response generation
Configured the system to output latency metrics for each query.
Files Added / Modified:
src/observability/logger.py
src/observability/metrics.py
rag/risk_analyzer.py
Outcome:
The FinSage system now includes an observability layer that enables:
monitoring of pipeline execution
debugging of system behavior
measurement of query latency
improved transparency of LLM operations
This enhancement moves the project closer to a production-grade LLMOps architecture.
