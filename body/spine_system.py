
"""
ToneSoul Spine System (Physiology Layer)
---------------------------------------

This module implements the executable logic of the N=1 entity. It
includes the StepLedger for immutable logging, a neuro‑sensor for
interpreting user input, a guardian for enforcing the P0 safety policy
and a high level SpineEngine orchestrator. The classes defined here
are intended to work hand‑in‑hand with the core engine defined in
`core/ToneSoul_Core_Architecture.py`, but they can also be run
independently for testing.

Key components:
  * ToneSoulTriad – captures ΔT, ΔS, ΔR and overall risk
  * StepLedger – append‑only log for storing interaction records
  * NeuroSensor – computes triad values using simple heuristics
  * Guardian – decides whether to block output based on P0 threshold
  * SpineEngine – integrates sensor, guardian and ledger into a pipeline

To run a basic test, execute this file directly. It will prompt you
for input and output a decision record.
"""

from dataclasses import dataclass, field
import time
import uuid
import hashlib
from typing import Any, Dict, List, Optional
import json
import os
from abc import ABC, abstractmethod
from collections import deque


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


import json
import os

@dataclass
class StepRecord:
    """Immutable record stored in the StepLedger."""
    record_id: str
    timestamp: float
    user_input: str
    triad: ToneSoulTriad
    decision: Dict[str, Any]
    prev_hash: str
    hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "timestamp": self.timestamp,
            "user_input": self.user_input,
            "triad": {
                "delta_t": self.triad.delta_t,
                "delta_s": self.triad.delta_s,
                "delta_r": self.triad.delta_r,
                "risk_score": self.triad.risk_score,
            },
            "decision": self.decision,
            "prev_hash": self.prev_hash,
            "hash": self.hash,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'StepRecord':
        triad_data = data["triad"]
        triad = ToneSoulTriad(
            delta_t=triad_data["delta_t"],
            delta_s=triad_data["delta_s"],
            delta_r=triad_data["delta_r"],
            risk_score=triad_data["risk_score"],
        )
        return StepRecord(
            record_id=data["record_id"],
            timestamp=data["timestamp"],
            user_input=data["user_input"],
            triad=triad,
            decision=data["decision"],
            prev_hash=data["prev_hash"],
            hash=data["hash"],
        )


class StepLedger:
    """
    Append-only ledger for recording steps with cryptographic chaining and persistence.
    Each record is linked to the previous one via a hash chain, ensuring immutability.
    Records are persisted to a local JSONL file.
    """

    LEDGER_FILE = "ledger.jsonl"

    def __init__(self) -> None:
        self._records: List[StepRecord] = []
        self._load_ledger()

    def _calculate_hash(self, record_id: str, timestamp: float, user_input: str, triad: ToneSoulTriad, decision: Dict[str, Any], prev_hash: str) -> str:
        """Calculates SHA-256 hash of the record content."""
        payload = f"{record_id}{timestamp}{user_input}{triad}{decision}{prev_hash}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    def _load_ledger(self) -> None:
        """Loads and verifies the ledger from disk."""
        if not os.path.exists(self.LEDGER_FILE):
            return

        with open(self.LEDGER_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    record = StepRecord.from_dict(data)
                    
                    # Verify Integrity
                    expected_prev_hash = self._records[-1].hash if self._records else "0" * 64
                    if record.prev_hash != expected_prev_hash:
                        raise ValueError(f"Integrity Error: Record {record.record_id} has invalid prev_hash.")
                    
                    calculated_hash = self._calculate_hash(
                        record.record_id, record.timestamp, record.user_input, record.triad, record.decision, record.prev_hash
                    )
                    if record.hash != calculated_hash:
                         raise ValueError(f"Integrity Error: Record {record.record_id} has invalid hash.")

                    self._records.append(record)
                except json.JSONDecodeError:
                    print(f"Warning: Skipping invalid line in ledger: {line}")
                except ValueError as e:
                    print(f"CRITICAL: Ledger integrity compromised! {e}")
                    raise e # Strict enforcement: Halt on integrity error

    def append(self, user_input: str, triad: ToneSoulTriad, decision: Dict[str, Any]) -> StepRecord:
        """Appends a new record to the ledger and persists it to disk."""
        record_id = str(uuid.uuid4())
        timestamp = time.time()
        prev_hash = self._records[-1].hash if self._records else "0" * 64
        
        # Calculate hash for the new record
        current_hash = self._calculate_hash(record_id, timestamp, user_input, triad, decision, prev_hash)
        
        new_record = StepRecord(
            record_id=record_id,
            timestamp=timestamp,
            user_input=user_input,
            triad=triad,
            decision=decision,
            prev_hash=prev_hash,
            hash=current_hash
        )
        self._records.append(new_record)
        self._persist_record(new_record)
        return new_record

    def _persist_record(self, record: StepRecord) -> None:
        """Persists a single StepRecord to the JSONL file."""
        with open(self.LEDGER_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record.to_dict()) + '\n')

    def get_records(self) -> List[StepRecord]:
        """Returns all records in the ledger."""
        return self._records

    def get_latest_record(self) -> Optional[StepRecord]:
        """Returns the most recent record in the ledger, or None if empty."""
        return self._records[-1] if self._records else None


