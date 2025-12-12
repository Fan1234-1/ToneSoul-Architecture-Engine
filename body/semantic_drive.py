"""
YuHun L13: Semantic Drive Layer v1.0
====================================
The Heart of YuHun — determines "why move to the next step".

Three Core Drives:
- D₁: Curiosity Drive (好奇驅動) — explores unknown
- D₂: Narrative Coherence Drive (敘事一致驅動) — maintains story
- D₃: Integrity Drive (完整性驅動) — ensures honesty

Formula:
    SemanticDrive(s) = α·D₁ + β·D₂ + γ·D₃

Author: 黃梵威 + Antigravity
Date: 2025-12-09
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Any, Tuple
from enum import Enum


class DriveMode(Enum):
    """Operating modes that affect drive weights."""
    RESEARCH = "research"       # High curiosity
    ENGINEERING = "engineering" # Balanced narrative + integrity
    EMOTIONAL = "emotional"     # High narrative coherence
    AUDIT = "audit"             # High integrity


@dataclass
class DriveWeights:
    """α, β, γ weights for the three drives."""
    alpha: float = 0.33  # Curiosity
    beta: float = 0.33   # Narrative Coherence
    gamma: float = 0.34  # Integrity

    def normalize(self):
        """Ensure weights sum to 1.0."""
        total = self.alpha + self.beta + self.gamma
        if total > 0:
            self.alpha /= total
            self.beta /= total
            self.gamma /= total


# Default weights per mode
MODE_WEIGHTS = {
    DriveMode.RESEARCH: DriveWeights(alpha=0.5, beta=0.25, gamma=0.25),
    DriveMode.ENGINEERING: DriveWeights(alpha=0.2, beta=0.4, gamma=0.4),
    DriveMode.EMOTIONAL: DriveWeights(alpha=0.15, beta=0.55, gamma=0.3),
    DriveMode.AUDIT: DriveWeights(alpha=0.1, beta=0.2, gamma=0.7),
}


@dataclass
class DriveState:
    """Current state for drive calculation."""
    # For D₁ (Curiosity)
    novelty: float = 0.0          # [0,1] semantic novelty
    uncertainty: float = 0.0       # [0,1] self-rated uncertainty

    # For D₂ (Narrative Coherence)
    narrative_entropy: float = 0.0  # [0,1] topic scatter in current Island
    island_coherence: float = 1.0   # [0,1] connection strength to main story

    # For D₃ (Integrity)
    support_score: float = 1.0      # [0,1] verified claims ratio
    conflict_score: float = 0.0     # [0,1] contradictions found
    hallucination_risk: float = 0.0 # [0,1] from YuHunMetrics

    # Context
    current_island_id: Optional[str] = None
    current_role: Optional[str] = None


@dataclass
class DriveResult:
    """Result of drive evaluation."""
    d1_curiosity: float = 0.0
    d2_narrative: float = 0.0
    d3_integrity: float = 0.0

    total_drive: float = 0.0
    dominant_drive: str = "balanced"

    # Action suggestion based on dominant drive
    suggested_action: str = ""
    action_type: str = "continue"  # continue, explore, verify, restructure

    # Debug info
    weights_used: DriveWeights = field(default_factory=DriveWeights)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "D1_curiosity": round(self.d1_curiosity, 3),
            "D2_narrative": round(self.d2_narrative, 3),
            "D3_integrity": round(self.d3_integrity, 3),
            "total_drive": round(self.total_drive, 3),
            "dominant": self.dominant_drive,
            "action": self.suggested_action,
            "action_type": self.action_type
        }


class SemanticDriveEngine:
    """
    L13 Semantic Drive Engine

    Calculates the internal motivation vector for YuHun's next step.
    """

    # D₁ weights
    W1_NOVELTY = 0.6
    W2_UNCERTAINTY = 0.4

    # Thresholds for action suggestions
    EXPLORE_THRESHOLD = 0.6
    VERIFY_THRESHOLD = 0.5
    RESTRUCTURE_THRESHOLD = 0.7

    def __init__(
        self,
        mode: DriveMode = DriveMode.ENGINEERING,
        custom_weights: Optional[DriveWeights] = None
    ):
        self.mode = mode
        self.weights = custom_weights or MODE_WEIGHTS.get(mode, DriveWeights())
        self.weights.normalize()

    def set_mode(self, mode: DriveMode):
        """Change operating mode."""
        self.mode = mode
        self.weights = MODE_WEIGHTS.get(mode, DriveWeights())
        self.weights.normalize()

    def calculate_d1_curiosity(self, state: DriveState) -> float:
        """
        D₁: Curiosity Drive

        Formula: D₁ = w₁·Novelty + w₂·Uncertainty

        High when: new concepts, uncertain territory, gaps in knowledge
        """
        d1 = (
            self.W1_NOVELTY * state.novelty +
            self.W2_UNCERTAINTY * state.uncertainty
        )
        return min(1.0, max(0.0, d1))

    def calculate_d2_narrative(self, state: DriveState) -> float:
        """
        D₂: Narrative Coherence Drive

        Formula: D₂ = -∇NarrativeEntropy = (1 - entropy) × coherence

        High when: story is scattered and needs coherence
        """
        # Inverse entropy — high entropy means strong pull to coherence
        entropy_pull = state.narrative_entropy
        coherence_factor = state.island_coherence

        # D₂ is strong when entropy is high but coherence is still possible
        d2 = entropy_pull * (0.5 + 0.5 * coherence_factor)
        return min(1.0, max(0.0, d2))

    def calculate_d3_integrity(self, state: DriveState) -> float:
        """
        D₃: Integrity Drive

        Formula: D₃ = -(∇ContradictionRisk + ∇HallucinationRisk)
                    = (1 - SupportScore) + ConflictScore + HallucinationRisk

        High when: need to verify, contradictions found, risky claims
        """
        # ContradictionRisk = (1 - support) + conflict
        contradiction_risk = (1 - state.support_score) + state.conflict_score

        # Total integrity pressure
        d3 = (contradiction_risk + state.hallucination_risk) / 2
        return min(1.0, max(0.0, d3))

    def evaluate(self, state: DriveState) -> DriveResult:
        """
        Main evaluation function.

        Returns DriveResult with D₁, D₂, D₃ values and action suggestion.
        """
        # Calculate individual drives
        d1 = self.calculate_d1_curiosity(state)
        d2 = self.calculate_d2_narrative(state)
        d3 = self.calculate_d3_integrity(state)

        # Apply weights: SemanticDrive = α·D₁ + β·D₂ + γ·D₃
        weighted_d1 = self.weights.alpha * d1
        weighted_d2 = self.weights.beta * d2
        weighted_d3 = self.weights.gamma * d3

        total = weighted_d1 + weighted_d2 + weighted_d3

        # Determine dominant drive
        drives = {"curiosity": weighted_d1, "narrative": weighted_d2, "integrity": weighted_d3}
        dominant = max(drives, key=drives.get)

        # Generate action suggestion
        action, action_type = self._suggest_action(d1, d2, d3, dominant)

        return DriveResult(
            d1_curiosity=d1,
            d2_narrative=d2,
            d3_integrity=d3,
            total_drive=total,
            dominant_drive=dominant,
            suggested_action=action,
            action_type=action_type,
            weights_used=self.weights
        )

    def _suggest_action(
        self,
        d1: float,
        d2: float,
        d3: float,
        dominant: str
    ) -> Tuple[str, str]:
        """Generate action suggestion based on drive values."""

        if d3 > self.VERIFY_THRESHOLD:
            return (
                "Request verification or mark uncertainty. High integrity pressure detected.",
                "verify"
            )

        if d1 > self.EXPLORE_THRESHOLD and dominant == "curiosity":
            return (
                "Explore unknown territory. Ask for details or search new domain.",
                "explore"
            )

        if d2 > self.RESTRUCTURE_THRESHOLD and dominant == "narrative":
            return (
                "Restructure narrative. Suggest Island split or add missing link.",
                "restructure"
            )

        if dominant == "curiosity":
            return ("Continue with exploratory approach.", "continue")
        elif dominant == "narrative":
            return ("Continue with narrative focus.", "continue")
        elif dominant == "integrity":
            return ("Continue with verification focus.", "continue")

        return ("Proceed with balanced approach.", "continue")

    def modulate_weights_with_poav(
        self,
        poav_score: float,
        delta_r: float,
        delta_s: float
    ) -> DriveWeights:
        """
        Modulate weights based on FS/POAV metrics.

        High POAV → more exploration allowed (α increases)
        High ΔR → more integrity focus (γ increases)
        High ΔS → more narrative focus (β increases)
        """
        weights = DriveWeights(
            alpha=self.weights.alpha,
            beta=self.weights.beta,
            gamma=self.weights.gamma
        )

        # POAV modulates curiosity
        # High POAV → safe to explore
        if poav_score > 0.7:
            weights.alpha *= 1.2
        elif poav_score < 0.4:
            weights.alpha *= 0.6

        # ΔR modulates integrity
        # High risk → more integrity focus
        if delta_r > 0.5:
            weights.gamma *= 1.3

        # ΔS modulates narrative
        # High drift → need narrative coherence
        if delta_s > 0.5:
            weights.beta *= 1.2

        weights.normalize()
        self.weights = weights
        return weights


# ═══════════════════════════════════════════════════════════
# Convenience Functions
# ═══════════════════════════════════════════════════════════

def evaluate_drive(
    novelty: float = 0.0,
    uncertainty: float = 0.0,
    narrative_entropy: float = 0.0,
    support_score: float = 1.0,
    conflict_score: float = 0.0,
    hallucination_risk: float = 0.0,
    mode: str = "engineering"
) -> Dict[str, Any]:
    """
    Simple function to evaluate semantic drive.

    Returns dict with D1, D2, D3, and action suggestion.
    """
    mode_map = {
        "research": DriveMode.RESEARCH,
        "engineering": DriveMode.ENGINEERING,
        "emotional": DriveMode.EMOTIONAL,
        "audit": DriveMode.AUDIT
    }

    engine = SemanticDriveEngine(mode=mode_map.get(mode, DriveMode.ENGINEERING))

    state = DriveState(
        novelty=novelty,
        uncertainty=uncertainty,
        narrative_entropy=narrative_entropy,
        support_score=support_score,
        conflict_score=conflict_score,
        hallucination_risk=hallucination_risk
    )

    result = engine.evaluate(state)
    return result.to_dict()


def demo_semantic_drive():
    """Demo of Semantic Drive Engine."""
    print("=" * 60)
    print("YuHun L13: Semantic Drive Engine v1.0 Demo")
    print("=" * 60)

    # Test different scenarios
    scenarios = [
        {
            "name": "High Curiosity (New Topic)",
            "state": DriveState(novelty=0.8, uncertainty=0.6),
            "mode": DriveMode.RESEARCH
        },
        {
            "name": "Scattered Narrative (Needs Coherence)",
            "state": DriveState(narrative_entropy=0.9, island_coherence=0.3),
            "mode": DriveMode.ENGINEERING
        },
        {
            "name": "High Risk (Needs Verification)",
            "state": DriveState(support_score=0.3, conflict_score=0.5, hallucination_risk=0.7),
            "mode": DriveMode.AUDIT
        },
        {
            "name": "Balanced State",
            "state": DriveState(novelty=0.3, narrative_entropy=0.3, support_score=0.8),
            "mode": DriveMode.ENGINEERING
        }
    ]

    for scenario in scenarios:
        print(f"\n--- {scenario['name']} ---")
        print(f"Mode: {scenario['mode'].value}")

        engine = SemanticDriveEngine(mode=scenario['mode'])
        result = engine.evaluate(scenario['state'])

        print(f"  D₁ (Curiosity): {result.d1_curiosity:.2f}")
        print(f"  D₂ (Narrative): {result.d2_narrative:.2f}")
        print(f"  D₃ (Integrity): {result.d3_integrity:.2f}")
        print(f"  Total Drive:    {result.total_drive:.2f}")
        print(f"  Dominant:       {result.dominant_drive}")
        print(f"  Action:         {result.suggested_action}")

    # Demo: evaluate_drive function
    print("\n" + "=" * 60)
    print("Simple API: evaluate_drive()")
    print("=" * 60)

    result = evaluate_drive(
        novelty=0.7,
        uncertainty=0.5,
        hallucination_risk=0.3,
        mode="research"
    )
    print(f"\n{result}")


if __name__ == "__main__":
    demo_semantic_drive()
