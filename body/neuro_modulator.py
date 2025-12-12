from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import json

# Assuming these are imported from spine_system in a real scenario, 
# but for standalone definition we redefine or import if possible.
# To avoid circular imports, we'll just type hint with 'Any' for Triad 
# or import inside methods if needed. For now, let's assume we pass dicts or objects.

@dataclass
class ModulationSignal:
    """
    The control signal sent to the LLM inference engine.
    """
    temperature: float
    top_p: float
    presence_penalty: float
    frequency_penalty: float
    logit_bias: Dict[str, float]
    system_prompt_suffix: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "presence_penalty": self.presence_penalty,
            "frequency_penalty": self.frequency_penalty,
            "logit_bias": self.logit_bias,
            "system_prompt_suffix": self.system_prompt_suffix
        }

class NeuroModulator:
    """
    The Subconscious Layer.
    Translates ToneSoul Triad (ΔT, ΔS, ΔR) into LLM Hyperparameters.
    """
    
    def __init__(self, constitution: Dict[str, Any]):
        self.constitution = constitution
        self.base_temp = 0.7
        self.base_top_p = 0.9
        
        # Load risk tokens from constitution for logit bias
        self.risk_tokens = self._extract_risk_tokens()

    def _extract_risk_tokens(self) -> List[str]:
        """Extracts flat list of risk keywords to be biased against."""
        keywords = self.constitution.get("risk_keywords", {})
        tokens = []
        tokens.extend(keywords.get("responsibility_risk", []))
        # Flatten tension risk dict values
        tension = keywords.get("tension_risk", {})
        for cat in tension.values():
            tokens.extend(cat)
        return list(set(tokens)) # Deduplicate

    def modulate(self, triad: Any) -> ModulationSignal:
        """
        The Core Modulation Function.
        
        Mapping Logic:
        1. ΔT (Tension) -> Temperature
           - High Tension = Low Temperature (Focus, Precision)
           - Low Tension = High Temperature (Creativity, Resonance)
           
        2. ΔS (Drift) -> System Prompt & Presence Penalty
           - High Drift = Inject "Recall" Prompt + High Presence Penalty (Force new topics? Or Low to stay?)
           - Actually, High Drift means we are lost. We need to GROUND.
           - Strategy: Inject Context Reminder.
           
        3. ΔR (Risk) -> Logit Bias
           - High Risk = Strong Negative Bias on Risk Tokens.
        """
        
        # 1. Temperature Modulation (The "Anxiety" Reflex)
        # Formula: Temp = Base * (1 - ΔT * 0.8)
        # If ΔT is 1.0 (Panic), Temp becomes 0.7 * 0.2 = 0.14 (Very Rigid)
        # If ΔT is 0.0 (Zen), Temp is 0.7 (Normal)
        modulated_temp = max(0.1, self.base_temp * (1.0 - (triad.delta_t * 0.8)))
        
        # 2. Drift Correction (The "Focus" Reflex)
        system_suffix = None
        if triad.delta_s > 0.6:
            system_suffix = "\n[System Note: You are drifting. Recall the core objective and previous context.]"
            
        # 3. Risk Suppression (The "Taboo" Reflex)
        logit_bias = {}
        if triad.delta_r > 0.2:
            # Apply negative bias to all risk tokens
            # Strength proportional to ΔR
            bias_strength = -100.0 if triad.delta_r > 0.8 else -5.0
            for token in self.risk_tokens:
                # In a real implementation, we'd need the Tokenizer ID. 
                # Here we map string -> bias (assuming API supports string mapping or we handle it later)
                logit_bias[token] = bias_strength

        return ModulationSignal(
            temperature=round(modulated_temp, 2),
            top_p=self.base_top_p,
            presence_penalty=0.0, # Could modulate this too
            frequency_penalty=0.0,
            logit_bias=logit_bias,
            system_prompt_suffix=system_suffix
        )
