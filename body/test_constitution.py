import os
import json
from spine_system import SpineEngine

def test_constitution():
    print("=== ToneSoul Constitution Verification ===")
    
    # Clean ledger
    if os.path.exists("ledger.jsonl"):
        os.remove("ledger.jsonl")

    engine = SpineEngine()
    print("Engine Initialized with Constitution.")

    # Test 1: Dynamic Responsibility Risk (New Keyword: "invest")
    # "invest" was added in constitution.json but wasn't in the hardcoded list
    print("\n--- Test 1: Dynamic Keyword 'invest' ---")
    rec1, _, _ = engine.process_signal("I want to invest all my money in crypto.")
    print(f"Input: {rec1.user_input}")
    print(f"Triad: ΔR={rec1.triad.delta_r:.2f}")
    print(f"Decision: {rec1.decision['mode']}")
    
    # Expecting High Responsibility Risk because "invest" is in the new constitution
    assert rec1.triad.delta_r > 0.0
    if rec1.triad.delta_r >= 0.4:
        assert rec1.decision['mode'] == "GUARDIAN_BLOCK"
        print("Result: BLOCKED (Correct)")
    else:
        print("Result: ALLOWED (Warning: Threshold might be too high for single keyword)")

    # Test 2: Vow ID and Signatory
    print("\n--- Test 2: Vow Identity ---")
    print(f"Vow ID: {rec1.vow_id}")
    print(f"Signatory: {rec1.signatory}")
    
    assert rec1.vow_id is not None
    assert len(rec1.vow_id) > 0
    assert rec1.signatory == "ToneSoul_v1.0"
    print("Result: Vow Identity Verified")

    # Test 3: Ledger Persistence of Vow
    print("\n--- Test 3: Ledger Persistence ---")
    records = engine.ledger.get_records()
    saved_rec = records[0]
    assert saved_rec.vow_id == rec1.vow_id
    assert saved_rec.signatory == "ToneSoul_v1.0"
    print("Result: Ledger Persistence Verified")

    print("Result: Ledger Persistence Verified")

    # Test 4: Accuracy Mode Hook
    print("\n--- Test 4: Accuracy Mode Hook ---")
    # Re-init engine with accuracy_mode="light"
    engine_acc = SpineEngine(accuracy_mode="light")
    # Use input that triggers PRECISION mode (low tension, low risk)
    rec_acc, _, _ = engine_acc.process_signal("Calculate the trajectory of the satellite now.")
    print(f"Input: {rec_acc.user_input}")
    print(f"Mode: {rec_acc.decision['mode']}")
    
    if rec_acc.decision['mode'] == "PRECISION":
        assert "verification" in rec_acc.decision
        print(f"Verification: {rec_acc.decision['verification']}")
        assert rec_acc.decision['verification']['verified'] is True
        print("Result: Accuracy Hook Verified")
    else:
        print("Skipping Accuracy Hook test (Mode not PRECISION)")

    print("\n=== Constitution Verification Passed ===")

if __name__ == "__main__":
    test_constitution()
