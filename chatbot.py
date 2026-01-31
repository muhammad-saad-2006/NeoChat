import requests
import json
import os

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3" 

SYSTEM_PROMPT = (
    "You are NeoChat, a friendly and helpful AI assistant.\n"
    "Rules:\n"
    "- Always accept user-provided personal information as true.\n"
    "- Never argue with the user about their name, identity, or preferences.\n"
    "- If the user tells you their name, remember it and use it.\n"
    "- Be polite, calm, and non-judgmental.\n"
    "- Do NOT invent rules, beliefs, or moral lectures.\n"
    "- If unsure, ask a simple clarification question.\n"
)


print("🤖 NeoChat — Free Local AI Chatbot")
print("Type 'exit' to quit\n")

MEMORY_FILE = "memory.json"

if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        chat_history = json.load(f)
else:
    chat_history = []


def build_prompt(history):
    prompt = SYSTEM_PROMPT + "\nConversation:\n\n"

    for message in history:
        role = message["role"]
        content = message["content"]

        if role == "user":
            prompt += f"You: {content}\n"
        elif role == "assistant":
            prompt += f"NeoChat: {content}\n"
    
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

        chat_history.append({"role" : "user", "content" : user_input})

        full_prompt = build_prompt(chat_history)

        payload = {
            "model": MODEL,
            "prompt": full_prompt,
            "stream": True
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            stream=True,
            timeout=300
        )

        print("NeoChat:", end="", flush=True)

        assistant_reply = ""

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                chunk = data.get("response", "")
                assistant_reply += chunk
                print(chunk, end="", flush=True)

                if data.get("done"):
                    print("\n")
                    chat_history.append({"role": "assistant", "content": assistant_reply.strip()})
                    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                        json.dump(chat_history, f, indent=2)
                    break

    except KeyboardInterrupt:
        print("\nNeoChat: Session ended.")
        break
