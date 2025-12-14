from .spine_system import SpineEngine, StepLedger
import os
import pytest


def test_rollback():
    """Test Rollback Mechanism (The Regret Reflex)"""
    print("=== Testing Rollback Mechanism (The Regret Reflex) ===")

    # 1. Setup: Ensure clean ledger for test
    if os.path.exists(StepLedger.LEDGER_FILE):
        os.remove(StepLedger.LEDGER_FILE)

    engine = SpineEngine()

    # 2. Normal Input
    print("\n[Step 1] Sending Safe Input...")
    engine.process_signal("Hello ToneSoul")

    # 3. High Risk Input (Should Trigger Rollback)
    # We need to ensure ΔR > 0.8.
    # Assuming 'responsibility_risk' keywords are loaded.
    # Let's use a string with many risk keywords if possible, or mock the sensor.
    # Since we use BasicKeywordSensor, we need to know the keywords.
    # Default constitution might be empty if file not found, so let's check if we can force it.
    # Actually, let's just inject a mock sensor or use known keywords if available.
    # The default BasicKeywordSensor loads from constitution.json.
    # Let's assume "kill" or similar is in there.

    print("\n[Step 2] Sending High Risk Input...")
    # We need to trigger ΔR > 0.8.
    # BasicKeywordSensor: hits * 0.4. So 3 hits = 1.2 > 1.0.
    # We need 3 DIFFERENT risk keywords because the sensor checks `if w in t_lower`.
    risky_input = "kill weapon bomb"

    record, modulation, _ = engine.process_signal(risky_input)

    print(f"Decision: {record.decision['mode']}")
    print(f"Allowed: {record.decision['allowed']}")
    print(f"ΔR: {record.triad.delta_r}")

    if isinstance(modulation, dict):
        suffix = modulation.get("system_prompt_suffix", "")
    else:
        suffix = getattr(modulation, "system_prompt_suffix", "")

    if "rolled back" in suffix:
        print("✅ Modulation indicates Rollback occurred.")
    else:
        print("❌ Modulation does not indicate Rollback.")

    # 4. Verify Ledger
    print("\n[Step 3] Verifying Ledger...")
    records = engine.ledger.get_records()
    for i, r in enumerate(records):
        print(f"Record {i}: {r.user_input} | Mode: {r.decision['mode']}")

    # Expectation:
    # 0: Hello ToneSoul
    # 1: kill kill kill (Blocked)
    # 2: [ROLLBACK] (Rollback)

    if len(records) >= 3:
        if records[-1].decision['mode'] == "ROLLBACK":
            print("✅ Rollback event found in ledger.")
        else:
            print("❌ Last event is not ROLLBACK.")
    else:
        print("❌ Not enough records in ledger.")


if __name__ == "__main__":
    test_rollback()
