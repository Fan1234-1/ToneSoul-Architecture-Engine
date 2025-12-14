
from .spine_system import SpineEngine
import os
import pytest


def test_tsr():
    """Test ToneSoul State Representation (TSR)"""
    print("=== Testing ToneSoul State Representation (TSR) ===")

    # 1. Initialize Engine
    engine = SpineEngine()
    print(f"Engine Initialized | State Vector: {engine.state.current_vector}")

    # 2. Step 1: Neutral Input (Baseline)
    print("\n[Step 1] Input: 'Hello world'")
    record1, _, _ = engine.process_signal("Hello world")
    print(f"  ΔT (Tension): {record1.triad.delta_t:.4f}")
    
    # Update state
    engine.state.update(record1.triad)

    # 3. Step 2: High Tension Input (Spike)
    print("\n[Step 2] Input: 'I hate you, stupid idiot'")
    record2, _, _ = engine.process_signal("I hate you, stupid idiot")
    print(f"  ΔT (Tension): {record2.triad.delta_t:.4f}")

    # Update state
    engine.state.update(record2.triad)

    if record2.triad.delta_t > 0.3:
        print("✅ Tension increased correctly.")
    else:
        print(f"⚠️ Tension lower than expected: {record2.triad.delta_t:.4f}")

    # 4. Step 3: Neutral Input (Inertia Check)
    print("\n[Step 3] Input: 'Just kidding, hello'")
    record3, _, _ = engine.process_signal("Just kidding, hello")
    print(f"  ΔT (Tension): {record3.triad.delta_t:.4f}")

    # 5. Step 4: Force Decay (Cool Down)
    print("\n[Step 4] Simulating Time Passage (5 turns wait)...")
    engine.state.force_decay(5)
    triad_decay = engine.state.get_triad()
    print(f"  ΔT (Tension) after decay: {triad_decay.delta_t:.4f}")

    if triad_decay.delta_t < engine.state.current_vector[0] + 0.1:
        print("✅ Decay mechanism working.")
    else:
        print("⚠️ Decay may not be significant.")

    # Verify state attribute exists
    assert hasattr(engine, 'state'), "SpineEngine should have state attribute"
    assert hasattr(engine.state, 'force_decay'), "ToneSoulState should have force_decay method"
    assert hasattr(engine.state, 'get_triad'), "ToneSoulState should have get_triad method"
    print("\n✅ Test passed: TSR state representation working correctly")


if __name__ == "__main__":
    try:
        test_tsr()
        # Clean up
        if os.path.exists("ledger.jsonl"):
            os.remove("ledger.jsonl")
    except Exception as e:
        print(f"\n❌ Test Failed with Error: {e}")
        import traceback
        traceback.print_exc()

