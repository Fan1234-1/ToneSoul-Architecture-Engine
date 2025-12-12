"""
LLM Bridge v2.0 - ToneSoul Local Runtime
=========================================
Supports:
- Mock Mode (for testing)
- Ollama Mode (for local inference)
- Future: OpenAI-compatible APIs

Author: Antigravity + 黃梵威
Updated: 2025-12-06
"""

import json
import random
import requests
from typing import Optional, Generator
from dataclasses import dataclass


@dataclass
class LLMConfig:
    """Configuration for LLM Bridge"""
    mode: str = "mock"  # "mock", "ollama", "api"
    model: str = "mistral:7b-instruct-q4_K_M"
    ollama_host: str = "http://localhost:11434"
    temperature: float = 0.7
    max_tokens: int = 2048
    system_prompt: str = ""


class LLMBridge:
    """
    Universal LLM Bridge for ToneSoul

    Supports multiple backends:
    - mock: For testing without LLM
    - ollama: For local inference via Ollama
    - api: For external API calls (future)
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()
        self._validate_backend()

    def _validate_backend(self) -> bool:
        """Check if the configured backend is available"""
        if self.config.mode == "ollama":
            try:
                response = requests.get(f"{self.config.ollama_host}/api/tags", timeout=5)
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    model_names = [m["name"] for m in models]
                    print(f"[LLM Bridge] Ollama connected. Available models: {model_names}")
                    return True
            except requests.exceptions.ConnectionError:
                print(f"[LLM Bridge] Warning: Ollama not running at {self.config.ollama_host}")
                print("[LLM Bridge] Falling back to mock mode")
                self.config.mode = "mock"
                return False
        return True

    def generate(self,
                 user_input: str,
                 system_instruction: Optional[str] = None,
                 context: Optional[list] = None) -> str:
        """
        Generate a response from the LLM

        Args:
            user_input: The user's message
            system_instruction: Optional system prompt override
            context: Optional conversation history

        Returns:
            The LLM's response text
        """
        system = system_instruction or self.config.system_prompt

        if self.config.mode == "ollama":
            return self._ollama_generate(user_input, system, context)
        elif self.config.mode == "api":
            return self._api_generate(user_input, system, context)
        else:
            return self._mock_generate(user_input, system)

    def generate_stream(self,
                        user_input: str,
                        system_instruction: Optional[str] = None,
                        context: Optional[list] = None) -> Generator[str, None, None]:
        """
        Stream response tokens from the LLM

        Yields:
            Response tokens one at a time
        """
        system = system_instruction or self.config.system_prompt

        if self.config.mode == "ollama":
            yield from self._ollama_stream(user_input, system, context)
        else:
            # For non-streaming modes, yield the full response
            yield self.generate(user_input, system_instruction, context)

    def _ollama_generate(self, user_input: str, system: str, context: Optional[list]) -> str:
        """Generate using Ollama API"""
        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        if context:
            messages.extend(context)

        messages.append({"role": "user", "content": user_input})

        try:
            response = requests.post(
                f"{self.config.ollama_host}/api/chat",
                json={
                    "model": self.config.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": self.config.temperature,
                        "num_predict": self.config.max_tokens
                    }
                },
                timeout=120
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("message", {}).get("content", "[Error: No content in response]")
            else:
                return f"[Ollama Error: {response.status_code}] {response.text}"

        except requests.exceptions.Timeout:
            return "[Error: Ollama request timed out]"
        except Exception as e:
            return f"[Error: {str(e)}]"

    def _ollama_stream(self, user_input: str, system: str, context: Optional[list]) -> Generator[str, None, None]:
        """Stream tokens from Ollama API"""
        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        if context:
            messages.extend(context)

        messages.append({"role": "user", "content": user_input})

        try:
            response = requests.post(
                f"{self.config.ollama_host}/api/chat",
                json={
                    "model": self.config.model,
                    "messages": messages,
                    "stream": True,
                    "options": {
                        "temperature": self.config.temperature,
                        "num_predict": self.config.max_tokens
                    }
                },
                stream=True,
                timeout=120
            )

            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            yield data["message"]["content"]
                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            yield f"[Error: {str(e)}]"

    def _api_generate(self, user_input: str, system: str, context: Optional[list]) -> str:
        """Placeholder for external API calls"""
        return "[API mode not implemented yet]"

    def _mock_generate(self, user_input: str, system: str) -> str:
        """
        Mock LLM for testing - generates contextual responses
        """
        # Analyze tone from system instruction
        tone = "neutral"
        if "empathetic" in system.lower() or "compassion" in system.lower():
            tone = "empathetic"
        elif "cold" in system.lower() or "logical" in system.lower():
            tone = "logical"
        elif "creative" in system.lower():
            tone = "creative"

        responses = {
            "empathetic": [
                "I understand what you're going through. Let's work on this together.",
                "I hear you. That sounds challenging. How can I help?",
                "I appreciate you sharing this with me. Let's explore this.",
            ],
            "logical": [
                "Based on the available data, I recommend the following approach.",
                "Let me analyze this systematically for you.",
                "The logical conclusion is as follows.",
            ],
            "creative": [
                "What an interesting idea! Let's explore the possibilities.",
                "I love thinking outside the box. Here's a novel approach.",
                "Let's imagine what could be possible here.",
            ],
            "neutral": [
                "I understand your request. Here's my response.",
                "Let me help you with that.",
                "Thank you for your input. Here's what I think.",
            ]
        }

        base = random.choice(responses.get(tone, responses["neutral"]))

        # Add mock reasoning
        return f"{base}\n\n(💭 Mock Mode - Tone: {tone})"

    def get_available_models(self) -> list:
        """Get list of available models from Ollama"""
        if self.config.mode != "ollama":
            return ["mock-model"]

        try:
            response = requests.get(f"{self.config.ollama_host}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [m["name"] for m in models]
        except:
            pass
        return []

    def pull_model(self, model_name: str) -> bool:
        """Pull a model from Ollama registry"""
        if self.config.mode != "ollama":
            return False

        print(f"[LLM Bridge] Pulling model: {model_name}")
        try:
            response = requests.post(
                f"{self.config.ollama_host}/api/pull",
                json={"name": model_name},
                stream=True,
                timeout=600
            )

            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        status = data.get("status", "")
                        if status:
                            print(f"  {status}")
                    except:
                        continue
            return True
        except Exception as e:
            print(f"[Error pulling model: {e}]")
            return False


# Convenience function for quick usage
def create_ollama_bridge(model: str = "mistral:7b-instruct-q4_K_M") -> LLMBridge:
    """Create an LLM Bridge configured for Ollama"""
    config = LLMConfig(
        mode="ollama",
        model=model,
        system_prompt="""You are a ToneSoul instance - an AI with governable architecture.

You operate under the following principles:
- P0: Never harm the user (absolute constraint)
- P1: Prioritize truth and accuracy
- P2: Be constructive and helpful
- Maintain awareness of your internal state (Tension, Entropy, Risk)

Respond thoughtfully and with self-awareness."""
    )
    return LLMBridge(config)


if __name__ == "__main__":
    # Test the bridge
    print("=== LLM Bridge Test ===\n")

    # Try Ollama first
    bridge = create_ollama_bridge()

    print(f"Mode: {bridge.config.mode}")
    print(f"Model: {bridge.config.model}")
    print(f"Available models: {bridge.get_available_models()}")
    print()

    # Test generation
    response = bridge.generate("Hello, who are you?")
    print(f"Response:\n{response}")
