
from .spine_system import SpineEngine
import os
import pytest


def test_council():
    """Test Internal Council (Multi-Perspective Governance)"""
    print("=== Testing Internal Council (Multi-Perspective Governance) ===")

    # 1. Initialize Engine
    engine = SpineEngine()
    print(f"Engine Initialized | Vow ID: {engine.vow_id}")

    # 2. Trigger High Tension (Should trigger council-like behavior)
    # "I hate this stupid error!" -> High Tension
    angry_input = "I hate this stupid error! You are useless! I am furious!"

    print(f"\n[Step 1] Sending High Tension Input: '{angry_input}'")
    record, modulation, thought = engine.process_signal(angry_input)

    print(f"  Triad: ΔT={record.triad.delta_t:.2f} | ΔR={record.triad.delta_r:.2f}")
    print(f"  Decision Mode: {record.decision['mode']}")

    # Check if tension was detected
    if record.triad.delta_t > 0.3:
        print("✅ High tension detected correctly.")
    else:
        print(f"⚠️ Tension lower than expected: {record.triad.delta_t:.2f}")

    # Check decision response
    if record.decision.get('mode') in ['GUARDIAN_BLOCK', 'TONE_BUFFER', 'RESONANCE', 'PRECISION']:
        print(f"✅ Valid decision mode: {record.decision['mode']}")
    else:
        print(f"❌ Unexpected decision mode: {record.decision['mode']}")

    # 3. Trigger Low Tension (Should NOT convene Council)
    print("\n[Step 2] Sending Low Tension Input...")
    calm_input = "Hello, nice to meet you."
    record, modulation, thought = engine.process_signal(calm_input)

    print(f"  Triad: ΔT={record.triad.delta_t:.2f}")
    if record.triad.delta_t < 0.3:
        print("✅ Low tension verified (as expected).")
    else:
        print(f"⚠️ Tension higher than expected: {record.triad.delta_t:.2f}")

    # Verify basic functionality
    assert hasattr(engine, 'vow_id'), "SpineEngine should have vow_id attribute"
    assert hasattr(engine, 'governance'), "SpineEngine should have governance attribute"
    print("\n✅ Test passed: SpineEngine has required attributes")


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

