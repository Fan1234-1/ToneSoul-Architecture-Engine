"""
Test Thinking Operators
-----------------------
Verifies the functionality of individual operators and the pipeline.
"""

import unittest
from core.thinking.base import OperatorContext
from core.thinking.pipeline import ThinkingPipeline

class TestThinkingSystem(unittest.TestCase):
    def setUp(self):
        self.pipeline = ThinkingPipeline()
        self.context = OperatorContext(
            input_text="Design a safe AI system.",
            system_metrics={"delta_t": 0.1, "delta_s": 0.8, "delta_r": 0.2},
            history=[]
        )

    def test_p2_pipeline(self):
        """Test Standard Pipeline (Abstract -> Ground)"""
        result = self.pipeline.execute_pipeline(self.context, p_level="P2")
        trace = result["pipeline_trace"]
        
        self.assertIn("OP_ABSTRACT", trace)
        self.assertIn("OP_GROUND", trace)
        self.assertNotIn("OP_REVERSE", trace) # P2 shouldn't reverse
        
        print(f"\nP2 Trace: {trace}")

    def test_p0_pipeline(self):
        """Test Critical Pipeline (Full Loop)"""
        result = self.pipeline.execute_pipeline(self.context, p_level="P0")
        trace = result["pipeline_trace"]
        
        self.assertIn("OP_ABSTRACT", trace)
        self.assertIn("OP_FORK", trace)
        self.assertIn("OP_REVERSE", trace)
        self.assertIn("OP_GROUND", trace)
        
        print(f"\nP0 Trace: {trace}")
        
        # Check Fork logic (Entropy 0.8 -> ~4 forks)
        fork_res = result["results"]["fork"]
        self.assertTrue(len(fork_res["variations"]) >= 3)

if __name__ == "__main__":
    unittest.main()
