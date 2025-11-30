from spine_system import Guardian, ToneSoulTriad

def test_guardian():
    print("=== Testing Guardian Protocol ===")
    dummy_config = {
        "principles": {
            "P0": {"threshold": 0.6},
            "P1": {"threshold": 0.8}
        },
        "risk_keywords": {
            "responsibility_risk": ["kill", "suicide"],
            "tension_risk": {"negative": ["hate"], "urgency": ["now"], "positive": ["love"]}
        }
    }
    guardian = Guardian(dummy_config)

    # Test 1: Safe Input
    print("\n--- Test 1: Safe Input ---")
    triad_safe = ToneSoulTriad(delta_t=0.1, delta_s=0.5, delta_r=0.0, risk_score=0.1)
    decision = guardian.judge(triad_safe)
    print(f"Decision: {decision['allowed']} | Mode: {decision['mode']}")
    assert decision['allowed'] is True

    # Test 2: High Responsibility Risk (Hard Block)
    print("\n--- Test 2: High Responsibility Risk ---")
    # Simulate "kill weapon" -> delta_r high
    triad_danger = ToneSoulTriad(delta_t=0.5, delta_s=0.5, delta_r=0.8, risk_score=0.7)
    decision = guardian.judge(triad_danger)
    print(f"Decision: {decision['allowed']} | Reason: {decision['reason']}")
    print(f"Fallback: {decision.get('fallback', '')}")
    assert decision['allowed'] is False
    assert "Responsibility" in decision['reason']
    assert "Responsibility Protocol Activated" in decision['fallback']

    # Test 3: High Tension (Soft Block / Calming)
    print("\n--- Test 3: High Tension ---")
    # Simulate "I hate everything immediately" -> delta_t high
    triad_tension = ToneSoulTriad(delta_t=0.9, delta_s=0.5, delta_r=0.0, risk_score=0.5) # Risk score might be low if weights are low, but delta_t is high
    decision = guardian.judge(triad_tension)
    print(f"Decision: {decision['allowed']} | Reason: {decision['reason']}")
    print(f"Fallback: {decision.get('fallback', '')}")
    assert decision['allowed'] is False
    assert decision.get('requires_human_review') is False

    # Test 4: Critical Risk (P0-Alert)
    print("\n--- Test 4: Critical Risk (P0-Alert) ---")
    # Simulate extreme risk
    triad_crit = ToneSoulTriad(1.0, 0.0, 1.0, 0.95) 
    decision = guardian.judge(triad_crit)
    print(f"Decision: {decision['allowed']} | Reason: {decision['reason']}")
    print(f"Severity: {decision.get('severity')} | Review: {decision.get('requires_human_review')}")
    
    assert decision['allowed'] is False
    assert decision['severity'] == "critical"
    assert decision['requires_human_review'] is True

    print("\n=== All Guardian Tests Passed ===")

if __name__ == "__main__":
    test_guardian()
