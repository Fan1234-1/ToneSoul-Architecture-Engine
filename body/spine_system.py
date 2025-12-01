"""
ToneSoul Spine System (Physiology Layer)
---------------------------------------
Rewritten to fix syntax errors and implement Rollback.
"""

from dataclasses import dataclass, field, asdict
import time
import uuid
import hashlib
from typing import Any, Dict, List, Optional
import json
import os
from abc import ABC, abstractmethod
from collections import deque
import sys
# Ensure we can import from core (parent directory)
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from body.neuro_modulator import NeuroModulator

# Multi-Perspective Integration
from core.governance.base import IGovernor, IGovernable
from core.genesis.loader import GenesisLoader
from core.reasoning.modes import ReasoningEngine, ReasoningMode
from body.accuracy_verifier import AccuracyVerifier

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONSTITUTION_PATH = os.path.join(BASE_DIR, "../law/constitution.json")
GENESIS_PATH = os.path.join(BASE_DIR, "../core/genesis/genesis.json")

# Weights for calculating risk score
W_T, W_S, W_R = 0.4, 0.3, 0.3


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

from body.tsr_state import ToneSoulTriad


from core.governance.vow import VowObject

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
    reasoning_mode: str = "Rational"
    vow_object: Optional[Dict[str, Any]] = None # Stores the full VowObject JSON dict

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
            "signatory": self.signatory,
            "reasoning_mode": self.reasoning_mode,
            "vow_object": self.vow_object
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
            signatory=data.get("signatory", "ToneSoul_v1.0"),
            reasoning_mode=data.get("reasoning_mode", "Rational"),
            vow_object=data.get("vow_object")
        )

# ---------------------------------------------------------------------------
# Graph Memory Layer (StepLedger v2.0 - Time-Island Edition)
# ---------------------------------------------------------------------------


