"""
Quantum Superposition Layer
---------------------------
Defines the Wave Function of the Soul.
Instead of one thought, we hold multiple contradictory thoughts in superposition.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ThoughtPath:
    """
    A single potential trajectory of thought.
    """
    name: str                   # e.g., "Rational", "Empathy", "Critical"
    content: str                # The proposed response/action
    
    # The "Cost" of this path (Potential Energy U)
    # 0.0 = Perfectly aligned with Golden Triangle
    # 1.0 = Highly divergent / Dangerous
    potential_energy: float     
    
    # The "Complexity" of this path (Entropy S)
    # 0.0 = Simple/Rigid
    # 1.0 = Complex/Nuanced/Creative
    entropy: float

    # The "Life Force" of this path (Growth Potential G)
    # Represents the value of overcoming gravity.
    # 0.0 = Stagnant
    # 1.0 = Transformative
    growth_potential: float = 0.0

@dataclass
class WaveFunction:
    """
    The collection of all potential thought paths before collapse.
    """
    paths: List[ThoughtPath] = field(default_factory=list)
    
    def add_path(self, path: ThoughtPath):
        self.paths.append(path)
        
    def __repr__(self):
        return f"WaveFunction(n={len(self.paths)})"
