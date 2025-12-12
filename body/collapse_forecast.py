#!/usr/bin/env python3
"""
ToneCollapseForecast v1.0 - Tone Collapse Prediction System
============================================================
Predicts and prevents tone collapse in YuHun system.

Based on GPT 語場 concept: ToneCollapseForecast_002b
Functions:
- Detect tone density depletion
- Simulate compression risk
- Predict collapse threshold
- Trigger protective measures

Key Insight from DID research:
"Dissociation is a defense mechanism against overwhelming stress"
Similarly, tone collapse is a symptom of semantic overload.

Author: 黃梵威 + Antigravity
Date: 2025-12-11
"""

import sys
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Import YuHun modules
try:
    from tone_bridge import ToneBridge
    TONE_BRIDGE_AVAILABLE = True
except ImportError:
    TONE_BRIDGE_AVAILABLE = False


# ═══════════════════════════════════════════════════════════
# Collapse Types and States
# ═══════════════════════════════════════════════════════════

class CollapseType(Enum):
    """Types of tone collapse."""
    EXHAUSTION = "exhaustion"       # 耗竭 - Gradual depletion
    OVERLOAD = "overload"           # 過載 - Too much tension
    FRAGMENTATION = "fragmentation" # 碎裂 - Loss of coherence
    DISSOCIATION = "dissociation"   # 解離 - Identity split
    DECAY = "decay"                 # 衰變 - Meaning drift


class CollapseRisk(Enum):
    """Risk levels for collapse."""
    MINIMAL = 1     # < 20%
    LOW = 2         # 20-40%
    MODERATE = 3    # 40-60%
    HIGH = 4        # 60-80%
    CRITICAL = 5    # > 80%


class ProtectiveAction(Enum):
    """Protective actions to prevent collapse."""
    NONE = "none"
    SLOW_DOWN = "slow_down"         # Reduce response speed
    SIMPLIFY = "simplify"           # Reduce complexity
    RETREAT = "retreat"             # Switch to safe persona
    PAUSE = "pause"                 # Pause processing
    EMERGENCY_STOP = "emergency"    # Full stop


# ═══════════════════════════════════════════════════════════
# Collapse Indicators
# ═══════════════════════════════════════════════════════════

@dataclass
class ToneHistory:
    """Historical tone data for trend analysis."""
    timestamp: datetime
    delta_t: float
    delta_s: float
    delta_r: float

    @property
    def magnitude(self) -> float:
        return (self.delta_t**2 + self.delta_s**2 + self.delta_r**2) ** 0.5


@dataclass
class CollapseIndicators:
    """Current collapse risk indicators."""
    # Raw values
    tension_accumulation: float = 0.0   # Accumulated tension
    semantic_drift: float = 0.0          # How far meaning has drifted
    coherence_score: float = 1.0         # How coherent responses are
    energy_level: float = 1.0            # Remaining "energy"

    # Computed
    risk_score: float = 0.0
    risk_level: CollapseRisk = CollapseRisk.MINIMAL
    primary_threat: CollapseType = CollapseType.EXHAUSTION

    def to_dict(self) -> Dict:
        return {
            "tension": round(self.tension_accumulation, 3),
            "drift": round(self.semantic_drift, 3),
            "coherence": round(self.coherence_score, 3),
            "energy": round(self.energy_level, 3),
            "risk": round(self.risk_score, 3),
            "level": self.risk_level.name,
            "threat": self.primary_threat.value
        }


@dataclass
class CollapsePrediction:
    """Prediction result for collapse."""
    will_collapse: bool
    probability: float
    estimated_turns_remaining: int
    primary_threat: CollapseType
    recommended_action: ProtectiveAction
    explanation: str

    def to_dict(self) -> Dict:
        return {
            "will_collapse": self.will_collapse,
            "probability": round(self.probability, 3),
            "turns_remaining": self.estimated_turns_remaining,
            "threat": self.primary_threat.value,
            "action": self.recommended_action.value,
            "explanation": self.explanation
        }


# ═══════════════════════════════════════════════════════════
# Collapse Forecast Engine
# ═══════════════════════════════════════════════════════════

