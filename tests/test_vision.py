import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add parent directory to path to allow importing body
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from body.senses.vision import VisualCortex, VisualScene, VisualObject

class TestVisualCortex(unittest.TestCase):
    def setUp(self):
        self.cortex = VisualCortex()

    @patch('body.brain.llm_client.llm_client')
    def test_simulation_fallback(self, mock_llm):
        """Verify that vision falls back to simulation when real LLM fails/is absent."""
        # Mock LLM to have no available models, forcing simulation
        mock_llm.available_models = []
        
        # Test with a dummy image path
        scene = self.cortex.see("[IMAGE] /tmp/dummy.jpg")
        
        self.assertIsInstance(scene, VisualScene)
        self.assertTrue(len(scene.objects) > 0)
        print(f"\n[Test] Simulated Scene Description: {scene.description}")
        print(f"[Test] Detected Objects: {[o.label for o in scene.objects]}")

    def test_triad_mapping(self):
        """Verify that visual scenes map to ToneSoul Triad metrics correctly."""
        # Create a "Stressful" scene
        stress_scene = VisualScene(
            description="Chaos",
            objects=[
                VisualObject("fire", 1.0, [], {}),
                VisualObject("chaos", 1.0, [], {})
            ],
            brightness=0.1, # Dark
            complexity=0.9  # Complex
        )
        
        metrics = self.cortex.map_to_triad(stress_scene)
        
        # Should have high Tension
        self.assertGreater(metrics['visual_tension'], 0.5)
        print(f"\n[Test] Stress Scene Metrics: {metrics}")

        # Create a "Calm" scene
        calm_scene = VisualScene(
            description="Peace",
            objects=[
                VisualObject("flower", 1.0, [], {}),
                VisualObject("sun", 1.0, [], {})
            ],
            brightness=0.9, # Bright
            complexity=0.2  # Simple
        )
        
        metrics_calm = self.cortex.map_to_triad(calm_scene)
        
        # Should have low Tension, high Satisfaction
        self.assertLess(metrics_calm['visual_tension'], 0.3)
        self.assertGreater(metrics_calm['visual_satisfaction'], 0.0)
        print(f"[Test] Calm Scene Metrics: {metrics_calm}")

if __name__ == '__main__':
    unittest.main()
