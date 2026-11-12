
import re
import json
from pathlib import Path


class MemoryManager:

    def __init__(self):
        self.memory_dir = Path(__file__).resolve().parent.parent / "data"
        self.memory_file = self.memory_dir / "personal_memory.json"
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        loaded_memories = self.load_memories()
        self.memories = []
        seen = set()

        for memory in loaded_memories:
            normalized = self.normalize_memory_content(memory)

            if normalized and normalized not in seen:
                seen.add(normalized)
                self.memories.append(memory)

        if len(self.memories) != len(loaded_memories):
            self.save_memories()

    def normalize_memory_content(self, content):
        if not isinstance(content, str):
            return ""

        content = " ".join(content.casefold().split())
        content = content.rstrip(".,!?;:").strip()

        return content

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

        normalized = self.normalize_memory_content(content)

        if any(
            self.normalize_memory_content(memory) == normalized
            for memory in self.memories
        ):
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

        normalized = self.normalize_memory_content(content)

        if any(
            index != number - 1
            and self.normalize_memory_content(memory) == normalized
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

    def categorize_memory(self, content):
        if not isinstance(content, str) or not content.strip():
            return "General"

        text = content.casefold()

        categories = {
            "Education": [
                "student", "study", "studying", "college",
                "university", "school", "semester",
                "engineering", "degree", "exam", "course"
            ],
            "Work": [
                "work", "working", "job", "career",
                "internship", "project", "developing",
                "developer", "building", "profession"
            ],
            "Preferences": [
                "favorite", "favourite", "prefer",
                "preference", "dislike"
            ],
            "Hobbies": [
                "hobby", "hobbies", "guitar", "harmonium",
                "playing", "singing", "reading", "gaming",
                "drawing", "painting", "sports"
            ],
            "Personal": [
                "family", "parents", "brother", "sister",
                "birthday", "born", "age", "live", "living",
                "hometown", "country"
            ]
        }

        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category

        return "General"

    def get_memories_by_category(self, category):
        if not isinstance(category, str) or not category.strip():
            return []

        category = category.strip().casefold()

        return [
            memory
            for memory in self.memories
            if self.categorize_memory(memory).casefold() == category
        ]

    def normalize_text(self, text):
        if not isinstance(text, str):
            return []

        text = text.casefold()

        words = {
            "programming": "coding",
            "programmer": "coding",
            "developer": "coding",
            "develop": "coding",
            "language": "coding",
            "languages": "coding",
            "sport": "sports",
            "game": "sports",
            "games": "sports",
            "enjoy": "like",
            "love": "like",
        }

        ignored_words = {
            "what", "which", "who", "where", "when",
            "is", "are", "am", "the", "a", "an",
            "my", "me", "i", "do", "does", "did",
            "you", "your", "about", "in", "on", "of",
            "to", "for", "and", "or", "remember",
            "tell", "know", "can", "could", "would",
            "please", "currently", "like", "prefer",
        }

        result = []

        for word in text.split():
            word = word.strip(".,!?;:'\"()[]{}")

            if not word or word in ignored_words:
                continue

            word = words.get(word, word)
            result.append(word)

        return result

    def search_relevant_memories(self, query, limit=3):
        if not isinstance(query, str) or not query.strip():
            return []

        if not isinstance(limit, int) or limit < 1:
            return []

        query_words = set(self.normalize_text(query))

        if not query_words:
            return []

        results = []

        for index, memory in enumerate(self.memories, start=1):
            memory_words = set(self.normalize_text(memory))
            matches = query_words.intersection(memory_words)

            if not matches:
                continue

            score = len(matches) / len(query_words)

            results.append({
                "number": index,
                "memory": memory,
                "score": round(score, 3)
            })

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return results[:limit]

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

    def update_existing_memory(self, old_content, new_content):
        if not isinstance(old_content, str) or not isinstance(new_content, str):
            return False

        old_content = old_content.strip()
        new_content = new_content.strip()

        if not old_content or not new_content:
            return False

        index = next(
            (
                i for i, memory in enumerate(self.memories)
                if memory == old_content
            ),
            None
        )

        if index is None:
            return False

        return self.update_memory(index + 1, new_content)

    def update_memory_by_subject(self, subject, new_content):
        if not isinstance(subject, str) or not isinstance(new_content, str):
            return False

        subject = " ".join(subject.casefold().split())
        new_content = " ".join(new_content.split())

        if not subject or not new_content:
            return False

        prefix = f"my {subject} is "

        matching = [
            index for index, memory in enumerate(self.memories)
            if memory.casefold().startswith(prefix)
        ]

        if not matching:
            return False

        previous = self.memories.copy()
        first_index = matching[0]

        updated = []

        for index, memory in enumerate(self.memories):
            if index == first_index:
                updated.append(new_content)
            elif index not in matching:
                updated.append(memory)

        self.memories = updated

        if self.save_memories():
            return True

        self.memories = previous
        return False

    def detect_memory_conflict(self, content):
        if not isinstance(content, str) or not content.strip():
            return None

        pattern = r"^my\s+(.+?)\s+is\s+(.+?)[.!?]*$"

        match = re.match(
            pattern,
            " ".join(content.split()),
            re.IGNORECASE
        )

        if not match:
            return None

        subject = " ".join(match.group(1).casefold().split())
        new_value = match.group(2).strip().rstrip(".!?").casefold()

        for memory in self.memories:
            existing_match = re.match(
                pattern,
                memory.strip(),
                re.IGNORECASE
            )

            if not existing_match:
                continue

            existing_subject = " ".join(
                existing_match.group(1).casefold().split()
            )

            existing_value = (
                existing_match.group(2).strip().rstrip(".!?").casefold()
            )

            if subject == existing_subject and new_value != existing_value:
                return {
                    "subject": subject,
                    "existing_memory": memory,
                    "new_memory": content.strip()
                }

        return None
