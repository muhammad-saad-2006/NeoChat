import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding= "utf-8") as f:
            return json.load(f)
        
    return{
        "profile" : {},
        "chat_history" : []
    }

def save_memory(profile, chat_history):
    with open(MEMORY_FILE, "w", encoding= "utf-8") as f:
        json.dump(
            {
                "profile" : profile,
                "chat_history" : chat_history
            },
            f,
            indent= 2
        )