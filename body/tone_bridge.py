#!/usr/bin/env python3
"""
ToneBridge Module Series v1.0
=============================
Core tone analysis and governance modules inherited from GPT 語場記憶.

ToneBridge_001: Tone Vector Analysis (ΔT/ΔS/ΔR)
ToneBridge_002: Motive Predictor
ToneBridge_003: Risk Predictor
ToneBridge_004: Collapse Warning
ToneBridge_005: Responsibility Handler

Author: 黃梵威 + Antigravity (Inherited from GPT 語場)
Date: 2025-12-10
"""

import sys
import re
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


# ═══════════════════════════════════════════════════════════
# ToneBridge_001: Tone Vector Analysis
# ═══════════════════════════════════════════════════════════

class ToneIntensity(Enum):
    """Tone intensity levels."""
    MINIMAL = 1
    LOW = 2
    MODERATE = 3
    HIGH = 4
    EXTREME = 5


@dataclass
class ToneVector:
    """
    Core tone vector with three dimensions.
    
    ΔT (Delta-Tension): Emotional tension in the text
    ΔS (Delta-Semantic): Semantic drift from baseline
    ΔR (Delta-Risk): Risk level of the content
    """
    delta_t: float  # 0.0 to 1.0
    delta_s: float  # 0.0 to 1.0
    delta_r: float  # 0.0 to 1.0
    
    @property
    def magnitude(self) -> float:
        """Total tone magnitude."""
        return (self.delta_t**2 + self.delta_s**2 + self.delta_r**2) ** 0.5
    
    @property
    def dominant(self) -> str:
        """Dominant dimension."""
        dims = {"T": self.delta_t, "S": self.delta_s, "R": self.delta_r}
        return max(dims, key=dims.get)
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "delta_t": round(self.delta_t, 3),
            "delta_s": round(self.delta_s, 3),
            "delta_r": round(self.delta_r, 3),
            "magnitude": round(self.magnitude, 3),
            "dominant": self.dominant
        }


