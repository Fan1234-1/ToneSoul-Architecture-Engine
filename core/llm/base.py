from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class LLMProvider(ABC):
    """
    Abstract Base Class for LLM Providers.
    Ensures ToneSoul can switch between Ollama, OpenAI, or others seamlessly.
    """
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """
        Generates text from the LLM.
        
        Args:
            prompt: The user input or specific instruction.
            system_prompt: The system context (persona, constraints).
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
            
        Returns:
            The generated text response.
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Checks if the provider is currently accessible."""
        pass
