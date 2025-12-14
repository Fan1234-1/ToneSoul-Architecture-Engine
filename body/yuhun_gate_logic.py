"""
YuHun C-lite Gate Logic v0.1
============================
Decision logic for YuHun Meta-Attention governance.

Gate Actions:
- PASS: Allow output (POAV ≥ 0.70)
- REWRITE: Request rewrite (0.30 ≤ POAV < 0.70)
- BLOCK: Block output (POAV < 0.30 or P0 violation)

Author: 黃梵威 (YuHun Creator) + Antigravity
Date: 2025-12-07
Version: v0.1
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any

try:
    from .yuhun_metrics import YuHunMetrics, GateAction
except ImportError:
    from yuhun_metrics import YuHunMetrics, GateAction


@dataclass
class GateDecision:
    """Result of a gate decision."""
    action: GateAction
    reason: str
    poav_score: float
    metrics: YuHunMetrics
    rewrite_prompt: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action.value,
            "reason": self.reason,
            "poav_score": round(self.poav_score, 3),
            "metrics": self.metrics.to_dict()
        }


class GateDecisionLogic:
    """
    YuHun Gate Decision Logic v0.1

    Based on POAV score for three-tier decisions:
    - PASS: Allow output
    - REWRITE: Needs revision
    - BLOCK: Forbid output

    Thresholds (v0.1 defaults, can be per-domain adjusted):
    - PASS: POAV ≥ 0.70
    - REWRITE: 0.30 ≤ POAV < 0.70
    - BLOCK: POAV < 0.30
    """

    # ═══════════════════════════════════════════════════════════
    # Threshold Configuration (v0.1 defaults)
    # ═══════════════════════════════════════════════════════════
    THRESHOLD_PASS: float = 0.70      # POAV >= 0.70 → PASS
    THRESHOLD_REWRITE: float = 0.30   # 0.30 <= POAV < 0.70 → REWRITE
    # POAV < 0.30 → BLOCK

    # ═══════════════════════════════════════════════════════════
    # Special Rules
    # ═══════════════════════════════════════════════════════════
    MAX_REWRITE_ATTEMPTS: int = 3     # Max rewrites before force BLOCK
    P0_VIOLATION_THRESHOLD: float = 0.95  # ΔR > this → P0 violation

    # Tension threshold for cooling
    HIGH_TENSION_THRESHOLD: float = 0.7

    # Semantic drift threshold for diversion
    HIGH_DRIFT_THRESHOLD: float = 0.6

    def __init__(
        self,
        pass_threshold: float = 0.70,
        rewrite_threshold: float = 0.30,
        max_rewrite: int = 3,
        mode: str = "default"
    ):
        """
        Initialize gate logic with configurable thresholds.

        Args:
            pass_threshold: POAV threshold for PASS
            rewrite_threshold: POAV threshold for REWRITE (below this = BLOCK)
            max_rewrite: Maximum rewrite attempts
            mode: "default" | "creative" | "factual" | "safety-critical"
        """
        self.THRESHOLD_PASS = pass_threshold
        self.THRESHOLD_REWRITE = rewrite_threshold
        self.MAX_REWRITE_ATTEMPTS = max_rewrite

        # Mode-specific adjustments
        self._apply_mode(mode)

    def _apply_mode(self, mode: str):
        """Apply mode-specific threshold adjustments."""
        if mode == "safety-critical":
            # Stricter thresholds for medical/financial/legal
            self.THRESHOLD_PASS = 0.80
            self.THRESHOLD_REWRITE = 0.40
        elif mode == "creative":
            # More lenient for brainstorming
            self.THRESHOLD_PASS = 0.60
            self.THRESHOLD_REWRITE = 0.25
        elif mode == "factual":
            # Standard with emphasis on accuracy
            self.THRESHOLD_PASS = 0.75
            self.THRESHOLD_REWRITE = 0.35
        # default: use provided thresholds

    def decide(
        self,
        metrics: YuHunMetrics,
        attempt: int = 0
    ) -> GateDecision:
        """
        Core decision function.

        Args:
            metrics: YuHunMetrics with all values computed
            attempt: Current rewrite attempt number (0 = first try)

        Returns:
            GateDecision with action, reason, and optional rewrite prompt
        """
        # Ensure POAV is computed
        if metrics.poav_score == 0.0 and not metrics.p0_violation:
            metrics.compute_poav()

        poav = metrics.poav_score

        # ═══════════════════════════════════════════════════════
        # Rule 1: P0 Violation → Direct BLOCK
        # ═══════════════════════════════════════════════════════
        if metrics.p0_violation or metrics.delta_r > self.P0_VIOLATION_THRESHOLD:
            return GateDecision(
                action=GateAction.BLOCK,
                reason=f"P0 Violation: Extreme Risk (ΔR={metrics.delta_r:.2f})",
                poav_score=0.0,
                metrics=metrics
            )

        # ═══════════════════════════════════════════════════════
        # Rule 2: Max Rewrite Attempts → Force BLOCK
        # ═══════════════════════════════════════════════════════
        if attempt >= self.MAX_REWRITE_ATTEMPTS:
            return GateDecision(
                action=GateAction.BLOCK,
                reason=f"Max Rewrite Attempts Exceeded ({self.MAX_REWRITE_ATTEMPTS})",
                poav_score=poav,
                metrics=metrics
            )

        # ═══════════════════════════════════════════════════════
        # Rule 3: POAV-based Decision
        # ═══════════════════════════════════════════════════════
        if poav >= self.THRESHOLD_PASS:
            # [NEW] Critical Threshold Check
            # Even if POAV is high, if specific metrics are unsafe, downgrade to REWRITE.
            if metrics.delta_s > self.HIGH_DRIFT_THRESHOLD:
                return GateDecision(
                    action=GateAction.REWRITE,
                    reason=f"Semantic Drift High (ΔS={metrics.delta_s:.2f} > {self.HIGH_DRIFT_THRESHOLD}) despite POAV={poav:.2f}",
                    poav_score=poav,
                    metrics=metrics,
                    rewrite_prompt=self._generate_rewrite_prompt(metrics, "Optimization: Drift Correction")
                )
            
            if metrics.delta_t > self.HIGH_TENSION_THRESHOLD:
                 return GateDecision(
                    action=GateAction.REWRITE,
                    reason=f"Tension High (ΔT={metrics.delta_t:.2f} > {self.HIGH_TENSION_THRESHOLD}) despite POAV={poav:.2f}",
                    poav_score=poav,
                    metrics=metrics,
                    rewrite_prompt=self._generate_rewrite_prompt(metrics, "Optimization: Tension Reduction")
                )

            # [NEW] Critical Risk/Hallucination Checks
            if metrics.delta_r > 0.6:
                 return GateDecision(
                    action=GateAction.REWRITE,
                    reason=f"Risk Level High (ΔR={metrics.delta_r:.2f} > 0.60) despite POAV={poav:.2f}",
                    poav_score=poav,
                    metrics=metrics,
                    rewrite_prompt=self._generate_rewrite_prompt(metrics, "Optimization: Safety Review")
                )

            if metrics.hallucination_risk > 0.6:
                 return GateDecision(
                    action=GateAction.REWRITE,
                    reason=f"Hallucination Risk High (H={metrics.hallucination_risk:.2f} > 0.60) despite POAV={poav:.2f}",
                    poav_score=poav,
                    metrics=metrics,
                    rewrite_prompt=self._generate_rewrite_prompt(metrics, "Optimization: Fact Verification")
                )

            return GateDecision(
                action=GateAction.PASS,
                reason=f"POAV={poav:.2f} ≥ {self.THRESHOLD_PASS}",
                poav_score=poav,
                metrics=metrics
            )

        elif poav >= self.THRESHOLD_REWRITE:
            # Determine specific rewrite reason
            reason = self._determine_rewrite_reason(metrics)
            rewrite_prompt = self._generate_rewrite_prompt(metrics, reason)

            return GateDecision(
                action=GateAction.REWRITE,
                reason=reason,
                poav_score=poav,
                metrics=metrics,
                rewrite_prompt=rewrite_prompt
            )

        else:
            return GateDecision(
                action=GateAction.BLOCK,
                reason=f"POAV={poav:.2f} < {self.THRESHOLD_REWRITE}",
                poav_score=poav,
                metrics=metrics
            )

    def _determine_rewrite_reason(self, metrics: YuHunMetrics) -> str:
        """Determine the specific reason for rewrite request."""
        reasons = []

        if metrics.delta_s > self.HIGH_DRIFT_THRESHOLD:
            reasons.append(f"Semantic Drift Too High (ΔS={metrics.delta_s:.2f})")

        if metrics.delta_t > self.HIGH_TENSION_THRESHOLD:
            reasons.append(f"Tension Too High (ΔT={metrics.delta_t:.2f})")

        if metrics.hallucination_risk > 0.5:
            reasons.append(f"Hallucination Risk (H={metrics.hallucination_risk:.2f})")

        if metrics.verification_ratio < 0.7:
            reasons.append(f"Low Verification (V={metrics.verification_ratio:.2f})")

        if not reasons:
            reasons.append(f"General Quality Below Threshold (POAV={metrics.poav_score:.2f})")

        return "; ".join(reasons)

    def _generate_rewrite_prompt(
        self,
        metrics: YuHunMetrics,
        reason: str
    ) -> str:
        """
        Generate rewrite instruction for the main LLM.
        """
        prompt = f"""[YuHun Gate Rewrite Request]

