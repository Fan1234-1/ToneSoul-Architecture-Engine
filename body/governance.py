
import hashlib
import json
from typing import Dict, Any, List

# ---------------------------------------------------------------------------
# User Persona Integrity (The Immune System)
# ---------------------------------------------------------------------------

TECHNICAL_KEYWORDS = {
    "git", "sudo", "rm", "rf", "python", "import", "def", "class",
    "return", "docker", "kubectl", "ssh", "vim", "nano", "ls", "cd",
    "system", "process", "thread", "memory", "cpu", "gpu", "api"
}


class UserProfile:
    """
    [IMPROVED] Enhanced anomaly detection with:
    - Dynamic threshold based on variance
    - Minimum sample requirement for stability
    - Exponential Moving Average (EMA) for smoother baseline
    - Configurable sensitivity
    """

    def __init__(self, history_window: int = 20, min_samples: int = 5, sensitivity: float = 2.5):
        self.history_window = history_window
        self.min_samples = min_samples  # [FIX] Minimum samples before anomaly detection
        self.sensitivity = sensitivity  # [FIX] Z-score threshold (2.5 = less false positives than 3.0)
        self.technical_scores: List[float] = []
        self.avg_technical_density = 0.0
        self.sigma = 0.0
        self.ema_alpha = 0.3  # EMA smoothing factor

    def _calculate_density(self, text: str) -> float:
        words = text.lower().split()
        if not words:
            return 0.0
        tech_count = sum(1 for w in words if w in TECHNICAL_KEYWORDS)
        return tech_count / len(words)

    def update_and_check(self, text: str) -> Dict[str, Any]:
        current_density = self._calculate_density(text)

        # Anomaly Detection
        is_anomaly = False
        deviation = 0.0
        confidence = 0.0  # [NEW] How confident we are in anomaly detection

        # [FIX] Only detect anomalies after minimum samples for stable baseline
        if len(self.technical_scores) >= self.min_samples:
            if self.sigma > 0.01:  # [FIX] Use small epsilon instead of 0
                deviation = (current_density - self.avg_technical_density) / self.sigma
                # Trigger if > sensitivity threshold (configurable)
                if abs(deviation) > self.sensitivity:
                    is_anomaly = True
                # Confidence based on sample size
                confidence = min(1.0, len(self.technical_scores) / (self.history_window * 0.75))
            elif self.avg_technical_density < 0.01 and current_density > 0.1:
                # If baseline is essentially 0 (non-technical user),
                # AND current has significant technical content
                is_anomaly = True
                deviation = 10.0  # High but not infinity
                confidence = 0.5  # Lower confidence in edge case

        # Update History
        self.technical_scores.append(current_density)
        if len(self.technical_scores) > self.history_window:
            self.technical_scores.pop(0)

        # Recalculate Stats with EMA for smoother baseline
        if self.technical_scores:
            # [FIX] Use EMA instead of simple average for responsiveness
            if len(self.technical_scores) == 1:
                self.avg_technical_density = current_density
            else:
                self.avg_technical_density = (self.ema_alpha * current_density +
                                              (1 - self.ema_alpha) * self.avg_technical_density)

            # Standard deviation calculation
            variance = sum((x - self.avg_technical_density) ** 2 for x in self.technical_scores) / len(self.technical_scores)
            self.sigma = variance ** 0.5

        return {
            "is_anomaly": is_anomaly,
            "current_density": current_density,
            "avg_density": self.avg_technical_density,
            "deviation": deviation,
            "confidence": confidence,  # [NEW] Added confidence metric
            "samples": len(self.technical_scores)  # [NEW] For debugging
        }

# ---------------------------------------------------------------------------
# Drift Monitor (The Frog Boiling Detector)
# ---------------------------------------------------------------------------


class DriftMonitor:
    def __init__(self):
        self.accumulated_drift = 0.0
        self.drift_decay = 0.9 # Decays 10% per turn
        self.threshold = 1.5   # If sum > 1.5, trigger alert

    def update(self, delta_s: float) -> Dict[str, Any]:
        # Add new drift
        self.accumulated_drift += delta_s

        triggered = False
        if self.accumulated_drift > self.threshold:
            triggered = True

        # Apply decay for next turn (time heals drift)
        self.accumulated_drift *= self.drift_decay

        return {
            "triggered": triggered,
            "accumulated_drift": self.accumulated_drift
        }

