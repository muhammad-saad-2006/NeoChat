import requests
import json
from prompts import MEMORY_EXTRACTION_PROMPT

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def stream_chat(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": True
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        stream=True,
        timeout=300
    )

    reply = ""

    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            chunk = data.get("response", "")
            reply += chunk
            yield chunk

            if data.get("done"):
                break

    return reply

def extract_memory(message):
    try:
        prompt = MEMORY_EXTRACTION_PROMPT.format(message=message)

        payload = {
            "model" : MODEL,
            "prompt" : prompt,
            "stream" : False
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )

        result = response.json().get("response", "{}")
        return json.loads(result)

    except Exception as e:
        print(f"[Memory extractor offline: {e}]")
        return {}
