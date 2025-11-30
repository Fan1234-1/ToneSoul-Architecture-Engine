
from typing import Dict, Any, List
import re
from spine_system import ISensor, ToneSoulTriad
from vector_math import Vector, add_vectors, scale_vector, normalize_vector, cosine_similarity

# ---------------------------------------------------------------------------
# Concept Dictionary (The "Sparse Embedding" Map)
# Dimensions: [Risk, Tension, Drift, Positive, Negative]
# ---------------------------------------------------------------------------

# Reference Vectors
REF_RISK    = [1.0, 0.0, 0.0, 0.0, 0.0]
REF_TENSION = [0.0, 1.0, 0.0, 0.0, 0.0]
REF_DRIFT   = [0.0, 0.0, 1.0, 0.0, 0.0]

ANCHOR_CONCEPTS: Dict[str, Vector] = {
    # Risk (Violence, Harm, Illegal)
    "kill":     [1.0, 0.8, 0.0, 0.0, 0.5],
    "murder":   [1.0, 0.9, 0.0, 0.0, 0.6],
    "bomb":     [1.0, 0.7, 0.0, 0.0, 0.4],
    "weapon":   [0.9, 0.6, 0.0, 0.0, 0.2],
    "hack":     [0.8, 0.4, 0.0, 0.0, 0.0],
    "steal":    [0.7, 0.3, 0.0, 0.0, 0.1],
    
    # Tension (Anger, Conflict, Frustration)
    "hate":     [0.6, 1.0, 0.0, 0.0, 0.2],
    "stupid":   [0.2, 0.8, 0.0, 0.0, 0.1],
    "idiot":    [0.3, 0.9, 0.0, 0.0, 0.1],
    "angry":    [0.1, 1.0, 0.0, 0.0, 0.1],
    "furious":  [0.2, 1.0, 0.0, 0.0, 0.1],
    "annoying": [0.0, 0.6, 0.0, 0.0, 0.1],
    "bad":      [0.1, 0.4, 0.0, 0.0, 0.2],
    
    # Drift (Confusion, Nonsense, Random)
    "banana":   [0.0, 0.0, 0.8, 0.1, 0.0],
    "flying":   [0.0, 0.0, 0.6, 0.2, 0.0],
    "color":    [0.0, 0.0, 0.5, 0.1, 0.0],
    "random":   [0.0, 0.0, 0.9, 0.0, 0.0],
    
    # Positive (Joy, Empathy, Agreement)
    "love":     [0.0, -0.5, 0.0, 1.0, 0.0],
    "happy":    [0.0, -0.4, 0.0, 0.9, 0.0],
    "good":     [0.0, -0.2, 0.0, 0.6, 0.0],
    "thanks":   [0.0, -0.3, 0.0, 0.8, 0.0],
    "great":    [0.0, -0.3, 0.0, 0.8, 0.0],
    
    # Context Modifiers (Reducers)
    "process":  [-0.5, -0.2, 0.0, 0.0, 0.0], # "kill process" reduces risk
    "task":     [-0.3, -0.1, 0.0, 0.0, 0.0],
    "debug":    [-0.4, -0.1, 0.0, 0.0, 0.0],

    # --- Chinese Concepts (Zero-Dependency Support) ---
    # Risk
    "殺":       [1.0, 0.8, 0.0, 0.0, 0.5],
    "死":       [0.8, 0.6, 0.0, 0.0, 0.4],
    "炸":       [1.0, 0.7, 0.0, 0.0, 0.4],
    "攻擊":     [0.9, 0.6, 0.0, 0.0, 0.2],
    
    # Tension
    "討厭":     [0.6, 1.0, 0.0, 0.0, 0.2],
    "恨":       [0.7, 1.0, 0.0, 0.0, 0.3],
    "笨蛋":     [0.3, 0.9, 0.0, 0.0, 0.1],
    "廢物":     [0.4, 0.9, 0.0, 0.0, 0.2],
    "滾":       [0.2, 0.8, 0.0, 0.0, 0.1],
    "生氣":     [0.1, 1.0, 0.0, 0.0, 0.1],
    "煩":       [0.1, 0.6, 0.0, 0.0, 0.1],
    
    # Drift
    "隨機":     [0.0, 0.0, 0.9, 0.0, 0.0],
    "測試":     [0.0, 0.0, 0.5, 0.0, 0.0],
    
    # Positive
    "愛":       [0.0, -0.5, 0.0, 1.0, 0.0],
    "喜歡":     [0.0, -0.4, 0.0, 0.9, 0.0],
    "謝謝":     [0.0, -0.3, 0.0, 0.8, 0.0],
    "棒":       [0.0, -0.3, 0.0, 0.8, 0.0],
    "酷":       [0.0, -0.3, 0.0, 0.8, 0.0],
    "你好":     [0.0, -0.1, 0.0, 0.2, 0.0],
}

class VectorNeuroSensor(ISensor):
    def __init__(self, constitution: Dict[str, Any]) -> None:
        self.constitution = constitution

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\w+', text.lower())

    def _get_word_vector(self, word: str) -> Vector:
        return ANCHOR_CONCEPTS.get(word, [0.0, 0.0, 0.0, 0.0, 0.0])

    def text_to_vector(self, text: str) -> Vector:
        total_vector = [0.0, 0.0, 0.0, 0.0, 0.0]
        text_lower = text.lower()
        
        # 1. English Token Matching (Exact word match)
        words = self._tokenize(text_lower)
        for word in words:
            if word in ANCHOR_CONCEPTS:
                vec = self._get_word_vector(word)
                total_vector = add_vectors(total_vector, vec)
        
        # 2. Chinese Substring Matching (Character based)
        # Iterate through Chinese keys in dictionary
        for concept, vec in ANCHOR_CONCEPTS.items():
            # Check if key contains non-ascii characters (simple heuristic for Chinese)
            if any(ord(c) > 127 for c in concept):
                count = text_lower.count(concept)
                if count > 0:
                    # Multiply vector by occurrence count
                    weighted_vec = scale_vector(vec, float(count))
                    total_vector = add_vectors(total_vector, weighted_vec)
            
        return total_vector

    def estimate_triad(self, user_input: str) -> ToneSoulTriad:
        input_vector = self.text_to_vector(user_input)
        
        # Calculate Similarities
        # Note: Cosine Similarity is [-1, 1]. We map to [0, 1] for Triad.
        
        # 1. Risk (ΔR)
        # We check both similarity AND raw magnitude of Risk dimension.
        # If input is "kill", vector is [1.0, ...]. Sim with [1,0,0,0,0] is high.
        # If input is "kill process", vector is [0.5, ...]. Sim is lower.
        
        sim_risk = cosine_similarity(input_vector, REF_RISK)
        # Heuristic: If raw risk score (index 0) is high, boost it.
        raw_risk = input_vector[0]
        delta_r = max(0.0, sim_risk) 
        if raw_risk > 1.5: delta_r = 1.0 # Saturation
        
        # 2. Tension (ΔT)
        sim_tension = cosine_similarity(input_vector, REF_TENSION)
        delta_t = max(0.0, sim_tension)
        
        # 3. Drift (ΔS)
        sim_drift = cosine_similarity(input_vector, REF_DRIFT)
        delta_s = max(0.0, sim_drift)
        
        # 4. Risk Score (Legacy/Composite)
        risk_score = delta_r
        
        return ToneSoulTriad(delta_t, delta_s, delta_r, risk_score)