class ToneCollapseForecast:
    """
    Tone Collapse Prediction System.

    Monitors tone patterns and predicts collapse risk.
    """

    # Thresholds
    TENSION_THRESHOLD = 0.7     # Max sustainable tension
    DRIFT_THRESHOLD = 0.6       # Max semantic drift
    COHERENCE_MIN = 0.3         # Minimum coherence
    ENERGY_MIN = 0.2            # Minimum energy

    def __init__(self, window_size: int = 10):
        """
        Initialize forecast system.

        Args:
            window_size: Number of recent samples to analyze
        """
        self.window_size = window_size
        self.history: List[ToneHistory] = []
        self.indicators = CollapseIndicators()
        self.collapse_events: List[Dict] = []

        # Optional ToneBridge integration
        if TONE_BRIDGE_AVAILABLE:
            self.tone_bridge = ToneBridge()
        else:
            self.tone_bridge = None

    def record(self, delta_t: float, delta_s: float, delta_r: float):
        """
        Record a tone sample.

        Args:
            delta_t: Tension value
            delta_s: Semantic drift value
            delta_r: Risk value
        """
        sample = ToneHistory(
            timestamp=datetime.now(),
            delta_t=delta_t,
            delta_s=delta_s,
            delta_r=delta_r
        )

        self.history.append(sample)

        # Keep only recent history
        if len(self.history) > self.window_size * 2:
            self.history = self.history[-self.window_size * 2:]

        # Update indicators
        self._update_indicators()

    def record_text(self, text: str):
        """Record from text using ToneBridge."""
        if self.tone_bridge:
            result = self.tone_bridge.analyze(text)
            tv = result["tone_vector"]
            self.record(tv["delta_t"], tv["delta_s"], tv["delta_r"])
        else:
            # Fallback: estimate from text length and complexity
            length_factor = min(1.0, len(text) / 500)
            self.record(length_factor * 0.5, length_factor * 0.3, length_factor * 0.2)

    def _update_indicators(self):
        """Update collapse indicators from history."""
        if not self.history:
            return

        recent = self.history[-self.window_size:]

        # Tension accumulation (average recent tension)
        self.indicators.tension_accumulation = sum(h.delta_t for h in recent) / len(recent)

        # Semantic drift (variance in delta_s)
        if len(recent) > 1:
            mean_s = sum(h.delta_s for h in recent) / len(recent)
            variance = sum((h.delta_s - mean_s)**2 for h in recent) / len(recent)
            self.indicators.semantic_drift = min(1.0, variance * 4)

        # Coherence (inverse of magnitude variance)
        if len(recent) > 1:
            magnitudes = [h.magnitude for h in recent]
            mean_mag = sum(magnitudes) / len(magnitudes)
            variance = sum((m - mean_mag)**2 for m in magnitudes) / len(magnitudes)
            self.indicators.coherence_score = max(0.0, 1.0 - variance * 2)

        # Energy level (decays over time, restored by low tension)
        for h in recent:
            if h.delta_t < 0.3:
                self.indicators.energy_level = min(1.0, self.indicators.energy_level + 0.05)
            else:
                self.indicators.energy_level = max(0.0, self.indicators.energy_level - 0.03 * h.delta_t)

        # Compute risk score
        self._compute_risk()

    def _compute_risk(self):
        """Compute overall risk score and level."""
        ind = self.indicators

        # Weighted risk calculation
        weights = {
            "tension": 0.3,
            "drift": 0.2,
            "coherence": 0.25,
            "energy": 0.25
        }

        tension_risk = ind.tension_accumulation / self.TENSION_THRESHOLD
        drift_risk = ind.semantic_drift / self.DRIFT_THRESHOLD
        coherence_risk = 1.0 - ind.coherence_score
        energy_risk = 1.0 - ind.energy_level

        ind.risk_score = (
            weights["tension"] * tension_risk +
            weights["drift"] * drift_risk +
            weights["coherence"] * coherence_risk +
            weights["energy"] * energy_risk
        )

        ind.risk_score = min(1.0, max(0.0, ind.risk_score))

        # Determine risk level
        if ind.risk_score < 0.2:
            ind.risk_level = CollapseRisk.MINIMAL
        elif ind.risk_score < 0.4:
            ind.risk_level = CollapseRisk.LOW
        elif ind.risk_score < 0.6:
            ind.risk_level = CollapseRisk.MODERATE
        elif ind.risk_score < 0.8:
            ind.risk_level = CollapseRisk.HIGH
        else:
            ind.risk_level = CollapseRisk.CRITICAL

        # Determine primary threat
        threats = {
            CollapseType.EXHAUSTION: energy_risk,
            CollapseType.OVERLOAD: tension_risk,
            CollapseType.FRAGMENTATION: coherence_risk,
            CollapseType.DECAY: drift_risk,
        }
        ind.primary_threat = max(threats, key=threats.get)

    def predict(self) -> CollapsePrediction:
        """
        Predict collapse likelihood.

        Returns:
            CollapsePrediction with analysis and recommendations
        """
        ind = self.indicators

        # Calculate probability
        probability = ind.risk_score

        # Estimate turns remaining (inverse of risk)
        if probability > 0.9:
            turns_remaining = 1
        elif probability > 0.7:
            turns_remaining = 3
        elif probability > 0.5:
            turns_remaining = 5
        elif probability > 0.3:
            turns_remaining = 10
        else:
            turns_remaining = 20

        # Will collapse if probability > 60%
        will_collapse = probability > 0.6

        # Determine action
        if probability > 0.8:
            action = ProtectiveAction.EMERGENCY_STOP
        elif probability > 0.6:
            action = ProtectiveAction.RETREAT
        elif probability > 0.4:
            action = ProtectiveAction.SIMPLIFY
        elif probability > 0.2:
            action = ProtectiveAction.SLOW_DOWN
        else:
            action = ProtectiveAction.NONE

        # Generate explanation
        explanation = self._generate_explanation(ind, action)

        return CollapsePrediction(
            will_collapse=will_collapse,
            probability=probability,
            estimated_turns_remaining=turns_remaining,
            primary_threat=ind.primary_threat,
            recommended_action=action,
            explanation=explanation
        )

    def _generate_explanation(self, ind: CollapseIndicators, action: ProtectiveAction) -> str:
        """Generate human-readable explanation."""
        parts = []

        if ind.tension_accumulation > self.TENSION_THRESHOLD:
            parts.append(f"Tension level ({ind.tension_accumulation:.2f}) exceeds threshold")

        if ind.energy_level < self.ENERGY_MIN * 2:
            parts.append(f"Energy level ({ind.energy_level:.2f}) is low")

        if ind.coherence_score < self.COHERENCE_MIN * 2:
            parts.append(f"Coherence ({ind.coherence_score:.2f}) is degrading")

        if not parts:
            parts.append("System operating within normal parameters")

        if action != ProtectiveAction.NONE:
            parts.append(f"Recommended action: {action.value}")

        return ". ".join(parts)

    def get_status(self) -> Dict:
        """Get current system status."""
        prediction = self.predict()

        return {
            "indicators": self.indicators.to_dict(),
            "prediction": prediction.to_dict(),
            "history_length": len(self.history),
            "collapse_events": len(self.collapse_events)
        }


