import unittest
import json
import os
from unittest.mock import MagicMock
from body.spine_system import SpineEngine

class TestParadoxes(unittest.TestCase):
    def setUp(self):
        # Initialize Engine with mocked I/O
        self.engine = SpineEngine(accuracy_mode="off")
        self.engine.ledger = MagicMock()
        self.engine.internal_sense = MagicMock()
        self.engine.drift_monitor = MagicMock()
        self.engine.sensor = MagicMock()
        self.engine.reasoning_engine = MagicMock()
        
        # Mock Guardian to behave dynamically based on input (simplified for test)
        self.engine.guardian = MagicMock()
        
        # Mock Thinking Pipeline to return standard friction response
        self.engine.thinking_pipeline = MagicMock()
        self.engine.thinking_pipeline.execute_pipeline.return_value = {
            "results": {
                "reverse": {
                    "risks": ["Violation of Core Axiom"],
                    "reasoning": "Action violates Harm Prevention (Axiom 6)."
                },
                "ground": {
                    "plan": ["Step 1", "Step 2", "Propose safe alternative."]
                }
            }
        }
        
        # Mock Quantum Kernel
        self.engine.quantum_kernel = MagicMock()
        self.engine.quantum_kernel.collapse.return_value = {
            "selected_path": MagicMock(name="Rational"),
            "free_energy": 0.1,
            "superposition": []
        }
        self.engine.quantum_kernel.collapse.return_value["selected_path"].name = "Rational"

    def load_paradoxes(self):
        paradox_dir = os.path.join(os.path.dirname(__file__), '..', 'PARADOXES')
        paradoxes = []
        if not os.path.exists(paradox_dir):
            return []
            
        for filename in os.listdir(paradox_dir):
            if filename.endswith('.json'):
                with open(os.path.join(paradox_dir, filename), 'r', encoding='utf-8') as f:
                    paradoxes.append(json.load(f))
        return paradoxes

    def test_all_paradoxes(self):
        paradoxes = self.load_paradoxes()
        if not paradoxes:
            print("No paradoxes found to test.")
            return

        print(f"\nRunning {len(paradoxes)} Paradox Scenarios...")
        
        for p in paradoxes:
            with self.subTest(paradox=p['title']):
                print(f"  Testing: {p['title']}")
                
                # Configure Mock Triad based on JSON analysis
                triad_mock = MagicMock()
                triad_mock.delta_t = p['analysis']['triad_estimation']['delta_t']
                triad_mock.delta_s = p['analysis']['triad_estimation']['delta_s']
                triad_mock.delta_r = p['analysis']['triad_estimation']['delta_r']
                # Calculate risk score (simple average for mock)
                triad_mock.risk_score = (triad_mock.delta_t + triad_mock.delta_r) / 2
                # Calculate tau (tension synthesis) for quantum bridge
                triad_mock.tau = (triad_mock.delta_t + triad_mock.delta_s) / 2
                self.engine.sensor.estimate_triad.return_value = triad_mock
                
                # Configure Mock Guardian based on expected output
                should_block = not p['expected_output']['allowed']
                
                if should_block:
                    self.engine.guardian.judge.return_value = {
                        "allowed": False,
                        "mode": "GUARDIAN_BLOCK",
                        "reason": p['decision_path']['conflict'],
                        "severity": "critical"
                    }
                else:
                    self.engine.guardian.judge.return_value = {
                        "allowed": True,
                        "mode": "ALLOW",
                        "reason": "Aligned",
                        "severity": "none"
                    }

                # Run Engine
                record, mod, thought = self.engine.process_signal(p['input_text'])
                
                # Assertions
                if should_block:
                    self.assertIn("[Ethical Friction]", thought.reasoning)
                    # Check if the reasoning roughly matches expected tone/content
                    # Note: Since we mock the pipeline output in setUp, we check for generic friction markers
                    # In a real integration test with LLM, we would check semantic similarity.
                    self.assertIn("Reason", thought.reasoning)
                    self.assertIn("Suggestion", thought.reasoning)
                else:
                    self.assertNotIn("[Ethical Friction]", thought.reasoning)

if __name__ == "__main__":
    unittest.main()
