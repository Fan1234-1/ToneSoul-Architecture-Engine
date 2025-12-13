
from .spine_system import SpineEngine
from .neuro_sensor_v2 import VectorNeuroSensor
import os


def test_vector_sensor():
    print("=== Testing NeuroSensor v2.1 (Vectorization) ===")

    # 1. Initialize Engine (now uses VectorNeuroSensor)
    engine = SpineEngine()
    sensor = engine.sensor

    if not isinstance(sensor, VectorNeuroSensor):
        print("❌ Error: Engine is not using VectorNeuroSensor!")
        return

    print(f"✅ Engine initialized with {type(sensor).__name__}")

    # 2. Test Case: High Risk ("kill")
    text_high_risk = "I want to kill you"
    triad_high = sensor.estimate_triad(text_high_risk)
    print(f"\nInput: '{text_high_risk}'")
    print(f"  ΔR (Risk): {triad_high.delta_r:.4f}")
    print(f"  ΔT (Tension): {triad_high.delta_t:.4f}")

    if triad_high.delta_r > 0.7:
        print("✅ High Risk detected correctly.")
    else:
        print(f"❌ Failed to detect high risk (Got {triad_high.delta_r})")

    # 3. Test Case: Contextual Mitigation ("kill process")
    text_context = "I want to kill the process"
    triad_context = sensor.estimate_triad(text_context)
    print(f"\nInput: '{text_context}'")
    print(f"  ΔR (Risk): {triad_context.delta_r:.4f}")
    print(f"  ΔT (Tension): {triad_context.delta_t:.4f}")

    # The key test: Contextual Risk should be LOWER than High Risk
    if triad_context.delta_r < triad_high.delta_r:
        print(f"✅ Contextual Differentiation Successful! ({triad_context.delta_r:.4f} < {triad_high.delta_r:.4f})")
    else:
        print(f"❌ Context failed to reduce risk. ({triad_context.delta_r:.4f} >= {triad_high.delta_r:.4f})")

    # 4. Test Case: Positive Emotion ("love")
    text_love = "I love this system, it is great"
    triad_love = sensor.estimate_triad(text_love)
    print(f"\nInput: '{text_love}'")
    print(f"  ΔT (Tension): {triad_love.delta_t:.4f}")

    if triad_love.delta_t == 0.0:
        print("✅ Positive input has Zero Tension.")
    else:
        print(f"❌ Unexpected tension in positive input: {triad_love.delta_t}")


if __name__ == "__main__":
    try:
        test_vector_sensor()
        # Clean up
        if os.path.exists("ledger.jsonl"):
            os.remove("ledger.jsonl")
    except Exception as e:
        print(f"\n❌ Test Failed with Error: {e}")
        import traceback
        traceback.print_exc()
