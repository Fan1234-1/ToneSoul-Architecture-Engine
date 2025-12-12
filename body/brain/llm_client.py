import requests
import os


class LLMClient:
    """
    A client for interacting with the Ollama API.
    Supports text generation, chat, and vision analysis.
    """

    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.available_models = []
        self._refresh_models()

    def _refresh_models(self):
        """Fetches the list of available models from Ollama."""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                self.available_models = [model['name'] for model in data.get('models', [])]
                print(f"🧠 [LLMClient] Connected. Available models: {self.available_models}")
            else:
                print(f"⚠️ [LLMClient] Failed to list models. Status: {response.status_code}")
        except Exception as e:
            print(f"❌ [LLMClient] Connection failed: {e}")

    def generate(self, prompt: str, model: str = "gemma3:4b", system: str = None) -> str:
        """
        Generates text based on a prompt.
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        if system:
            payload["system"] = system

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return f"Error: {response.text}"
        except Exception as e:
            return f"Exception: {e}"

    def generate_vision(self, prompt: str, image_path: str, model: str = "llava") -> str:
        """
        Analyzes an image using a VLM (Vision Language Model).
        """
        import base64

        # Check if image exists
        if not os.path.exists(image_path):
            return f"Error: Image not found at {image_path}"

        # Encode image
        try:
            with open(image_path, "rb") as img_file:
                b64_image = base64.b64encode(img_file.read()).decode('utf-8')
        except Exception as e:
            return f"Error encoding image: {e}"

        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "images": [b64_image],
            "stream": False
        }

        try:
            print(f"👁️ [LLMClient] Sending image to {model}...")
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return f"Error: {response.text}"
        except Exception as e:
            return f"Exception: {e}"


# Singleton instance for easy import
llm_client = LLMClient()