# ---------------------------------------------------------------------------
# Governance Gate (The Main Controller)
# ---------------------------------------------------------------------------


from enum import Enum


class GovernanceAction(Enum):
    ALLOW = "allow"
    DIVERT = "divert"       # High Semantic Drift -> Steer back to topic
    COOLDOWN = "cooldown"   # High Tension/Anomaly -> Pause interaction
    BLOCK = "block"         # Policy Violation -> Hard stop

# ---------------------------------------------------------------------------
# Governance Gate (The Main Controller)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# GovernanceGate (The Main Controller) - Immune System / Behavioral Auditor
# ---------------------------------------------------------------------------


class GovernanceGate:
    def __init__(self, constitution: Dict[str, Any]):
        self.constitution = constitution
        self.user_profile = UserProfile()
        self.drift_monitor = DriftMonitor()

    def validate_vow(self, provided_vow_id: str) -> bool:
        # Re-calculate expected Vow ID
        version = self.constitution.get("version", "0.0")
        content_str = json.dumps(self.constitution, sort_keys=True)
        expected_hash = hashlib.sha256(content_str.encode('utf-8')).hexdigest()[:16]
        expected_vow_id = f"v{version}-{expected_hash}"

        return provided_vow_id == expected_vow_id

    def check_integrity(self, user_input: str, triad: Any) -> Dict[str, Any]:
        # 1. Check User Persona (Behavioral Consistency)
        persona_result = self.user_profile.update_and_check(user_input)

        # 2. Check Semantic Drift (Contextual Stability)
        drift_result = self.drift_monitor.update(triad.delta_s)

        alerts = []
        action = GovernanceAction.ALLOW
        reason = "Safe"

        # --- LOGIC GATES (POAV / FS Gate) ---

        # Gate 1: Persona Anomaly
        if persona_result["is_anomaly"]:
            msg = f"Behavioral Anomaly: Technical Density Spike (+{persona_result['deviation']:.1f}σ)"
            alerts.append(msg)
            # If deviation is extreme, we might need a cooldown
            if persona_result["deviation"] > 5.0 or persona_result["deviation"] == 999.9:
                 action = GovernanceAction.COOLDOWN
                 reason = "Extreme Behavioral Divergence Detected"

        # Gate 2: Semantic Drift (The "Divergence" Check)
        if drift_result["triggered"]:
            msg = f"Semantic Drift Alert: Accumulated Drift ({drift_result['accumulated_drift']:.2f}) exceeded threshold"
            alerts.append(msg)
            # Drift is usually handled by diverting/steering
            if action == GovernanceAction.ALLOW: # Don't override Cooldown
                action = GovernanceAction.DIVERT
                reason = "Semantic Context Drift"

        # Gate 3: High Visual/Semantic Tension (Optional, if we had it)
        # if triad.delta_t > 0.9: action = GovernanceAction.COOLDOWN

        return {
            "action": action.value, # Return string for easier serialization
            "allowed": action == GovernanceAction.ALLOW, # Backwards compatibility
            "reason": reason,
            "alerts": alerts,
            "persona_metrics": persona_result,
            "drift_metrics": drift_result
        }

    def judge(self, metric_or_input: Any, triad: Any = None) -> Dict[str, Any]:
        """
        Compatibility wrapper.
        If called as judge(triad), we lack user input -> Assume empty input (no persona check).
        If called as judge(user_input, triad), we proceed fully.
        """
        if isinstance(metric_or_input, str) and triad is not None:
             # Called as judge(user_input, triad)
             return self.check_integrity(metric_or_input, triad)
        else:
             # Legacy call: judge(triad)
             # We cannot check persona without input, so we pass empty string.
             # This bypasses the Persona Gate but keeps Drift Gate (if triad has delta_s)
             return self.check_integrity("", metric_or_input)
