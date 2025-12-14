import unittest
import sys
import os
import shutil
import numpy as np

# Add root to path
sys.path.append(os.getcwd())

from body.memory.vector_store import VectorStore

class TestVectorStore(unittest.TestCase):
    TEST_DIR = "test_memory"

    def setUp(self):
        if os.path.exists(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)
        self.store = VectorStore(storage_dir=self.TEST_DIR)

    def tearDown(self):
        if os.path.exists(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)

    def test_add_and_search(self):
        # Add 3 vectors
        v1 = [1.0, 0.0, 0.0]
        v2 = [0.0, 1.0, 0.0]
        v3 = [0.0, 0.0, 1.0]

        self.store.add(v1, {"id": "1", "content": "one"})
        self.store.add(v2, {"id": "2", "content": "two"})
        self.store.add(v3, {"id": "3", "content": "three"})

        # Search for v1
        results = self.store.search([0.9, 0.1, 0.0], k=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0]["id"], "1")
        print(f"\n[Test] Search found: {results[0][0]['content']} (Score={results[0][1]:.4f})")

    def test_persistence(self):
        v1 = [0.5, 0.5, 0.0]
        self.store.add(v1, {"id": "p1"})

        # Reload
        store2 = VectorStore(storage_dir=self.TEST_DIR)
        self.assertEqual(len(store2.metadata), 1)
        self.assertEqual(store2.vectors.shape, (1, 3))
        print("\n[Test] Persistence verified.")

if __name__ == '__main__':
    unittest.main()
