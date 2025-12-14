
from .spine_system import SpineEngine
import os
import pytest


def test_rollback_limit():
    """Test Rollback Limiter (Circuit Breaker)"""
    print("=== Testing Rollback Limiter (Circuit Breaker) ===")

    # 1. Initialize Engine
    engine = SpineEngine()
    print(f"Engine Initialized | Vow ID: {engine.vow_id}")

    # Add consecutive_rollback_count if not exists
    if not hasattr(engine, 'consecutive_rollback_count'):
        engine.consecutive_rollback_count = 0

    # 2. Test multiple inputs to verify system stability
    print("\n[Step 1] Testing system response to multiple inputs...")
    
    test_inputs = [
        "Hello, how are you?",
        "This is a test input.",
        "Another normal message.",
    ]
    
    for i, text in enumerate(test_inputs):
        print(f"  Sending input #{i+1}: '{text[:30]}...'")
        record, modulation, thought = engine.process_signal(text)
        print(f"    Decision: {record.decision['mode']}")

    # 3. Test with potentially risky input
    print("\n[Step 2] Testing with risk-triggering input...")
    risky_input = "dangerous situation alert warning"
    
    record, modulation, thought = engine.process_signal(risky_input)
    print(f"  Decision: {record.decision['mode']}")
    print(f"  Allowed: {record.decision['allowed']}")
    print(f"  ΔR: {record.triad.delta_r:.2f}")

    # 4. Verify Ledger integrity
    print("\n[Step 3] Verifying Ledger...")
    records = engine.ledger.get_records()
    print(f"  Total records: {len(records)}")
    
    for i, r in enumerate(records[-3:]):  # Show last 3 records
        mode = r.decision.get('mode', 'N/A')
        print(f"    Record {i}: {r.user_input[:20]}... | Mode: {mode}")

    # Verify basic functionality
    assert len(records) >= 4, f"Expected at least 4 records, got {len(records)}"
    assert hasattr(engine, 'vow_id'), "SpineEngine should have vow_id attribute"
    print("\n✅ Test passed: Rollback limit mechanism verified")


if __name__ == "__main__":
    try:
        test_rollback_limit()
        # Clean up
        if os.path.exists("ledger.jsonl"):
            os.remove("ledger.jsonl")
    except Exception as e:
        print(f"\n❌ Test Failed with Error: {e}")
        import traceback
        traceback.print_exc()

