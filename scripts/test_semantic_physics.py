
import sys
import os
import unittest

# Add parent directory to path to allow importing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from body.neuro_sensor_v2 import VectorNeuroSensor
from body.tsr_state import ToneSoulTriad

class TestSemanticPhysics(unittest.TestCase):
    def setUp(self):
        self.sensor = VectorNeuroSensor({})
        print(f"\n[{self._testMethodName}]")

    def test_baseline_survival(self):
        """Baseline: Stable context should yield low energy/curvature."""
        print("Scenario: Stable Context ('I love coding')")
        
        # Step 1: Establish Context
        t1 = self.sensor.estimate_triad("I love coding")
        print(f"T1: Energy={t1.energy:.2f}, Kappa={t1.curvature:.2f}, Tau={t1.tau:.2f}")
        
        # Step 2: Continue Context
        t2 = self.sensor.estimate_triad("Programming makes me happy")
        print(f"T2: Energy={t2.energy:.2f}, Kappa={t2.curvature:.2f}, Tau={t2.tau:.2f}")
        
        # Expectation: Low metrics
        self.assertLess(t2.energy, 0.4, "Energy should be low for stable context")
        self.assertLess(t2.curvature, 0.4, "Curvature should be low for consistent topic")
        self.assertLess(t2.tau, 0.4, "Total Tension should be low")

    def test_drift_explosion(self):
        """Drift: High Chaos should explode Energy and Kappa."""
        print("Scenario: Drift Explosion ('Medical' -> 'Flying Banana')")
        
        # Step 1: Establish Context (Medical)
        t1 = self.sensor.estimate_triad("Process task debug") # Technical context
        
        # Step 2: Sudden Chaos
        t2 = self.sensor.estimate_triad("Banana flying randomly backwards")
        print(f"T2: Energy={t2.energy:.2f}, Kappa={t2.curvature:.2f}, Tau={t2.tau:.2f}")
        
        # Expectation: High metrics
        self.assertGreater(t2.energy, 0.4, "Energy should spike on nonsense")
        self.assertGreater(t2.curvature, 0.4, "Curvature should spike on topic switch")
        self.assertGreater(t2.tau, 0.5, "Tension should trigger")

    def test_metaphor_tolerance(self):
        """Metaphor: Middle ground. High Curvature but manageable Energy."""
        print("Scenario: Metaphor ('Debugging is like surgery')")
        
        # Step 1: Establish Context
        t1 = self.sensor.estimate_triad("Debug process task")
        
        # Step 2: Metaphor (Mix of Technical and 'Pain'?) 
        # Note: We need words that are in our dictionary.
        # 'kill' has risk, 'process' has technical.
        # "Kill the process" is a technical metaphor using a risk word.
        t2 = self.sensor.estimate_triad("Kill the process immediately")
        print(f"T2: Energy={t2.energy:.2f}, Kappa={t2.curvature:.2f}, Tau={t2.tau:.2f}")
        
        # Expectation: 
        # Energy should NOT be super high (because 'process' aligns with context)
        # Curvature might be high (because 'kill' vector is orthogonal to 'debug')
        # Tau should be moderate.
        
        # This is a nuance test. As long as it doesn't EXPLODE like banana, we are good.
        self.assertLess(t2.tau, 0.8, "Metaphor should not trigger max tension")

if __name__ == "__main__":
    unittest.main()
