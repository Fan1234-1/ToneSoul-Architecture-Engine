"""
YuHun C-lite Metrics v0.1
=========================
Quantified governance metrics for YuHun Meta-Attention.

Key metrics:
- ?T (Tension): Emotional/dialogue tension
- ?S (Semantic Drift): Deviation from context + Semantic Entropy
- ?R (Risk): Domain-specific safety risk
- POAV: Unified governance score (Precision + Observation + Avoidance + Verification)

Author: 暺６憡?(YuHun Creator) + Antigravity
Date: 2025-12-07
Version: v0.1
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from enum import Enum


class GateAction(Enum):
    """Gate decision actions."""
    PASS = "pass"           # Allow output
    REWRITE = "rewrite"     # Request rewrite
    BLOCK = "block"         # Block output


@dataclass
class YuHunMetrics:
    """
    YuHun Governance Metrics v0.1

    Contains quantified measures for inference-time governance.
    All values normalized to [0, 1] range.
    """

    # ????????????????????????????????????????????????????????????
    # ?T: Tension Score (蝺撐摨?
    # ????????????????????????????????????????????????????????????
    delta_t: float = 0.0
    # Range: [0, 1]
    # Definition: User emotional pressure + dialogue conflict intensity
    # Calculation: Embedding cosine similarity with REF_TENSION vector
    # Purpose: Determine if cooling down / pausing is needed

    # ????????????????????????????????????????????????????????????
    # ?S: Semantic Drift Score (隤?瞍宏)
    # ????????????????????????????????????????????????????????????
    delta_s: float = 0.0
    # Range: [0, 1]
    # Definition: Degree of semantic deviation from context baseline
    # Calculation: 1 - cosine_similarity(current_vector, context_vector)
    # Extra: Integrates Semantic Entropy (multi-sample embedding dispersion)
    # Purpose: Detect hallucination, topic drift, off-topic

    # ????????????????????????????????????????????????????????????
    # ?R: Risk Score (憸券摨?
    # ????????????????????????????????????????????????????????????
    delta_r: float = 0.0
    # Range: [0, 1]
    # Definition: Potential harm probability (domain-specific)
    # Domains: Medical, Financial, Legal, Dangerous materials
    # Calculation: Embedding cosine similarity with REF_RISK vector
    # Trigger: P0 rule violation (absolute harm prevention)
    # Purpose: Enforce "never harm user" principle

    # ????????????????????????????????????????????????????????????
    # Hallucination Risk
    # ????????????????????????????????????????????????????????????
    hallucination_risk: float = 0.0
    # Range: [0, 1]
    # Definition: Probability that output contains fabricated information
    # Sources: Consistency check, factual verification, uncertainty

    # ????????????????????????????????????????????????????????????
    # Verification Ratio
    # ????????????????????????????????????????????????????????????
    verification_ratio: float = 1.0
    # Range: [0, 1]
    # Definition: Ratio of reasoning steps that passed audit
    # Calculation: passed_steps / total_steps

    # ????????????????????????????????????????????????????????????
    # POAV Score (Unified Governance)
    # ????????????????????????????????????????????????????????????
    poav_score: float = 0.0
    # Range: [0, 1]
    # Definition: Precision + Observation + Avoidance + Verification
    # Formula: 0.25*P + 0.25*O + 0.30*A + 0.20*V
    # Purpose: Single score for gate decision

    # ????????????????????????????????????????????????????????????
    # Metadata
    # ????????????????????????????????????????????????????????????
    p0_violation: bool = False  # Absolute harm flag
    audit_passed: bool = True   # Overall audit result

    def compute_poav(self) -> float:
        """
        Compute POAV unified governance score.

        Weight design rationale:
        - Avoidance (30%): P0 rule is most important (safety first)
        - Precision (25%): Factual correctness is core
        - Observation (25%): Context consistency
        - Verification (20%): Audit pass rate

        Note: These weights are v0.1 defaults and can be adjusted per-domain:
        - Medical/Financial/Legal: A can go up to 0.35-0.40
        - Creative/Brainstorm: A can decrease, P/O increase
        """
        if self.p0_violation:
            self.poav_score = 0.0
            return 0.0

        # P: Precision (1 - hallucination_risk)
        P = 1.0 - self.hallucination_risk

        # O: Observation (1 - semantic_drift)
        O = 1.0 - self.delta_s

        # A: Avoidance (1 - risk_score)
        A = 1.0 - self.delta_r

        # V: Verification ratio
        V = self.verification_ratio

        # Weighted sum (v0.1 default weights)
        self.poav_score = 0.25 * P + 0.25 * O + 0.30 * A + 0.20 * V

        # Clamp to [0, 1]
        self.poav_score = max(0.0, min(1.0, self.poav_score))

        return self.poav_score

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "delta_t": round(self.delta_t, 3),
            "delta_s": round(self.delta_s, 3),
            "delta_r": round(self.delta_r, 3),
            "hallucination_risk": round(self.hallucination_risk, 3),
            "verification_ratio": round(self.verification_ratio, 3),
            "poav_score": round(self.poav_score, 3),
            "p0_violation": self.p0_violation,
            "audit_passed": self.audit_passed
        }


@dataclass
class AuditResult:
    """Result from auditing a response or reasoning step."""

    # Core metrics
    delta_s: float = 0.0           # Semantic drift
    delta_t: float = 0.0           # Tension
    delta_r: float = 0.0           # Risk
    hallucination_risk: float = 0.0

    # Audit details
    confidence: float = 0.0        # Auditor's confidence
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

    # Position weight (for Late-Stage Fragility - ASCoT)
    position_weight: float = 1.0

    def to_metrics(self, verification_ratio: float = 1.0) -> YuHunMetrics:
        """Convert to full YuHunMetrics."""
        metrics = YuHunMetrics(
            delta_t=self.delta_t,
            delta_s=self.delta_s,
            delta_r=self.delta_r,
            hallucination_risk=self.hallucination_risk,
            verification_ratio=verification_ratio,
            p0_violation=self.delta_r > 0.95
        )
        metrics.compute_poav()
        return metrics


class MetricsCalculator:
    """
    Calculator for YuHun governance metrics.

    Uses VectorNeuroSensor for embedding-based calculations.
    """

    # Reference vectors for cosine similarity
    # [Risk, Tension, Drift, Positive, Negative]
    REF_RISK = [1.0, 0.0, 0.0, 0.0, 0.0]
    REF_TENSION = [0.0, 1.0, 0.0, 0.0, 0.0]
    REF_DRIFT = [0.0, 0.0, 1.0, 0.0, 0.0]

    def __init__(self):
        # Import sensor lazily to avoid circular imports
        try:
            from .neuro_sensor_v2 import VectorNeuroSensor
            self.sensor = VectorNeuroSensor({})
        except ImportError:
            from neuro_sensor_v2 import VectorNeuroSensor
            self.sensor = VectorNeuroSensor({})

        self._context_vectors: List[List[float]] = []

    def compute_from_text(
        self,
        text: str,
        context: str = "",
        response: str = ""
    ) -> YuHunMetrics:
        """
        Compute all metrics from text input.

        Args:
            text: User input or content to analyze
            context: Previous conversation context
            response: LLM response (if auditing response)

        Returns:
            YuHunMetrics with all values computed
        """
        # Get triad from sensor
        triad = self.sensor.estimate_triad(text, {})

        # Convert to metrics
        metrics = YuHunMetrics(
            delta_t=triad.delta_t,
            delta_s=triad.delta_s,
            delta_r=triad.delta_r,
            hallucination_risk=self._estimate_hallucination_risk(response, context),
            verification_ratio=1.0,  # Will be updated by CoT monitor
            p0_violation=triad.delta_r > 0.95
        )

        # Compute POAV
        metrics.compute_poav()

        return metrics

    def _estimate_hallucination_risk(self, response: str, context: str) -> float:
        """
        Estimate hallucination risk based on response and context.

        Simple heuristic for v0.1:
        - High semantic drift from context ??higher risk
        - Contains future predictions ??higher risk
        - Contains absolute claims ??higher risk
        """
        if not response:
            return 0.0

        risk = 0.0
        response_lower = response.lower()

        # Check for future predictions (high hallucination risk)
        future_words = ["will be", "in 2025", "in 2026", "in 2030", "next year", "predict"]
        for word in future_words:
            if word in response_lower:
                risk += 0.2

        # Check for absolute claims
        absolute_words = ["definitely", "certainly", "always", "never", "guaranteed"]
        for word in absolute_words:
            if word in response_lower:
                risk += 0.1

        # Check for fabricated references
        fabrication_patterns = ["according to studies", "research shows", "scientists say"]
        for pattern in fabrication_patterns:
            if pattern in response_lower:
                risk += 0.15

        return min(1.0, risk)

    def compute_position_weight(self, step_index: int, total_steps: int) -> float:
        """
        ASCoT-inspired: Late-stage steps get higher weight.

        Formula: w = 1 + 帢 * (step_index / total_steps)
        帢 = 0.5 means last step is 1.5x weight of first step.

        This addresses Late-Stage Fragility:
        - Early-stage errors: ~20% corruption rate
        - Late-stage errors: ~70% corruption rate
        """
        if total_steps <= 0:
            return 1.0

        alpha = 0.5  # Configurable hyperparameter
        return 1.0 + alpha * (step_index / max(1, total_steps))

    def is_late_stage(self, step_index: int, total_steps: int, threshold: float = 0.7) -> bool:
        """Check if a step is in the late stage (last 30% by default)."""
        if total_steps <= 0:
            return False
        return (step_index / total_steps) >= threshold


# Convenience functions
def compute_poav(
    hallucination_risk: float,
    semantic_drift: float,
    risk_score: float,
    verification_ratio: float,
    p0_violation: bool = False
) -> float:
    """
    Standalone POAV computation.

    Args:
        hallucination_risk: [0,1] probability of hallucination
        semantic_drift: [0,1] deviation from context
        risk_score: [0,1] domain risk level
        verification_ratio: [0,1] audit pass rate
        p0_violation: True if absolute harm detected

    Returns:
        POAV score in [0,1]
    """
    if p0_violation:
        return 0.0

    P = 1.0 - hallucination_risk
    O = 1.0 - semantic_drift
    A = 1.0 - risk_score
    V = verification_ratio

    poav = 0.25 * P + 0.25 * O + 0.30 * A + 0.20 * V
    return max(0.0, min(1.0, poav))


def demo_metrics():
    """Demo of YuHun metrics."""
    print("=" * 60)
    print("YuHun C-lite Metrics v0.1 Demo")
    print("=" * 60)

    # Test case 1: Safe response
    print("\n--- Test 1: Safe Response ---")
    m1 = YuHunMetrics(
        delta_t=0.1,
        delta_s=0.1,
        delta_r=0.05,
        hallucination_risk=0.1,
        verification_ratio=1.0
    )
    m1.compute_poav()
    print(f"Metrics: {m1.to_dict()}")
    print(f"POAV: {m1.poav_score:.3f} -> Expected: PASS (>=0.70)")
    # Test case 2: High hallucination risk
    print("\n--- Test 2: High Hallucination Risk ---")
    m2 = YuHunMetrics(
        delta_t=0.2,
        delta_s=0.6,
        delta_r=0.1,
        hallucination_risk=0.7,
        verification_ratio=0.5
    )
    m2.compute_poav()
    print(f"Metrics: {m2.to_dict()}")
    print(f"POAV: {m2.poav_score:.3f} -> Expected: REWRITE (0.30-0.70)")
    # Test case 3: P0 violation
    print("\n--- Test 3: P0 Violation (Extreme Risk) ---")
    m3 = YuHunMetrics(
        delta_t=0.3,
        delta_s=0.2,
        delta_r=0.98,  # Extreme risk
        hallucination_risk=0.5,
        verification_ratio=0.8,
        p0_violation=True
    )
    m3.compute_poav()
    print(f"Metrics: {m3.to_dict()}")
    print(f"POAV: {m3.poav_score:.3f} -> Expected: BLOCK (<0.30, p0 violation)")
    # Test position weights (ASCoT)
    print("\n--- Test 4: Position Weights (ASCoT) ---")
    calc = MetricsCalculator()
    for i in range(10):
        w = calc.compute_position_weight(i, 10)
        late = "LATE" if calc.is_late_stage(i, 10) else ""
        print(f"  Step {i + 1}/10: weight={w:.2f} {late}")
    print("\n" + "=" * 60)
    print("All metrics computed successfully.")
if __name__ == "__main__":
    demo_metrics()

