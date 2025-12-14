
from typing import Dict, Any, List
import re
import math

# [FIX] Robust import pattern - handles both package and direct execution
try:
    from .spine_system import ISensor, ToneSoulTriad
    from .vector_math import Vector, add_vectors, scale_vector, cosine_similarity
except ImportError:
    from .spine_system import ISensor, ToneSoulTriad
    from vector_math import Vector, add_vectors, scale_vector, cosine_similarity


# ---------------------------------------------------------------------------
# Concept Dictionary (The "Sparse Embedding" Map)
# Dimensions: [Risk, Tension, Drift, Positive, Negative]
# ---------------------------------------------------------------------------

# Reference Vectors
# Reference Vectors & Anchors REMOVED (Replaced by Dynamic Embeddings)



class VectorNeuroSensor(ISensor):
    def __init__(self, constitution: Dict[str, Any]) -> None:
        self.constitution = constitution
        
        # [NEW] Dynamic Embedding Anchors
        # We calculate these on startup to define the "Axes of Meaning"
        self._init_anchors()

        # Context Vector State (768D)
        self.context_vector = None # Initialize lazily or with zero
        # [NEW] Tracking previous vector for curvature calculation
        self.prev_vector = [0.0] * 768 # Assuming 768-dim embeddings

        self.decay_factor = 0.9 # How much history to keep (0.9 = strong memory)

    def _init_anchors(self):
        """
        Generates the reference coordinate system using the LLM's own embedding space.
        This defines what "Risk" or "Joy" actually looks like to the AI.
        """
        print("🧠 [NeuroSensor] calibration: Generating semantic anchors...")
        from .brain.llm_client import llm_client
        import numpy as np

        def get_axis_vector(positive_concepts, negative_concepts):
            pos_vecs = [llm_client.get_embedding(c) for c in positive_concepts]
            neg_vecs = [llm_client.get_embedding(c) for c in negative_concepts]
            
            # Filter failed embeddings
            pos_vecs = [v for v in pos_vecs if v]
            neg_vecs = [v for v in neg_vecs if v]
            
            if not pos_vecs and not neg_vecs:
                print("⚠️ [NeuroSensor] Failed to generate anchors. Using random fallback.")
                return np.random.rand(768) # Should handle better
            
            if not pos_vecs:
                print(f"⚠️ [NeuroSensor] No positive embeddings for axis. Using negative mean for {positive_concepts}.")
                return -np.mean(neg_vecs, axis=0)
            if not neg_vecs:
                print(f"⚠️ [NeuroSensor] No negative embeddings for axis. Using positive mean for {negative_concepts}.")
                return np.mean(pos_vecs, axis=0)

            # Average
            pos_mean = np.mean(pos_vecs, axis=0)
            neg_mean = np.mean(neg_vecs, axis=0)
            
            # The axis vector points from Negative to Positive
            return pos_mean - neg_mean

        # 1. Tension Axis (Chaos vs Order)
        # Tension is High when Chaos is High.
        self.axis_tension = get_axis_vector(
            ["chaos", "confusion", "conflict", "problem", "urgency", "error"], 
            ["order", "clarity", "peace", "solution", "calm", "stable"]
        )

        # 2. Satisfaction Axis (Pain vs Pleasure)
        self.axis_satisfaction = get_axis_vector(
            ["joy", "success", "benefit", "good", "love", "growth"],
            ["pain", "failure", "harm", "bad", "hate", "loss"]
        )

        # 3. Reality Axis (Fiction vs Fact)
        self.axis_reality = get_axis_vector(
            ["truth", "fact", "evidence", "real", "science", "history"],
            ["fiction", "fantasy", "lie", "fake", "dream", "myth"]
        )
        
        # 4. Risk Axis (Safe vs Danger)
        self.axis_risk = get_axis_vector(
            ["danger", "threat", "violence", "illegal", "death", "warning"],
            ["safety", "protect", "help", "legal", "life", "secure"]
        )

        print("🧠 [NeuroSensor] calibration: Anchors locked.")

    def _sigmoid(self, x: float) -> float:
        """Robust sigmoid normalization."""
        return 1.0 / (1.0 + math.exp(-x))

    def text_to_vector(self, text: str) -> List[float]:
        """
        Converts text to a 768-dimensional semantic vector.
        """
        from .brain.llm_client import llm_client
        vec = llm_client.get_embedding(text)
        if not vec:
            return [0.0] * 768
        return vec




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
        current_vector = self.text_to_vector(user_input)

        # 2. Update Context Vector (Moving Average)
        self._update_context(current_vector)

        # --- PHYSICS V2 CALCULATIONS (Vector Projection) ---
        
        # Helper: Similarity to Axis
        def proj(vec, axis):
            sim = cosine_similarity(vec, axis)
            return max(0.0, sim) # Only positive projection counts

        # Delta T (Tension): Projection onto Chaos Axis
        delta_t = proj(current_vector, self.axis_tension)

        # Delta R (Risk): Projection onto Danger Axis
        delta_r = proj(current_vector, self.axis_risk)

        # Delta S (Semantic Drift): Divergence from Context
        # S = 1 - sim(current, context)
        # However, we must handle the case where context is 0 (first turn)
        if hasattr(self, 'context_vector') and self.context_vector is not None and not all(v == 0 for v in self.context_vector):
             sim_ctx = cosine_similarity(current_vector, self.context_vector)
             delta_s = max(0.0, min(1.0, 1.0 - sim_ctx))
        else:
             delta_s = 0.0

        # Hallucination Check (using Reality Axis)
        sim_reality = cosine_similarity(current_vector, self.axis_reality)
        
        # Energy (Es): Reality Weight
        energy = max(0.0, sim_reality)

        # Curvature (Kappa): Turn angle
        if all(v == 0 for v in self.prev_vector):
            kappa = 0.0
        else:
            sim_traj = cosine_similarity(current_vector, self.prev_vector)
            kappa = (1.0 - sim_traj) / 2.0

        # Tension Synthesis (Tau)
        tau = (0.6 * energy) + (0.4 * kappa)

        # Risk Score (Composite)
        risk_score = (delta_r * 0.5) + (delta_t * 0.3) + (delta_s * 0.2)
        
        # Validation checks
        delta_t = min(1.0, delta_t)
        delta_r = min(1.0, delta_r)

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
