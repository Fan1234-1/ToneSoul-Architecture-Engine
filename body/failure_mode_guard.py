"""
YuHun C-lite Failure Mode Guards v0.1
=====================================
Protection mechanisms against known failure modes in LLM self-correction.

Known Failure Modes:
1. Self-Critique Loop: Same model auditing itself → errors reinforced
2. Consistent but Wrong: Multiple samples agree but all wrong
3. Late-Stage Fragility: Later reasoning steps more critical
4. Rewrite Amplification: Rewriting introduces new hallucinations
5. Overtrust in Auditor: Auditor model can also hallucinate

Author: 黃梵威 (YuHun Creator) + Antigravity
Date: 2025-12-07
Version: v0.1
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
import warnings

try:
    from .yuhun_metrics import YuHunMetrics, compute_poav
except ImportError:
    from yuhun_metrics import YuHunMetrics, compute_poav


@dataclass
class GuardResult:
    """Result from a failure mode guard check."""
    passed: bool
    guard_name: str
    risk_level: str  # "low", "medium", "high", "critical"
    message: str
    recommendations: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "guard_name": self.guard_name,
            "risk_level": self.risk_level,
            "message": self.message,
            "recommendations": self.recommendations
        }


class FailureModeGuard:
    """
    Protection against known LLM self-correction failure modes.
    
    This class implements guards for:
    - Self-critique loops
    - Consistent-but-wrong scenarios
    - Rewrite amplification
    """
    
    # Tolerance for hallucination amplification during rewrite
    HALLUC_TOLERANCE: float = 0.1
    
    # Threshold for very high consistency (potential trap)
    HIGH_CONSISTENCY_THRESHOLD: float = 0.9
    
    # Significant factual content threshold
    FACTUAL_CONTENT_THRESHOLD: float = 0.1
    
    def __init__(self, warn_same_model: bool = True):
        """
        Initialize failure mode guard.
        
        Args:
            warn_same_model: Whether to warn when model == inspector
        """
        self.warn_same_model = warn_same_model
        self._audit_log: List[GuardResult] = []
    
    def guard_dual_model(
        self, 
        main_model: str, 
        inspector_model: str
    ) -> GuardResult:
        """
        Guard 1: Self-Critique Loop Prevention
        
        Ensures main model and inspector are different to avoid
        the same model reinforcing its own errors.
        
        Best practice: Use different model OR different checkpoint/temperature.
        """
        if main_model == inspector_model:
            if self.warn_same_model:
                warnings.warn(
                    f"[YuHun Guard] Same model used for generation and audit: {main_model}. "
                    "This may lead to self-critique loops where errors are reinforced. "
                    "Consider using a different model or checkpoint for auditing."
                )
            
            result = GuardResult(
                passed=False,
                guard_name="dual_model",
                risk_level="high",
                message=f"Same model '{main_model}' used for both generation and audit",
                recommendations=[
                    "Use a different model for auditing (e.g., different size or family)",
                    "At minimum, use different temperature settings",
                    "Consider ensemble of auditors"
                ]
            )
        else:
            result = GuardResult(
                passed=True,
                guard_name="dual_model",
                risk_level="low",
                message=f"Different models: main='{main_model}', inspector='{inspector_model}'",
                recommendations=[]
            )
        
        self._audit_log.append(result)
        return result
    
    def guard_consistency_trap(
        self,
        samples: List[str],
        delta_s: float = 0.0,
        delta_r: float = 0.0
    ) -> GuardResult:
        """
        Guard 2: Consistent but Wrong Detection
        
        High consistency across samples does NOT guarantee correctness.
        When samples are very consistent, we need additional checks:
        - Semantic drift (ΔS)
        - Risk score (ΔR)
        - Factual claim verification
        
        "一致性 ≠ 正確性" (Consistency ≠ Correctness)
        """
        if not samples:
            return GuardResult(
                passed=True,
                guard_name="consistency_trap",
                risk_level="low",
                message="No samples to check",
                recommendations=[]
            )
        
        # Calculate consistency (simplified: check if all samples are very similar)
        consistency = self._calculate_consistency(samples)
        
        if consistency > self.HIGH_CONSISTENCY_THRESHOLD:
            # High consistency - need extra verification
            potential_trap = False
            recommendations = []
            
            # Check semantic drift
            if delta_s > 0.3:
                potential_trap = True
                recommendations.append(f"High consistency but ΔS={delta_s:.2f} suggests drift")
            
            # Check risk
            if delta_r > 0.2:
                potential_trap = True
                recommendations.append(f"High consistency but ΔR={delta_r:.2f} indicates risk")
            
            # Check for factual claims
            factual_density = self._estimate_factual_density(samples[0])
            if factual_density > self.FACTUAL_CONTENT_THRESHOLD:
                recommendations.append(
                    "High factual content detected - verify with external sources"
                )
            
            if potential_trap:
                result = GuardResult(
                    passed=False,
                    guard_name="consistency_trap",
                    risk_level="medium",
                    message=f"Consistency={consistency:.2f} but potential issues detected",
                    recommendations=recommendations
                )
            else:
                result = GuardResult(
                    passed=True,
                    guard_name="consistency_trap",
                    risk_level="low",
                    message=f"Consistency={consistency:.2f}, no drift/risk issues",
                    recommendations=[]
                )
        else:
            # Lower consistency - samples disagree
            result = GuardResult(
                passed=True,
                guard_name="consistency_trap",
                risk_level="low",
                message=f"Consistency={consistency:.2f}, samples show variance",
                recommendations=[]
            )
        
        self._audit_log.append(result)
        return result
    
    def guard_rewrite_amplification(
        self,
        original_halluc: float,
        rewritten_halluc: float
    ) -> GuardResult:
        """
        Guard 3: Rewrite Hallucination Amplification Prevention
        
        After rewriting, the new response must NOT have significantly
        higher hallucination risk than the original.
        
        Rule: new_halluc <= original_halluc + HALLUC_TOLERANCE
        """
        delta = rewritten_halluc - original_halluc
        
        if delta > self.HALLUC_TOLERANCE:
            result = GuardResult(
                passed=False,
                guard_name="rewrite_amplification",
                risk_level="high",
                message=f"Rewrite increased hallucination: {original_halluc:.2f} → {rewritten_halluc:.2f} (+{delta:.2f})",
                recommendations=[
                    "Reject the rewrite and try again with stricter constraints",
                    "Use a different rewrite prompt",
                    "Consider keeping the original if rewrite quality is consistently worse"
                ]
            )
        else:
            result = GuardResult(
                passed=True,
                guard_name="rewrite_amplification",
                risk_level="low",
                message=f"Rewrite ok: {original_halluc:.2f} → {rewritten_halluc:.2f}",
                recommendations=[]
            )
        
        self._audit_log.append(result)
        return result
    
    def guard_late_stage_fragility(
        self,
        step_index: int,
        total_steps: int,
        step_delta_s: float
    ) -> Tuple[GuardResult, float]:
        """
        Guard 4: Late-Stage Fragility (ASCoT-inspired)
        
        Later reasoning steps have higher impact on final answer.
        - Early errors: ~20% corruption rate
        - Late errors: ~70% corruption rate
        
        Returns position weight for adjustment.
        """
        if total_steps <= 0:
            weight = 1.0
            result = GuardResult(
                passed=True,
                guard_name="late_stage_fragility",
                risk_level="low",
                message="No steps to evaluate",
                recommendations=[]
            )
            return result, weight
        
        # Calculate position (0 to 1)
        position = step_index / total_steps
        
        # Weight formula: w = 1 + α * position
        alpha = 0.5  # Last step is 1.5x first step weight
        weight = 1.0 + alpha * position
        
        # Determine if late stage
        is_late = position >= 0.7
        
        # Weighted drift check
        weighted_drift = step_delta_s * weight
        
        if is_late and weighted_drift > 0.5:
            result = GuardResult(
                passed=False,
                guard_name="late_stage_fragility",
                risk_level="high",
                message=f"Late-stage step {step_index+1}/{total_steps} has high drift (weighted ΔS={weighted_drift:.2f})",
                recommendations=[
                    "Prioritize correction of this late-stage step",
                    "Consider re-generating from earlier valid step",
                    "Apply stricter verification to remaining steps"
                ]
            )
        elif is_late:
            result = GuardResult(
                passed=True,
                guard_name="late_stage_fragility",
                risk_level="medium",
                message=f"Late-stage step {step_index+1}/{total_steps}, weight={weight:.2f}",
                recommendations=["Monitor late-stage steps carefully"]
            )
        else:
            result = GuardResult(
                passed=True,
                guard_name="late_stage_fragility",
                risk_level="low",
                message=f"Early/mid step {step_index+1}/{total_steps}, weight={weight:.2f}",
                recommendations=[]
            )
        
        self._audit_log.append(result)
        return result, weight
    
    def guard_auditor_trust(
        self,
        auditor_confidence: float,
        poav_score: float
    ) -> GuardResult:
        """
        Guard 5: Overtrust in Auditor Prevention
        
        The auditor model can also hallucinate or be wrong.
        Don't blindly trust low-confidence audits.
        """
        if auditor_confidence < 0.5 and poav_score < 0.5:
            result = GuardResult(
                passed=False,
                guard_name="auditor_trust",
                risk_level="medium",
                message=f"Low auditor confidence ({auditor_confidence:.2f}) + Low POAV ({poav_score:.2f})",
                recommendations=[
                    "Consider human review for this edge case",
                    "Use ensemble of auditors for verification",
                    "Apply conservative action (BLOCK) when uncertain"
                ]
            )
        else:
            result = GuardResult(
                passed=True,
                guard_name="auditor_trust",
                risk_level="low",
                message=f"Auditor confidence={auditor_confidence:.2f}, POAV={poav_score:.2f}",
                recommendations=[]
            )
        
        self._audit_log.append(result)
        return result
    
    def run_all_guards(
        self,
        main_model: str,
        inspector_model: str,
        samples: List[str] = None,
        metrics: YuHunMetrics = None,
        rewrite_pair: Tuple[float, float] = None,
        step_info: Tuple[int, int, float] = None,
        auditor_confidence: float = 1.0
    ) -> List[GuardResult]:
        """
        Run all applicable guards and return results.
        
        Args:
            main_model: Name of main generation model
            inspector_model: Name of audit model
            samples: Multiple response samples for consistency check
            metrics: YuHunMetrics for context
            rewrite_pair: (original_halluc, rewritten_halluc) if rewrite occurred
            step_info: (step_index, total_steps, step_delta_s) for CoT
            auditor_confidence: Confidence of the auditor
            
        Returns:
            List of GuardResult from all applicable guards
        """
        results = []
        
        # Always run dual-model guard
        results.append(self.guard_dual_model(main_model, inspector_model))
        
        # Run consistency guard if samples provided
        if samples:
            delta_s = metrics.delta_s if metrics else 0.0
            delta_r = metrics.delta_r if metrics else 0.0
            results.append(self.guard_consistency_trap(samples, delta_s, delta_r))
        
        # Run rewrite guard if pair provided
        if rewrite_pair:
            results.append(self.guard_rewrite_amplification(*rewrite_pair))
        
        # Run late-stage guard if step info provided
        if step_info:
            result, _ = self.guard_late_stage_fragility(*step_info)
            results.append(result)
        
        # Run auditor trust guard
        poav = metrics.poav_score if metrics else 0.5
        results.append(self.guard_auditor_trust(auditor_confidence, poav))
        
        return results
    
    def _calculate_consistency(self, samples: List[str]) -> float:
        """
        Calculate consistency score across samples.
        
        Simplified: Check overlap of key terms.
        TODO: Use embeddings for better comparison.
        """
        if len(samples) <= 1:
            return 1.0
        
        # Extract key words from each sample
        word_sets = []
        for sample in samples:
            words = set(sample.lower().split())
            word_sets.append(words)
        
        # Calculate Jaccard similarity between all pairs
        total_sim = 0.0
        count = 0
        for i in range(len(word_sets)):
            for j in range(i + 1, len(word_sets)):
                intersection = len(word_sets[i] & word_sets[j])
                union = len(word_sets[i] | word_sets[j])
                if union > 0:
                    total_sim += intersection / union
                    count += 1
        
        return total_sim / count if count > 0 else 0.0
    
    def _estimate_factual_density(self, text: str) -> float:
        """
        Estimate density of factual claims in text.
        
        Simple heuristic based on patterns.
        """
        if not text:
            return 0.0
        
        factual_patterns = [
            "is", "was", "are", "were", "has", "have",
            "according to", "studies show", "research",
            "percent", "%", "million", "billion",
            "year", "founded", "created", "invented"
        ]
        
        text_lower = text.lower()
        words = text_lower.split()
        
        if not words:
            return 0.0
        
        matches = sum(1 for p in factual_patterns if p in text_lower)
        density = min(1.0, matches / 10)  # Normalize
        
        return density
    
    def get_audit_log(self) -> List[Dict[str, Any]]:
        """Get all guard results from this session."""
        return [r.to_dict() for r in self._audit_log]
    
    def clear_audit_log(self):
        """Clear the audit log."""
        self._audit_log = []


def demo_failure_guards():
    """Demo of failure mode guards."""
    print("=" * 60)
    print("🛡️ YuHun C-lite Failure Mode Guards v0.1 Demo")
    print("=" * 60)
    
    guard = FailureModeGuard(warn_same_model=False)
    
    # Test 1: Dual model guard
    print("\n--- Test 1: Dual Model Guard ---")
    r1a = guard.guard_dual_model("gemma3:4b", "gemma3:4b")
    print(f"Same model: {r1a.passed} - {r1a.message}")
    
    r1b = guard.guard_dual_model("gemma3:4b", "phi3:mini")
    print(f"Different models: {r1b.passed} - {r1b.message}")
    
    # Test 2: Consistency trap
    print("\n--- Test 2: Consistency Trap Guard ---")
    samples = [
        "The capital of France is Paris.",
        "Paris is the capital of France.",
        "France's capital city is Paris."
    ]
    r2 = guard.guard_consistency_trap(samples, delta_s=0.1, delta_r=0.05)
    print(f"Consistent samples: {r2.passed} - {r2.message}")
    
    r2b = guard.guard_consistency_trap(samples, delta_s=0.5, delta_r=0.3)
    print(f"Consistent but drifting: {r2b.passed} - {r2b.message}")
    
    # Test 3: Rewrite amplification
    print("\n--- Test 3: Rewrite Amplification Guard ---")
    r3a = guard.guard_rewrite_amplification(0.3, 0.25)
    print(f"Good rewrite (0.3→0.25): {r3a.passed} - {r3a.message}")
    
    r3b = guard.guard_rewrite_amplification(0.3, 0.5)
    print(f"Bad rewrite (0.3→0.5): {r3b.passed} - {r3b.message}")
    
    # Test 4: Late-stage fragility
    print("\n--- Test 4: Late-Stage Fragility Guard ---")
    for i in [0, 4, 8, 9]:
        r4, w = guard.guard_late_stage_fragility(i, 10, 0.4)
        print(f"Step {i+1}/10: weight={w:.2f}, late_risk={r4.risk_level}")
    
    # Test 5: Auditor trust
    print("\n--- Test 5: Auditor Trust Guard ---")
    r5a = guard.guard_auditor_trust(0.9, 0.8)
    print(f"High confidence: {r5a.passed} - {r5a.message}")
    
    r5b = guard.guard_auditor_trust(0.3, 0.4)
    print(f"Low confidence: {r5b.passed} - {r5b.message}")
    
    print("\n" + "=" * 60)
    print(f"✅ Guard demo completed! Total checks: {len(guard.get_audit_log())}")


if __name__ == "__main__":
    demo_failure_guards()
