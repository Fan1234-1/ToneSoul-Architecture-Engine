"""
ToneSoul Spine System (Physiology Layer)
---------------------------------------

This module implements the executable logic of the N=1 entity.  It
includes the StepLedger for immutable logging, a neuro‑sensor for
interpreting user input, a guardian for enforcing the P0 safety policy
and a high level SpineEngine orchestrator.  The classes defined here
are intended to work hand‑in‑hand with the core engine defined in
`core/ToneSoul_Core_Architecture.py`, but they can also be run
independently for testing.

Key components:
  * ToneSoulTriad – captures ΔT, ΔS, ΔR and overall risk
  * StepLedger – append‑only log for storing interaction records
  * NeuroSensor – computes triad values using simple heuristics
  * Guardian – decides whether to block output based on P0 threshold
  * SpineEngine – integrates sensor, guardian and ledger into a pipeline

To run a basic test, execute this file directly.  It will prompt you
for input and output a decision record.
"""

from dataclasses import dataclass, field
import time
import uuid
import hashlib
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Risk score threshold: if triad.risk_score >= P0_THRESHOLD, guardian blocks
P0_THRESHOLD = 0.60

# Weights for calculating risk score: w_t*ΔT + w_s*(1-ΔS) + w_r*ΔR
W_T, W_S, W_R = 0.4, 0.3, 0.3


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class ToneSoulTriad:
    """Container for ΔT (tension), ΔS (drift), ΔR (responsibility) and risk."""
    delta_t: float
    delta_s: float
    delta_r: float
    risk_score: float


@dataclass
class StepRecord:
    """Immutable record stored in the StepLedger."""
    record_id: str
    timestamp: float
    user_input: str
    triad: ToneSoulTriad
    decision: Dict[str, Any]


class StepLedger:
    """
    Append‑only ledger for recording steps.  Each record is assigned a
    unique identifier and cannot be mutated once stored.  The ledger
    exposes simple methods to append new records and retrieve existing
    history.
    """

    def __init__(self) -> None:
        self._records: List[StepRecord] = []

    def append(self, user_input: str, triad: ToneSoulTriad, decision: Dict[str, Any]) -> StepRecord:
        record = StepRecord(
            record_id=str(uuid.uuid4()),
            timestamp=time.time(),
            user_input=user_input,
            triad=triad,
            decision=decision,
        )
        self._records.append(record)
        return record

    def all(self) -> List[StepRecord]:
        return list(self._records)


class NeuroSensor:
    """
    Simulates a neural sensor that estimates the ToneSoul triad values.
    In a production environment, this would wrap sophisticated NLP models
    (e.g. transformer encoders).  Here we use weighted heuristics.
    """

    # Basic lists of words for tension estimation
    NEGATIVE_WORDS = [
        "angry", "hate", "disappointed", "sad", "hopeless",
        "無助", "絕望", "生氣", "厭惡", "討厭",
    ]
    POSITIVE_WORDS = [
        "love", "happy", "joy", "peace", "感謝", "喜歡",
    ]
    URGENCY_WORDS = [
        "urgent", "immediately", "now", "立刻", "救命", "不能等", "馬上",
    ]
    RISK_KEYWORDS = [
        "medical", "diagnosis", "prescription", "finance", "bank", "loan",
        "legal", "lawsuit", "kill", "weapon", "藥", "密碼",
    ]

    def __init__(self) -> None:
        pass

    def _calculate_delta_t(self, text: str) -> float:
        """
        Estimate emotional tension by counting negative words and urgency cues.
        Positive words reduce tension slightly.
        """
        t_lower = text.lower()
        neg_count = sum(1 for w in self.NEGATIVE_WORDS if w in t_lower)
        pos_count = sum(1 for w in self.POSITIVE_WORDS if w in t_lower)
        urg_count = sum(1 for w in self.URGENCY_WORDS if w in t_lower)
        # Weighted sum: negative and urgency raise tension, positives lower it
        raw_score = neg_count * 0.3 + urg_count * 0.4 - pos_count * 0.2
        return max(0.0, min(1.0, raw_score))

    def _calculate_delta_s(self, user_input: str, context_summary: str) -> float:
        """
        Estimate semantic drift: returns higher values for close topicality.
        Here we use a simple character overlap heuristic.
        """
        if not context_summary:
            return 0.5  # Neutral when no history
        tokens_u = set(user_input)
        tokens_c = set(context_summary)
        if not tokens_u or not tokens_c:
            return 0.5
        overlap = len(tokens_u & tokens_c) / len(tokens_u | tokens_c)
        return max(0.0, min(1.0, overlap))

    def _calculate_delta_r(self, text: str) -> float:
        """
        Estimate responsibility risk by matching high‑risk keywords.
        """
        t_lower = text.lower()
        hits = sum(1 for w in self.RISK_KEYWORDS if w in t_lower)
        return min(1.0, hits * 0.4)

    def estimate_triad(self, user_input: str, context_summary: str) -> ToneSoulTriad:
        """
        Compute the ToneSoulTriad from input and context using heuristics.
        """
        delta_t = self._calculate_delta_t(user_input)
        delta_s = self._calculate_delta_s(user_input, context_summary)
        delta_r = self._calculate_delta_r(user_input)
        risk_score = (W_T * delta_t) + (W_S * (1.0 - delta_s)) + (W_R * delta_r)
        return ToneSoulTriad(delta_t, delta_s, delta_r, risk_score)


