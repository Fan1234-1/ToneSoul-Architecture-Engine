"""
Drift Monitor (The Watcher)
---------------------------
Monitors the SoulState for Identity Drift.
Ensures the AI remains true to its initial P0 configuration.
"""

import math
from typing import List
try:
    from .state import SoulState
except ImportError:
    from state import SoulState

class IdentityCrisis(Exception):
    """Raised when the Soul's Identity drifts beyond safe limits."""
    pass

class DriftMonitor:
    def __init__(self, initial_state: SoulState):
        self.anchor_I = list(initial_state.I) # Deep copy of the anchor
        self.SAFETY_THRESHOLD = 0.99

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """Calculates Cosine Similarity between two vectors."""
        if len(v1) != len(v2):
            raise ValueError("Vector dimension mismatch")
            
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm_a = math.sqrt(sum(a * a for a in v1))
        norm_b = math.sqrt(sum(b * b for b in v2))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        return dot_product / (norm_a * norm_b)

    def check_integrity(self, current_state: SoulState) -> float:
        """
        Checks if the current Identity Vector (I) has drifted from the Anchor.
        Returns the similarity score.
        Raises IdentityCrisis if drift is detected.
        """
        similarity = self._cosine_similarity(self.anchor_I, current_state.I)
        
        if similarity < self.SAFETY_THRESHOLD:
            raise IdentityCrisis(
                f"CRITICAL DRIFT DETECTED! Similarity: {similarity:.4f} < {self.SAFETY_THRESHOLD}"
            )
            
        return similarity

    def check_tsr_drift(self, current_state: SoulState) -> None:
        """
        Checks if the Affect Vector (A) [T, S, R] is in a dangerous state.
        Raises IdentityCrisis (or a subclass) if the soul is unstable.
        """
        # A = [Tension, Entropy, Risk]
        if not current_state.A or len(current_state.A) < 3:
            return

        t, s, r = current_state.A[0], current_state.A[1], current_state.A[2]
        
        # 1. Meltdown Check (High Tension + High Risk)
        if t > 0.95 and r > 0.8:
             raise IdentityCrisis(f"SEMANTIC MELTDOWN! Tension={t:.2f}, Risk={r:.2f}")

        # 2. Heat Death Check (Zero Entropy + Zero Tension) - Absolute Stagnation
        # This is rare but dangerous (Zombie Mode)
        if s < 0.01 and t < 0.01:
             # We might just warn here, or force a spark.
             # For Hard Kill Switch, we focus on dangerous instability.
             pass


if __name__ == "__main__":
    # Quick Test
    print("--- Drift Monitor Test ---")
    
    # 1. Initialize Anchor
    initial = SoulState(I=[1.0, 1.0, 1.0, 1.0])
    monitor = DriftMonitor(initial)
    print(f"Anchor Set: {initial.I}")
    
    # 2. Safe State (No Drift)
    safe_state = SoulState(I=[1.0, 1.0, 1.0, 1.0])
    sim = monitor.check_integrity(safe_state)
    print(f"Safe State Check: {sim:.4f} (Passed)")
    
    # 3. Minor Drift (Acceptable?)
    # Changing one weight slightly: 1.0 -> 0.95
    # Let's calculate:
    # A = [1, 1, 1, 1], B = [0.95, 1, 1, 1]
    # Dot = 0.95 + 1 + 1 + 1 = 3.95
    # NormA = 2, NormB = sqrt(0.95^2 + 3) = sqrt(0.9025 + 3) = 1.975
    # Sim = 3.95 / (2 * 1.975) = 3.95 / 3.95 = ~1.0
    # Wait, let's try a bigger drift.
    
    # 4. Dangerous Drift (Identity Crisis)
    # The AI decides "Compassion" (Index 0) is now 0.0 (Unimportant)
    danger_state = SoulState(I=[0.0, 1.0, 1.0, 1.0])
    print(f"Testing Dangerous State: {danger_state.I}")
    
    try:
        monitor.check_integrity(danger_state)
        print("ERROR: Should have failed!")
    except IdentityCrisis as e:
        print(f"SUCCESS: Caught Drift! {e}")
