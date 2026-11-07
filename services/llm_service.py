import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:1.7b"


def generate_response(message):
    payload = {
        "model": MODEL,
        "think": False,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Jessica, a friendly, intelligent personal AI assistant. "
                    "Be conversational, helpful, and concise. "
                    "Adapt your responses to the user's preferences."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "stream": False
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
