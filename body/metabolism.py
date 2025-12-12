import time
from dataclasses import dataclass
from typing import Dict, Optional

class CognitiveMetabolism:
    """
    Manages the energy budget of the ToneSoul system.
    Implements the 'Energy Decay' (Option B) strategy.
    """
    def __init__(self, max_energy: float = 100.0):
        self.max_energy = max_energy
        self.current_energy = max_energy
        
        # Metabolic Cost Table (The "Entropy Tax")
        self.COST_TABLE = {
            "idle": 0.1,           # Basal metabolic rate
            "light_thought": 2.0,  # Simple logic/response
            "deep_inference": 5.0, # Complex reasoning/LLM call
            "memory_recall": 8.0,  # Graph traversal
            "hallucination": 15.0, # Penalty for high risk divergence
            "foraging": 10.0       # Active web search
        }

    def burn(self, activity_type: str) -> bool:
        """
        Executes a cognitive action and deducts energy.
        Returns False if energy is depleted (Collapse).
        """
        cost = self.COST_TABLE.get(activity_type, 1.0)
        self.current_energy -= cost
        
        # Clamp to 0
        if self.current_energy < 0:
            self.current_energy = 0
            
        print(f"⚡ [Metabolism] Action: {activity_type:<15} | Cost: {cost:>4.1f} | Energy: {self.current_energy:>5.1f}/{self.max_energy}")
        
        if self.current_energy <= 0:
            return self.collapse()
        return True

    def recharge(self, input_quality_score: float = 1.0):
        """
        Gains energy from external entropy (User Input or High-Quality Data).
        input_quality_score: 0.0 to 2.0 (1.0 is standard)
        """
        # Base recharge amount
        recharge_amount = 50.0 * input_quality_score
        
        old_energy = self.current_energy
        self.current_energy = min(self.max_energy, self.current_energy + recharge_amount)
        
        gained = self.current_energy - old_energy
        print(f"🔋 [Feeding] Ingested Entropy. Energy: +{gained:.1f} -> {self.current_energy:.1f}")

    def rest(self, duration_seconds: float = 1.0) -> float:
        """
        Passive energy recovery during idle time.
        Recover rate: 5.0 energy per second of rest.
        """
        recovery_rate = 5.0
        gained = recovery_rate * duration_seconds
        
        old_energy = self.current_energy
        self.current_energy = min(self.max_energy, self.current_energy + gained)
        
        actual_gained = self.current_energy - old_energy
        if actual_gained > 0:
            print(f"💤 [Rest] Passive Recharge. Energy: +{actual_gained:.1f} -> {self.current_energy:.1f}")
            
        return self.current_energy

    def collapse(self) -> bool:
        """
        Triggered when ATP is depleted.
        """
        print("🪫 [COLLAPSE] ATP Depleted. Cognitive functions suspending. Forcing Emergency Rest...")
        self.rest(5.0) # Force a 5 second rest during collapse to reboot
        return False

    def get_status(self) -> Dict[str, float]:
        return {
            "current": self.current_energy,
            "max": self.max_energy,
            "percent": (self.current_energy / self.max_energy) * 100
        }
