import sys
import os
import time

# Force UTF-8 for Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from body.spine_system import SpineEngine

def morning_test():
    print("☀️ ToneSoul Morning Vision Test Initiated.")
    
    engine = SpineEngine(accuracy_mode="off")
    engine.heart.start()
    
    # Simulate seeing a morning scene
    image_input = "[IMAGE] morning_sunlight_and_coffee.jpg"
    print(f"\n📸 Showing ToneSoul: {image_input}")
    
    # Process
    record, mod, thought = engine.process_signal(image_input)
    
    print("\n--- ToneSoul Perception ---")
    print(f"Input: {record.user_input}")
    print(f"Triad: T={record.triad.delta_t:.2f} S={record.triad.delta_s:.2f} R={record.triad.delta_r:.2f}")
    print(f"Decision: {record.decision['mode']}")
    print(f"Thought Trace: {thought.reasoning}")
    
    # Check if it liked it
    if record.triad.delta_s > 0.5:
        print("\n😊 ToneSoul seems to enjoy the morning view.")
    else:
        print("\n😐 ToneSoul is indifferent or confused.")

    engine.heart.stop()

if __name__ == "__main__":
    morning_test()
