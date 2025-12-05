import sys
import os
import time

# Force UTF-8
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from body.senses.vision import VisualCortex

def test_vision():
    print("👁️ Testing VisualCortex Isolation...")
    
    vision = VisualCortex()
    image_path = "morning_sunlight_and_coffee.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return

    print(f"📸 Input: {image_path}")
    
    # Test see()
    start_time = time.time()
    scene = vision.see(f"[IMAGE] {image_path}")
    duration = time.time() - start_time
    
    print(f"\n⏱️ Processing Time: {duration:.2f}s")
    print("\n--- Visual Scene ---")
    print(f"Description: {scene.description[:200]}...")
    print(f"Brightness: {scene.brightness}")
    print(f"Complexity: {scene.complexity}")
    print(f"Objects: {[o.label for o in scene.objects]}")
    
    # Test map_to_triad()
    triad = vision.map_to_triad(scene)
    print("\n--- Triad Mapping ---")
    print(f"Tension (Delta T): {triad['visual_tension']:.2f}")
    print(f"Satisfaction (Delta S): {triad['visual_satisfaction']:.2f}")
    print(f"Reality (Delta R): {triad['visual_reality']:.2f}")

if __name__ == "__main__":
    test_vision()
