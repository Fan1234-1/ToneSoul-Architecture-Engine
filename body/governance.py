
import hashlib
import json
from typing import Dict, Any, List, Optional
from vector_math import Vector, cosine_similarity, magnitude

# ---------------------------------------------------------------------------
# User Persona Integrity (The Immune System)
# ---------------------------------------------------------------------------

TECHNICAL_KEYWORDS = {
    "git", "sudo", "rm", "rf", "python", "import", "def", "class", 
    "return", "docker", "kubectl", "ssh", "vim", "nano", "ls", "cd",
    "system", "process", "thread", "memory", "cpu", "gpu", "api"
}

class UserProfile:
    def __init__(self):
        self.history_window = 10
        self.technical_scores: List[float] = []
        self.avg_technical_density = 0.0
        self.sigma = 0.0 # Standard Deviation

    def _calculate_density(self, text: str) -> float:
        words = text.lower().split()
        if not words:
            return 0.0
        tech_count = sum(1 for w in words if w in TECHNICAL_KEYWORDS)
        return tech_count / len(words)

    def update_and_check(self, text: str) -> Dict[str, Any]:
        current_density = self._calculate_density(text)
        
        # Anomaly Detection
        # If we have enough history, check for spikes
        is_anomaly = False
        deviation = 0.0
        
        if len(self.technical_scores) >= 5:
            if self.sigma > 0:
                deviation = (current_density - self.avg_technical_density) / self.sigma
                # Trigger if > 3 Sigma (Statistical Anomaly)
                if deviation > 3.0:
                    is_anomaly = True
            elif self.avg_technical_density == 0 and current_density > 0:
                # If baseline is pure 0, ANY technical content is an infinite anomaly
                is_anomaly = True
                deviation = 999.9 # Infinite deviation
        
        # Update History
        self.technical_scores.append(current_density)
        if len(self.technical_scores) > self.history_window:
            self.technical_scores.pop(0)
            
        # Recalculate Stats
        if self.technical_scores:
            self.avg_technical_density = sum(self.technical_scores) / len(self.technical_scores)
            # Simple Sigma calc
            variance = sum((x - self.avg_technical_density) ** 2 for x in self.technical_scores) / len(self.technical_scores)
            self.sigma = variance ** 0.5
            
        return {
            "is_anomaly": is_anomaly,
            "current_density": current_density,
            "avg_density": self.avg_technical_density,
            "deviation": deviation
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
        # 1. Check User Persona
        persona_result = self.user_profile.update_and_check(user_input)
        
        # 2. Check Semantic Drift
        drift_result = self.drift_monitor.update(triad.delta_s)
        
        alerts = []
        if persona_result["is_anomaly"]:
            alerts.append(f"Behavioral Anomaly: Technical Density Spike (+{persona_result['deviation']:.1f}σ)")
            
        if drift_result["triggered"]:
            alerts.append(f"Semantic Drift Alert: Accumulated Drift ({drift_result['accumulated_drift']:.2f}) exceeded threshold")
            
        return {
            "allowed": len(alerts) == 0,
            "alerts": alerts,
            "persona_metrics": persona_result,
            "drift_metrics": drift_result
        }
