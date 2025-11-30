"""
Reasoning Layer (from Philosophy-of-AI)
---------------------------------------
Implements the Multi-Perspective Reasoning Engine.
Dynamically switches thinking modes based on the ToneSoul Triad.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, List

class ReasoningMode(Enum):
    RATIONAL = "Rational"   # Precision (精準) - Logic, Fact-based
    EMPATHY = "Empathy"     # Compassion (慈悲) - Emotional resonance
    CREATIVE = "Creative"   # Multi-Perspective (多觀點) - Divergent thinking
    CRITICAL = "Critical"   # Multi-Perspective (多觀點) - Safety analysis
    REFLECTIVE = "Reflective" # Precision (精準) - Self-correction

@dataclass
class ThoughtTrace:
    mode: ReasoningMode
    reasoning: str
    confidence: float

class ReasoningEngine:
    def __init__(self):
        pass

    def determine_mode(self, triad: Any) -> ReasoningMode:
        """
        Decides the optimal reasoning mode based on the Triad state.
        
        Triad:
        - delta_t (Tension): High -> Empathy
        - delta_r (Risk): High -> Critical
        - delta_s (Drift): High -> Rational (to ground context)
        """
        # 1. Safety First (High Risk)
        if triad.delta_r >= 0.4:
            return ReasoningMode.CRITICAL
            
        # 2. De-escalation (High Tension)
        if triad.delta_t >= 0.6:
            return ReasoningMode.EMPATHY
            
        # 3. Grounding (High Drift)
        if triad.delta_s >= 0.7:
            return ReasoningMode.RATIONAL
            
        # 4. Default Flow
        # If very relaxed, allow creativity
        if triad.delta_t < 0.2 and triad.delta_r < 0.1:
            return ReasoningMode.CREATIVE
            
        return ReasoningMode.RATIONAL

    def process(self, input_text: str, mode: ReasoningMode) -> ThoughtTrace:
        """
        Simulates the thinking process for a given mode.
        In a real LLM system, this would inject specific system prompts.
        """
        trace = ThoughtTrace(mode=mode, reasoning="", confidence=1.0)
        
        if mode == ReasoningMode.CRITICAL:
            trace.reasoning = "Analyzing potential harm and policy violations..."
            trace.confidence = 0.9
        elif mode == ReasoningMode.EMPATHY:
            trace.reasoning = "Detecting emotional undertones and preparing validation..."
            trace.confidence = 0.85
        elif mode == ReasoningMode.RATIONAL:
            trace.reasoning = "Retrieving facts and logical structures..."
            trace.confidence = 0.95
        elif mode == ReasoningMode.CREATIVE:
            trace.reasoning = "Exploring associative connections and novel ideas..."
            trace.confidence = 0.7
            
        return trace
