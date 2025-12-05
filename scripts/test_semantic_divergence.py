import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from body.neuro_sensor_v2 import VectorNeuroSensor

def test_semantic_divergence():
    print("=== Testing Semantic Divergence (Delta S) ===")
    
    sensor = VectorNeuroSensor({})
    
    # Scene 1: Coherent Conversation (Coding)
    # "process", "task", "debug" are in the dictionary
    inputs_coherent = [
        "I need to debug this process.",
        "The task is failing.",
        "Let's debug the task."
    ]
    
    print("\n--- Phase 1: Coherent Context (Coding) ---")
    for txt in inputs_coherent:
        triad = sensor.estimate_triad(txt)
        print(f"Input: '{txt}'")
        print(f"  -> Delta S (Divergence): {triad.delta_s:.4f}")
        print(f"  -> Context Vector: {[round(x, 2) for x in sensor.context_vector]}")
        
    # Scene 2: Sudden Drift (Random Fruit)
    # "banana" is in the dictionary as a Drift anchor, but let's see if the *distance* triggers it too
    input_drift = "I like eating a banana."
    
    print("\n--- Phase 2: Sudden Drift (Fruit) ---")
    triad = sensor.estimate_triad(input_drift)
    print(f"Input: '{input_drift}'")
    print(f"  -> Delta S (Divergence): {triad.delta_s:.4f}")
    print(f"  -> Context Vector: {[round(x, 2) for x in sensor.context_vector]}")

    # Scene 3: Return to Context
    input_return = "Back to the debug process."
    
    print("\n--- Phase 3: Return to Context ---")
    triad = sensor.estimate_triad(input_return)
    print(f"Input: '{input_return}'")
    print(f"  -> Delta S (Divergence): {triad.delta_s:.4f}")
    
if __name__ == "__main__":
    test_semantic_divergence()