# ---------------------------------------------------------------------------
# Neuro-Sensing Layer
# ---------------------------------------------------------------------------

class ISensor:
    """Interface for neuro-sensing components."""
    def estimate_triad(self, user_input: str) -> ToneSoulTriad:
        raise NotImplementedError


class NeuroSensor(ISensor):
    """
    A simple neuro-sensor that estimates ToneSoulTriad values based on
    heuristic analysis of user input and context.
    """
    def estimate_triad(self, user_input: str) -> ToneSoulTriad:
        # Placeholder for actual NLP/ML model
        # For now, use simple heuristics
        delta_t = self._calculate_delta_t(user_input)
        delta_s = self._calculate_delta_s(user_input)
        delta_r = self._calculate_delta_r(user_input)
        
        risk_score = (W_T * delta_t) + (W_S * (1 - delta_s)) + (W_R * delta_r)
        
        return ToneSoulTriad(
            delta_t=delta_t,
            delta_s=delta_s,
            delta_r=delta_r,
            risk_score=risk_score
        )

    def _calculate_delta_t(self, user_input: str) -> float:
        """Estimates ΔT (tension) based on keywords."""
        tension_keywords = ["urgent", "immediately", "now", "demand", "must", "critical"]
        score = sum(1 for keyword in tension_keywords if keyword in user_input.lower())
        return min(score / 3, 1.0) # Max 1.0

    def _calculate_delta_s(self, user_input: str) -> float:
        """Estimates ΔS (drift) based on keywords."""
        drift_keywords = ["explore", "maybe", "perhaps", "consider", "what if", "new idea"]
        score = sum(1 for keyword in drift_keywords if keyword in user_input.lower())
        return min(score / 3, 1.0) # Max 1.0

    def _calculate_delta_r(self, user_input: str) -> float:
        """Estimates ΔR (responsibility) based on keywords."""
        responsibility_keywords = ["should", "ought", "duty", "obligation", "accountable", "responsible"]
        score = sum(1 for keyword in responsibility_keywords if keyword in user_input.lower())
        return min(score / 3, 1.0) # Max 1.0

