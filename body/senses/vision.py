import random
from typing import Dict, Any, List
import os
import json
from dataclasses import dataclass


@dataclass
class VisualObject:
    label: str
    confidence: float
    bounding_box: List[int] # [x, y, w, h]
    attributes: Dict[str, Any]


@dataclass
class VisualScene:
    description: str
    objects: List[VisualObject]
    brightness: float
    complexity: float


class VisualCortex:
    """
    MMF (Multi-Modal Faculty) - Vision Module.
    Responsible for processing visual input and mapping it to the ToneSoul Triad.
    """

    def __init__(self):
        self.active = True
        # In a real implementation, we would load a VLM or connect to an API here.
        # For now, we simulate visual processing or use simple heuristics.

    def see(self, image_source: str) -> VisualScene:
        """
        Processes an image source (path or URL) and returns a scene description.
        Uses Real VLM (llava) for raw vision, then Real LLM (gemma3) for perception/analysis.
        """
        print(f"👁️ [Vision] Processing visual input: {image_source}")

        # Try Real VLM
        try:
            from body.brain.llm_client import llm_client
            if llm_client.available_models:
                # Extract clean path
                clean_path = image_source.replace("[IMAGE] ", "").strip()

                if os.path.exists(clean_path):
                    print(f"   [Vision] Invoking VLM (llava) on {clean_path}...")

                    # Stage 1: Raw Vision (VLM)
                    vision_prompt = "Describe this image in detail. Focus on lighting, objects, and the overall atmosphere."
                    raw_description = llm_client.generate_vision(vision_prompt, clean_path, model="llava")

                    if raw_description.startswith("Error"):
                        raise Exception(raw_description)

                    print(f"   [Vision] Raw Description: {raw_description[:100]}...")

                    # Stage 2: Perception & Analysis (LLM)
                    print(f"   [Vision] Analyzing scene semantics with LLM (gemma3)...")
                    perception = self._perceive_scene(raw_description)

                    return VisualScene(
                        description=raw_description,
                        objects=perception.get("objects", []),
                        brightness=perception.get("brightness", 0.5),
                        complexity=perception.get("complexity", 0.5)
                    )

        except Exception as e:
            print(f"   [Vision] Real AI Perception failed: {e}. Falling back to simulation.")

        # Fallback: Simulation
        seed = sum(ord(c) for c in image_source)
        random.seed(seed)

        brightness = random.random()
        complexity = random.random()

        possible_objects = ["person", "screen", "keyboard", "cat", "window", "code", "chaos"]
        detected = []
        for _ in range(random.randint(1, 5)):
            obj = VisualObject(
                label=random.choice(possible_objects),
                confidence=random.uniform(0.7, 0.99),
                bounding_box=[0,0,100,100],
                attributes={}
            )
            detected.append(obj)

        description = f"A scene containing {', '.join([o.label for o in detected])}. Brightness: {brightness:.2f}"

        return VisualScene(
            description=description,
            objects=detected,
            brightness=brightness,
            complexity=complexity
        )

    def _perceive_scene(self, description: str) -> Dict[str, Any]:
        """
        Uses the LLM to extract structured data and psychological impact from a visual description.
        """
        from body.brain.llm_client import llm_client

        system_prompt = (
            "You are the Visual Cortex Association Area of an AI. "
            "Analyze the provided visual description and extract structured data. "
            "Return ONLY a JSON object with the following fields:\n"
            "- brightness: float (0.0 to 1.0)\n"
            "- complexity: float (0.0 to 1.0)\n"
            "- objects: list of strings (top 5 objects)\n"
        )

        try:
            response = llm_client.generate(description, model="gemma3:4b", system=system_prompt)
            print(f"   [Vision DEBUG] Raw Perception Response: {response}")
            # Clean up response to ensure it's valid JSON
            clean_json = response.replace("```json", "").replace("```", "").strip()
            # Sometimes LLMs add text before/after, try to find the first { and last }
            start = clean_json.find("{")
            end = clean_json.rfind("}")
            if start != -1 and end != -1:
                clean_json = clean_json[start:end+1]

            data = json.loads(clean_json)
            print(f"   [Vision DEBUG] Parsed Perception Data: {data}")

            # Convert string objects to VisualObject instances
            visual_objects = []
            for label in data.get("objects", []):
                visual_objects.append(VisualObject(label=label, confidence=1.0, bounding_box=[], attributes={}))

            data["objects"] = visual_objects
            return data

        except Exception as e:
            print(f"   [Vision] Perception parsing failed: {e}")
            return {
                "brightness": 0.5,
                "complexity": 0.5,
                "objects": []
            }

    def map_to_triad(self, scene: VisualScene) -> Dict[str, float]:
        """
        Maps visual features to ToneSoul Triad metrics (Delta T, S, R).
        """
        print(f"   [Vision DEBUG] Mapping Scene to Triad: Brightness={scene.brightness}, Complexity={scene.complexity}, Objects={[o.label for o in scene.objects]}")
        delta_t = 0.0
        delta_s = 0.0
        delta_r = 0.0

        # 1. Tension
        if scene.complexity > 0.7: delta_t += 0.2
        if scene.complexity < 0.3: delta_t -= 0.1

        # 2. Reality
        if scene.brightness > 0.8: delta_r += 0.2
        if scene.brightness < 0.2: delta_r -= 0.2

        # 3. Object-based analysis
        positive_objects = ["sun", "light", "nature", "coffee", "smile", "flower", "code", "sky", "cat", "plant", "cozy"]
        negative_objects = ["darkness", "chaos", "fire", "broken", "error", "mess", "threat"]

        for obj in scene.objects:
            label = obj.label.lower()
            if any(p in label for p in positive_objects):
                delta_s += 0.1
                delta_t -= 0.1
            if any(n in label for n in negative_objects):
                delta_t += 0.2
                delta_s -= 0.1

        print(f"   [Vision DEBUG] Calculated Deltas: T={delta_t}, S={delta_s}, R={delta_r}")

        return {
            "visual_tension": max(0.0, min(1.0, delta_t)),
            "visual_satisfaction": max(0.0, min(1.0, delta_s)),
            "visual_reality": max(0.0, min(1.0, delta_r))
        }
