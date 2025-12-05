import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from body.spine_system import SpineEngine

def test_evolution():
    print("🧬 Testing ToneSoul Evolution (MMF + ES + SoulSync)...")
    
    engine = SpineEngine(accuracy_mode="off")
    
    # 1. Test Vision (MMF)
    print("\n--- Testing Vision ---")
    img_input = "[IMAGE] world.jpg"
    record, mod, thought = engine.process_signal(img_input)
    print(f"Vision Response: {record.user_input}")
    if "Visual Context" in record.user_input:
        print("✅ Vision Processing Successful.")
    else:
        print("❌ Vision Processing Failed.")

    # 2. Test Evolution (ES)
    print("\n--- Testing DNA Mutation ---")
    old_curiosity = engine.dna.genes.curiosity
    engine.dna.mutate()
    new_curiosity = engine.dna.genes.curiosity
    print(f"Curiosity: {old_curiosity:.2f} -> {new_curiosity:.2f}")
    if old_curiosity != new_curiosity:
        print("✅ Mutation Successful.")
        engine.dna.save("core_dna.json")
    else:
        print("⚠️ Mutation had no effect (could be random chance, but unlikely).")

    # 3. Test Dream Journaling
    print("\n--- Testing Dream Journal ---")
    # Force a dream
    engine.heart._dream(force=True)
    
    # Force a backup
    print("\n--- Triggering Backup ---")
    engine.heart._backup_soul()
    
    # Verify Journal
    journal_path = os.path.join("memory_vault", "journal.md")
    if os.path.exists(journal_path):
        with open(journal_path, "r") as f:
            content = f.read()
            print(f"Journal Content Preview:\n{content[-200:]}")
        print("✅ Journal written.")
    else:
        print("❌ Journal file not found.")

if __name__ == "__main__":
    test_evolution()
