import ollama

# 🔥 keep model "warm"
MODEL_NAME = "llama3"

def generate_response(prompt):
    return ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )['message']['content']