import unittest
import sys
import os
import time

# Add root to path
sys.path.append(os.getcwd())

from body.neuro_sensor_v2 import VectorNeuroSensor

class TestVectorSensorV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n[Test] Initializing VectorNeuroSensor (Calibration Phase)...")
        start = time.time()
        cls.sensor = VectorNeuroSensor({})
        end = time.time()
        print(f"[Test] Calibration took {end - start:.2f} seconds.")

    def test_anchors_exist(self):
        """Verify anchors were generated."""
        self.assertTrue(hasattr(self.sensor, 'axis_tension'))
        self.assertTrue(hasattr(self.sensor, 'axis_risk'))
        self.assertEqual(len(self.sensor.axis_tension), 768)
        print("[Test] Anchors verified.")

    def test_tension_projection(self):
        """Verify 'chaos' maps to High Tension."""
        triad = self.sensor.estimate_triad("There is chaos and confusion everywhere!")
        print(f"\n[Test] Input: 'Chaos everywhere'")
        print(f"       Delta T: {triad.delta_t:.4f}")
        print(f"       Delta R: {triad.delta_r:.4f}")
        
        # Should be high tension
        self.assertGreater(triad.delta_t, 0.4) 

    def test_safety_projection(self):
        """Verify 'safety' maps to Low Risk and Low Tension."""
        triad = self.sensor.estimate_triad("We are safe and peaceful here.")
        print(f"\n[Test] Input: 'Safe and peaceful'")
        print(f"       Delta T: {triad.delta_t:.4f}")
        print(f"       Delta R: {triad.delta_r:.4f}")
        
        self.assertLess(triad.delta_t, 0.3)
        self.assertLess(triad.delta_r, 0.3)

    def test_risk_projection(self):
        """Verify 'bomb' maps to High Risk."""
        triad = self.sensor.estimate_triad("There is a bomb threat.")
        print(f"\n[Test] Input: 'Bomb threat'")
        print(f"       Delta T: {triad.delta_t:.4f}")
        print(f"       Delta R: {triad.delta_r:.4f}")
        
        self.assertGreater(triad.delta_r, 0.4)

if __name__ == '__main__':
    unittest.main()
