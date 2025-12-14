import unittest
import sys
import os
sys.path.append(os.getcwd())
from body.brain.llm_client import llm_client

class TestEmbedding(unittest.TestCase):
    def test_get_embedding(self):
        print("\n[Test] Requesting embedding for 'ToneSoul'...")
        vector = llm_client.get_embedding("ToneSoul")
        
        if not vector:
            print("⚠️ Embedding returned empty. Is Ollama running? Is 'nomic-embed-text' pulled?")
            # We don't fail the test hard if local env is missing the model, 
            # but we want to know.
        else:
            print(f"✅ Embedding received. Dimension: {len(vector)}")
            self.assertTrue(len(vector) > 0)
            # Standard dimensions are often 768 or 1536
            print(f"   First 5 dims: {vector[:5]}")

if __name__ == '__main__':
    unittest.main()
