import requests
from typing import Dict

OLLAMA_HOST = "http://localhost:11434"  # 預設

def generate(model: str, prompt: str) -> str:
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    try:
        resp = requests.post(url, json=payload, timeout=600)
        resp.raise_for_status()
        data = resp.json()
        return data["response"]
    except requests.exceptions.RequestException as e:
        return f"Error calling Ollama: {e}"
