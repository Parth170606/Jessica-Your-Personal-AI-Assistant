
from services.llm_service import generate_response


class JessicaAssistant:

    def __init__(self):
        self.system_prompt = {
            "role": "system",
            "content": (
                "You are Jessica, a highly capable personal AI assistant. "
                "You are intelligent, friendly, conversational and helpful. "
                "You communicate naturally and avoid unnecessary explanations. "
                "You remember the context of the current conversation. "
                "You address the user respectfully and adapt to their preferences. "
                "Never pretend to perform actions you cannot actually perform."
            )
        }

        self.messages = [self.system_prompt]

    def chat(self, user_message):

        self.messages.append({
            "role": "user",
            "content": user_message
        })

        self.messages = [
            self.system_prompt
        ] + self.messages[1:][-20:]

        response = generate_response(self.messages)

        if response.startswith("Connection error:"):
            self.messages.pop()
            return response

        self.messages.append({
            "role": "assistant",
            "content": response
        })

        return response

    def reset_conversation(self):
        self.messages = [self.system_prompt]
        return "Conversation memory cleared."
