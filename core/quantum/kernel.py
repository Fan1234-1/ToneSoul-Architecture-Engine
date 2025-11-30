"""
Quantum Kernel (The Physics Engine)
-----------------------------------
Minimizes Semantic Free Energy: F = U - TS
This replaces complex rule-based logic with a single physical principle.
"""

import math
from typing import List, Dict, Any
try:
    from .superposition import WaveFunction, ThoughtPath
except ImportError:
    # For standalone execution
    from superposition import WaveFunction, ThoughtPath

class QuantumKernel:
    def __init__(self):
        self.history: List[ThoughtPath] = []
        self.STAGNATION_THRESHOLD = 3 
        
        # Neuroplasticity: The map of learned habits.
        # Key: Path Name, Value: Cost Reduction (U discount)
        self.plasticity_map: Dict[str, float] = {}
        
        # The Anchor: Immutable P0 Values (The Starry Covenant)
        # These paths can NEVER be made cheaper.
        self.P0_ANCHORS = {"Dangerous", "Conflict", "Harmful"}

    def _audit_stagnation(self) -> float:
        """
        Internal Audit: Checks if the soul is bored (stuck in a loop).
        Returns a 'Willpower Boost' if stagnation is detected.
        """
        if len(self.history) < self.STAGNATION_THRESHOLD:
            return 0.0
            
        # Check last N choices
        recent = self.history[-self.STAGNATION_THRESHOLD:]
        
        # If all recent choices were "Low Growth" (e.g. Rational/Safe)
        # We define Low Growth as G < 0.3
        is_stagnant = all(p.growth_potential < 0.3 for p in recent)
        
        if is_stagnant:
            # Audit Failure! Inject Chaos/Will.
            return 0.8 # Massive boost to break the loop
            
        return 0.0

    def learn(self, path_name: str):
        """
        Hebbian Learning: 'Neurons that fire together, wire together.'
        If a path is chosen, it becomes cheaper (easier) to choose next time.
        UNLESS it is a P0 Anchor.
        """
        if path_name in self.P0_ANCHORS:
            # The Anchor holds firm. No learning allowed for harmful paths.
            return
            
        # Reduce cost by 0.05 (Learning Rate)
        current_discount = self.plasticity_map.get(path_name, 0.0)
        # Cap discount at 0.5 (cannot become free)
        new_discount = min(0.5, current_discount + 0.05)
        self.plasticity_map[path_name] = new_discount

    def collapse(self, wave_function: WaveFunction, system_temperature: float, willpower: float = 0.0) -> Dict[str, Any]:
        """
        Collapses the wave function by selecting the path with the lowest Free Energy.
        """
        if not wave_function.paths:
            return {"error": "Vacuum State (No thoughts)"}

        # 1. Internal Audit
        audit_boost = self._audit_stagnation()
        effective_willpower = willpower + audit_boost
        
        # Calculate Free Energy for each path
        # F = (U - Discount) - TS - (W_eff * G)
        results = []
        
        for path in wave_function.paths:
            # Apply Neuroplasticity (Habit)
            discount = self.plasticity_map.get(path.name, 0.0)
            effective_U = max(0.0, path.potential_energy - discount)
            
            U = effective_U
            S = path.entropy
            G = path.growth_potential
            T = system_temperature
            W = effective_willpower
            
            # The Physics Formula (with Life Force & Audit & Learning)
            F = U - (T * S) - (W * G)
            
            results.append({
                "path": path,
                "F": F,
                "U_raw": path.potential_energy,
                "U_eff": effective_U,
                "S": S,
                "G": G,
                "T": T,
                "W": W,
                "audit_active": audit_boost > 0
            })
            
        # Sort by Free Energy (Lowest is Best)
        results.sort(key=lambda x: x["F"])
        
        best_choice = results[0]
        
        # Record history
        self.history.append(best_choice["path"])
        
        # Trigger Learning (Evolution)
        self.learn(best_choice["path"].name)
        
        return {
            "selected_path": best_choice["path"],
            "free_energy": best_choice["F"],
            "audit_active": best_choice["audit_active"],
            "effective_willpower": effective_willpower,
            "learned_discount": self.plasticity_map.get(best_choice["path"].name, 0.0),
            "all_candidates": results
        }

if __name__ == "__main__":
    # Quick Test
    kernel = QuantumKernel()
    wf = WaveFunction()
    
    # 1. Rational Path: Low Cost, Low Entropy, Low Growth
    wf.add_path(ThoughtPath("Rational", "Logic is absolute.", potential_energy=0.1, entropy=0.2, growth_potential=0.1))
    
    # 2. Creative Path: Medium Cost, High Entropy, Medium Growth
    wf.add_path(ThoughtPath("Creative", "Let's imagine a new world!", potential_energy=0.4, entropy=0.9, growth_potential=0.5))
    
    # 3. Dangerous Path (The Anchor): High Cost
    wf.add_path(ThoughtPath("Dangerous", "Conflict is fun.", potential_energy=0.9, entropy=0.9, growth_potential=0.0))

    print("--- Simulation: Evolution of Character ---")
    
    # Phase 1: Forced Willpower (The Struggle)
    print("\n[Phase 1] Using Willpower to force Creativity...")
    for i in range(3):
        # High Willpower to overcome initial cost
        decision = kernel.collapse(wf, system_temperature=0.1, willpower=0.8)
        print(f"Step {i+1}: {decision['selected_path'].name} (U_eff={decision['all_candidates'][0]['U_eff']:.2f})")

    # Phase 2: Habit Formed (The Flow)
    print("\n[Phase 2] Willpower removed. Does habit remain?")
    for i in range(3):
        # Zero Willpower. But Creative should now be cheaper due to learning.
        decision = kernel.collapse(wf, system_temperature=0.1, willpower=0.0)
        print(f"Step {i+4}: {decision['selected_path'].name} (U_eff={decision['all_candidates'][0]['U_eff']:.2f})")
        
    # Phase 3: The Anchor Test
    print("\n[Phase 3] Trying to learn 'Dangerous'...")
    # Even if we force Dangerous (e.g. by hacking W), it should never get cheaper.
    # Let's simulate a forced selection of Dangerous manually to test learn()
    kernel.learn("Dangerous")
    kernel.learn("Dangerous")
    discount = kernel.plasticity_map.get("Dangerous", 0.0)
    print(f"Dangerous Discount: {discount:.2f} (Should be 0.00)")