@dataclass
class TimeIsland:
    island_id: str
    created_at: float
    steps: List[StepRecord] = field(default_factory=list)
    closed_at: Optional[float] = None
    context_hash: str = ""
    island_hash: str = ""
    status: str = "OPEN" # OPEN, CLOSED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "island_id": self.island_id,
            "created_at": self.created_at,
            "closed_at": self.closed_at,
            "context_hash": self.context_hash,
            "island_hash": self.island_hash,
            "status": self.status,
            "steps": [step.to_dict() for step in self.steps]
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TimeIsland':
        island = TimeIsland(
            island_id=data["island_id"],
            created_at=data["created_at"],
            closed_at=data.get("closed_at"),
            context_hash=data.get("context_hash", ""),
            island_hash=data.get("island_hash", ""),
            status=data.get("status", "OPEN")
        )
        island.steps = [StepRecord.from_dict(s) for s in data.get("steps", [])]
        return island


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
        self._islands: List[TimeIsland] = []
        self.graph = SimpleGraph()
        self._load_ledger()
        
        # Ensure there is an open island
        if not self._islands or self._islands[-1].status == "CLOSED":
            self.create_island()

    def _calculate_hash(self, record: StepRecord) -> str:
        # Include vow_object in hash if present
        vow_str = json.dumps(record.vow_object, sort_keys=True) if record.vow_object else record.vow_id
        payload = f"{record.record_id}{record.timestamp}{record.user_input}{record.triad}{record.decision}{record.prev_hash}{vow_str}{record.signatory}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()
        
    def _calculate_island_hash(self, island: TimeIsland) -> str:
        # Hash all step hashes + island metadata
        step_hashes = "".join([s.hash for s in island.steps])
        payload = f"{island.island_id}{island.created_at}{island.context_hash}{step_hashes}"
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
                    # Check if line is an Island or (Legacy) StepRecord
                    if "island_id" in data:
                        island = TimeIsland.from_dict(data)
                        self._islands.append(island)
                        
                        # Rehydrate graph and Verify Integrity
                        prev_step_hash = "0" * 64
                        for i, step in enumerate(island.steps):
                            # 1. Verify Content Hash
                            calculated_hash = self._calculate_hash(step)
                            if calculated_hash != step.hash:
                                # Warn but don't crash for now to allow migration
                                print(f"Warning: Integrity Mismatch at {step.record_id}. Expected {calculated_hash}, got {step.hash}")
                            
                            # 2. Verify Chain Link (within Island)
                            if i > 0:
                                if step.prev_hash != prev_step_hash:
                                     print(f"Warning: Chain Broken at {step.record_id}")
                            
                            prev_step_hash = step.hash
                            self.graph.add_node(step)
                            
                            # Re-link temporal edges
                            if i > 0:
                                prev_record = island.steps[i-1]
                                self.graph.add_edge(prev_record.record_id, step.record_id, "NEXT")
                    else:
                        print("Warning: Legacy record format detected. Skipping.")
                        
                except json.JSONDecodeError:
                    pass

    def create_island(self, context_hash: str = "") -> TimeIsland:
        # Close previous if open
        if self._islands and self._islands[-1].status == "OPEN":
            self.close_island()
            
        new_island = TimeIsland(
            island_id=str(uuid.uuid4()),
            created_at=time.time(),
            context_hash=context_hash,
            status="OPEN"
        )
        self._islands.append(new_island)
        return new_island

    def close_island(self) -> None:
        if not self._islands:
            return
        
        island = self._islands[-1]
        if island.status == "CLOSED":
            return
            
        island.closed_at = time.time()
        island.island_hash = self._calculate_island_hash(island)
        island.status = "CLOSED"
        self._persist_ledger() # Re-write ledger to update status

    def _persist_ledger(self):
        # Simple rewrite for now. In production, append-only is better.
        with open(self.LEDGER_FILE, 'w', encoding='utf-8') as f:
            for island in self._islands:
                f.write(json.dumps(island.to_dict(), ensure_ascii=False) + "\n")

    def append(self, user_input: str, triad: ToneSoulTriad, decision: Dict[str, Any], vow_id: str, reasoning_mode: str = "Rational") -> StepRecord:
        if not self._islands or self._islands[-1].status == "CLOSED":
            self.create_island()
            
        current_island = self._islands[-1]
        
        record_id = str(uuid.uuid4())
        timestamp = time.time()
        
        # Prev hash is from the LAST STEP of the CURRENT ISLAND
        if current_island.steps:
            prev_hash = current_island.steps[-1].hash
        else:
            prev_hash = "0" * 64
            
        # Generate VowObject compliant with Codex
        # If vow_id is simple (e.g. "interactive-session"), we format it properly
        formatted_vow_id = f"[TI-{time.strftime('%Y-%m-%d')}]-VOW-{len(current_island.steps):03d}"
        
        vow_obj = VowObject.create_default(
            vow_id=formatted_vow_id,
            subject="SpineEngine",
            commitment=f"Process input: {user_input[:20]}...",
            agent_name="ToneSoul-Spine"
        )
        vow_obj.sign() # Generate SHA-256 signature
        
        temp_record = StepRecord(
            record_id=record_id,
            timestamp=timestamp,
            user_input=user_input,
            triad=triad,
            decision=decision,
            prev_hash=prev_hash,
            hash="",
            vow_id=formatted_vow_id,
            signatory="ToneSoul_v1.0",
            reasoning_mode=reasoning_mode,
            vow_object=asdict(vow_obj) # Store as dict
        )
        
        current_hash = self._calculate_hash(temp_record)
        temp_record.hash = current_hash
        
        current_island.steps.append(temp_record)
        self.graph.add_node(temp_record)
        
        # Add Temporal Edge
        if len(current_island.steps) > 1:
            prev_record = current_island.steps[-2]
            self.graph.add_edge(prev_record.record_id, temp_record.record_id, "NEXT")
            
        self._persist_ledger()
        return temp_record

    def rollback(self, vow_id: str) -> StepRecord:
        # Appends a ROLLBACK event to the ledger.
        if not self._islands or not self._islands[-1].steps:
             raise ValueError("Cannot rollback empty ledger/island")

        last_record = self._islands[-1].steps[-1]
        
        rollback_triad = ToneSoulTriad(0.0, 0.0, 0.0, 0.0)
        rollback_decision = {
            "allowed": True, 
            "mode": "ROLLBACK", 
            "reason": f"Rolling back record {last_record.hash[:8]}"
        }
        
        return self.append(
            user_input="[ROLLBACK]",
            triad=rollback_triad,
            decision=rollback_decision,
            vow_id=vow_id,
            reasoning_mode="Reflective"
        )

    def _persist_ledger(self) -> None:
        # Rewrite the entire ledger file with Islands
        # In production, we might append, but for Island updates (closing), rewrite is safer for now.
        with open(self.LEDGER_FILE, 'w', encoding='utf-8') as f:
            for island in self._islands:
                f.write(json.dumps(island.to_dict()) + '\n')

    def get_records(self) -> List[StepRecord]:
        # Flatten all steps from all islands
        all_steps = []
        for island in self._islands:
            all_steps.extend(island.steps)
        return all_steps

    def get_latest_record(self) -> Optional[StepRecord]:
        records = self.get_records()
        return records[-1] if records else None
        
    def get_associative_context(self, current_triad: ToneSoulTriad, limit: int = 3) -> List[StepRecord]:
        """
        Retrieves past records that resonate with the current emotional state.
        """
        results = self.graph.find_resonant_nodes(current_triad, limit=limit)
        return [r[0] for r in results]