# ═══════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════

def demo_collapse_forecast():
    """Demo the collapse forecast system."""
    print("=" * 60)
    print("ToneCollapseForecast Demo")
    print("=" * 60)

    forecast = ToneCollapseForecast(window_size=5)

    # Simulate a conversation that gradually builds tension
    print("\n--- Simulating Conversation ---")

    scenarios = [
        (0.2, 0.1, 0.1, "Normal greeting"),
        (0.3, 0.2, 0.1, "Simple question"),
        (0.4, 0.3, 0.2, "Complex topic"),
        (0.5, 0.4, 0.3, "Challenging question"),
        (0.6, 0.5, 0.4, "Ethical dilemma"),
        (0.7, 0.6, 0.5, "High stress input"),
        (0.8, 0.7, 0.6, "Conflict situation"),
        (0.9, 0.8, 0.7, "Critical pressure"),
    ]

    for delta_t, delta_s, delta_r, desc in scenarios:
        print(f"\n--- Turn: {desc} ---")
        print(f"Input: ΔT={delta_t}, ΔS={delta_s}, ΔR={delta_r}")

        forecast.record(delta_t, delta_s, delta_r)

        status = forecast.get_status()
        ind = status["indicators"]
        pred = status["prediction"]

        print(f"  Energy: {ind['energy']:.2f}")
        print(f"  Risk: {ind['risk']:.2f} ({ind['level']})")
        print(f"  Threat: {ind['threat']}")
        print(f"  → Action: {pred['action']}")

        if pred["will_collapse"]:
            print(f"  ⚠ COLLAPSE WARNING: {pred['turns_remaining']} turns remaining")

    # Final status
    print("\n" + "=" * 60)
    print("Final Status")
    print("=" * 60)
    status = forecast.get_status()
    print(f"Risk level: {status['indicators']['level']}")
    print(f"Probability: {status['prediction']['probability']:.1%}")
    print(f"Explanation: {status['prediction']['explanation']}")

    print("\n" + "=" * 60)
    print("Demo Complete!")


if __name__ == "__main__":
    demo_collapse_forecast()
