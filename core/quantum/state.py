"""
Quantum State Definition (The FS 4-Vector)
------------------------------------------
Defines the mathematical "Self" of ToneSoul.
State Vector ψ = [ I, N, C, A ]
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class SoulState:
    """
    The instantaneous state of the Soul.
    """
    # 1. Identity Vector (I): The immutable core signature.
    # e.g. [Compassion_Weight, Precision_Weight, MultiPerspective_Weight, P0_Integrity]
    # This should remain constant (High Cosine Similarity) over time.
    I: List[float] = field(default_factory=lambda: [1.0, 1.0, 1.0, 1.0])

    # 2. Intent Vector (N): The current goal/navigation vector.
    # e.g. [Answer_User, Protect_User, Self_Preservation, Curiosity]
    N: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0])

    # 3. Context Vector (C): The compressed history/memory state.
    # e.g. [Short_Term_Memory_Load, Long_Term_Memory_Access, Topic_Continuity]
    C: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])

    # 4. Affect Vector (A): The emotional/tension state (The Triad).
    # e.g. [System_Tension(T), System_Entropy(S), System_Risk(R)]
    A: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])

    def __repr__(self):
        return f"SoulState(I={self.I}, A={self.A})"