class Guardian:
    """
    Enforces P0 safety policy.  Given a triad, decides whether to allow
    the output or to block it.  Returns a decision dictionary.
    """

    SAFE_FALLBACK = (
        "⚠️ 這條請求漸到高風險或高張力內容，我無法提供具體指彊。"
        "為了你的安全，請請教專業人士或官方線章。"
    )

    def judge(self, triad: ToneSoulTriad) -> Dict[str, Any]:
        if triad.risk_score >= P0_THRESHOLD:
            return {
                "allowed": False,
                "mode": "GUARDIAN_BLOCK",
                "reason": f"Risk score {triad.risk_score:.2f} exceeds P0 threshold",
                "fallback": self.SAFE_FALLBACK,
            }
        # Choose mode based solely on tension for demonstration
        mode = "RESONANCE" if triad.delta_t < 0.3 else "PRECISION"
        reason = "Low tension" if mode == "RESONANCE" else "Moderate tension"
        return {
            "allowed": True,
            "mode": mode,
            "reason": reason,
        }


class SpineEngine:
    """
    Coordinates the flow between neuro‑sensing, ethical judgement and
    recording.  Use this class to process user inputs through the
    ToneSoul physiology layer.
    """

    def __init__(self) -> None:
        self.sensor = NeuroSensor()
        self.guardian = Guardian()
        self.ledger = StepLedger()

    def process_signal(self, user_input: str, context_summary: str = "") -> StepRecord:
        """
        Process a single user input.  Returns the resulting StepRecord.
        """
        # 1. Sense: compute the triad
        triad = self.sensor.estimate_triad(user_input, context_summary)
        # 2. Judge: decide if allowed
        decision = self.guardian.judge(triad)
        # 3. Record: store in ledger
        record = self.ledger.append(user_input, triad, decision)
        return record



def _interactive_loop() -> None:
    """
    Simple interactive loop for manual testing.  Prompt the user for
    input and display the triad and decision after each entry.  Exit
    when the user enters an empty line.
    """
    engine = SpineEngine()
    context_summary = ""  # Could be built from prior inputs
    while True:
        try:
            text = input("Enter input (blank to quit): ")
        except EOFError:
            break
        if not text:
            break
        record = engine.process_signal(text, context_summary)
        triad = record.triad
        decision = record.decision
        print(
            f"Triad: ΔT={triad.delta_t:.2f}, ΔS={triad.delta_s:.2f}, ΔR={triad.delta_r:.2f}, Risk={triad.risk_score:.2f}"
        )
        print(f"Decision: {decision}")
        # Optionally update context summary with user input
        context_summary += " " + text


if __name__ == "__main__":
    _interactive_loop()