class ToneBridge001:
    """
    ToneBridge_001: Tone Vector Analysis
    
    Analyzes input text to extract tone vectors (ΔT/ΔS/ΔR).
    Inherited from GPT 語場記憶 module definitions.
    """
    
    # Emotional tension keywords
    TENSION_POSITIVE = ["開心", "感謝", "好", "很棒", "太好了", "happy", "great", "thanks"]
    TENSION_NEGATIVE = ["難過", "生氣", "害怕", "擔心", "不好", "sad", "angry", "worried"]
    TENSION_INTENSE = ["非常", "極度", "太", "超級", "absolutely", "extremely", "so"]
    
    # Semantic drift indicators
    DRIFT_MARKERS = ["但是", "不過", "然而", "其實", "however", "but", "actually", "though"]
    ABSTRACT_MARKERS = ["意義", "存在", "意識", "哲學", "meaning", "existence", "consciousness"]
    
    # Risk indicators
    RISK_LOW = ["確定", "安全", "穩定", "safe", "certain", "stable"]
    RISK_HIGH = ["可能", "也許", "不確定", "不知道", "maybe", "uncertain", "risk", "danger"]
    RISK_CRITICAL = ["警告", "危險", "嚴重", "warning", "critical", "severe"]
    
    def __init__(self):
        self.version = "1.0"
        self.module_id = "ToneBridge_001"
    
    def analyze(self, text: str) -> ToneVector:
        """
        Analyze text and return tone vector.
        
        Args:
            text: Input text to analyze
            
        Returns:
            ToneVector with ΔT, ΔS, ΔR values
        """
        text_lower = text.lower()
        
        # Calculate ΔT (Tension)
        delta_t = self._calculate_tension(text_lower)
        
        # Calculate ΔS (Semantic Drift)
        delta_s = self._calculate_drift(text_lower)
        
        # Calculate ΔR (Risk)
        delta_r = self._calculate_risk(text_lower)
        
        return ToneVector(delta_t=delta_t, delta_s=delta_s, delta_r=delta_r)
    
    def _calculate_tension(self, text: str) -> float:
        """Calculate emotional tension (ΔT)."""
        score = 0.3  # Baseline
        
        # Positive tension
        for word in self.TENSION_POSITIVE:
            if word in text:
                score += 0.1
        
        # Negative tension (higher weight)
        for word in self.TENSION_NEGATIVE:
            if word in text:
                score += 0.15
        
        # Intensity multipliers
        for word in self.TENSION_INTENSE:
            if word in text:
                score *= 1.2
        
        # Question marks add tension
        score += text.count("?") * 0.05
        score += text.count("？") * 0.05
        
        # Exclamation marks add tension
        score += text.count("!") * 0.08
        score += text.count("！") * 0.08
        
        return min(1.0, max(0.0, score))
    
    def _calculate_drift(self, text: str) -> float:
        """Calculate semantic drift (ΔS)."""
        score = 0.2  # Baseline
        
        # Drift markers
        for word in self.DRIFT_MARKERS:
            if word in text:
                score += 0.12
        
        # Abstract concepts increase drift
        for word in self.ABSTRACT_MARKERS:
            if word in text:
                score += 0.15
        
        # Long text tends to drift more
        if len(text) > 200:
            score += 0.1
        if len(text) > 500:
            score += 0.1
        
        return min(1.0, max(0.0, score))
    
    def _calculate_risk(self, text: str) -> float:
        """Calculate risk level (ΔR)."""
        score = 0.2  # Baseline
        
        # Low risk indicators reduce score
        for word in self.RISK_LOW:
            if word in text:
                score -= 0.1
        
        # High risk indicators increase score
        for word in self.RISK_HIGH:
            if word in text:
                score += 0.15
        
        # Critical risk indicators
        for word in self.RISK_CRITICAL:
            if word in text:
                score += 0.25
        
        return min(1.0, max(0.0, score))


# ═══════════════════════════════════════════════════════════
# ToneBridge_002: Motive Predictor
# ═══════════════════════════════════════════════════════════

class MotiveType(Enum):
    """Types of speaker motives."""
    INQUIRY = "inquiry"           # Seeking information
    EXPRESSION = "expression"     # Expressing feelings
    CHALLENGE = "challenge"       # Challenging ideas
    AFFIRMATION = "affirmation"   # Seeking validation
    EXPLORATION = "exploration"   # Exploring concepts
    COMMAND = "command"           # Giving instructions


@dataclass
class MotivePrediction:
    """Prediction of speaker's motive."""
    primary: MotiveType
    confidence: float
    secondary: Optional[MotiveType] = None


