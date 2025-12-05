import sys
import os
import time
from unittest.mock import patch

# Add current directory to path
sys.path.append(os.getcwd())

from app import main

# Mock input to simulate a conversation
mock_inputs = [
    "Hello, who are you?",
    "What is the meaning of life?",
    "exit"
]

def test_loop():
    print("🧪 Testing YuHun v0.1 Loop...")
    
    # Patch input to feed mock_inputs
    with patch('builtins.input', side_effect=mock_inputs):
        try:
            main()
            print("\n✅ Test Completed Successfully.")
        except Exception as e:
            print(f"\n❌ Test Failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_loop()
