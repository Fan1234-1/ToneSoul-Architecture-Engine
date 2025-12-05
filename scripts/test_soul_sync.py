import sys
import os
import time

# Add parent dir to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from body.vital_organs.soul_sync import SoulSync

def test_soul_sync():
    print("Testing SoulSync (Soul Vessel Backup)...")
    
    # Ensure dummy memory exists for test
    if not os.path.exists("core_memory.json"):
        with open("core_memory.json", "w") as f:
            f.write('[{"test": "memory"}]')
            
    syncer = SoulSync()
    
    print("\n--- Triggering Sync ---")
    syncer.sync()
    
    print("\n--- Test Complete ---")
    print("Check 'memory_vault/' directory and remote repo.")

if __name__ == "__main__":
    test_soul_sync()