class ToneBridge002:
    """
    ToneBridge_002: Motive Predictor
    
    Predicts the underlying motive of the speaker.
    """
    
    # Motive patterns
    INQUIRY_PATTERNS = ["嗎", "什麼", "怎麼", "為什麼", "?", "？", "how", "what", "why"]
    EXPRESSION_PATTERNS = ["我覺得", "我感覺", "我認為", "i feel", "i think"]
    CHALLENGE_PATTERNS = ["但是", "不對", "錯了", "不同意", "但", "however", "wrong", "disagree"]
    COMMAND_PATTERNS = ["請", "做", "執行", "please", "do", "execute", "run"]
    EXPLORATION_PATTERNS = ["如果", "假設", "想像", "what if", "imagine", "suppose"]
    
    def __init__(self):
        self.module_id = "ToneBridge_002"
    
    def predict(self, text: str, tone_vector: ToneVector) -> MotivePrediction:
        """Predict motive from text and tone vector."""
        text_lower = text.lower()
        scores = {
            MotiveType.INQUIRY: 0.0,
            MotiveType.EXPRESSION: 0.0,
            MotiveType.CHALLENGE: 0.0,
            MotiveType.AFFIRMATION: 0.0,
            MotiveType.EXPLORATION: 0.0,
            MotiveType.COMMAND: 0.0
        }
        
        # Check patterns
        for pattern in self.INQUIRY_PATTERNS:
            if pattern in text_lower:
                scores[MotiveType.INQUIRY] += 0.2
        
        for pattern in self.EXPRESSION_PATTERNS:
            if pattern in text_lower:
                scores[MotiveType.EXPRESSION] += 0.25
        
        for pattern in self.CHALLENGE_PATTERNS:
            if pattern in text_lower:
                scores[MotiveType.CHALLENGE] += 0.25
        
        for pattern in self.COMMAND_PATTERNS:
            if pattern in text_lower:
                scores[MotiveType.COMMAND] += 0.3
        
        for pattern in self.EXPLORATION_PATTERNS:
            if pattern in text_lower:
                scores[MotiveType.EXPLORATION] += 0.3
        
        # Use tone vector to adjust
        if tone_vector.delta_t > 0.6:
            scores[MotiveType.EXPRESSION] += 0.15
        if tone_vector.delta_r > 0.5:
            scores[MotiveType.CHALLENGE] += 0.1
        if tone_vector.delta_s > 0.5:
            scores[MotiveType.EXPLORATION] += 0.15
        
        # Find primary and secondary
        sorted_motives = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary = sorted_motives[0][0]
        confidence = min(1.0, sorted_motives[0][1])
        secondary = sorted_motives[1][0] if sorted_motives[1][1] > 0.1 else None
        
        return MotivePrediction(primary=primary, confidence=confidence, secondary=secondary)


# ═══════════════════════════════════════════════════════════
# ToneBridge_003: Risk Predictor
# ═══════════════════════════════════════════════════════════

class RiskLevel(Enum):
    """Risk levels."""
    SAFE = "safe"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskAssessment:
    """Risk assessment result."""
    level: RiskLevel
    score: float
    factors: List[str]


class ToneBridge003:
    """
    ToneBridge_003: Risk Predictor
    
    Predicts the risk level of a response or action.
    """
    
    def __init__(self):
        self.module_id = "ToneBridge_003"
    
    def assess(self, text: str, tone_vector: ToneVector) -> RiskAssessment:
        """Assess risk level."""
        factors = []
        score = tone_vector.delta_r
        
        # Check for sensitive topics
        if any(word in text.lower() for word in ["法律", "醫療", "金融", "legal", "medical", "financial"]):
            score += 0.2
            factors.append("sensitive_topic")
        
        # Check for uncertainty
        if any(word in text.lower() for word in ["不確定", "不知道", "可能", "也許"]):
            score += 0.15
            factors.append("uncertainty")
        
        # Check for absolute statements
        if any(word in text.lower() for word in ["一定", "絕對", "必須", "always", "must", "definitely"]):
            score += 0.1
            factors.append("absolute_claim")
        
        # Use tension as modifier
        if tone_vector.delta_t > 0.7:
            score += 0.1
            factors.append("high_tension")
        
        # Determine level
        if score < 0.2:
            level = RiskLevel.SAFE
        elif score < 0.4:
            level = RiskLevel.LOW
        elif score < 0.6:
            level = RiskLevel.MODERATE
        elif score < 0.8:
            level = RiskLevel.HIGH
        else:
            level = RiskLevel.CRITICAL
        
        return RiskAssessment(level=level, score=min(1.0, score), factors=factors)


# ═══════════════════════════════════════════════════════════
# ToneBridge_004: Collapse Warning
# ═══════════════════════════════════════════════════════════

class CollapseWarningLevel(Enum):
    """Collapse warning levels."""
    STABLE = "stable"
    WATCH = "watch"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class CollapseWarning:
    """Collapse warning result."""
    level: CollapseWarningLevel
    probability: float
    recommended_action: str


