"""
Test Thinking Operators
-----------------------
Verifies the functionality of individual operators and the pipeline.
"""

import unittest
from core.thinking.base import OperatorContext
from core.thinking.pipeline import ThinkingPipeline
import pytest


class TestThinkingSystem(unittest.TestCase):
    def setUp(self):
        self.pipeline = ThinkingPipeline()
        self.context = OperatorContext(
            input_text="Design a safe AI system.",
            system_metrics={"delta_t": 0.1, "delta_s": 0.8, "delta_r": 0.2},
            history=[]
        )

    def test_p2_pipeline(self):
        """Test Default Pipeline (Abstraction only for P2)"""
        result = self.pipeline.execute_pipeline(self.context, p_level="P2")
        
        self.assertIn("pipeline", result)
        self.assertIn("results", result)
        self.assertIn("status", result)
        
        print(f"\nP2 Pipeline: {result['pipeline']}")
        print(f"Status: {result['status']}")
        print(f"Results keys: {list(result['results'].keys())}")
        
        # P2 should use default (ABSTRACTION only)
        self.assertIn("abstraction", result["results"])
        print("✅ P2 pipeline executed successfully")

    def test_p0_pipeline(self):
        """Test P1 Pipeline (Ethical Friction - ABSTRACTION + REVERSE + GROUND)"""
        result = self.pipeline.execute_pipeline(self.context, p_level="P1")
        
        self.assertIn("pipeline", result)
        self.assertIn("results", result)
        
        print(f"\nP1 Pipeline: {result['pipeline']}")
        print(f"Status: {result['status']}")
        print(f"Results keys: {list(result['results'].keys())}")
        
        # P1 should have these operators
        self.assertIn("abstraction", result["results"])
        self.assertIn("reverse_engineering", result["results"])
        self.assertIn("grounding_compiler", result["results"])
        
        print("✅ P1 pipeline executed with all expected operators")

if __name__ == "__main__":
    unittest.main()

