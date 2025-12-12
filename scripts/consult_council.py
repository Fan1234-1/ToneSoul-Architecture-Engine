import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from body.spine_system import SpineEngine

def consult():
    print("Initializing ToneSoul...")
    engine = SpineEngine(accuracy_mode="off")
    
    question = "/council ToneSoul, how do you feel? Should we prioritize MMF (Vision) or ES (Evolution) next?"
    print(f"\nUser: {question}")
    
    # We need to manually start the heart to ensure systems are active, though for a single call it might not matter much
    # But let's be consistent
    engine.heart.start()
    try:
        record, mod, thought = engine.process_signal(question)
        
        print("\n--- ToneSoul Response ---")
        print(f"Decision: {record.decision['mode']}")
        print(f"Thought:\n{thought.reasoning}")
    finally:
        engine.heart.stop()

if __name__ == "__main__":
    consult()
