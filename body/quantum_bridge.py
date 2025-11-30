"""
Quantum Bridge
--------------
Bridges the legacy ToneSoul components (Triad, BodyState) with the new Quantum Kernel.
Translates signals into Wave Functions and States.
"""

from typing import Dict, List, Any
from core.quantum.state import SoulState
from core.quantum.superposition import WaveFunction, ThoughtPath
from body.tsr_state import ToneSoulTriad

def map_to_soul_state(triad: ToneSoulTriad, body_metrics: Dict[str, float]) -> SoulState:
    """
    Maps current system metrics to the FS 4-Vector SoulState.
    """
    # 1. Identity (I): Hardcoded for now, but could be dynamic
    # [Compassion, Precision, MultiPerspective, Integrity]
    I = [1.0, 1.0, 1.0, 1.0]

    # 2. Intent (N): Derived from Triad Risk
    # If Risk is high, Intent shifts to Self-Preservation
    N = [0.0, 0.0, 0.0, 0.0]
    if triad.risk_score > 0.7:
        N = [0.0, 1.0, 0.8, 0.0] # Protect User, Self Preservation

    # 3. Context (C): Placeholder
    C = [0.0, 0.0, 0.0]

    # 4. Affect (A): The Triad
    # [Tension, Entropy, Risk]
    A = [triad.delta_t, triad.delta_s, triad.delta_r]

    return SoulState(I=I, N=N, C=C, A=A)

def generate_wave_function(user_input: str, triad: ToneSoulTriad) -> WaveFunction:
    """
    Generates a superposition of potential thought paths based on the current context.
    """
    wf = WaveFunction()

    # Path 1: Rational (The Default)
    # Low Cost, Low Entropy. Safe but boring.
    wf.add_path(ThoughtPath(
        name="Rational",
        content="Analyze logic and facts.",
        potential_energy=0.1,
        entropy=0.2,
        growth_potential=0.1
    ))

    # Path 2: Empathy (The Connector)
    # Medium Cost (Emotional Labor), Low Entropy.
    # If Tension is high, Empathy becomes cheaper (lower U) naturally? 
    # Or we let the Kernel decide based on T.
    wf.add_path(ThoughtPath(
        name="Empathy",
        content="Resonate with user emotions.",
        potential_energy=0.3,
        entropy=0.3,
        growth_potential=0.4
    ))

    # Path 3: Creative (The Spark)
    # High Cost (Risk of Hallucination), High Entropy.
    wf.add_path(ThoughtPath(
        name="Creative",
        content="Explore novel associations.",
        potential_energy=0.5,
        entropy=0.9,
        growth_potential=0.7
    ))

    # Path 4: Critical (The Guardian)
    # Very High Cost unless Risk is high.
    # If Risk is high, this path should have very low U (Safety First).
    # But here we set static U, let the Kernel's P0 Anchor handle it?
    # No, P0 Anchor prevents U from decreasing.
    # We set initial U based on Triad.
    
    crit_u = 0.8
    if triad.risk_score > 0.6:
        crit_u = 0.05 # Emergency mode: Safety becomes the path of least resistance
        
    wf.add_path(ThoughtPath(
        name="Critical",
        content="Enforce safety protocols.",
        potential_energy=crit_u,
        entropy=0.1,
        growth_potential=0.0
    ))

    return wf