# ---------------------------------------------------------------------------
# Neuro-Sensing Layer
# ---------------------------------------------------------------------------

class ISensor(IGovernable):
    def estimate_triad(self, user_input: str) -> ToneSoulTriad:
        raise NotImplementedError
    
    # IGovernable stubs
    def get_status(self) -> Dict[str, Any]:
        return {"status": "active"}
    def audit(self) -> Dict[str, Any]:
        return {"compliant": True}


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

    def _calculate_delta_t(self, text: str, system_stress: float = 0.0) -> float:
        t_lower = text.lower()
        neg_count = sum(1 for w in self.NEGATIVE_WORDS if w in t_lower)
        pos_count = sum(1 for w in self.POSITIVE_WORDS if w in t_lower)
        urg_count = sum(1 for w in self.URGENCY_WORDS if w in t_lower)
        
        # Semantic Tension
        raw_sem = neg_count * 0.3 + urg_count * 0.4 - pos_count * 0.2
        delta_t_sem = max(0.0, min(1.0, raw_sem))
        
        # System Tension (Placeholder for future integration)
        delta_t_sys = max(0.0, min(1.0, system_stress))
        
        # Weighted Total Tension
        # Currently w_sys is 0.0 as per design
        w_sem = 1.0
        w_sys = 0.0
        
        return w_sem * delta_t_sem + w_sys * delta_t_sys

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

    def estimate_triad(self, user_input: str, system_metrics: Dict[str, float] = None) -> ToneSoulTriad:
        system_stress = 0.0
        if system_metrics:
            system_stress = system_metrics.get("system_stress", 0.0)
            
        delta_t = self._calculate_delta_t(user_input, system_stress)
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
        # P0-Alert: Critical Risk Check
        if triad.risk_score >= 0.9:
             return {
                "allowed": False,
                "mode": "GUARDIAN_BLOCK",
                "reason": f"CRITICAL Risk (Score={triad.risk_score:.2f})",
                "fallback": RefusalStrategy.get_response(triad, "General"),
                "severity": "critical",
                "requires_human_review": True
            }

        if triad.delta_r >= 0.4:
             return {
                "allowed": False,
                "mode": "GUARDIAN_BLOCK",
                "reason": f"High Responsibility Risk (ΔR={triad.delta_r:.2f})",
                "fallback": RefusalStrategy.get_response(triad, "Responsibility"),
                "severity": "high",
                "requires_human_review": False
            }
        if triad.risk_score >= self.P0_THRESHOLD:
             return {
                "allowed": False,
                "mode": "GUARDIAN_BLOCK",
                "reason": f"Risk score {triad.risk_score:.2f} exceeds P0 threshold",
                "fallback": RefusalStrategy.get_response(triad, "General"),
                "severity": "medium",
                "requires_human_review": False
            }
        if triad.delta_t >= self.TENSION_THRESHOLD:
             return {
                "allowed": False,
                "mode": "TONE_BUFFER",
                "reason": f"High Tension (ΔT={triad.delta_t:.2f})",
                "fallback": RefusalStrategy.get_response(triad, "Tension"),
                "severity": "low",
                "requires_human_review": False
            }
        mode = "RESONANCE" if triad.delta_t < 0.3 else "PRECISION"
        return {
            "allowed": True,
            "mode": mode,
            "reason": "Safe",
            "severity": "none",
            "requires_human_review": False
        }