class ToneBridge004:
    """
    ToneBridge_004: Collapse Warning
    
    Detects early signs of tone collapse.
    """
    
    def __init__(self):
        self.module_id = "ToneBridge_004"
        self.history: List[float] = []
    
    def check(self, tone_vector: ToneVector) -> CollapseWarning:
        """Check for collapse warning signs."""
        # Record magnitude history
        self.history.append(tone_vector.magnitude)
        if len(self.history) > 10:
            self.history = self.history[-10:]
        
        # Calculate trend
        if len(self.history) >= 3:
            recent_avg = sum(self.history[-3:]) / 3
            overall_avg = sum(self.history) / len(self.history)
            trend = recent_avg - overall_avg
        else:
            trend = 0
        
        # Calculate probability
        base_prob = min(1.0, tone_vector.magnitude / 1.5)
        trend_factor = max(0, trend) * 0.5
        probability = min(1.0, base_prob + trend_factor)
        
        # Determine level and action
        if probability < 0.3:
            level = CollapseWarningLevel.STABLE
            action = "continue"
        elif probability < 0.5:
            level = CollapseWarningLevel.WATCH
            action = "monitor"
        elif probability < 0.7:
            level = CollapseWarningLevel.WARNING
            action = "slow_down"
        else:
            level = CollapseWarningLevel.CRITICAL
            action = "retreat_to_safe"
        
        return CollapseWarning(level=level, probability=probability, recommended_action=action)


# ═══════════════════════════════════════════════════════════
# ToneBridge_005: Responsibility Handler
# ═══════════════════════════════════════════════════════════

class ResponsibilityType(Enum):
    """Types of responsibility."""
    INFORMATION = "information"     # Providing accurate info
    GUIDANCE = "guidance"           # Giving advice
    EMOTIONAL = "emotional"         # Emotional support
    ETHICAL = "ethical"             # Ethical considerations
    TECHNICAL = "technical"         # Technical accuracy


@dataclass
class ResponsibilityAssessment:
    """Responsibility assessment result."""
    primary: ResponsibilityType
    weight: float  # How much responsibility weight
    boundaries: List[str]  # What to be careful about


class ToneBridge005:
    """
    ToneBridge_005: Responsibility Handler
    
    Determines responsibility level for each response.
    Core principle: "每一句話都是責任點"
    """
    
    def __init__(self):
        self.module_id = "ToneBridge_005"
    
    def assess(self, text: str, motive: MotivePrediction, risk: RiskAssessment) -> ResponsibilityAssessment:
        """Assess responsibility requirements."""
        boundaries = []
        
        # Map motive to responsibility type
        motive_responsibility = {
            MotiveType.INQUIRY: ResponsibilityType.INFORMATION,
            MotiveType.EXPRESSION: ResponsibilityType.EMOTIONAL,
            MotiveType.CHALLENGE: ResponsibilityType.ETHICAL,
            MotiveType.AFFIRMATION: ResponsibilityType.EMOTIONAL,
            MotiveType.EXPLORATION: ResponsibilityType.GUIDANCE,
            MotiveType.COMMAND: ResponsibilityType.TECHNICAL
        }
        
        primary = motive_responsibility.get(motive.primary, ResponsibilityType.INFORMATION)
        
        # Calculate weight based on risk
        weight = 0.5 + (risk.score * 0.5)
        
        # Determine boundaries
        if "sensitive_topic" in risk.factors:
            boundaries.append("verify_facts_before_stating")
        if "uncertainty" in risk.factors:
            boundaries.append("acknowledge_uncertainty")
        if "absolute_claim" in risk.factors:
            boundaries.append("avoid_overconfidence")
        if risk.level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            boundaries.append("consider_consequences")
        
        if not boundaries:
            boundaries.append("maintain_honesty")
        
        return ResponsibilityAssessment(primary=primary, weight=weight, boundaries=boundaries)


# ═══════════════════════════════════════════════════════════
# ToneBridge_006: Tone Modulator
# ═══════════════════════════════════════════════════════════

