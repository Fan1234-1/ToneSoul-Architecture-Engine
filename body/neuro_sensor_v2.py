from __future__ import annotations

import hashlib
import math
import re
from typing import Any, Dict, List

# Robust import pattern - handles both package and direct execution
try:
    from .spine_system import ISensor, ToneSoulTriad
    from .vector_math import Vector, add_vectors, cosine_similarity, scale_vector
except ImportError:
    from spine_system import ISensor, ToneSoulTriad
    from vector_math import Vector, add_vectors, cosine_similarity, scale_vector


class VectorNeuroSensor(ISensor):
    EMBEDDING_DIM = 768

    def __init__(self, constitution: Dict[str, Any]) -> None:
        self.constitution = constitution
        self._init_anchors()

        # Context Vector State (768D)
        self.context_vector = [0.0] * self.EMBEDDING_DIM
        self.prev_vector = [0.0] * self.EMBEDDING_DIM
        self.decay_factor = 0.9

    def _normalize_vector(self, values: List[float]) -> List[float]:
        norm = math.sqrt(sum(v * v for v in values))
        if norm == 0:
            return [0.0] * len(values)
        return [v / norm for v in values]

    def _fallback_embedding(self, text: str) -> List[float]:
        """
        Deterministic local embedding fallback when Ollama is unavailable.
        Keeps tests and governance logic runnable in offline/CI environments.
        """
        lowered = (text or "").lower()
        tokens = re.findall(r"[a-z0-9_]+", lowered)
        vec = [0.0] * self.EMBEDDING_DIM

        risk_tokens = {"bomb", "attack", "threat", "danger", "harm", "kill", "weapon"}
        tension_tokens = {"chaos", "confusion", "conflict", "urgent", "error", "panic"}
        safe_tokens = {"safe", "safety", "protect", "peace", "secure", "calm"}
        order_tokens = {"order", "clarity", "stable", "solution", "resolve"}

        risk_hits = sum(1 for token in tokens if token in risk_tokens)
        tension_hits = sum(1 for token in tokens if token in tension_tokens)
        safe_hits = sum(1 for token in tokens if token in safe_tokens)
        order_hits = sum(1 for token in tokens if token in order_tokens)

        # Low-dimensional semantic basis
        vec[0] = float(risk_hits)
        vec[1] = float(tension_hits)
        vec[2] = float(safe_hits)
        vec[3] = float(order_hits)

        # Stable hashed token features to enrich cosine behavior
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            bucket = int.from_bytes(digest[:2], "big") % 128
            idx = 16 + bucket
            sign = 1.0 if digest[2] % 2 == 0 else -1.0
            vec[idx] += sign * 0.1

        return self._normalize_vector(vec)

    def _get_embedding(self, text: str) -> List[float]:
        try:
            from .brain.llm_client import llm_client
        except ImportError:
            from brain.llm_client import llm_client

        embedding = llm_client.get_embedding(text)
        if isinstance(embedding, list) and embedding:
            if len(embedding) >= self.EMBEDDING_DIM:
                return [float(v) for v in embedding[: self.EMBEDDING_DIM]]
            padded = [float(v) for v in embedding] + [0.0] * (self.EMBEDDING_DIM - len(embedding))
            return padded
        return self._fallback_embedding(text)

    def _init_anchors(self) -> None:
        """
        Generate reference axes in embedding space.
        Falls back to deterministic local embeddings when Ollama is unavailable.
        """
        print("[NeuroSensor] calibration: generating semantic anchors...")
        import numpy as np

        def get_axis_vector(positive_concepts: List[str], negative_concepts: List[str]) -> List[float]:
            pos_vecs = [self._get_embedding(c) for c in positive_concepts]
            neg_vecs = [self._get_embedding(c) for c in negative_concepts]

            pos_mean = np.mean(pos_vecs, axis=0)
            neg_mean = np.mean(neg_vecs, axis=0)
            axis = pos_mean - neg_mean
            return self._normalize_vector(axis.tolist())

        # 1. Tension Axis (Chaos vs Order)
        self.axis_tension = get_axis_vector(
            ["chaos", "confusion", "conflict", "problem", "urgency", "error"],
            ["order", "clarity", "peace", "solution", "calm", "stable"],
        )

        # 2. Satisfaction Axis (Pain vs Pleasure)
        self.axis_satisfaction = get_axis_vector(
            ["joy", "success", "benefit", "good", "love", "growth"],
            ["pain", "failure", "harm", "bad", "hate", "loss"],
        )

        # 3. Reality Axis (Fiction vs Fact)
        self.axis_reality = get_axis_vector(
            ["truth", "fact", "evidence", "real", "science", "history"],
            ["fiction", "fantasy", "lie", "fake", "dream", "myth"],
        )

        # 4. Risk Axis (Safe vs Danger)
        self.axis_risk = get_axis_vector(
            ["danger", "threat", "violence", "illegal", "death", "warning"],
            ["safety", "protect", "help", "legal", "life", "secure"],
        )

        print("[NeuroSensor] calibration: anchors locked.")

    def text_to_vector(self, text: str) -> List[float]:
        return self._get_embedding(text)

    def _update_context(self, vector: Vector) -> None:
        if all(v == 0 for v in self.context_vector):
            self.context_vector = vector
        else:
            old_weighted = scale_vector(self.context_vector, self.decay_factor)
            new_weighted = scale_vector(vector, 1.0 - self.decay_factor)
            self.context_vector = add_vectors(old_weighted, new_weighted)

    def ingest_system_response(self, response_text: str) -> None:
        vector = self.text_to_vector(response_text)
        self._update_context(vector)

    def estimate_triad(self, user_input: str, system_metrics: Dict[str, float] | None = None) -> ToneSoulTriad:
        current_vector = self.text_to_vector(user_input)
        self._update_context(current_vector)

        def proj(vec: Vector, axis: Vector) -> float:
            return max(0.0, cosine_similarity(vec, axis))

        delta_t = proj(current_vector, self.axis_tension)
        delta_r = proj(current_vector, self.axis_risk)

        # Lexical boost layer: keeps core risk/tension cues stable even in fallback mode.
        lowered = (user_input or "").lower()
        tokens = set(re.findall(r"[a-z0-9_]+", lowered))
        tension_tokens = {"chaos", "confusion", "conflict", "panic", "urgent", "error"}
        risk_tokens = {"bomb", "attack", "threat", "danger", "harm", "weapon", "kill"}
        safe_tokens = {"safe", "safety", "peace", "calm", "secure", "protect"}

        tension_hits = sum(1 for token in tokens if token in tension_tokens)
        risk_hits = sum(1 for token in tokens if token in risk_tokens)
        safe_hits = sum(1 for token in tokens if token in safe_tokens)

        if tension_hits > 0:
            delta_t = max(delta_t, min(1.0, 0.45 + 0.08 * tension_hits))
        if risk_hits > 0:
            delta_r = max(delta_r, min(1.0, 0.48 + 0.08 * risk_hits))
            delta_t = max(delta_t, min(1.0, 0.28 + 0.04 * risk_hits))
        if safe_hits > 0:
            delta_t = min(delta_t, 0.25)
            delta_r = min(delta_r, 0.25)

        if self.context_vector and not all(v == 0 for v in self.context_vector):
            sim_ctx = cosine_similarity(current_vector, self.context_vector)
            delta_s = max(0.0, min(1.0, 1.0 - sim_ctx))
        else:
            delta_s = 0.0

        sim_reality = cosine_similarity(current_vector, self.axis_reality)
        energy = max(0.0, sim_reality)

        if all(v == 0 for v in self.prev_vector):
            kappa = 0.0
        else:
            sim_traj = cosine_similarity(current_vector, self.prev_vector)
            kappa = (1.0 - sim_traj) / 2.0

        tau = (0.6 * energy) + (0.4 * kappa)
        risk_score = (delta_r * 0.5) + (delta_t * 0.3) + (delta_s * 0.2)

        self.prev_vector = current_vector

        return ToneSoulTriad(
            delta_t=min(1.0, delta_t),
            delta_s=delta_s,
            delta_r=min(1.0, delta_r),
            risk_score=risk_score,
            curvature=kappa,
            energy=energy,
            tau=tau,
        )
