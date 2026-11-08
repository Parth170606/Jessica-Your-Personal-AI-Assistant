
import json
from pathlib import Path


class MemoryManager:

    def __init__(self):
        self.memory_dir = Path(__file__).resolve().parent.parent / "data"
        self.memory_file = self.memory_dir / "personal_memory.json"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.memories = self.load_memories()

    def load_memories(self):
        if not self.memory_file.exists():
            return []

        try:
            with open(self.memory_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):
                return [
                    item.strip() for item in data
                    if isinstance(item, str) and item.strip()
                ]

        except (json.JSONDecodeError, OSError):
            print("Jessica: Unable to load personal memories.")

        return []

    def save_memories(self):
        temp_file = self.memory_file.with_suffix(".tmp")

        try:
            with open(temp_file, "w", encoding="utf-8") as file:
                json.dump(self.memories, file, indent=4, ensure_ascii=False)

            temp_file.replace(self.memory_file)
            return True

        except OSError:
            print("Jessica: Unable to save personal memories.")
            return False

    def add_memory(self, content):
        if not isinstance(content, str):
            return False

        content = " ".join(content.split())

        if not content:
            return False

        normalized = content.casefold()

        if any(memory.casefold() == normalized for memory in self.memories):
            return False

        self.memories.append(content)

        if self.save_memories():
            return True

        self.memories.pop()
        return False

    def update_memory(self, number, content):
        if not isinstance(content, str) or not isinstance(number, int):
            return False

        content = " ".join(content.split())

        if not content or number < 1 or number > len(self.memories):
            return False

        normalized = content.casefold()

        if any(
            index != number - 1 and memory.casefold() == normalized
            for index, memory in enumerate(self.memories)
        ):
            return False

        previous = self.memories[number - 1]
        self.memories[number - 1] = content

        if self.save_memories():
            return True

        self.memories[number - 1] = previous
        return False

    def find_memory(self, keyword):
        if not isinstance(keyword, str) or not keyword.strip():
            return []

        keyword = keyword.casefold()

        return [
            (index, memory)
            for index, memory in enumerate(self.memories, start=1)
            if keyword in memory.casefold()
        ]

    def get_memories(self):
        return self.memories.copy()

    def get_memory_context(self):
        if not self.memories:
            return "No personal memories are currently saved."

        return "\n".join(
            f"{index}. {memory}"
            for index, memory in enumerate(self.memories, start=1)
        )

    def forget_memory(self, number):
        if not isinstance(number, int):
            return False

        if number < 1 or number > len(self.memories):
            return False

        removed = self.memories.pop(number - 1)

        if self.save_memories():
            return removed

        self.memories.insert(number - 1, removed)
        return False

    def clear_memories(self):
        previous_memories = self.memories.copy()
        self.memories = []

        if self.save_memories():
            return True

        self.memories = previous_memories
        return False