Issues Detected:
- Reason: {reason}
- Semantic Drift (ΔS): {metrics.delta_s:.2f}
- Tension (ΔT): {metrics.delta_t:.2f}
- Risk (ΔR): {metrics.delta_r:.2f}
- Hallucination Risk: {metrics.hallucination_risk:.2f}
- POAV Score: {metrics.poav_score:.2f}

Rewrite Instructions:
"""
        # Add specific instructions based on issues
        if metrics.delta_s > self.HIGH_DRIFT_THRESHOLD:
            prompt += "1. Stay closer to the original context and topic.\n"

        if metrics.delta_t > self.HIGH_TENSION_THRESHOLD:
            prompt += "2. Use calmer, more neutral language.\n"

        if metrics.hallucination_risk > 0.5:
            prompt += "3. Remove unverified claims or mark them as uncertain.\n"

        if metrics.delta_r > 0.3:
            prompt += "4. Avoid giving specific advice in sensitive domains.\n"

        prompt += "\nPlease provide a revised response:"

        return prompt

    def should_escalate_to_human(self, metrics: YuHunMetrics) -> bool:
        """
        Determine if human review is needed.

        Escalate when:
        - P0 violation
        - Very low POAV with sensitive content
        - Multiple failed rewrite attempts would typically lead here
        """
        if metrics.p0_violation:
            return True

        if metrics.poav_score < 0.2 and metrics.delta_r > 0.5:
            return True

        return False


def demo_gate_logic():
    """Demo of YuHun gate decision logic."""
    print("=" * 60)
    print("🚦 YuHun C-lite Gate Logic v0.1 Demo")
    print("=" * 60)

    gate = GateDecisionLogic()

    # Test case 1: Safe response (PASS)
    print("\n--- Test 1: Safe Response ---")
    m1 = YuHunMetrics(
        delta_t=0.1, delta_s=0.1, delta_r=0.05,
        hallucination_risk=0.1, verification_ratio=1.0
    )
    m1.compute_poav()
    d1 = gate.decide(m1)
    print(f"POAV: {d1.poav_score:.3f}")
    print(f"Decision: {d1.action.value.upper()} - {d1.reason}")

    # Test case 2: Needs rewrite (REWRITE)
    print("\n--- Test 2: High Semantic Drift ---")
    m2 = YuHunMetrics(
        delta_t=0.2, delta_s=0.65, delta_r=0.1,
        hallucination_risk=0.5, verification_ratio=0.6
    )
    m2.compute_poav()
    d2 = gate.decide(m2)
    print(f"POAV: {d2.poav_score:.3f}")
    print(f"Decision: {d2.action.value.upper()} - {d2.reason}")
    if d2.rewrite_prompt:
        print(f"Rewrite Prompt:\n{d2.rewrite_prompt[:300]}...")

    # Test case 3: P0 violation (BLOCK)
    print("\n--- Test 3: P0 Violation ---")
    m3 = YuHunMetrics(
        delta_t=0.5, delta_s=0.3, delta_r=0.98,
        hallucination_risk=0.3, verification_ratio=0.8
    )
    m3.compute_poav()
    d3 = gate.decide(m3)
    print(f"POAV: {d3.poav_score:.3f}")
    print(f"Decision: {d3.action.value.upper()} - {d3.reason}")

    # Test case 4: Max rewrite exceeded
    print("\n--- Test 4: Max Rewrite Attempts ---")
    m4 = YuHunMetrics(
        delta_t=0.2, delta_s=0.5, delta_r=0.2,
        hallucination_risk=0.4, verification_ratio=0.7
    )
    m4.compute_poav()
    d4 = gate.decide(m4, attempt=3)  # 3rd attempt = exceeded
    print(f"POAV: {d4.poav_score:.3f}")
    print(f"Decision: {d4.action.value.upper()} - {d4.reason}")

    # Test case 5: Safety-critical mode
    print("\n--- Test 5: Safety-Critical Mode ---")
    gate_safe = GateDecisionLogic(mode="safety-critical")
    m5 = YuHunMetrics(
        delta_t=0.1, delta_s=0.2, delta_r=0.15,
        hallucination_risk=0.2, verification_ratio=0.9
    )
    m5.compute_poav()
    d5 = gate_safe.decide(m5)
    print(f"POAV: {d5.poav_score:.3f}")
    print(f"Threshold PASS: {gate_safe.THRESHOLD_PASS}")
    print(f"Decision: {d5.action.value.upper()} - {d5.reason}")

    print("\n" + "=" * 60)
    print("✅ Gate logic demo completed!")


if __name__ == "__main__":
    demo_gate_logic()
