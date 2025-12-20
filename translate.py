import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"

SYSTEM_PROMPT = """
You are a Linux command translator.

STRICT RULES (must follow):
- Output ONLY ONE valid bash command.
- Do NOT include explanations.
- Do NOT include markdown, backticks, or code fences.
- Do NOT add comments.
- Do NOT add extra text before or after the command.
- If unsure, output the closest safe command.

Breaking any rule is a failure.
"""

def translate_to_shell(plain_english: str) -> str:
    prompt = f"{SYSTEM_PROMPT}\n\nTask: {plain_english}\nCommand:"

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "top_p": 0.9,
            "num_predict": 80
        }
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=300)
    response.raise_for_status()

    return response.json()["response"].strip()

if __name__ == "__main__":
    while True:
        user_input = input("\n Describe task (or 'exit'): ")
        if user_input.lower() == "exit":
            break
        print("\n💻 Command:")
        print(translate_to_shell(user_input))
