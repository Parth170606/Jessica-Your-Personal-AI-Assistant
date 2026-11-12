
from core.assistant import JessicaAssistant


def main():

    jessica = JessicaAssistant()

    print("\n================================")
    print("       JESSICA AI")
    print("   Your Personal AI Assistant")
    print("================================")

    print("\nJessica is online. Type 'exit' to quit.")
    print("Type 'reset' to clear conversation memory.\n")

    while True:

        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("\nJessica: Goodbye! See you soon.")
            break

        if user_input.lower() == "reset":
            print("\nJessica:", jessica.reset_conversation())
            continue

        print("\nJessica: ", end="", flush=True)

        for chunk in jessica.chat_stream(user_input):
            print(chunk, end="", flush=True)

        if jessica.last_timings:
            print("\n\n--- Performance Diagnostics ---")

            for stage, duration in jessica.last_timings.items():
                if duration is not None:
                    print(f"{stage}: {duration:.2f}s")

        if jessica.last_ollama_metrics:
            print("\n--- Ollama Diagnostics ---")

            for metric, value in jessica.last_ollama_metrics.items():
                if isinstance(value, float):
                    print(f"{metric}: {value:.2f}")
                else:
                    print(f"{metric}: {value}")

        print("\n")


if __name__ == "__main__":
    main()
