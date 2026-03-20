import requests

MODEL_NAME = "llama3"

def generate_response(prompt):
    url = "http://localhost:11434/api/chat"

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    response = requests.post(url, json=payload)

    return response.json()["message"]["content"]