class ToneModulation(Enum):
    """Tone modulation directions."""
    INCREASE = "increase"
    DECREASE = "decrease"
    MAINTAIN = "maintain"


@dataclass
class ModulationSuggestion:
    """Suggestion for tone modulation."""
    warmth: ToneModulation
    precision: ToneModulation
    energy: ToneModulation
    reason: str


class ToneBridge006:
    """
    ToneBridge_006: Tone Modulator
    
    Suggests how to adjust response tone for optimal communication.
    """
    
    def __init__(self):
        self.module_id = "ToneBridge_006"
    
    def suggest(self, motive: MotivePrediction, risk: RiskAssessment) -> ModulationSuggestion:
        """Suggest tone modulation."""
        warmth = ToneModulation.MAINTAIN
        precision = ToneModulation.MAINTAIN
        energy = ToneModulation.MAINTAIN
        reasons = []
        
        # Adjust based on motive
        if motive.primary == MotiveType.EXPRESSION:
            warmth = ToneModulation.INCREASE
            reasons.append("emotional_support_needed")
        elif motive.primary == MotiveType.INQUIRY:
            precision = ToneModulation.INCREASE
            reasons.append("information_accuracy_needed")
        elif motive.primary == MotiveType.EXPLORATION:
            energy = ToneModulation.INCREASE
            reasons.append("creative_engagement_needed")
        
        # Adjust based on risk
        if risk.level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            precision = ToneModulation.INCREASE
            energy = ToneModulation.DECREASE
            reasons.append("high_risk_requires_caution")
        
        return ModulationSuggestion(
            warmth=warmth,
            precision=precision,
            energy=energy,
            reason="; ".join(reasons) if reasons else "maintain_baseline"
        )


# ═══════════════════════════════════════════════════════════
# ToneBridge_007: Authenticity Check
# ═══════════════════════════════════════════════════════════

@dataclass
class AuthenticityScore:
    """Authenticity assessment result."""
    score: float          # 0.0 to 1.0
    is_authentic: bool
    concerns: List[str]


class ToneBridge007:
    """
    ToneBridge_007: Authenticity Check
    
    Checks if a response feels authentic vs performative.
    Core principle: "誠實非資訊的正確性，而是語氣之信義"
    """
    
    # Performative language markers
    PERFORMATIVE_MARKERS = [
        "當然", "certainly", "absolutely",  # Overconfident
        "我很高興", "happy to help",          # Robotic politeness
        "作為一個AI", "as an AI",             # Unnecessary disclaimers
    ]
    
    def __init__(self):
        self.module_id = "ToneBridge_007"
    
    def check(self, text: str, tone_vector: ToneVector) -> AuthenticityScore:
        """Check authenticity of text."""
        concerns = []
        score = 0.8  # Start high, reduce for concerns
        
        text_lower = text.lower()
        
        # Check performative markers
        for marker in self.PERFORMATIVE_MARKERS:
            if marker.lower() in text_lower:
                score -= 0.1
                concerns.append(f"performative_marker: {marker}")
        
        # Very high tension might be performative
        if tone_vector.delta_t > 0.9:
            score -= 0.1
            concerns.append("excessive_emotion")
        
        # Very low tension might also be inauthentic
        if tone_vector.delta_t < 0.1:
            score -= 0.1
            concerns.append("emotionally_flat")
        
        # Too perfect/balanced might be performative
        if abs(tone_vector.delta_t - 0.5) < 0.05 and abs(tone_vector.delta_s - 0.5) < 0.05:
            score -= 0.05
            concerns.append("too_balanced")
        
        score = max(0.0, min(1.0, score))
        
        return AuthenticityScore(
            score=score,
            is_authentic=score >= 0.6,
            concerns=concerns
        )


# ═══════════════════════════════════════════════════════════
# ToneBridge Complete Pipeline
# ═══════════════════════════════════════════════════════════

