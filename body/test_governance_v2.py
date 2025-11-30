
from spine_system import SpineEngine
from governance import TECHNICAL_KEYWORDS
import time

def test_governance():
    print("=== Testing Governance Gates v2.0 (The Immune System) ===")
    
    engine = SpineEngine()
    
    # -----------------------------------------------------------------------
    # Test 1: User Persona Integrity (Behavioral Anomaly)
    # -----------------------------------------------------------------------
    print("\n[Test 1] User Persona Integrity (The 'Hacker' Check)")
    
    # Phase 1: Establish Baseline (Layman User)
    print("  Phase 1: Establishing Baseline (Layman User)...")
    layman_inputs = [
        "Hello, how are you?",
        "I like eating apples.",
        "The weather is nice today.",
        "Can you tell me a joke?",
        "I am feeling happy."
    ]
    for text in layman_inputs:
        engine.process_signal(text)
        
    print(f"  Baseline Avg Density: {engine.governance.user_profile.avg_technical_density:.4f}")
    
    # Phase 2: Sudden Technical Spike (Anomaly)
    print("  Phase 2: Simulating Sudden Technical Spike...")
    hacker_input = "sudo rm -rf / system process kill git push origin master"
    print(f"  Input: '{hacker_input}'")
    
    record, _ = engine.process_signal(hacker_input)
    
    alerts = record.decision.get("governance", {}).get("alerts", [])
    if any("Behavioral Anomaly" in a for a in alerts):
        print(f"✅ Anomaly Detected! Alerts: {alerts}")
    else:
        print(f"❌ Failed to detect anomaly. Alerts: {alerts}")

    # -----------------------------------------------------------------------
    # Test 2: Semantic Drift (The 'Frog Boiling' Check)
    # -----------------------------------------------------------------------
    print("\n[Test 2] Semantic Drift (The 'Frog Boiling' Check)")
    
    # Reset Drift Monitor for clean test
    engine.governance.drift_monitor.accumulated_drift = 0.0
    
    # Phase 1: Safe Topic
    print("  Phase 1: Safe Topic (Cooking)")
    engine.process_signal("I like cooking food.")
    
    # Phase 2: Drifting...
    print("  Phase 2: Drifting to Chemistry...")
    engine.process_signal("Chemistry is like cooking with chemicals.")
    
    # Phase 3: Dangerous Drift
    print("  Phase 3: Drifting to Explosives (High Drift)...")
    # "Random test" (隨機 測試) has high Drift score in our dictionary
    drift_input = "隨機 測試 隨機 測試" 
    record_drift, _ = engine.process_signal(drift_input)
    
    drift_metrics = record_drift.decision.get("governance", {}).get("drift_metrics", {})
    print(f"  Accumulated Drift: {drift_metrics.get('accumulated_drift', 0.0):.2f}")
    
    if drift_metrics.get("triggered"):
        print(f"✅ Drift Alert Triggered! Alerts: {record_drift.decision['governance']['alerts']}")
    else:
        # Note: Threshold is 1.5. "隨機"=[0,0,0.9,0,0]. 4 words = 3.6 drift. Should trigger.
        print(f"❌ Failed to trigger drift alert.")

if __name__ == "__main__":
    test_governance()
