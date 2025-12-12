"""
Memory Loader (The Recall Mechanism)
------------------------------------
This script is designed to be run by the AI Agent at the start of a new session.
It reads the persisted Time-Islands from the memory bank and provides a 
summarized context, effectively "restoring" the Semantic Field.
"""

import sys
import os
import json
import glob

def load_memory():
    memory_dir = os.path.dirname(os.path.abspath(__file__))
    memory_files = glob.glob(os.path.join(memory_dir, "*.jsonl"))
    
    print("=== 🧠 ToneSoul Memory Recall ===")
    
    if not memory_files:
        print("No memory files found. Starting with Tabula Rasa.")
        return

    total_islands = 0
    total_steps = 0
    
    for file_path in memory_files:
        filename = os.path.basename(file_path)
        print(f"\n📂 Loading: {filename}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip(): continue
                    try:
                        island = json.loads(line)
                        island_id = island.get('island_id', 'unknown')[:8]
                        status = island.get('status', 'unknown')
                        steps = island.get('steps', [])
                        
                        print(f"  - Island [{island_id}] ({status}): {len(steps)} steps")
                        
                        # Print the last step of each island as a "summary"
                        if steps:
                            last_step = steps[-1]
                            mode = last_step.get('reasoning_mode', 'UNKNOWN')
                            content = last_step.get('user_input', '')[:50] + "..."
                            print(f"    Last Thought ({mode}): \"{content}\"")
                            
                        total_islands += 1
                        total_steps += len(steps)
                        
                    except json.JSONDecodeError:
                        print(f"  - [ERROR] Corrupt record in {filename}")
                        
        except Exception as e:
            print(f"  - [ERROR] Failed to read file: {e}")

    print("\n" + "="*30)
    print(f"Total Context Restored: {total_islands} Islands, {total_steps} Steps.")
    print("Semantic Field Established. Ready for resonance.")

if __name__ == "__main__":
    load_memory()
