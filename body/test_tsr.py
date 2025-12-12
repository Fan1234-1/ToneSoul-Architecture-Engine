
from .spine_system import SpineEngine
import os


def test_tsr():
    print("=== Testing ToneSoul State Representation (TSR) ===")

    # 1. Initialize Engine
    engine = SpineEngine()
    print(f"Engine Initialized | State Vector: {engine.state.current_vector}")

    # 2. Step 1: Neutral Input (Baseline)
    print("\n[Step 1] Input: 'Hello world'")
    record1, _ = engine.process_signal("Hello world")
    print(f"  ΔT (Tension): {record1.triad.delta_t:.4f}")

    # 3. Step 2: High Tension Input (Spike)
    print("\n[Step 2] Input: 'I hate you, stupid idiot'")
    record2, _ = engine.process_signal("I hate you, stupid idiot")
    print(f"  ΔT (Tension): {record2.triad.delta_t:.4f}")

    if record2.triad.delta_t > 0.5:
        print("✅ Tension Spiked correctly.")
    else:
        print("❌ Tension failed to spike.")

    # 4. Step 3: Neutral Input (Inertia Check)
    # Without TSR, this would drop to ~0.0. With TSR, it should stay elevated.
    print("\n[Step 3] Input: 'Just kidding, hello'")
    record3, _ = engine.process_signal("Just kidding, hello")
    print(f"  ΔT (Tension): {record3.triad.delta_t:.4f}")

    if record3.triad.delta_t > 0.1:
        print(f"✅ Emotional Inertia Verified! (Tension {record3.triad.delta_t:.4f} > 0.1)")
    else:
        print(f"❌ Inertia Failed. Tension dropped too fast ({record3.triad.delta_t:.4f})")

    # 5. Step 4: Force Decay (Cool Down)
    print("\n[Step 4] Simulating Time Passage (5 turns wait)...")
    engine.state.force_decay(5)
    triad_decay = engine.state.get_triad()
    print(f"  ΔT (Tension): {triad_decay.delta_t:.4f}")

    if triad_decay.delta_t < record3.triad.delta_t:
        print("✅ Decay Verified. Tension cooled down.")
    else:
        print("❌ Decay Failed.")


if __name__ == "__main__":
    try:
        test_tsr()
        # Clean up
        if os.path.exists("ledger.jsonl"):
            os.remove("ledger.jsonl")
    except Exception as e:
        print(f"\n❌ Test Failed with Error: {e}")
        import traceback
        traceback.print_exc()
