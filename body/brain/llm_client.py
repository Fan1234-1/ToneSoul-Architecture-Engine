from __future__ import annotations

import os
from typing import Any, List

import requests


class LLMClient:
    """
    Lightweight Ollama client with fail-fast timeouts.
    Designed to degrade safely when Ollama is unavailable.
    """

    def __init__(self, base_url: str | None = None, timeout: float | None = None):
        env_url = os.getenv("OLLAMA_HOST")
        self.base_url = (base_url or env_url or "http://localhost:11434").rstrip("/")
        self.timeout = float(timeout or os.getenv("OLLAMA_TIMEOUT_SEC", "2.0"))
        self.available_models: List[str] = []
        self.online = False
        self._refresh_models()

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)
        return requests.request(method=method, url=url, **kwargs)

    def _refresh_models(self) -> None:
        """Fetch list of available models from Ollama."""
        try:
            response = self._request("GET", "/api/tags")
            if response.status_code == 200:
                data = response.json()
                self.available_models = [model["name"] for model in data.get("models", [])]
                self.online = True
                print(f"[LLMClient] Connected. Available models: {self.available_models}")
                return
            print(f"[LLMClient] Failed to list models. Status: {response.status_code}")
        except requests.RequestException as exc:
            print(f"[LLMClient] Connection failed: {exc}")
        self.available_models = []
        self.online = False

    def generate(self, prompt: str, model: str = "gemma3:4b", system: str | None = None) -> str:
        if not self.online:
            return "Exception: Ollama unavailable"

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system

        try:
            response = self._request("POST", "/api/generate", json=payload)
            if response.status_code == 200:
                return response.json().get("response", "")
            return f"Error: {response.text}"
        except requests.RequestException as exc:
            return f"Exception: {exc}"

    def generate_vision(self, prompt: str, image_path: str, model: str = "llava") -> str:
        if not self.online:
            return "Exception: Ollama unavailable"

        import base64

        if not os.path.exists(image_path):
            return f"Error: Image not found at {image_path}"

        try:
            with open(image_path, "rb") as img_file:
                b64_image = base64.b64encode(img_file.read()).decode("utf-8")
        except OSError as exc:
            return f"Error encoding image: {exc}"

        payload = {
            "model": model,
            "prompt": prompt,
            "images": [b64_image],
            "stream": False,
        }

        try:
            print(f"[LLMClient] Sending image to {model}...")
            response = self._request("POST", "/api/generate", json=payload)
            if response.status_code == 200:
                return response.json().get("response", "")
            return f"Error: {response.text}"
        except requests.RequestException as exc:
            return f"Exception: {exc}"

    def get_embedding(self, text: str, model: str = "nomic-embed-text") -> list:
        if not self.online:
            return []

        payload = {
            "model": model,
            "prompt": text,
        }

        try:
            response = self._request("POST", "/api/embeddings", json=payload)
            if response.status_code == 200:
                embedding = response.json().get("embedding", [])
                if isinstance(embedding, list):
                    return embedding
                return []
            print(f"[LLMClient] Embedding failed: {response.text}")
            return []
        except requests.RequestException as exc:
            print(f"[LLMClient] Embedding exception: {exc}")
            return []


# Singleton instance for easy import
llm_client = LLMClient()
