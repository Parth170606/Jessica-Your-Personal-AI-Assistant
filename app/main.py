
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

        response = jessica.chat(user_input)

        print("\nJessica:", response, "\n")


if __name__ == "__main__":
    main()
