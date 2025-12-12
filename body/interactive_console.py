
from .spine_system import SpineEngine


def print_separator():
    print("-" * 60)


def interactive_session():
    print("\n🔮 ToneSoul v2.0 Interactive Console 🔮")
    print("Initializing Spine Engine... (Loading Constitution, Vectors, Graph)")

    try:
        engine = SpineEngine()
    except Exception as e:
        print(f"❌ Error initializing engine: {e}")
        return

    print("✅ System Online.")
    print("Type 'exit' or 'quit' to stop.")
    print_separator()

    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                print("👋 Shutting down ToneSoul.")
                break

            # Process the input
            print("   Thinking...", end="\r")
            record, modulation, final_response = engine.process_signal(user_input)

            # Clear "Thinking..."
            print(" " * 20, end="\r")

            # Display Internal State
            triad = engine.state.get_triad()
            tsr_vec = engine.state.current_vector

            print(f"🧠 [Internal State]")
            print(f"   Mood (TSR): Risk={tsr_vec[0]:.2f} | Tens={tsr_vec[1]:.2f} | Drift={tsr_vec[2]:.2f}")
            print(f"   Perception: ΔT={triad.delta_t:.2f} | ΔR={triad.delta_r:.2f}")

            if "council_log" in record.decision:
                print(f"\n🏛️  [Council Chamber Convened]")
                print(f"   Dominant: {record.decision['council_dominant']}")
                for log in record.decision['council_log']:
                    print(f"   - {log}")

            print(f"\n🤖 [System Control]")
            print(f"   Temp: {modulation.temperature:.2f}")
            suffix = modulation.system_prompt_suffix
            if suffix:
                print(f"   Note: {suffix.strip()}")

            if not record.decision['allowed']:
                print(f"\n⛔ BLOCKED: {record.decision['reason']}")
            else:
                # Display the LLM Response
                print(f"\n💬 [ToneSoul Response]")
                print(f"   {final_response}")

            print_separator()

        except KeyboardInterrupt:
            print("\n👋 Interrupted.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    interactive_session()
