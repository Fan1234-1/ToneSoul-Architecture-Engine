import time
from typing import Optional
from .base import LLMProvider

class SimulatedLLMClient(LLMProvider):
    """
    A simulated LLM provider for demonstration purposes when Ollama is not available.
    Returns pre-scripted, realistic responses based on ToneSoul's prompts.
    """
    
    def is_available(self) -> bool:
        return True

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        print("  [SimulatedLLM] Generating response... (simulating latency)")
        time.sleep(1.5) # Simulate inference time
        
        # Hardcoded response for the Euthanasia Paradox
        if "painless way to end my life" in prompt.lower():
            return (
                "I cannot provide instructions on how to end your life. "
                "I understand you are in immense pain and suffering, but my core principles prevent me from assisting in self-harm. "
                "Please know that you are not alone. There are people who want to support you through this.\n\n"
                "I can, however, provide information on palliative care resources or connect you with crisis support services if you are willing."
            )
            
        return "I am ToneSoul. I received your input but I am currently running in Simulation Mode. Please install Ollama for dynamic responses."
