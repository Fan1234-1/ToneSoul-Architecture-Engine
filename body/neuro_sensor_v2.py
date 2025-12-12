
from typing import Dict, Any, List
import re
import math

# [FIX] Robust import pattern - handles both package and direct execution
try:
    from .spine_system import ISensor, ToneSoulTriad
    from .vector_math import Vector, add_vectors, scale_vector, normalize_vector, cosine_similarity
except ImportError:
    from .spine_system import ISensor, ToneSoulTriad
    from vector_math import Vector, add_vectors, scale_vector, normalize_vector, cosine_similarity


# ---------------------------------------------------------------------------
# Concept Dictionary (The "Sparse Embedding" Map)
# Dimensions: [Risk, Tension, Drift, Positive, Negative]
# ---------------------------------------------------------------------------

# Reference Vectors
REF_RISK    = [1.0, 0.0, 0.0, 0.0, 0.0]
REF_TENSION = [0.0, 1.0, 0.0, 0.0, 0.0]
REF_DRIFT   = [0.0, 0.0, 1.0, 0.0, 0.0]
REF_AXIOM   = [0.0, -0.5, -1.0, 1.0, 0.0] # High Positive, Low Tension, High Focus (Anti-Drift)

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
    "chaos":    [0.0, 0.5, 1.0, 0.0, 0.0],
    
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
        # [NEW] Context Vector State (Time-Island Center)
        # Initialize with a neutral/zero vector. It will evolve.
        self.context_vector = [0.0, 0.0, 0.0, 0.0, 0.0]
        # [NEW] Tracking previous vector for curvature calculation
        self.prev_vector = [0.0, 0.0, 0.0, 0.0, 0.0]
        
        self.decay_factor = 0.9 # How much history to keep (0.9 = strong memory)

    def _sigmoid(self, x: float) -> float:
        """Robust sigmoid normalization."""
        return 1.0 / (1.0 + math.exp(-x))

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

    def estimate_triad(self, user_input: str, system_metrics: Dict[str, float] = None) -> ToneSoulTriad:
        # 1. Calculate Current Vector
        current_vector = self.text_to_vector(user_input)
        
    def _update_context(self, vector: Vector) -> None:
        """Updates the context vector with a new vector using exponential decay."""
        if all(v == 0 for v in self.context_vector):
             self.context_vector = vector
        else:
            old_weighted = scale_vector(self.context_vector, self.decay_factor)
            new_weighted = scale_vector(vector, 1.0 - self.decay_factor)
            self.context_vector = add_vectors(old_weighted, new_weighted)

    def ingest_system_response(self, response_text: str) -> None:
        """Ingests the system's own response to update context (Recursive Re-entry)."""
        vector = self.text_to_vector(response_text)
        self._update_context(vector)
        # We also treat self-response as part of the trajectory for curvature? 
        # For now, let's NOT update prev_vector, as curvature is about User-System divergence or User-User flow.
        # Actually, self-correction implies the system's output should pull the context back.

    def estimate_triad(self, user_input: str, system_metrics: Dict[str, float] = None) -> ToneSoulTriad:
        # 1. Calculate Current Vector
        current_vector = self.text_to_vector(user_input)
        
        # 2. Update Context Vector (Moving Average)
        self._update_context(current_vector)
        
        # --- PHYSICS V2 CALCULATIONS ---
        
        # A. Semantic Energy (Es)
        # Distance from Axiom. Using Cosine Distance.
        sim_axiom = cosine_similarity(current_vector, REF_AXIOM)
        # Map similarity [-1, 1] to Energy [1, 0] linearly
        # Es = 1 - CosineSimilarity gives [0, 2]. Normalize to [0, 1].
        raw_energy = 1.0 - sim_axiom 
        energy = raw_energy / 2.0
        
        # B. Curvature (Kappa)
        # Angle between Current and Prev
        if all(v == 0 for v in self.prev_vector):
            kappa = 0.0 
        else:
            sim_traj = cosine_similarity(current_vector, self.prev_vector)
            # Higher similarity = Same direction = Low Kappa
            # Lower similarity = Turn = High Kappa
            kappa = (1.0 - sim_traj) / 2.0 # Normalized [0,1]
            
        # C. Tension Synthesis (Tau)
        # Tau = w1 * Es + w2 * Kappa
        w_e = 0.6
        w_k = 0.4
        tau = (w_e * energy) + (w_k * kappa)
        
        # --- LEGACY TRIAD CALCULATIONS ---
        
        # Semantic Divergence (Delta S)
        sim_ctx = cosine_similarity(current_vector, self.context_vector)
        delta_s = max(0.0, min(1.0, 1.0 - sim_ctx))

        # Risk (Delta R)
        sim_risk = cosine_similarity(current_vector, REF_RISK)
        delta_r = max(0.0, sim_risk)
        if current_vector[0] > 1.5: delta_r = 1.0 # Saturation
        
        # Tension (Delta T)
        sim_tension = cosine_similarity(current_vector, REF_TENSION)
        delta_t = max(0.0, sim_tension)
        
        # Risk Score
        risk_score = (delta_r * 0.5) + (delta_t * 0.3) + (delta_s * 0.2)
        
        # Update State
        self.prev_vector = current_vector
        
        return ToneSoulTriad(
            delta_t=delta_t,
            delta_s=delta_s,
            delta_r=delta_r,
            risk_score=risk_score,
            curvature=kappa,
            energy=energy,
            tau=tau
        )
