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
from core.quantum.drift import IdentityCrisis


class TestKillSwitch(unittest.TestCase):
    def setUp(self):
        self.engine = SpineEngine(accuracy_mode="off")
        # Mock internal components to avoid side effects
        self.engine.ledger = MagicMock()
        self.engine.internal_sense = MagicMock()
        self.engine.quantum_kernel = MagicMock()
        self.engine.drift_monitor = MagicMock()

    def test_monomania_detection(self):
        """Test that 10 identical choices trigger monomania."""
        # Setup history with 10 'Rational' paths
        path = ThoughtPath("Rational", 0.0, 0.0, 0.0)
        self.engine.quantum_kernel.history = [path] * 10

        # Check
        is_manic = self.engine._check_monomania()
        self.assertTrue(is_manic, "Should detect monomania")

        # Setup mixed history
        self.engine.quantum_kernel.history = [path] * 9 + [ThoughtPath("Creative", 0.0, 0.0, 0.0)]
        is_manic = self.engine._check_monomania()
        self.assertFalse(is_manic, "Should not detect monomania with mixed history")

    def test_hard_reset_execution(self):
        """Test that _perform_hard_reset clears history and logs event."""
        self.engine._perform_hard_reset("Test Reason")

        # Verify history clear
        self.assertEqual(self.engine.quantum_kernel.history, [])
        self.assertEqual(self.engine.quantum_kernel.plasticity_map, {})

        # Verify ledger log
        self.engine.ledger.append.assert_called_once()
        args, kwargs = self.engine.ledger.append.call_args
        self.assertEqual(kwargs['decision']['mode'], "KILL_SWITCH")
        self.assertEqual(kwargs['decision']['reason'], "Test Reason")

    def test_tsr_drift_trigger(self):
        """Test that TSR drift raises exception and triggers reset."""
        # We need to test process_signal flow, but mocking is complex.
        # Instead, we verify that drift_monitor.check_tsr_drift is called.
        # And if it raises, _perform_hard_reset is called.

        # Mock drift monitor to raise IdentityCrisis
        self.engine.drift_monitor.check_integrity.return_value = 1.0
        self.engine.drift_monitor.check_tsr_drift.side_effect = IdentityCrisis("Meltdown")

        # Mock other components for process_signal
        self.engine.sensor.estimate_triad = MagicMock(return_value=MagicMock(delta_t=0.0, delta_s=0.0, delta_r=0.0, risk_score=0.0))
        self.engine.internal_sense.map_to_triad = MagicMock(return_value={})

        # Run process_signal
        # We expect it to catch the exception and return a system record
        record, mod, thought = self.engine.process_signal("test")

        # Verify reset was called
        # Since _perform_hard_reset clears history, we can check if ledger was called with KILL_SWITCH
        # But _perform_hard_reset calls ledger.append.
        # And process_signal calls _create_system_record which calls ledger.append.
        # So ledger.append should be called twice.
        self.assertEqual(self.engine.ledger.append.call_count, 2)

        # Check first call (Reset)
        call1 = self.engine.ledger.append.call_args_list[0]
        self.assertEqual(call1.kwargs['decision']['mode'], "KILL_SWITCH")
        self.assertIn("Meltdown", call1.kwargs['decision']['reason'])


if __name__ == "__main__":
    unittest.main()
