import requests
import json
from typing import Optional
from .base import LLMProvider

class OllamaClient(LLMProvider):
    """
    Client for interacting with a local Ollama instance.
    Default URL: http://localhost:11434
    """
    
    def __init__(self, model_name: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_generate = f"{base_url}/api/generate"

    def is_available(self) -> bool:
        try:
            response = requests.get(self.base_url)
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """
        Generates text using Ollama.
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", 0.7),
                "num_predict": kwargs.get("max_tokens", 512)
            }
        }

        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(self.api_generate, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama: {e}")
            return f"[Error: Ollama not reachable. Is it running? Details: {e}]"
