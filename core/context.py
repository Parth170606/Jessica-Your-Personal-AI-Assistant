
import json
from pathlib import Path


class ConversationContextManager:

    def __init__(self, file_path):
        self.context_file = Path(file_path)

        self.context_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.context = {
            "current_topic": None,
            "previous_topics": [],
            "entities": []
        }

        self.load_context()

    def load_context(self):
        if not self.context_file.exists():
            self.save_context()
            return

        try:
            with open(
                self.context_file,
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            if not isinstance(data, dict):
                return

            self.context["current_topic"] = (
                data.get("current_topic")
                if isinstance(data.get("current_topic"), str)
                else None
            )

            previous_topics = data.get("previous_topics", [])
            entities = data.get("entities", [])

            self.context["previous_topics"] = [
                topic for topic in previous_topics
                if isinstance(topic, str)
            ][-10:]

            self.context["entities"] = [
                entity for entity in entities
                if isinstance(entity, str)
            ][-20:]

        except (json.JSONDecodeError, OSError):
            print("Jessica: Unable to load conversation context.")

    def save_context(self):
        try:
            temp_file = self.context_file.with_suffix(".tmp")

            with open(
                temp_file,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    self.context,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            temp_file.replace(self.context_file)

        except OSError:
            print("Jessica: Unable to save conversation context.")

    def update_context(self, topic=None, entities=None):

        topic_changed = False

        if isinstance(topic, str) and topic.strip():

            topic = topic.strip()
            current_topic = self.context["current_topic"]

            if (
                current_topic is None
                or current_topic.casefold() != topic.casefold()
            ):

                if current_topic:
                    previous_topics = self.context["previous_topics"]

                    previous_topics = [
                        item for item in previous_topics
                        if item.casefold() != current_topic.casefold()
                    ]

                    previous_topics.append(current_topic)

                    self.context["previous_topics"] = previous_topics[-10:]

                self.context["current_topic"] = topic
                topic_changed = True

        if topic_changed:
            self.context["entities"] = []

        if isinstance(entities, list):

            existing = self.context["entities"]

            for entity in entities:

                if not isinstance(entity, str) or not entity.strip():
                    continue

                entity = entity.strip()

                if not any(
                    item.casefold() == entity.casefold()
                    for item in existing
                ):
                    existing.append(entity)

            self.context["entities"] = existing[-20:]

        self.save_context()

    def get_context(self):
        return self.context.copy()

    def get_context_prompt(self):

        current_topic = self.context["current_topic"]
        previous_topics = self.context["previous_topics"]
        entities = self.context["entities"]

        return (
            f"CURRENT TOPIC:\n{current_topic or 'Not established'}\n\n"
            f"PREVIOUS TOPICS:\n"
            f"{', '.join(previous_topics) if previous_topics else 'None'}\n\n"
            f"CURRENTLY RELEVANT ENTITIES:\n"
            f"{', '.join(entities) if entities else 'None'}"
        )

    def clear_context(self):

        self.context = {
            "current_topic": None,
            "previous_topics": [],
            "entities": []
        }

        self.save_context()

        return "Conversation context cleared."
