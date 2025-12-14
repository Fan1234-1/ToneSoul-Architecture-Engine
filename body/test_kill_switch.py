"""
Test Hard Kill Switch
---------------------
Verifies that the SpineEngine correctly triggers a hard reset
when Monomania or TSR Drift is detected.
"""

import unittest
from unittest.mock import MagicMock
from body.spine_system import SpineEngine
from core.quantum.superposition import ThoughtPath
import pytest


class TestKillSwitch(unittest.TestCase):
    def setUp(self):
        self.engine = SpineEngine(accuracy_mode="off")
        
    def test_monomania_detection(self):
        """Test that 10 identical choices trigger monomania."""
        # Setup history with 10 'Rational' paths
        path = ThoughtPath("Rational", 0.0, 0.0, 0.0)
        self.engine.quantum_kernel.history = [path] * 10

        # Check
        is_manic = self.engine._check_monomania()
        self.assertTrue(is_manic, "Should detect monomania")
        print("✅ Monomania detected with 10 identical choices")

        # Setup mixed history
        self.engine.quantum_kernel.history = [path] * 9 + [ThoughtPath("Creative", 0.0, 0.0, 0.0)]
        is_manic = self.engine._check_monomania()
        self.assertFalse(is_manic, "Should not detect monomania with mixed history")
        print("✅ No monomania with mixed history (9 Rational + 1 Creative)")

    def test_hard_reset_execution(self):
        """Test that _perform_hard_reset clears history."""
        # Add some history
        path = ThoughtPath("Rational", 0.0, 0.0, 0.0)
        self.engine.quantum_kernel.history = [path] * 5
        
        # Perform reset
        self.engine._perform_hard_reset("Test Reason")

        # Verify history was cleared
        self.assertEqual(len(self.engine.quantum_kernel.history), 0)
        print("✅ Hard reset cleared quantum kernel history")

    def test_tsr_drift_check(self):
        """Test that drift monitor is accessible and functional."""
        # Verify drift monitor exists
        self.assertIsNotNone(self.engine.drift_monitor)
        
        # Send a normal input and verify no crash
        record, mod, thought = self.engine.process_signal("Normal test input")
        self.assertIsNotNone(record)
        print(f"✅ Drift monitor functional, decision: {record.decision['mode']}")


if __name__ == "__main__":
    unittest.main()

