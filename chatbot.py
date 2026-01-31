import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi"  

print("🤖 NeoChat — Free Local AI Chatbot")
print("Type 'exit' to quit\n")

while True:
    try:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "q"]:
            print("NeoChat: Goodbye 👋")
            break

        payload = {
            "model": MODEL,
            "prompt": user_input,
            "stream": True
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            stream=True,
            timeout=300
        )

        print("NeoChat:", end=" ", flush=True)

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                chunk = data.get("response", "")
                print(chunk, end="", flush=True)

                if data.get("done"):
                    print("\n")
                    break

    except KeyboardInterrupt:
        print("\nNeoChat: Session ended.")
        break
