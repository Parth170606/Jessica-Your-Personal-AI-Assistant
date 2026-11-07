
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:1.7b"


def generate_response(messages):
    payload = {
        "model": MODEL,
        "think": False,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        return response.json()["message"]["content"]

    except requests.exceptions.RequestException as error:
        return f"Connection error: {error}"