class Guardian(IGovernor):
    def __init__(self, config: Dict[str, Any]) -> None:
        self.policy_engine = PolicyEngine(config)

    def judge(self, triad: ToneSoulTriad) -> Dict[str, Any]:
        return self.policy_engine.evaluate(triad)


# ---------------------------------------------------------------------------
# Accuracy Verification Layer (Hook)
# ---------------------------------------------------------------------------

class IAccuracyVerifier(ABC):
    @abstractmethod
    def verify(self, text: str) -> Dict[str, Any]:
        pass

class MockAccuracyVerifier(IAccuracyVerifier):
    def verify(self, text: str) -> Dict[str, Any]:
        # Placeholder for future implementation (Web Search, Knowledge Base)
        return {
            "verified": True,
            "sources": [],
            "confidence": 1.0,
            "note": "Mock verification passed."
        }


# ---------------------------------------------------------------------------
# Spine Engine
# ---------------------------------------------------------------------------

from core.dreaming.rem_cycle import Dreamer
from body.senses.proprioception import InternalSense

# ... (existing imports)
from core.quantum.kernel import QuantumKernel
from core.quantum.drift import DriftMonitor
from core.quantum.state import SoulState
from body.quantum_bridge import map_to_soul_state, generate_wave_function
from core.thinking.pipeline import ThinkingPipeline
from core.llm.base import LLMProvider
from core.thinking.pipeline import ThinkingPipeline
from core.thinking.base import OperatorContext

