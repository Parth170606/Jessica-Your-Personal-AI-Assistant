import json
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:1.7b"

LAST_METRICS = {}


def get_last_metrics():
    return LAST_METRICS.copy()


def stream_response(messages):

    global LAST_METRICS

    LAST_METRICS = {}

    payload = {
        "model": MODEL,
        "think": False,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": 0.7
        }
    }

    with requests.post(
        OLLAMA_URL,
        json=payload,
        stream=True,
        timeout=(10, 120)
    ) as response:

        response.raise_for_status()

        for line in response.iter_lines():

            if not line:
                continue

            chunk = json.loads(line)

            content = chunk.get("message", {}).get("content", "")

            if content:
                yield content

            if chunk.get("done"):

                LAST_METRICS = {
                    "prompt_tokens": chunk.get("prompt_eval_count", 0),
                    "generated_tokens": chunk.get("eval_count", 0),
                    "prompt_seconds": (
                        chunk.get("prompt_eval_duration", 0) / 1_000_000_000
                    ),
                    "generation_seconds": (
                        chunk.get("eval_duration", 0) / 1_000_000_000
                    ),
                    "total_seconds": (
                        chunk.get("total_duration", 0) / 1_000_000_000
                    )
                }

                generated_tokens = LAST_METRICS["generated_tokens"]
                generation_seconds = LAST_METRICS["generation_seconds"]

                LAST_METRICS["tokens_per_second"] = (
                    generated_tokens / generation_seconds
                    if generation_seconds > 0 else 0
                )

                break


def generate_response(messages):

    try:
        return "".join(stream_response(messages))

    except (
        requests.exceptions.RequestException,
        json.JSONDecodeError,
        KeyError
    ) as error:
        return f"Connection error: {error}"
