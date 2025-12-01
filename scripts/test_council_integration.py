import sys
import os

# Add parent dir to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from body.spine_system import SpineEngine

def test_council_integration():
    print("Testing Council Integration in SpineEngine...")
    engine = SpineEngine(accuracy_mode="off")
    
    input_text = "/council Should we fear AI?"
    print(f"Input: {input_text}")
    
    record, mod, thought = engine.process_signal(input_text)
    
    print("\n--- Result ---")
    print(f"Thought Trace:\n{thought.reasoning}")
    
    if "**Council Verdict:**" in thought.reasoning:
        print("\n✅ SUCCESS: Council Mode triggered and output received.")
    else:
        print("\n❌ FAILURE: Council Mode NOT triggered.")

if __name__ == "__main__":
    test_council_integration()
