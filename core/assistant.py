
import json
from pathlib import Path

from services.llm_service import generate_response


class JessicaAssistant:

    def __init__(self):
        self.system_prompt = {
            "role": "system",
            "content": (
                "You are Jessica, a highly capable personal AI assistant. "
                "You are intelligent, friendly, conversational and helpful. "
                "You communicate naturally and avoid unnecessary explanations. "
                "You remember the context of previous conversations when provided. "
                "You address the user respectfully and adapt to their preferences. "
                "Never pretend to perform actions you cannot actually perform."
            )
        }

        self.memory_dir = Path(__file__).resolve().parent.parent / "data"
        self.memory_file = self.memory_dir / "conversation_history.json"

        self.memory_dir.mkdir(parents=True, exist_ok=True)

        self.messages = [self.system_prompt]

        self.load_memory()

    def load_memory(self):

        if not self.memory_file.exists():
            return

        try:
            with open(self.memory_file, "r", encoding="utf-8") as file:
                history = json.load(file)

            if isinstance(history, list):
                valid_history = [
                    message for message in history
                    if isinstance(message, dict)
                    and message.get("role") in ("user", "assistant")
                    and isinstance(message.get("content"), str)
                ]

                self.messages = [
                    self.system_prompt
                ] + valid_history[-20:]

        except (json.JSONDecodeError, OSError):
            print("Jessica: Unable to load previous conversation history.")

    def save_memory(self):

        history = self.messages[1:]

        try:
            with open(self.memory_file, "w", encoding="utf-8") as file:
                json.dump(history[-20:], file, indent=4, ensure_ascii=False)

        except OSError:
            print("Jessica: Unable to save conversation history.")

    def chat(self, user_message):

        self.messages.append({
            "role": "user",
            "content": user_message
        })

        response = generate_response(self.messages)

        if response.startswith("Connection error:"):
            self.messages.pop()
            return response

        self.messages.append({
            "role": "assistant",
            "content": response
        })

        self.messages = [
            self.system_prompt
        ] + self.messages[1:][-20:]

        self.save_memory()

        return response

    def reset_conversation(self):

        self.messages = [self.system_prompt]
        self.save_memory()

        return "Conversation memory cleared successfully."
