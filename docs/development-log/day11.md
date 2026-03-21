#  Day 11 – Development Log

## FinSage LLMOps FinTech Risk Analyzer

---
##  Objective of Day 11

The primary goal for Day 11 was to **transition towards a microservices-based architecture** by building a dedicated **Risk Analysis Service** using FastAPI.

This marks a major architectural upgrade from a monolithic backend to a scalable, production-ready system.

---

##  Key Concepts Implemented

* Microservices Architecture
* FastAPI Backend Development
* API Endpoint Design
* Service Decoupling
* JSON-based Risk Evaluation

---

## 🏗️ What Was Built

### 1. Risk Analysis Microservice

A separate backend service was created to handle all risk-related logic.

📁 Directory:

```
backend/risk_service/
```

### 2. FastAPI Application

A FastAPI app was initialized with:

* Health check endpoint
* Risk analysis endpoint

### 3. API Endpoints

####  Health Check

```
GET /
```

Response:

```json
{
  "message": "Risk Service is running"
}
```

####  Risk Analysis Endpoint

```
POST /analyze-risk
```

Sample Input:

```json
{
  "income": 50000,
  "expenses": 30000,
  "loan_amount": 200000
}
```

Sample Output:

```json
{
  "risk_score": 0.4,
  "risk_level": "Medium"
}
```

---

##  Core Logic Implemented

Basic financial risk calculation based on:

* Income vs Expenses
* Loan burden

### Sample Logic (Simplified)

```python
risk_score = (expenses / income) + (loan_amount / (income * 12))

if risk_score < 0.3:
    risk_level = "Low"
elif risk_score < 0.6:
    risk_level = "Medium"
else:
    risk_level = "High"
```

---

##  Testing

Tested using:

* Browser (for GET endpoint)
* Postman (for POST endpoint)

Common issue faced:

*  `{"detail":"Not Found"}`

  * Cause: Wrong route or server not running
  * Fix: Ensure correct endpoint `/analyze-risk` and server is running on correct port

---

##  How to Run the Service

```bash
cd backend/risk_service
source ../../venv/bin/activate
uvicorn main:app --reload --port 8001
```

Then open:

```
http://127.0.0.1:8001/docs
```

---

##  Git Commit

```bash
git add .
git commit -m "Day 11: FastAPI risk analysis microservice completed"
git push origin main
```

---

##  Key Learnings

* Importance of separating services for scalability
* FastAPI makes API development extremely fast
* Clear API contracts are critical for microservices
* Debugging endpoints is a key backend skill

---

##  Outcome of Day 11

✅ Successfully built a standalone Risk Analysis Microservice
✅ Established foundation for microservices architecture
✅ Ready for integration with main backend (Day 12)

---


**End of Day 11 Log** ✅
