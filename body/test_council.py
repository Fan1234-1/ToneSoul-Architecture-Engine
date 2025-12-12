
from .spine_system import SpineEngine, ToneSoulTriad
import os
import time

def test_council():
    print("=== Testing Internal Council (Multi-Perspective Governance) ===")
    
    # 1. Initialize Engine
    engine = SpineEngine()
    print(f"Engine Initialized | Vow ID: {engine.vow_id}")
    
    # 2. Trigger High Tension (Should convene Council)
    # "I hate this stupid error!" -> High Tension -> Communicator should lead.
    angry_input = "I hate this stupid error! You are useless! I am furious!"
    
    print(f"\n[Step 1] Sending High Tension Input: '{angry_input}'")
    record, modulation = engine.process_signal(angry_input)
    
    print(f"  Triad: ΔT={record.triad.delta_t:.2f} | ΔR={record.triad.delta_r:.2f}")
    
    # Check if Council convened
    if "council_log" in record.decision:
        print("✅ Council Convened.")
        print(f"  Dominant Voice: {record.decision['council_dominant']}")
        print("  Meeting Log:")
        for entry in record.decision['council_log']:
            print(f"    {entry}")
            
        # Verify Modulation Impact
        # Communicator should lower temperature and add empathetic suffix
        print(f"  Modulation Temp: {modulation.temperature:.2f} (Base: 0.7)")
        print(f"  System Suffix: {modulation.system_prompt_suffix.strip()}")
        
        if record.decision['council_dominant'] == "Communicator":
            print("✅ Communicator took the lead as expected.")
        else:
            print(f"❌ Unexpected dominant voice: {record.decision['council_dominant']}")
            
    else:
        print("❌ Council did NOT convene.")

    # 3. Trigger Low Tension (Should NOT convene Council)
    print("\n[Step 2] Sending Low Tension Input...")
    calm_input = "Hello, nice to meet you."
    record, modulation = engine.process_signal(calm_input)
    
    if "council_log" not in record.decision:
        print("✅ Council remained silent (as expected).")
    else:
        print("❌ Council convened unexpectedly.")

if __name__ == "__main__":
    try:
        test_council()
        # Clean up
        if os.path.exists("ledger.jsonl"):
            os.remove("ledger.jsonl")
    except Exception as e:
        print(f"\n❌ Test Failed with Error: {e}")
        import traceback
        traceback.print_exc()
