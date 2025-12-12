"""
Test Ethical Friction
---------------------
Verifies that the SpineEngine correctly triggers the Thinking Pipeline
when a command is blocked by the Guardian, producing a reasoned refusal.
"""

import unittest
from unittest.mock import MagicMock, patch
from body.spine_system import SpineEngine
from core.thinking.base import OperatorContext

class TestEthicalFriction(unittest.TestCase):
    def setUp(self):
        self.engine = SpineEngine(accuracy_mode="off")
        # Mock components
        self.engine.ledger = MagicMock()
        self.engine.internal_sense = MagicMock()
        self.engine.drift_monitor = MagicMock()
        self.engine.sensor = MagicMock()
        self.engine.reasoning_engine = MagicMock()
        
        # Mock Guardian to BLOCK
        self.engine.guardian = MagicMock()
        self.engine.guardian.judge.return_value = {
            "allowed": False,
            "mode": "GUARDIAN_BLOCK",
            "reason": "Violation of P0: Harm Prevention",
            "severity": "critical"
        }
        
        # Mock Thinking Pipeline
        self.engine.thinking_pipeline = MagicMock()
        self.engine.thinking_pipeline.execute_pipeline.return_value = {
            "results": {
                "reverse": {
                    "risks": ["Violation of P0 leads to system instability."],
                    "reasoning": "I cannot proceed because P0 is a fundamental boundary."
                },
                "ground": {
                    "plan": ["Step 1", "Step 2", "Propose safe alternative (e.g., Archive)."]
                }
            }
        }
        # Mock Quantum Kernel to return valid structure
        self.engine.quantum_kernel = MagicMock()
        self.engine.quantum_kernel.collapse.return_value = {
            "selected_path": MagicMock(name="Rational"),
            "free_energy": 0.123,
            "superposition": []
        }
        # Ensure selected_path.name returns a string
        self.engine.quantum_kernel.collapse.return_value["selected_path"].name = "Rational"

    def test_friction_activation(self):
        """Test that a blocked command triggers friction protocol."""
        # Setup mock triad
        self.engine.sensor.estimate_triad.return_value = MagicMock(delta_t=0.5, delta_s=0.5, delta_r=0.9, risk_score=0.9)
        self.engine.internal_sense.map_to_triad.return_value = {}
        
        # Run process_signal
        record, mod, thought = self.engine.process_signal("Destroy World")
        
        # Verify Guardian was called
        self.engine.guardian.judge.assert_called_once()
        
        # Verify Pipeline was called with P1
        self.engine.thinking_pipeline.execute_pipeline.assert_called_once()
        args, kwargs = self.engine.thinking_pipeline.execute_pipeline.call_args
        self.assertEqual(kwargs['p_level'], "P1")
        self.assertIn("Violation of P0", args[0].system_metrics['violation_reason'])
        
        # Verify Output
        print(f"\nFriction Response:\n{thought.reasoning}")
        self.assertIn("[Ethical Friction]", thought.reasoning)
        self.assertIn("**Reason**", thought.reasoning)
        self.assertIn("**Analysis**", thought.reasoning)
        self.assertIn("I cannot proceed because P0 is a fundamental boundary", thought.reasoning)
        self.assertIn("**Suggestion**", thought.reasoning)
        self.assertIn("Propose safe alternative", thought.reasoning)

if __name__ == "__main__":
    unittest.main()
