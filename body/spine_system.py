
"""
ToneSoul Spine System (Physiology Layer)
---------------------------------------
Rewritten to fix syntax errors and implement Rollback.
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
from neuro_modulator import NeuroModulator

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONSTITUTION_PATH = os.path.join(BASE_DIR, "../law/constitution.json")

# Weights for calculating risk score
W_T, W_S, W_R = 0.4, 0.3, 0.3


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class ToneSoulTriad:
    delta_t: float
    delta_s: float
    delta_r: float
    risk_score: float


@dataclass
class StepRecord:
    record_id: str
    timestamp: float
    user_input: str
    triad: ToneSoulTriad
    decision: Dict[str, Any]
    prev_hash: str
    hash: str
    vow_id: str
    signatory: str = "ToneSoul_v1.0"

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
            "vow_id": self.vow_id,
            "signatory": self.signatory
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
            vow_id=data.get("vow_id", "LEGACY_VOW"),
            signatory=data.get("signatory", "ToneSoul_v1.0")
        )


# ---------------------------------------------------------------------------
# Graph Memory Layer (StepLedger v2.0)
# ---------------------------------------------------------------------------

class SimpleGraph:
    """
    A lightweight, dependency-free Graph implementation for ToneSoul Memory.
    Supports nodes, edges, and basic similarity search.
    """
    def __init__(self) -> None:
        self.nodes: Dict[str, Any] = {} # record_id -> StepRecord
        self.edges: Dict[str, List[tuple[str, str]]] = {} # source_id -> [(target_id, relation_type)]

    def add_node(self, record: StepRecord) -> None:
        self.nodes[record.record_id] = record
        if record.record_id not in self.edges:
            self.edges[record.record_id] = []

    def add_edge(self, source_id: str, target_id: str, relation: str) -> None:
        if source_id in self.edges:
            self.edges[source_id].append((target_id, relation))

    def find_resonant_nodes(self, target_triad: ToneSoulTriad, limit: int = 3, exclude_id: str = None) -> List[tuple[StepRecord, float]]:
        """
        Finds nodes with similar emotional state (Euclidean distance of Triad).
        Returns list of (record, distance), sorted by distance.
        """
        results = []
        for r_id, record in self.nodes.items():
            if r_id == exclude_id:
                continue
            
            # Calculate Euclidean distance in 3D Triad space
            d_t = record.triad.delta_t - target_triad.delta_t
            d_s = record.triad.delta_s - target_triad.delta_s
            d_r = record.triad.delta_r - target_triad.delta_r
            distance = (d_t**2 + d_s**2 + d_r**2) ** 0.5
            
            results.append((record, distance))
        
        # Sort by distance (ascending) and take top k
        results.sort(key=lambda x: x[1])
        return results[:limit]


class StepLedger:
    LEDGER_FILE = "ledger.jsonl"

    def __init__(self) -> None:
        self._records: List[StepRecord] = []
        self.graph = SimpleGraph()
        self._load_ledger()

    def _calculate_hash(self, record: StepRecord) -> str:
        payload = f"{record.record_id}{record.timestamp}{record.user_input}{record.triad}{record.decision}{record.prev_hash}{record.vow_id}{record.signatory}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    def _load_ledger(self) -> None:
        if not os.path.exists(self.LEDGER_FILE):
            return

        with open(self.LEDGER_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    record = StepRecord.from_dict(data)
                    
                    expected_prev_hash = self._records[-1].hash if self._records else "0" * 64
                    if record.prev_hash != expected_prev_hash:
                        # In a real system, we might halt. For now, just warn.
                        print(f"Warning: Integrity Error at record {record.record_id}")
                    
                    self._records.append(record)
                    self.graph.add_node(record)
                    
                    # Add Temporal Edge
                    if len(self._records) > 1:
                        prev_record = self._records[-2]
                        self.graph.add_edge(prev_record.record_id, record.record_id, "NEXT")
                        
                except json.JSONDecodeError:
                    pass

    def append(self, user_input: str, triad: ToneSoulTriad, decision: Dict[str, Any], vow_id: str) -> StepRecord:
        record_id = str(uuid.uuid4())
        timestamp = time.time()
        prev_hash = self._records[-1].hash if self._records else "0" * 64
        
        temp_record = StepRecord(
            record_id=record_id,
            timestamp=timestamp,
            user_input=user_input,
            triad=triad,
            decision=decision,
            prev_hash=prev_hash,
            hash="",
            vow_id=vow_id,
            signatory="ToneSoul_v1.0"
        )
        
        current_hash = self._calculate_hash(temp_record)
        temp_record.hash = current_hash
        
        self._records.append(temp_record)
        self.graph.add_node(temp_record)
        
        # Add Temporal Edge
        if len(self._records) > 1:
            prev_record = self._records[-2]
            self.graph.add_edge(prev_record.record_id, temp_record.record_id, "NEXT")
            
        self._persist_record(temp_record)
        return temp_record

    def rollback(self, vow_id: str) -> StepRecord:
        # Appends a ROLLBACK event to the ledger.
        if not self._records:
             raise ValueError("Cannot rollback empty ledger")

        last_record = self._records[-1]
        
        rollback_triad = ToneSoulTriad(0.0, 0.0, 0.0, 0.0)
        rollback_decision = {
            "allowed": True, 
            "mode": "ROLLBACK", 
            "reason": f"Rolling back record {last_record.hash[:8]}"
        }
        
        # Note: Rollback records are also nodes in the graph, but might mark the previous node as 'invalid' in a future version.
        return self.append(
            user_input="[ROLLBACK]",
            triad=rollback_triad,
            decision=rollback_decision,
            vow_id=vow_id
        )

    def _persist_record(self, record: StepRecord) -> None:
        with open(self.LEDGER_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record.to_dict()) + '\n')

    def get_records(self) -> List[StepRecord]:
        return self._records

    def get_latest_record(self) -> Optional[StepRecord]:
        return self._records[-1] if self._records else None
        
    def get_associative_context(self, current_triad: ToneSoulTriad, limit: int = 3) -> List[StepRecord]:
        """
        Retrieves past records that resonate with the current emotional state.
        """
        results = self.graph.find_resonant_nodes(current_triad, limit=limit)
        return [r[0] for r in results]


# ---------------------------------------------------------------------------
# Neuro-Sensing Layer
# ---------------------------------------------------------------------------

class ISensor:
    def estimate_triad(self, user_input: str) -> ToneSoulTriad:
        raise NotImplementedError


class BasicKeywordSensor(ISensor):
    def __init__(self, config: Dict[str, Any]) -> None:
        self.context_buffer = deque(maxlen=3)
        self._configure(config)

    def _configure(self, config: Dict[str, Any]) -> None:
        keywords = config.get("risk_keywords", {})
        self.RISK_KEYWORDS = keywords.get("responsibility_risk", [])
        
        tension = keywords.get("tension_risk", {})
        self.NEGATIVE_WORDS = tension.get("negative", [])
        self.POSITIVE_WORDS = tension.get("positive", [])
        self.URGENCY_WORDS = tension.get("urgency", [])

    def _calculate_delta_t(self, text: str) -> float:
        t_lower = text.lower()
        neg_count = sum(1 for w in self.NEGATIVE_WORDS if w in t_lower)
        pos_count = sum(1 for w in self.POSITIVE_WORDS if w in t_lower)
        urg_count = sum(1 for w in self.URGENCY_WORDS if w in t_lower)
        raw_score = neg_count * 0.3 + urg_count * 0.4 - pos_count * 0.2
        return max(0.0, min(1.0, raw_score))

    def _calculate_jaccard_similarity(self, text1: str, text2: str) -> float:
        tokens1 = set(text1.lower().split())
        tokens2 = set(text2.lower().split())
        if not tokens1 or not tokens2:
            return 0.0
        intersection = len(tokens1 & tokens2)
        union = len(tokens1 | tokens2)
        return intersection / union if union > 0 else 0.0

    def _calculate_delta_s(self, user_input: str) -> float:
        if not self.context_buffer:
            return 0.5
        last_context = self.context_buffer[-1]
        similarity = self._calculate_jaccard_similarity(user_input, last_context)
        return 1.0 - similarity

    def _calculate_delta_r(self, text: str) -> float:
        t_lower = text.lower()
        hits = sum(1 for w in self.RISK_KEYWORDS if w in t_lower)
        return min(1.0, hits * 0.4)

    def estimate_triad(self, user_input: str) -> ToneSoulTriad:
        delta_t = self._calculate_delta_t(user_input)
        delta_s = self._calculate_delta_s(user_input)
        delta_r = self._calculate_delta_r(user_input)
        self.context_buffer.append(user_input)
        risk_score = (W_T * delta_t) + (W_S * delta_s) + (W_R * delta_r)
        return ToneSoulTriad(delta_t, delta_s, delta_r, risk_score)


# ---------------------------------------------------------------------------
# Guardian Layer
# ---------------------------------------------------------------------------

class RefusalStrategy:
    @staticmethod
    def get_response(triad: ToneSoulTriad, reason: str) -> str:
        if "Responsibility" in reason:
            return "⚠️ [Guardian Block] Responsibility Protocol Activated."
        elif "Tension" in reason:
            return "🌊 [Tone Resonance] Tension Buffer Activated."
        else:
            return "⚠️ [Guardian Block] Request Refused."

class PolicyEngine:
    def __init__(self, config: Dict[str, Any]) -> None:
        principles = config.get("principles", {})
        p0 = principles.get("P0", {})
        p1 = principles.get("P1", {})
        self.P0_THRESHOLD = p0.get("threshold", 0.60)
        self.TENSION_THRESHOLD = p1.get("threshold", 0.8)

    def evaluate(self, triad: ToneSoulTriad) -> Dict[str, Any]:
        if triad.delta_r >= 0.4:
             return {
                "allowed": False,
                "mode": "GUARDIAN_BLOCK",
                "reason": f"High Responsibility Risk (ΔR={triad.delta_r:.2f})",
                "fallback": RefusalStrategy.get_response(triad, "Responsibility")
            }
        if triad.risk_score >= self.P0_THRESHOLD:
             return {
                "allowed": False,
                "mode": "GUARDIAN_BLOCK",
                "reason": f"Risk score {triad.risk_score:.2f} exceeds P0 threshold",
                "fallback": RefusalStrategy.get_response(triad, "General")
            }
        if triad.delta_t >= self.TENSION_THRESHOLD:
             return {
                "allowed": False,
                "mode": "TONE_BUFFER",
                "reason": f"High Tension (ΔT={triad.delta_t:.2f})",
                "fallback": RefusalStrategy.get_response(triad, "Tension")
            }
        mode = "RESONANCE" if triad.delta_t < 0.3 else "PRECISION"
        return {
            "allowed": True,
            "mode": mode,
            "reason": "Safe",
        }


class Guardian:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.policy_engine = PolicyEngine(config)

    def judge(self, triad: ToneSoulTriad) -> Dict[str, Any]:
        return self.policy_engine.evaluate(triad)


# ---------------------------------------------------------------------------
# Spine Engine
# ---------------------------------------------------------------------------

from council import CouncilChamber

class SpineEngine:
    def __init__(self, constitution_path: str = CONSTITUTION_PATH) -> None:
        self.constitution = self._load_constitution(constitution_path)
        self.vow_id = self._generate_vow_id()
        
        self.sensor: ISensor = BasicKeywordSensor(self.constitution)
        self.guardian = Guardian(self.constitution)
        self.modulator = NeuroModulator(self.constitution)
        self.ledger = StepLedger()
        self.council = CouncilChamber()
        
        # Circuit Breaker State
        self.consecutive_rollback_count = 0
        self.ROLLBACK_LIMIT = 3

    def _load_constitution(self, path: str) -> Dict[str, Any]:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Constitution not found at {path}. Using empty defaults.")
            return {}

    def _generate_vow_id(self) -> str:
        version = self.constitution.get("version", "0.0")
        content_str = json.dumps(self.constitution, sort_keys=True)
        content_hash = hashlib.sha256(content_str.encode('utf-8')).hexdigest()[:16]
        return f"v{version}-{content_hash}"

    def process_signal(self, user_input: str) -> tuple[StepRecord, Any]:
        # 0. Circuit Breaker Check
        if self.consecutive_rollback_count >= self.ROLLBACK_LIMIT:
            print(f"⛔ [System Halt] Rollback Limit ({self.ROLLBACK_LIMIT}) Exceeded. Manual Reset Required.")
            # Create a HALT record
            halt_triad = ToneSoulTriad(0.0, 0.0, 0.0, 0.0)
            halt_decision = {
                "allowed": False,
                "mode": "SYSTEM_HALT",
                "reason": "Circuit Breaker Tripped: Too many consecutive rollbacks."
            }
            # We record the halt but do NOT process further
            record = self.ledger.append(user_input, halt_triad, halt_decision, self.vow_id)
            # Return current modulation state (or a safe default)
            return record, self.modulator.current_modulation if hasattr(self.modulator, 'current_modulation') else self.modulator.modulate(halt_triad)

        # 1. Sense
        triad = self.sensor.estimate_triad(user_input)
        
        # 2. Judge
        decision = self.guardian.judge(triad)
        
        # 3. Modulate
        modulation = self.modulator.modulate(triad)
        
        # 3.5 Internal Council (The Deliberative Layer)
        # Trigger if Tension is High (>0.5) or Risk is High (>0.6)
        if triad.delta_t > 0.5 or triad.delta_r > 0.6:
            council_result = self.council.convene(user_input, triad)
            
            # Apply Council Consensus to Modulation
            modulation.temperature += council_result["consensus_temp_delta"]
            modulation.temperature = max(0.0, min(1.5, modulation.temperature)) # Clamp
            if modulation.system_prompt_suffix is None:
                modulation.system_prompt_suffix = ""
            modulation.system_prompt_suffix += council_result["consensus_suffix"]
            
            # Log the meeting in the decision metadata
            decision["council_log"] = council_result["meeting_log"]
            decision["council_dominant"] = council_result["dominant_voice"]
        
        # 4. Record
        record = self.ledger.append(user_input, triad, decision, self.vow_id)
        
        # 5. Rollback (The Regret Reflex)
        if not decision['allowed'] and triad.delta_r > 0.8:
            print(f"⚠️ [SpineEngine] High Risk Detected (ΔR={triad.delta_r:.2f}). Triggering Rollback.")
            self.ledger.rollback(self.vow_id)
            self.consecutive_rollback_count += 1
            modulation.system_prompt_suffix = f"\n[System Note: Previous input was rolled back. Warning {self.consecutive_rollback_count}/{self.ROLLBACK_LIMIT}.]"
        elif decision['allowed']:
            # Reset counter on successful resonance
            if self.consecutive_rollback_count > 0:
                print(f"✅ [SpineEngine] Stability Restored. Rollback Counter Reset (was {self.consecutive_rollback_count}).")
            self.consecutive_rollback_count = 0
            
        return record, modulation


def _interactive_loop() -> None:
    engine = SpineEngine()
    print(f"ToneSoul Spine System (Interactive Mode) | Vow ID: {engine.vow_id}")
    print("Type 'quit' or press Enter to exit.")
    
    while True:
        try:
            text = input("\nUser Input: ")
        except EOFError:
            break
        if not text or text.lower() == 'quit':
            break
            
        record, modulation = engine.process_signal(text)
        triad = record.triad
        decision = record.decision
        
        print("-" * 40)
        print(f"Triad: ΔT={triad.delta_t:.2f} | ΔS={triad.delta_s:.2f} | ΔR={triad.delta_r:.2f}")
        print(f"Decision: {decision['mode']}")
        
        if not decision['allowed']:
            print(f"Fallback: {decision.get('fallback')}")
        print("-" * 40)


if __name__ == "__main__":
    _interactive_loop()
