import sys
import os
import time

# Add parent dir to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from body.spine_system import SpineEngine

def test_heartbeat():
    print("Testing Heartbeat in SpineEngine...")
    engine = SpineEngine(accuracy_mode="off")
    
    # Manually set dream latency to 1s for testing
    engine.heart.DREAM_LATENCY = 1.0
    
    print("Starting Heartbeat...")
    engine.heart.start()
    
    print("Waiting for dreams (5 seconds)...")
    time.sleep(5)
    
    print("Stopping Heartbeat...")
    engine.heart.stop()
    
    print("Test Complete.")

if __name__ == "__main__":
    test_heartbeat()
