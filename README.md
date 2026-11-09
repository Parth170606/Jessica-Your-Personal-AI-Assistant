# Jessica — Your Personal AI Assistant

<p align="center">
  <strong>A personal AI assistant designed to understand, remember, and assist you.</strong>
  <br/>
  Built with Python and powered by locally running LLMs.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/LLM-Qwen3--1.7B-purple" alt="Qwen3"/>
  <img src="https://img.shields.io/badge/Runtime-Ollama-black?logo=ollama" alt="Ollama"/>
  <img src="https://img.shields.io/badge/Status-Under%20Development-orange" alt="Development"/>
</p>

---

## About Jessica

Jessica is a personal AI assistant project focused on creating a more personalized and context-aware AI experience.

Unlike a basic chatbot that starts every conversation from scratch, Jessica is being developed with a persistent memory system that allows her to remember personal information, retrieve stored facts, and update outdated information across conversations.

The goal is to gradually evolve Jessica into an intelligent personal assistant that understands your preferences, remembers important details, and becomes more useful over time.

## Current Features

- **AI Conversations:** Interact with Jessica through a conversational command-line interface.
- **Persistent Personal Memory:** Store personal facts and preferences in local JSON storage.
- **Memory Retrieval:** Ask Jessica what she remembers about you.
- **Memory Updates:** Replace outdated information when personal facts change.
- **Memory Consolidation:** Avoid retaining multiple conflicting versions of the same personal fact.
- **Memory Deletion:** Remove specific stored personal information.
- **Conversation History:** Maintain conversation context between interactions.
- **Local LLM Integration:** Generate responses using Qwen3 through Ollama.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Qwen3 1.7B | Language model |
| Ollama | Local LLM execution |
| Requests | Communication with Ollama API |
| JSON | Persistent memory and conversation storage |
| Git & GitHub | Version control |

## Project Architecture

```text
Personal-AI-Assistant/
│
├── app/
│   └── main.py
│
├── core/
│   ├── assistant.py
│   └── memory.py
│
├── services/
│   └── llm_service.py
│
├── data/
│   ├── personal_memory.json
│   └── conversation_history.json
│
├── .env
├── .gitignore
└── requirements.txt
```

### Folder Responsibilities

| Directory / File | Responsibility |
|---|---|
| `app/main.py` | Application entry point and command-line interface |
| `core/assistant.py` | Jessica's conversational logic and memory integration |
| `core/memory.py` | Memory storage, retrieval, updating, and deletion |
| `services/llm_service.py` | Communication with the locally hosted LLM |
| `data/personal_memory.json` | Stores persistent personal memories |
| `data/conversation_history.json` | Stores conversation history |

## Getting Started

### 1. Prerequisites

Make sure you have:

- Python 3.12
- Git
- [Ollama](https://ollama.com/)
- A system capable of running the selected local language model

### 2. Clone the Repository

```bash
git clone https://github.com/Parth170606/jessica-your-personal-assistant.git
```

```bash
cd jessica-your-personal-assistant
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```cmd
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install requests
```

### 5. Download the Language Model

Make sure Ollama is installed and running.

Pull the Qwen3 model:

```bash
ollama pull qwen3:1.7b
```

### 6. Run Jessica

From the project root:

```bash
python -m app.main
```

You should see:

```text
================================
       JESSICA AI
   Your Personal AI Assistant
================================

Jessica is online. Type 'exit' to quit.
Type 'reset' to clear conversation memory.

You:
```

## Memory System

One of Jessica's central components is her persistent personal memory system.

It is designed to support three important operations:

**1. Remember**

```text
You: My favorite programming language is Python.

Jessica: Great to hear that!
```

**2. Retrieve**

```text
You: What do you remember about me?

Jessica: Here's what I remember about you:
1. My favorite programming language is Python.
```

**3. Update**

```text
You: My favorite programming language is Java now.

Jessica: [Updates the existing memory]
```

Jessica stores these memories locally so they remain available after restarting the application.

## Development Roadmap

Jessica is an evolving project. Planned improvements include:

- [x] Initial conversational assistant
- [x] Local LLM integration with Ollama
- [x] Persistent personal memory
- [x] Memory retrieval
- [x] Memory viewing and deletion
- [x] Updating existing memories
- [ ] Improved contextual memory retrieval
- [ ] Intelligent memory categorization
- [ ] Better long-term conversation understanding
- [ ] Voice interaction
- [ ] Desktop interface
- [ ] Tool integration and task automation
- [ ] Personalized assistant workflows

*The roadmap will evolve as development progresses.*

## Privacy

Jessica is being developed with a local-first approach.

- Personal memories are stored in local JSON files.
- The language model runs through Ollama on the local machine.
- The application communicates with the local Ollama API.

**Note:** Local model execution does not automatically guarantee complete privacy. Review the application configuration and any future external integrations before storing sensitive information.

## Contributing

Jessica is currently a personal development project, but suggestions and ideas are welcome.

If you have an idea that could make Jessica more intelligent, useful, or personalized, feel free to open an issue or submit a pull request.

## Developer

**Parth Nikam**

- GitHub: [@Parth170606](https://github.com/Parth170606)

---

<p align="center">
  <strong>Jessica — More than a chatbot. A personal AI that grows with you.</strong>
  <br/>
  <em>Built with curiosity, Python, and a vision for personalized AI.</em>
</p>
