#  Day 12 – API Gateway Integration

##  Overview

On Day 12, we transformed our backend from standalone microservices into a **structured, production-style architecture** by introducing an **API Gateway**.

This allows the frontend to interact with a **single entry point**, while the gateway internally communicates with different services.

---

##  Key Concepts Learned

* Microservices Architecture
* API Gateway Pattern
* Service-to-Service Communication
* Port Management & Debugging

---

##  Final Architecture

```
Client (Frontend / Swagger)
        ↓
API Gateway (Port 8000)
        ↓
Risk Service (Port 8001)
```

---

##  Implementation Steps

### 1️⃣ Risk Service Setup (`backend/risk_service/main.py`)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Risk service running"}

@app.post("/risk-score")
def risk_score(data: dict):
    return {
        "risk_score": 85,
        "status": "HIGH RISK",
        "input": data
    }
```

---

### 2️⃣ API Gateway Setup (`backend/main.py`)

```python
from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API Gateway Running"}

@app.post("/analyze-risk")
def analyze_risk(data: dict):
    try:
        response = requests.post(
            "http://127.0.0.1:8001/risk-score",
            json=data
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}
```

---

## ▶️ Running the Services

### Terminal 1 – Risk Service

```bash
cd backend/risk_service
uvicorn main:app --port 8001 --reload
```

### Terminal 2 – API Gateway

```bash
cd backend
uvicorn main:app --port 8000 --reload
```

---

##  Testing

### Direct Risk Service

```
http://127.0.0.1:8001/docs
```

### API Gateway

```
http://127.0.0.1:8000/docs
```

---

### Sample Request

```json
{
  "amount": 100000,
  "merchant": "crypto",
  "location": "unknown"
}
```

---

### Expected Response

```json
{
  "risk_score": 85,
  "status": "HIGH RISK",
  "input": {
    "amount": 100000,
    "merchant": "crypto",
    "location": "unknown"
  }
}
```

---

##  Common Issues Faced

### 1. Port Already in Use

```bash
lsof -i :8000
kill -9 <PID>
```

### 2. Module Not Found

* Ensure correct folder before running `uvicorn`

### 3. App Not Starting

* Ensure `app = FastAPI()` exists in `main.py`

### 4. Wrong Routing

* Gateway should call `/risk-score`
* Client should call `/analyze-risk`

---

##  Key Takeaways

* API Gateway centralizes all client requests
* Services remain independent and scalable
* Clear separation of concerns improves maintainability

---



## ✅ Day 12 Status

*  Risk Service running
*  API Gateway implemented
*  Gateway to Service communication working
*  Tested via Swagger
*  Code pushed to GitHub

---


