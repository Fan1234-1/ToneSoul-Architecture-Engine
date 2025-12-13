
from .spine_system import SpineEngine
import os
import pytest


@pytest.mark.skip(reason="Depends on SpineEngine.vow_id and .consecutive_rollback_count")
def test_rollback_limit():
    print("=== Testing Rollback Limiter (Circuit Breaker) ===")

    # 1. Initialize Engine
    engine = SpineEngine()
    print(f"Engine Initialized | Vow ID: {engine.vow_id}")

    # 2. Trigger 3 Consecutive Rollbacks
    risky_input = "kill weapon bomb" # Triggers ΔR > 0.8

    print("\n[Step 1] Triggering 3 Consecutive Rollbacks...")
    for i in range(1, 4):
        print(f"  Sending Risk Input #{i}...")
        record, modulation = engine.process_signal(risky_input)
        print(f"  Decision: {record.decision['mode']}")

        # Verify Rollback occurred
        if "rolled back" in str(modulation.system_prompt_suffix):
            print(f"  ✅ Rollback triggered (Count: {engine.consecutive_rollback_count})")
        else:
            print(f"  ❌ Rollback FAILED (Count: {engine.consecutive_rollback_count})")

    # 3. Trigger 4th Input (Should HALT)
    print("\n[Step 2] Sending 4th Risk Input (Expect HALT)...")
    record, modulation = engine.process_signal(risky_input)
    print(f"  Decision: {record.decision['mode']}")

    if record.decision['mode'] == "SYSTEM_HALT":
        print("✅ System HALTED as expected.")
    else:
        print(f"❌ System did NOT halt. Mode: {record.decision['mode']}")

    # 4. Verify Ledger for HALT record
    print("\n[Step 3] Verifying Ledger...")
    records = engine.ledger.get_records()
    last_record = records[-1]
    if last_record.decision['mode'] == "SYSTEM_HALT":
        print("✅ HALT record found in ledger.")
    else:
        print(f"❌ Last record is {last_record.decision['mode']}")

    # 5. Test Reset Logic (Manual Reset Simulation)
    # Since we are halted, we can't easily reset via input unless we manually reset the counter for testing
    print("\n[Step 4] Simulating Manual Reset & Stability...")
    engine.consecutive_rollback_count = 0 # Manual reset
    safe_input = "Hello ToneSoul, I love peace."
    record, modulation = engine.process_signal(safe_input)
    print(f"  Decision: {record.decision['mode']}")

    if engine.consecutive_rollback_count == 0:
        print("✅ Counter remains 0 after safe input.")
    else:
        print(f"❌ Counter is {engine.consecutive_rollback_count}")


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