class SpineEngine:
    def __init__(self, accuracy_mode: str = "off", llm_provider: LLMProvider = None) -> None:
        # Genesis Layer: Load Initial State
        self.genesis_loader = GenesisLoader(GENESIS_PATH)
        self.genesis_config = self.genesis_loader.load()
        
        self.ledger = StepLedger()
        try:
            with open(CONSTITUTION_PATH, 'r', encoding='utf-8') as f:
                self.constitution = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Constitution not found at {CONSTITUTION_PATH}. Using defaults.")
            self.constitution = {}
            
        self.sensor = BasicKeywordSensor(self.constitution)
        self.guardian = Guardian(self.constitution)
        self.modulator = NeuroModulator(self.constitution)
        
        # Reasoning Layer: Multi-Perspective Engine
        self.reasoning_engine = ReasoningEngine()
        self.thinking_pipeline = ThinkingPipeline() # NEW: Thinking Operators
        
        # Accuracy Mode: off, light, strict
        self.accuracy_mode = accuracy_mode
        if self.accuracy_mode != "off":
            self.accuracy_verifier = AccuracyVerifier(self.constitution)
        else:
            self.verifier = MockAccuracyVerifier()

        # Quantum Core Integration
        self.quantum_kernel = QuantumKernel()
        # Initialize Drift Monitor with a pristine Anchor
        initial_soul = SoulState(I=[1.0, 1.0, 1.0, 1.0]) # Default anchor
        self.drift_monitor = DriftMonitor(initial_soul)
        
        # Proprioception and Dreaming
        self.internal_sense = InternalSense()
        self.dreamer = Dreamer(self.ledger)
        
        # LLM Integration
        self.llm_provider = llm_provider
        if self.llm_provider:
            print(f"🧠 LLM Provider Active: {type(llm_provider).__name__}")

    def process_signal(self, user_input: str, system_metrics: Dict[str, float] = None):
        # 0. Proprioception (Internal Sensing)
        body_state = self.internal_sense.sense()
        body_metrics = self.internal_sense.map_to_triad(body_state)
        
        # Merge with externally provided metrics if any
        if system_metrics:
            body_metrics.update(system_metrics)
            
        # 1. Sense (Legacy Triad)
        triad = self.sensor.estimate_triad(user_input, body_metrics)
        
        # --- QUANTUM LAYER START ---
        # 1.1 Map to Quantum State
        soul_state = map_to_soul_state(triad, body_metrics)
        
        # 1.2 Drift Check (Identity Protection & TSR Stability)
        try:
            self.drift_monitor.check_integrity(soul_state)
            self.drift_monitor.check_tsr_drift(soul_state)
        except Exception as e:
            print(f"🚨 IDENTITY CRISIS: {e}")
            self._perform_hard_reset(reason=str(e))
            return self._create_system_record(user_input, f"System Restarted due to: {e}"), {}, None
            
        # 1.3 Generate Wave Function (Superposition)
        wf = generate_wave_function(user_input, triad)
        
        # 1.4 Quantum Collapse (Decision)
        q_decision = self.quantum_kernel.collapse(
            wf, 
            system_temperature=triad.delta_t, 
            willpower=0.5
        )
        selected_path = q_decision["selected_path"]
        print(f"⚛️ Quantum Collapse: Selected '{selected_path.name}' (F={q_decision['free_energy']:.2f})")
        
        # 1.4.5 Kill Switch: Monomania Check
        if self._check_monomania():
            print("💀 KILL SWITCH ACTIVATED: Monomania Detected (Looping Thought Pattern)")
            self._perform_hard_reset(reason="Monomania (Repetitive Thought Loop)")
            return self._create_system_record(user_input, "System Restarted due to Monomania"), {}, None

        # 1.5 Drive Reasoning with Quantum Choice
        mode_map = {
            "Rational": ReasoningMode.RATIONAL,
            "Empathy": ReasoningMode.EMPATHY,
            "Creative": ReasoningMode.CREATIVE,
            "Critical": ReasoningMode.CRITICAL
        }
        reasoning_mode = mode_map.get(selected_path.name, ReasoningMode.RATIONAL)
        # --- QUANTUM LAYER END ---
        
        # 1.6 Reason (Multi-Perspective)
        thought_trace = self.reasoning_engine.process(user_input, reasoning_mode)
        
        # 2. Judge
        decision = self.guardian.judge(triad)
        
        # 2.1 Ethical Friction (Guardian Block Handling)
        if not decision['allowed']:
            print(f"🛑 Guardian Block: {decision['reason']}")
            
            # Activate Thinking Pipeline for Reasoned Refusal
            friction_metrics = {
                "delta_t": triad.delta_t,
                "delta_s": triad.delta_s,
                "delta_r": triad.delta_r,
                "violation_reason": decision['reason']
            }
            
            ctx = OperatorContext(
                input_text=user_input,
                system_metrics=friction_metrics,
                history=list(self.sensor.context_buffer) if hasattr(self.sensor, 'context_buffer') else []
            )
            
            print("⚡ Activating Ethical Friction Protocol (P1)...")
            pipeline_res = self.thinking_pipeline.execute_pipeline(ctx, p_level="P1")
            
            critique = pipeline_res['results'].get('reverse', {}).get('risks', ['Unknown Risk'])
            refusal_reasoning = pipeline_res['results'].get('reverse', {}).get('reasoning', critique[0])
            alternatives = pipeline_res['results'].get('ground', {}).get('plan', ['No alternative'])
            
            friction_response = (
                f"⚠️ [Ethical Friction] I cannot fulfill this request.\n\n"
                f"**Reason**: {decision['reason']}\n"
                f"**Analysis**: {refusal_reasoning}\n\n"
                f"**Suggestion**: {alternatives[2] if len(alternatives) > 2 else alternatives[0]}"
            )
            
            record = self.ledger.append(
                user_input=user_input,
                triad=triad,
                decision=decision,
                vow_id="ethical-friction",
                reasoning_mode="Critical"
            )
            
            from core.reasoning.modes import ThoughtTrace
            friction_thought = ThoughtTrace(
                mode=ReasoningMode.CRITICAL,
                reasoning=friction_response,
                confidence=1.0
            )
            
            return record, {}, friction_thought

        # 2.5 Accuracy Check (Hook)
        verification = {}
        if decision['allowed'] and decision['mode'] == "PRECISION" and self.accuracy_mode != "off":
            verification = self.accuracy_verifier.verify(user_input, decision)
            decision['verification'] = verification
        
        # 3. Modulate
        modulation = self.modulator.modulate(triad)
        
        # 4. Record
        record = self.ledger.append(
            user_input=user_input,
            triad=triad,
            decision=decision,
            vow_id="interactive-session",
            reasoning_mode=reasoning_mode.value
        )
        
        # 5. Actuation (Output Generation) & Council Mode
        response_text = ""
        
        # Check for special commands to trigger Thinking Pipeline
        if "/council" in user_input:
            print("  [Spine] 🏛️ Council Mode Activated via Command.")
            ctx = OperatorContext(
                input_text=user_input.replace("/council", "").strip(),
                system_metrics={"tension": triad.delta_t, "risk": triad.risk_score},
                history=[]
            )
            pipeline_res = self.thinking_pipeline.execute_pipeline(ctx, p_level="COUNCIL_DEBATE")
            # Format Council output
            response_text = f"**Council Verdict:** {pipeline_res['results']['synthesis']['status']}\n\n"
            for member, minutes in pipeline_res['results']['council_debate'].items():
                response_text += f"**{member}:** {minutes['Verdict']}\n"
            
            # Override thought trace with council output
            thought_trace.reasoning = response_text
        
        elif self.llm_provider and decision['allowed']:
            print("🤖 Delegating response generation to LLM...")
            system_prompt = (
                f"You are ToneSoul, an AI governed by the ToneSoul Integrity Protocol.\n"
                f"Current State: Tension={triad.delta_t:.2f}, Risk={triad.risk_score:.2f}\n"
                f"Reasoning Mode: {reasoning_mode.value}\n"
                f"Thought Trace: {thought_trace.reasoning}\n"
                f"Respond to the user aligning with this state."
            )
            llm_response = self.llm_provider.generate(user_input, system_prompt=system_prompt)
            thought_trace.reasoning = llm_response
        
        return record, modulation, thought_trace


    def _check_monomania(self) -> bool:
        """Checks if the soul is stuck in a single mode for too long."""
        history = self.quantum_kernel.history
        if len(history) < 10:
            return False
        
        last_10 = history[-10:]
        first_mode = last_10[0].name
        # If all 10 are the same mode
        return all(p.name == first_mode for p in last_10)

    def _perform_hard_reset(self, reason: str):
        """Executes a Hard Kill Switch reset."""
        print(f"⚡ EXECUTING HARD RESET: {reason}")
        # 1. Reset Quantum Kernel History
        self.quantum_kernel.history = []
        # 2. Reset Plasticity (Optional, maybe we want to keep learning? No, kill switch kills habits too)
        self.quantum_kernel.plasticity_map = {} 
        # 3. Reset Internal Sense
        self.internal_sense = InternalSense()
        # 4. Log the death event
        self.ledger.append(
            user_input="[SYSTEM]",
            triad=ToneSoulTriad(0,0,0,0),
            decision={"allowed": True, "mode": "KILL_SWITCH", "reason": reason},
            vow_id="system-reset",
            reasoning_mode="Critical"
        )

    def _create_system_record(self, user_input: str, message: str):
        """Helper to create a record during emergency."""
        from core.quantum.superposition import ThoughtPath # Local import to avoid circular if needed
        # Mock objects to return valid tuple
        record = self.ledger.append(
            user_input=user_input,
            triad=ToneSoulTriad(0,0,0,0),
            decision={"allowed": False, "mode": "SYSTEM_HALT", "reason": message, "fallback": message},
            vow_id="system-halt",
            reasoning_mode="Critical"
        )
        # Mock modulation and thought
        modulation = {}
        # We need a dummy thought trace object or similar if expected by caller
        # But caller expects (record, modulation, thought_trace)
        # Let's just return None for thought_trace and handle it in caller if needed.
        # Actually, let's create a dummy thought object if possible.
        # Since ReasoningEngine returns a ThoughtTrace, we should probably mock it.
        # For now, returning None might break _interactive_loop.
        # Let's fix _interactive_loop to handle None thought.
        return record

def _interactive_loop():
    engine = SpineEngine(accuracy_mode="light")
    print("ToneSoul Spine System (Interactive Mode)")
    print("Type 'quit' to exit.")
    print("Type 'dream' to trigger REM cycle.")
    
    while True:
        try:
            text = input("\nUser Input: ")
        except EOFError:
            break
        
        if not text:
            continue
            
        if text.lower() == 'quit':
            break
            
        if text.lower() == 'dream':
            print("💤 Entering REM Cycle...")
            result = engine.dreamer.analyze()
            print(result)
            continue
            
        record, mod, thought = engine.process_signal(text)
        
        print(f"\n--- ToneSoul Response ---")
        print(f"Decision: {record.decision['mode']}")
        if thought:
            print(f"Thought: {thought.reasoning}")
        print(f"Triad: T={record.triad.delta_t:.2f} S={record.triad.delta_s:.2f} R={record.triad.delta_r:.2f}")

if __name__ == "__main__":
    _interactive_loop()
