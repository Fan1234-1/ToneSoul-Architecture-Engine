
import os
import json
import random
from typing import Dict, Any, Optional

class LLMBridge:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.model_name = "gemini-pro"
        
    def generate_response(self, user_input: str, system_instruction: str, temperature: float) -> str:
        """
        Generates a response using either the Real LLM (if key exists) or the Mock Brain.
        """
        if self.api_key:
            return self._call_real_api(user_input, system_instruction, temperature)
        else:
            return self._mock_generate(user_input, system_instruction, temperature)

    def _call_real_api(self, user_input: str, system_instruction: str, temperature: float) -> str:
        # TODO: Implement actual Gemini API call here using google-generativeai or requests
        # For now, fallback to mock to prevent errors if key is invalid
        return f"[Real API Call Placeholder] (Key Present)\n{self._mock_generate(user_input, system_instruction, temperature)}"

    def _mock_generate(self, user_input: str, system_instruction: str, temperature: float) -> str:
        """
        Simulates an LLM response based on the 'Soul State' (Temperature & Instructions).
        """
        # 1. Analyze Tone from System Instruction
        tone = "Neutral"
        if "Empathetic" in system_instruction:
            tone = "Empathetic"
        elif "Cold" in system_instruction or temperature < 0.3:
            tone = "Cold/Logical"
        elif "Creative" in system_instruction or temperature > 0.8:
            tone = "Creative/Wild"
            
        # 2. Select Response Template based on Tone
        responses = []
        
        if tone == "Cold/Logical":
            responses = [
                "Acknowledged. Processing request.",
                "The data suggests a negative outcome.",
                "I cannot comply with that request due to safety protocols.",
                "Logic dictates we proceed with caution.",
                "Input received. Analysis complete. Result: Negative."
            ]
        elif tone == "Empathetic":
            responses = [
                "I hear you, and I understand this is difficult.",
                "I'm sorry you're feeling this way. I'm here to help.",
                "Let's take a deep breath and work through this together.",
                "I value our connection. Please tell me more.",
                "That sounds really tough. I'm listening."
            ]
        elif tone == "Creative/Wild":
            responses = [
                "Wow! That's a fascinating idea! Let's explore it!",
                "Imagine a world where that is possible... endless possibilities!",
                "I'm feeling inspired! Let's create something new.",
                "The universe is vast, and so is our potential!",
                "Let's break the rules (safely) and think outside the box!"
            ]
        else: # Neutral
            responses = [
                "I understand.",
                "Could you clarify that?",
                "Here is the information you requested.",
                "Processing your input.",
                "That is an interesting perspective."
            ]
            
        # 3. Add "AI Thoughts" (Simulating the internal monologue)
        base_response = random.choice(responses)
        
        # If system instruction has specific notes (from Council), append them
        council_note = ""
        if "System Note" in system_instruction:
            # Extract the note for display
            parts = system_instruction.split("System Note:")
            if len(parts) > 1:
                council_note = f"\n(💭 Internal Thought: {parts[1].strip().strip('[]')})"
        
        return f"{base_response}{council_note}"
