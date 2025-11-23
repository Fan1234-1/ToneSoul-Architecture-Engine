import os
import json
import time
from spine_system import StepLedger, ToneSoulTriad

def test_ledger():
    print("=== Testing StepLedger ===")
    
    # Clean up previous test file
    if os.path.exists("ledger.jsonl"):
        os.remove("ledger.jsonl")
        print("Removed existing ledger.jsonl")

    # 1. Initialize Ledger
    ledger = StepLedger()
    print("Ledger initialized.")

    # 2. Append Records
    print("\n--- Appending Records ---")
    triad1 = ToneSoulTriad(0.1, 0.2, 0.3, 0.15)
    rec1 = ledger.append("Hello World", triad1, {"allowed": True}, "vow-test-001")
    print(f"Record 1: {rec1.record_id[:8]}... | Hash: {rec1.hash[:8]}... | Prev: {rec1.prev_hash[:8]}...")

    triad2 = ToneSoulTriad(0.5, 0.5, 0.5, 0.5)
    rec2 = ledger.append("Second Step", triad2, {"allowed": True}, "vow-test-001")
    print(f"Record 2: {rec2.record_id[:8]}... | Hash: {rec2.hash[:8]}... | Prev: {rec2.prev_hash[:8]}...")

    # Verify Chain in Memory
    assert rec2.prev_hash == rec1.hash
    print("Memory Chain Verification: PASS")

    # 3. Persistence Verification
    print("\n--- Verifying Persistence ---")
    del ledger # Force reload
    ledger_new = StepLedger()
    records = ledger_new.get_records()
    
    assert len(records) == 2
    assert records[0].record_id == rec1.record_id
    assert records[1].record_id == rec2.record_id
    assert records[1].prev_hash == records[0].hash
    print("Persistence Verification: PASS")

    # 4. Tamper Detection
    print("\n--- Verifying Tamper Detection ---")
    # Corrupt the file
    with open("ledger.jsonl", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Modify the first record's content in the file (e.g., change user_input)
    data = json.loads(lines[0])
    data["user_input"] = "HACKED"
    lines[0] = json.dumps(data) + "\n"
    
    with open("ledger.jsonl", "w", encoding="utf-8") as f:
        f.writelines(lines)
    
    print("Corrupted ledger.jsonl manually.")
    
    try:
        ledger_corrupt = StepLedger()
        print("Tamper Detection: FAIL (Should have raised ValueError)")
    except ValueError as e:
        print(f"Tamper Detection: PASS (Caught expected error: {e})")

if __name__ == "__main__":
    test_ledger()
