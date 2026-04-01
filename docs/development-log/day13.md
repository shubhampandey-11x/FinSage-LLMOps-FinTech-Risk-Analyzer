## Day 13 — Dockerizing FastAPI Backend

## Objective

Containerize the FastAPI backend of the FinSage LLMOps project using Docker to ensure consistent deployment across environments.

---

## Tasks Completed

* Created `requirements.txt` using:

  ```bash
  python -m pip freeze > requirements.txt
  ```

* Wrote initial `Dockerfile` for FastAPI backend

* Optimized Docker build using:

  * Layer caching (copying `requirements.txt` first)
  * `.dockerignore` to exclude unnecessary files

* Created `.dockerignore` to remove:

  * Virtual environments (`venv_clean/`)
  * Cache files (`__pycache__/`)
  * System files (`.DS_Store`)
  * Git metadata

* Successfully built Docker image:

  ```bash
  docker build -t finsage-app .
  ```

* Ran container:

  ```bash
  docker run -p 8000:8000 finsage-app
  ```

---

## Issues Faced & Fixes

1. **Empty `requirements.txt`**

   * Cause: pip execution issue
   * Fix: Used `python -m pip freeze`

2. **Slow Docker build (400+ seconds)**

   * Cause: Large build context (venv included)
   * Fix: Added `.dockerignore` → reduced build to ~10 seconds

3. **ASGI app import error**

   * Error:

     ```
     Attribute "app" not found in module "main"
     ```
   * Cause: Incorrect module path
   * Fix:

     ```dockerfile
     CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
     ```

---

## Key Learnings

* Docker builds are layer-based and benefit from caching
* `.dockerignore` is critical for performance optimization
* Correct module paths are essential for container runtime
* First build is slow; subsequent builds are faster

---

## Outcome

* FastAPI backend successfully containerized
* Build time optimized from minutes → seconds
* Application accessible at:

  ```
  http://localhost:8000/docs
  ```

---

## Interview Talking Point

> “Containerized a FastAPI backend using Docker, optimized build performance using `.dockerignore`, and resolved runtime ASGI configuration issues.”

---

## Next Step

Proceed to **Day 14 — Docker Compose (multi-container setup)**