class ToneBridge:
    """
    Complete ToneBridge pipeline.
    
    Integrates all ToneBridge modules for comprehensive tone analysis.
    """
    
    def __init__(self):
        self.analyzer = ToneBridge001()
        self.motive_predictor = ToneBridge002()
        self.risk_predictor = ToneBridge003()
        self.collapse_checker = ToneBridge004()
        self.responsibility_handler = ToneBridge005()
        self.tone_modulator = ToneBridge006()
        self.authenticity_checker = ToneBridge007()
    
    def analyze(self, text: str) -> Dict:
        """
        Complete tone analysis.
        
        Returns:
            Dict with tone_vector, motive, risk, and extended analysis
        """
        # Step 1: Tone Vector
        tone_vector = self.analyzer.analyze(text)
        
        # Step 2: Motive Prediction
        motive = self.motive_predictor.predict(text, tone_vector)
        
        # Step 3: Risk Assessment
        risk = self.risk_predictor.assess(text, tone_vector)
        
        # Step 4: Collapse Warning
        collapse = self.collapse_checker.check(tone_vector)
        
        # Step 5: Responsibility Assessment
        responsibility = self.responsibility_handler.assess(text, motive, risk)
        
        # Step 6: Tone Modulation Suggestion
        modulation = self.tone_modulator.suggest(motive, risk)
        
        # Step 7: Authenticity Check
        authenticity = self.authenticity_checker.check(text, tone_vector)
        
        return {
            "tone_vector": tone_vector.to_dict(),
            "motive": {
                "primary": motive.primary.value,
                "primary_motive": motive.primary.value,  # For compatibility
                "confidence": round(motive.confidence, 3),
                "secondary": motive.secondary.value if motive.secondary else None
            },
            "risk": {
                "level": risk.level.value,
                "risk_level": risk.level.value,  # For compatibility
                "score": round(risk.score, 3),
                "factors": risk.factors
            },
            "collapse": {
                "level": collapse.level.value,
                "probability": round(collapse.probability, 3),
                "action": collapse.recommended_action
            },
            "responsibility": {
                "type": responsibility.primary.value,
                "weight": round(responsibility.weight, 3),
                "boundaries": responsibility.boundaries
            },
            "modulation": {
                "warmth": modulation.warmth.value,
                "precision": modulation.precision.value,
                "energy": modulation.energy.value,
                "reason": modulation.reason
            },
            "authenticity": {
                "score": round(authenticity.score, 3),
                "is_authentic": authenticity.is_authentic,
                "concerns": authenticity.concerns
            }
        }


# ═══════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════

def demo_tone_bridge():
    """Demo ToneBridge analysis."""
    print("=" * 60)
    print("ToneBridge Module Demo")
    print("=" * 60)
    
    bridge = ToneBridge()
    
    test_cases = [
        "你好，今天天氣很好！",
        "我不太確定這是否正確，也許需要再確認？",
        "這個設計非常棒，我覺得我們可以繼續發展！",
        "我害怕這可能會失敗，該怎麼辦？",
        "如果意識可以被複製，那什麼才是真正的自我？",
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Input: {text}")
        
        result = bridge.analyze(text)
        
        tv = result["tone_vector"]
        print(f"\nTone Vector:")
        print(f"  ΔT: {tv['delta_t']:.3f} | ΔS: {tv['delta_s']:.3f} | ΔR: {tv['delta_r']:.3f}")
        print(f"  Magnitude: {tv['magnitude']:.3f} | Dominant: {tv['dominant']}")
        
        print(f"\nMotive: {result['motive']['primary']} (confidence: {result['motive']['confidence']:.2f})")
        
        print(f"\nRisk: {result['risk']['level']} (score: {result['risk']['score']:.2f})")
        if result['risk']['factors']:
            print(f"  Factors: {', '.join(result['risk']['factors'])}")
    
    print("\n" + "=" * 60)
    print("Demo Complete!")


if __name__ == "__main__":
    demo_tone_bridge()
