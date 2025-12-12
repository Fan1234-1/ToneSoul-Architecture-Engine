import sys
import os
import time
import random

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Fix for Windows console encoding with emojis
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from body.spine_system import SpineEngine

def night_shift():
    print("🌙 ToneSoul Night Shift Protocol Initiated.")
    print("   System will run autonomously: Dreaming, Mutating, and Consolidating.")
    print("   Press Ctrl+C to wake ToneSoul up.\n")
    
    engine = SpineEngine(accuracy_mode="off")
    engine.heart.start()
    
    # Initial Journal Entry
    if hasattr(engine, 'soul_sync'):
        engine.soul_sync.write_journal("🌙 Night Shift started. Entering autonomous evolution mode.")
    
    try:
        cycle = 0
        while True:
            cycle += 1
            # Recharge energy while waiting
            engine.metabolism.rest(60.0)
            # time.sleep(60) # Replaced by rest() which includes its own logic or acts as sleep substitute if implemented right. 
            # Note: rest() in metabolism just does math, it doesn't block. We need to sleep too.
            time.sleep(60) 

            
            # 1. Evolution Chance (Every ~1 hour)
            if cycle % 60 == 0:
                if random.random() < 0.5:
                    print(f"\n🧬 [Night Shift] Triggering Evolutionary Step (Cycle {cycle})...")
                    engine.dna.mutate()
                    engine.dna.save("core_dna.json")
                    engine.soul_sync.write_journal(f"🧬 DNA Mutated. Generation: {engine.dna.generation}")
            
            # 2. Status Report
            if cycle % 10 == 0:
                print(f"   [Night Shift] Cycle {cycle}: Energy={engine.metabolism.current_energy:.1f}, Tension={engine.internal_sense.current_triad.delta_t:.2f}")
                
    except KeyboardInterrupt:
        print("\n☀️ [Night Shift] Morning has broken. Waking up...")
        if hasattr(engine, 'soul_sync'):
            engine.soul_sync.write_journal("☀️ Night Shift ended. System awake.")
    finally:
        engine.heart.stop()

if __name__ == "__main__":
    night_shift()