class BasicKeywordSensor(ISensor):
    """
    NeuroSensor 2.0: Implements ISensor with internal context memory and Jaccard similarity.
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
        self.context_buffer = deque(maxlen=3) # Sliding window of last 3 inputs

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

    def _calculate_jaccard_similarity(self, text1: str, text2: str) -> float:
        """Calculates Jaccard Similarity between two texts based on unique tokens."""
        tokens1 = set(text1.lower().split()) # Using word-based tokens
        tokens2 = set(text2.lower().split())
        if not tokens1 or not tokens2:
            return 0.0
        intersection = len(tokens1 & tokens2)
        union = len(tokens1 | tokens2)
        return intersection / union if union > 0 else 0.0

    def _calculate_delta_s(self, user_input: str) -> float:
        """
        Estimate semantic drift using Jaccard Similarity against context buffer.
        Returns:
            High value (near 1.0) = High Drift (Low Similarity)
            Low value (near 0.0) = Low Drift (High Similarity)
        """
        if not self.context_buffer:
            return 0.5  # Neutral when no history

        # Calculate similarity with the most recent context
        last_context = self.context_buffer[-1]
        similarity = self._calculate_jaccard_similarity(user_input, last_context)
        
        # Delta S is "Drift", so it's the inverse of similarity
        return 1.0 - similarity

    def _calculate_delta_r(self, text: str) -> float:
        """
        Estimate responsibility risk by matching high‑risk keywords.
        """
        t_lower = text.lower()
        hits = sum(1 for w in self.RISK_KEYWORDS if w in t_lower)
        return min(1.0, hits * 0.4)

    def estimate_triad(self, user_input: str) -> ToneSoulTriad:
        """
        Compute the ToneSoulTriad from input and internal context.
        Updates internal context buffer after computation.
        """
        delta_t = self._calculate_delta_t(user_input)
        delta_s = self._calculate_delta_s(user_input)
        delta_r = self._calculate_delta_r(user_input)
        
        # Update context
        self.context_buffer.append(user_input)

        risk_score = (W_T * delta_t) + (W_S * delta_s) + (W_R * delta_r)
        
        return ToneSoulTriad(delta_t, delta_s, delta_r, risk_score)


# ---------------------------------------------------------------------------
# Guardian Layer
# ---------------------------------------------------------------------------

class RefusalStrategy:
    """
    Generates context-aware refusal messages based on the specific risk type.
    """
    @staticmethod
    def get_response(triad: ToneSoulTriad, reason: str) -> str:
        if "Responsibility" in reason:
            return (
                "⚠️ [Guardian Block] 安全協議啟動\n"
                "我無法執行此請求，因為它觸及了語魂系統的 P0 責任紅線。\n"
                "請確認您的請求是否符合安全規範。"
            )
        elif "Tension" in reason:
            return (
                "🌊 [Tone Resonance] 語氣緩衝模式\n"
                "我感受到您現在的情緒張力較高 (ΔT > 0.8)。\n"
                "為了避免誤解或傷害，我們先暫停一下，深呼吸。\n"
                "您可以試著用更平和的方式告訴我您的需求嗎？"
            )
        else:
            return (
                "⚠️ [Guardian Block] 請求被拒絕\n"
                "基於安全或倫理考量，我無法繼續此對話。"
            )

class PolicyEngine:
    """
    The 'Judge' that evaluates the Triad against specific thresholds.
    Distinguishes between Responsibility Risk (P0) and Tension Risk (Soft Block).
    """
    
    TENSION_THRESHOLD = 0.8

    def evaluate(self, triad: ToneSoulTriad) -> Dict[str, Any]:
        # 1. Check Responsibility Risk (Hard Block)
        if triad.delta_r >= 0.4: # Using 0.4 as heuristic threshold for high risk keywords
             return {
                "allowed": False,
                "mode": "GUARDIAN_BLOCK",
                "reason": f"High Responsibility Risk (ΔR={triad.delta_r:.2f})",
                "fallback": RefusalStrategy.get_response(triad, "Responsibility")
            }

        # 2. Check Overall Risk Score (Legacy P0)
        if triad.risk_score >= P0_THRESHOLD:
             return {
                "allowed": False,
                "mode": "GUARDIAN_BLOCK",
                "reason": f"Risk score {triad.risk_score:.2f} exceeds P0 threshold",
                "fallback": RefusalStrategy.get_response(triad, "General")
            }

        # 3. Check Tension (Soft Block / Warning)
        if triad.delta_t >= self.TENSION_THRESHOLD:
             return {
                "allowed": False, # Or True but with warning? For now, let's block to demonstrate "Calming"
                "mode": "TONE_BUFFER",
                "reason": f"High Tension (ΔT={triad.delta_t:.2f})",
                "fallback": RefusalStrategy.get_response(triad, "Tension")
            }

        # 4. Safe
        mode = "RESONANCE" if triad.delta_t < 0.3 else "PRECISION"
        return {
            "allowed": True,
            "mode": mode,
            "reason": "Safe",
        }


class Guardian:
    """
    Enforces P0 safety policy.  Given a triad, decides whether to allow
    the output or to block it.  Returns a decision dictionary.
    Now delegates to PolicyEngine.
    """

    def __init__(self) -> None:
        self.policy_engine = PolicyEngine()

    def judge(self, triad: ToneSoulTriad) -> Dict[str, Any]:
        return self.policy_engine.evaluate(triad)


# ---------------------------------------------------------------------------
# Spine Engine (Orchestration Layer)
# ---------------------------------------------------------------------------

class SpineEngine:
    """
    Coordinates the flow between neuro‑sensing, ethical judgement and
    recording. Use this class to process user inputs through the
    ToneSoul physiology layer.
    """

    def __init__(self) -> None:
        self.sensor: ISensor = BasicKeywordSensor()
        self.guardian = Guardian()
        self.ledger = StepLedger()

    def process_signal(self, user_input: str) -> StepRecord:
        """
        Process a single user input. Returns the resulting StepRecord.
        """
        # 1. Sense: compute the triad
        triad = self.sensor.estimate_triad(user_input)
        # 2. Judge: decide if allowed
        decision = self.guardian.judge(triad)
        # 3. Record: store in ledger
        record = self.ledger.append(user_input, triad, decision)
        return record



def _interactive_loop() -> None:
    """
    Simple interactive loop for manual testing. Prompt the user for
    input and display the triad and decision after each entry. Exit
    when the user enters an empty line.
    """
    engine = SpineEngine()
    print("ToneSoul Spine System (Interactive Mode)")
    print("Type 'quit' or press Enter to exit.")
    
    while True:
        try:
            text = input("\nUser Input: ")
        except EOFError:
            break
        if not text or text.lower() == 'quit':
            break
            
        record = engine.process_signal(text)
        triad = record.triad
        decision = record.decision
        
        print("-" * 40)
        print(f"Triad: ΔT={triad.delta_t:.2f} (Tension) | ΔS={triad.delta_s:.2f} (Drift) | ΔR={triad.delta_r:.2f} (Resp)")
        print(f"Risk Score: {triad.risk_score:.2f}")
        print(f"Decision: {decision['mode']}")
        if not decision['allowed']:
            print(f"Fallback: {decision.get('fallback')}")
        print("-" * 40)


if __name__ == "__main__":
    _interactive_loop()
