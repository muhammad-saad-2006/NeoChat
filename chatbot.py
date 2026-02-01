from memory import load_memory, save_memory
from llm import stream_chat, extract_memory
from commands import handle_command
from prompts import SYSTEM_PROMPT

print("🤖 NeoChat — Free Local AI Chatbot")
print("Type 'exit' to quit\n")

memory = load_memory()
profile = memory["profile"]
chat_history = memory["chat_history"]

def build_prompt():
    prompt = SYSTEM_PROMPT + "\nConversation:\n\n"
    for message in chat_history:
        role = message["role"]
        content = message["content"]
        prompt += f"{role.capitalize()} : {content}\n"
    prompt += "Assistant:"
    return prompt

while True:
    try:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "q", "bye"]:
            print("NeoChat: Goodbye 👋")
            break

        if handle_command(user_input.lower(), profile, chat_history):
            save_memory(profile, chat_history)
            continue

        chat_history.append({"role": "user", "content": user_input})
        
        extracted = extract_memory(user_input)
        if extracted:
            profile.update(extracted)
            save_memory(profile, chat_history)

        print("NeoChat: ", end="", flush=True)

        assistant_reply = ""
        for chunk in stream_chat(build_prompt()):
            print(chunk, end="", flush=True)
            assistant_reply += chunk

        print("\n")
        chat_history.append({"role": "assistant", "content": assistant_reply})
        save_memory(profile, chat_history)

    except KeyboardInterrupt:
        print("\nNeoChat: Session ended.")
        break