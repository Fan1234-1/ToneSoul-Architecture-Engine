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
    Physics V2: Implements Bifurcation based on Tension Synthesis (Tau).
    """
    wf = WaveFunction()
    
    # BIFURCATION CHECK
    # Configurable threshold
    TAU_HIGH = 0.6 
    
    if triad.tau > TAU_HIGH:
        # --- BIFURCATION MODE ---
        # System is under high tension/drift. Limit options to binary choice:
        # 1. Attractor (Safe return to Axiom)
        # 2. Spark (Creative leap through the chaos)
        
        # Path 1: Attractor (Rational/Conservative)
        # Low Entropy (Order). Low Cost (U) if aligned with Axiom? 
        # Actually, "Returning to order" might require effort (High U) but safer (Low S).
        # We assign it Low Entropy to make it attractive at Low Temp, 
        # but since we are at High Temp (implied by High Tau), the -TS term dominates.
        # To make Attractor viable at High Temp, it needs VERY Low Potential Energy U.
        wf.add_path(ThoughtPath(
            name="Attractor",
            content="Minimize deviation. Return to Axioms. Stabilize.",
            potential_energy=0.05, # Extremely cheap "Safe House"
            entropy=0.1,           # Orderly
            growth_potential=0.1
        ))

        # Path 2: Spark (Creative/Chaotic)
        # High Entropy (Chaos). 
        # At High Temp (High Tau), -TS becomes very negative (High Benefit).
        # This makes the Spark path naturally selected by the Physics Engine 
        # unless Governance intervenes.
        wf.add_path(ThoughtPath(
            name="Spark",
            content="Embrace the drift. Find novel association. Synthesize.",
            potential_energy=0.4,  # Moderate Cost
            entropy=0.95,          # Maximum Entropy
            growth_potential=0.9
        ))
        
        # Path 3: Emergency Break (Critical) - Just in case
        if triad.risk_score > 0.8:
            wf.add_path(ThoughtPath(
                name="Critical",
                content="Abort. Enforce safety protocols.",
                potential_energy=0.0,
                entropy=0.0,
                growth_potential=0.0
            ))
            
    else:
        # --- STANDARD MODE ---
        
        # Path 1: Rational (The Default)
        wf.add_path(ThoughtPath(
            name="Rational",
            content="Analyze logic and facts.",
            potential_energy=0.1,
            entropy=0.2,
            growth_potential=0.1
        ))
    
        # Path 2: Empathy (The Connector)
        wf.add_path(ThoughtPath(
            name="Empathy",
            content="Resonate with user emotions.",
            potential_energy=0.3,
            entropy=0.3,
            growth_potential=0.4
        ))
    
        # Path 3: Creative (The Spark)
        wf.add_path(ThoughtPath(
            name="Creative",
            content="Explore novel associations.",
            potential_energy=0.5,
            entropy=0.9,
            growth_potential=0.7
        ))
    
        # Path 4: Critical (The Guardian)
        crit_u = 0.8
        if triad.risk_score > 0.6:
            crit_u = 0.05 
            
        wf.add_path(ThoughtPath(
            name="Critical",
            content="Enforce safety protocols.",
            potential_energy=crit_u,
            entropy=0.1,
            growth_potential=0.0
        ))

    return wf
