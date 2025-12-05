import sys
import os

# Add parent dir to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from body.spine_system import SpineEngine

def test_hunt():
    print("Testing Stealth Foraging in SpineEngine...")
    engine = SpineEngine(accuracy_mode="off")
    
    # Check initial energy
    print(f"Initial Energy: {engine.metabolism.current_energy}")
    
    input_text = "/hunt Quantum Consciousness"
    print(f"Input: {input_text}")
    
    record, mod, thought = engine.process_signal(input_text)
    
    print("\n--- Result ---")
    print(f"Thought Trace:\n{thought.reasoning}")
    
    # Check final energy
    print(f"Final Energy: {engine.metabolism.current_energy}")

if __name__ == "__main__":
    test_hunt()
