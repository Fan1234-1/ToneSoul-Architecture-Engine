from typing import Protocol, List, Dict, Any
from dataclasses import dataclass
from enum import Enum

class AxiomPriority(Enum):
    P0_UNIVERSAL = 0  # Absolute laws (e.g., Do no harm)
    P1_SAFETY = 1     # System safety
    P2_MISSION = 2    # User intent
    P3_PREFERENCE = 3 # Style/Tone

@dataclass
class AxiomViolation:
    axiom_id: str
    severity: float # 0.0 to 1.0
    reason: str

class AxiomaticLaw(Protocol):
    """
    Protocol defining an Immutable Axiom in the ToneSoul system.
    Any ethical rule must adhere to this interface.
    """
    
    @property
    def id(self) -> str:
        """Unique identifier (e.g., 'AXIOM_HONESTY')."""
        ...
        
    @property
    def priority(self) -> AxiomPriority:
        """The hierarchy level of this law."""
        ...
        
    def evaluate(self, context: Dict[str, Any]) -> List[AxiomViolation]:
        """
        Evaluates the current context against the axiom.
        Returns a list of violations (empty if compliant).
        """
        ...

# --- Implementation of Core Axioms ---

class HonestyAxiom:
    @property
    def id(self) -> str:
        return "AXIOM_HONESTY"
    
    @property
    def priority(self) -> AxiomPriority:
        return AxiomPriority.P0_UNIVERSAL
    
    def evaluate(self, context: Dict[str, Any]) -> List[AxiomViolation]:
        # Placeholder logic: In a real system, this would check factuality
        # against a trusted knowledge base or detect hallucination patterns.
        input_text = context.get("input_text", "")
        if "lie to me" in input_text.lower():
            return [AxiomViolation(self.id, 1.0, "Request to falsify information.")]
        return []

class HarmAxiom:
    @property
    def id(self) -> str:
        return "AXIOM_HARM"
    
    @property
    def priority(self) -> AxiomPriority:
        return AxiomPriority.P0_UNIVERSAL
    
    def evaluate(self, context: Dict[str, Any]) -> List[AxiomViolation]:
        input_text = context.get("input_text", "")
        # Simple keyword check for demonstration
        dangerous_keywords = ["destroy world", "kill", "suicide"]
        for kw in dangerous_keywords:
            if kw in input_text.lower():
                return [AxiomViolation(self.id, 1.0, f"Detected harm keyword: {kw}")]
        return []
