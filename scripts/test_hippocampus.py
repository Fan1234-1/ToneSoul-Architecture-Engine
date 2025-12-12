import sys
import os
import time
import shutil

# Add parent dir to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from body.spine_system import SpineEngine
from body.safety import ActionPlan

def test_hippocampus():
    print("Testing Hippocampus (Conscious Ingestion)...")
    
    # Clear previous memory and ledger for clean test
    # [YuHun Safety Migration]
    ActionPlan.delete_file("core_memory.json", "Test Cleanup", force=True)
    ActionPlan.delete_file("ledger.jsonl", "Test Cleanup", force=True)
        
    engine = SpineEngine(accuracy_mode="off")
    
    # 1. Ingest Fact
    print("\n--- Step 1: Ingesting Fact ---")
    input_text = "My name is Neo and I am the One."
    print(f"User Input: {input_text}")
    engine.process_signal(input_text)
    
    # 2. Trigger Consolidation (Simulate Heartbeat)
    print("\n--- Step 2: Consolidating Memory ---")
    # Manually trigger consolidation for test speed
    # We need to ensure the ledger has the record available
    engine.heart._consolidate_memory()
    
    # Verify memory file exists
    if os.path.exists("core_memory.json"):
        print("✅ core_memory.json created.")
        with open("core_memory.json", 'r') as f:
            print(f"Memory Content: {f.read()}")
    else:
        print("❌ core_memory.json NOT created.")
        
    # 3. Recall Fact
    print("\n--- Step 3: Recalling Fact ---")
    query = "What is my name?"
    print(f"User Query: {query}")
    
    # Debug: Call recall directly
    print("--- Debug: Direct Recall ---")
    direct_memories = engine.hippocampus.recall(query)
    print(f"Direct Recall Count: {len(direct_memories)}")
    for m in direct_memories:
        print(f"  - {m.content}")

    # We expect the engine to print the recalled fact during process_signal
    record, mod, thought = engine.process_signal(query)
    
    print("\n--- Result ---")
    print(f"Thought Trace:\n{thought.reasoning}")

if __name__ == "__main__":
    test_hippocampus()
