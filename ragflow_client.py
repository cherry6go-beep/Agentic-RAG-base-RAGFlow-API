# ragflow_client.py
import os
import requests

RAGFLOW_BASE_URL = os.getenv("RAGFLOW_BASE_URL", "http://localhost:9380")
RAGFLOW_API_KEY = os.getenv("RAGFLOW_API_KEY", "ragflow-zVUGLuOWxAdI9QTDWmkMeUqHzdCVC1WRCcEqOhEpqsA")
RAGFLOW_CHAT_ID = os.getenv("RAGFLOW_CHAT_ID", "c8639a1e51e011f18221f5d90a8ca27c")


def ask_ragflow(question: str) -> str:
    url = f"{RAGFLOW_BASE_URL}/api/v1/openai/{RAGFLOW_CHAT_ID}/chat/completions"

    payload = {
        "model": "qwen3:8b",
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "stream": False
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RAGFLOW_API_KEY}"
    }

    response = requests.post(url, json=payload, headers=headers, timeout=120)
    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"]