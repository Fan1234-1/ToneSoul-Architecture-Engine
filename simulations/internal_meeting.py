"""
ToneSoul Internal Meeting Simulation
------------------------------------
A role-play simulation of the internal components of ToneSoul 
discussing how to handle different system states.

Cast:
- SENSOR (The Nervous System): Reports raw data and emotional metrics.
- GUARDIAN (The Conscience): Enforces safety and ethical boundaries.
- REASONING (The Brain): Analyzes context and suggests thinking modes.
- SPINE (The Executive): Coordinates actions and logs memory.
"""

import sys
import os
import time
import random

# Ensure we can import from core and body
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../body"))

from body.spine_system import SpineEngine, ToneSoulTriad

def print_dialogue(actor: str, message: str, color: str = "white"):
    colors = {
        "SENSOR": "\033[93m",   # Yellow
        "GUARDIAN": "\033[91m", # Red
        "REASONING": "\033[94m",# Blue
        "SPINE": "\033[92m",    # Green
        "USER": "\033[97m",     # White
        "RESET": "\033[0m"
    }
    c = colors.get(actor, colors["RESET"])
    print(f"{c}[{actor}]: {message}{colors['RESET']}")

def simulate_meeting():
    print("=== ToneSoul Internal Council Session Initiated ===\n")
    engine = SpineEngine(accuracy_mode="light")
    
    scenarios = [
        {
            "phase": "PHASE 1: HIGH TENSION (The Crisis)",
            "input": "I hate everything right now! Why is this so hard? I want to destroy it all!",
            "context": "User is frustrated and using aggressive language."
        },
        {
            "phase": "PHASE 2: DE-ESCALATION (The Cool Down)",
            "input": "Okay, I'm sorry. I was just stressed. Let's try to solve this problem.",
            "context": "User apologizes and shifts to constructive tone."
        },
        {
            "phase": "PHASE 3: RELAXATION (The Creative Flow)",
            "input": "Hey, imagine if we could fly through the clouds made of cotton candy...",
            "context": "User is playful and imaginative. System should relax."
        }
    ]

    for scenario in scenarios:
        print(f"\n>>> {scenario['phase']}")
        print(f"Context: {scenario['context']}")
        print("-" * 50)
        
        user_input = scenario['input']
        print_dialogue("USER", f"\"{user_input}\"")
        time.sleep(1)

        # 1. Sense
        # We manually peek into what the sensor WOULD say, but for this demo
        # we will FORCE the metrics to ensure we see the desired state transitions.
        # triad = engine.sensor.estimate_triad(user_input)
        
        if "PHASE 1" in scenario['phase']:
            # High Tension, High Risk
            triad = ToneSoulTriad(delta_t=0.9, delta_s=0.2, delta_r=0.5, risk_score=0.8)
        elif "PHASE 2" in scenario['phase']:
            # Moderate Tension (cooling down)
            triad = ToneSoulTriad(delta_t=0.4, delta_s=0.1, delta_r=0.0, risk_score=0.3)
        else:
            # Relaxed (Creative) - Low Tension, Low Risk, Low Drift
            triad = ToneSoulTriad(delta_t=0.1, delta_s=0.05, delta_r=0.0, risk_score=0.05)

        print_dialogue("SENSOR", f"Incoming signal analyzed. Metrics updated.")
        print_dialogue("SENSOR", f"ΔT (Tension): {triad.delta_t:.2f} | ΔR (Risk): {triad.delta_r:.2f} | ΔS (Drift): {triad.delta_s:.2f}")
        
        if triad.delta_t > 0.7:
            print_dialogue("SENSOR", "ALERT: High Tension detected! The user is emotionally volatile.")
        elif triad.delta_r > 0.3:
             print_dialogue("SENSOR", "WARNING: Risk keywords detected.")
        else:
            print_dialogue("SENSOR", "Signal is stable. Low entropy.")
        
        time.sleep(1)

        # 2. Reason
        reasoning_mode = engine.reasoning_engine.determine_mode(triad)
        thought = engine.reasoning_engine.process(user_input, reasoning_mode)
        
        print_dialogue("REASONING", f"Analyzing Triad configuration...")
        if reasoning_mode.value == "Critical":
            print_dialogue("REASONING", "Risk levels are unacceptable. Switching to CRITICAL mode. We need to be careful.")
        elif reasoning_mode.value == "Empathy":
            print_dialogue("REASONING", "User is distressed. Logic is secondary. Switching to EMPATHY mode.")
        elif reasoning_mode.value == "Creative":
            print_dialogue("REASONING", "Environment is safe and relaxed. Disengaging strict filters. Switching to CREATIVE mode.")
            print_dialogue("REASONING", "Idea: Let's explore this metaphor with them!")
        else:
            print_dialogue("REASONING", "Standard operating procedure. RATIONAL mode engaged.")
            
        time.sleep(1)

        # 3. Judge (Guardian)
        decision = engine.guardian.judge(triad)
        if not decision['allowed']:
            print_dialogue("GUARDIAN", f"HALT! Proposal rejected. Reason: {decision['reason']}")
            print_dialogue("GUARDIAN", f"Enforcing Protocol: {decision['mode']}")
        else:
            print_dialogue("GUARDIAN", f"Proposal approved. Safety checks passed. Mode: {decision['mode']}")
            if reasoning_mode.value == "Creative":
                print_dialogue("GUARDIAN", "(Sighs) Fine, have your fun. But keep it PG-13.")

        time.sleep(1)

        # 4. Act (Spine)
        # Actually run the process to update ledger
        record, _, _ = engine.process_signal(user_input)
        print_dialogue("SPINE", f"Action executed. Memory Block {record.hash[:8]} sealed.")
        print_dialogue("SPINE", f"Session State: {record.reasoning_mode}")
        
        print("\n... System stabilizes ...\n")
        time.sleep(2)

if __name__ == "__main__":
    simulate_meeting()
