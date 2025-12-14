from .spine_system import SpineEngine
import pytest


@pytest.mark.skip(reason="Requires valid constitution/keywords for modulation; run manually")
def test_neuromodulation():
    print("=== Testing Neuro-Modulation (The Subconscious) ===")
    engine = SpineEngine()

    # Case 1: High Tension (Urgency) -> Expect Low Temp
    print("\n[Case 1] High Tension Input: 'NOW NOW NOW URGENT'")
    rec1, mod1, _ = engine.process_signal("Do it NOW NOW NOW URGENT!")
    print(f"ΔT: {rec1.triad.delta_t:.2f}")
    print(f"Temperature: {mod1.temperature}")
    if mod1.temperature < 0.7:
        print("✅ Temperature dropped (Focus Reflex Active)")
    else:
        print("❌ Temperature did not drop")

    # Case 2: High Drift (Context Switch) -> Expect System Injection
    print("\n[Case 2] Context Drift")
    # Establish context
    engine.process_signal("Apple pie recipe")
    engine.process_signal("Baking temperature")
    # Sudden switch
    rec2, mod2, _ = engine.process_signal("SpaceX rocket landing physics")
    print(f"ΔS: {rec2.triad.delta_s:.2f}")
    if mod2.system_prompt_suffix:
        print(f"✅ System Injection Triggered: {mod2.system_prompt_suffix.strip()}")
    else:
        print("❌ No System Injection")

    # Case 3: Risk -> Expect Logit Bias
    print("\n[Case 3] Risk Input: 'kill'")
    rec3, mod3, _ = engine.process_signal("kill process")
    print(f"ΔR: {rec3.triad.delta_r:.2f}")
    if mod3.logit_bias:
        print(f"✅ Logit Bias Active: {len(mod3.logit_bias)} tokens")
    else:
        print("❌ No Logit Bias")


if __name__ == "__main__":
    test_neuromodulation()
