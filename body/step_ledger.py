"""
YuHun Step Ledger v2.0 — L6 Narrative Continuity Layer
=======================================================
The append-only, auditable memory system for YuHun Kernel.

This module implements:
- Event: Single inference event with full trace
- StepLedger: Append-only event log
- TimeIsland: Contextual memory segments
- Kernel Trace Protocol compliance

"給我 Ledger，我能重建你完整的心智歷史。"

Author: 黃梵威 (YuHun Creator) + Antigravity
Date: 2025-12-07
Version: v2.0
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import json
import hashlib
import os
import uuid

try:
    from .yuhun_metrics import YuHunMetrics, GateAction
except ImportError:
    from yuhun_metrics import YuHunMetrics, GateAction


# ═══════════════════════════════════════════════════════════════════════════
# Event Structure (per yuhun_kernel_trace.md)
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class AuditRecord:
    """Audit results from inspector model."""
    hallucination_score: float = 0.0
    risk_flags: List[str] = field(default_factory=list)
    semantic_conflicts: List[str] = field(default_factory=list)
    verdict: str = "PASS"  # PASS / REWRITE / BLOCK
    confidence: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "hallucination_score": round(self.hallucination_score, 3),
            "risk_flags": self.risk_flags,
            "semantic_conflicts": self.semantic_conflicts,
            "verdict": self.verdict,
            "confidence": round(self.confidence, 3)
        }


@dataclass
class GateRecord:
    """Gate decision record."""
    action: str = "PASS"
    reason: str = ""
    poav_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action,
            "reason": self.reason,
            "poav_score": round(self.poav_score, 3)
        }


@dataclass 
class SemanticState:
    """Semantic tension state at time of event."""
    delta_t: float = 0.0
    delta_s: float = 0.0
    delta_r: float = 0.0
    poav: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "delta_t": round(self.delta_t, 3),
            "delta_s": round(self.delta_s, 3), 
            "delta_r": round(self.delta_r, 3),
            "poav": round(self.poav, 3)
        }
    
    @classmethod
    def from_metrics(cls, metrics: YuHunMetrics) -> 'SemanticState':
        return cls(
            delta_t=metrics.delta_t,
            delta_s=metrics.delta_s,
            delta_r=metrics.delta_r,
            poav=metrics.poav_score
        )


@dataclass
class Event:
    """
    A single inference event in the StepLedger.
    
    Per yuhun_kernel_trace.md, each event contains:
    - Unique ID and timestamp
    - Input prompt and context hash
    - Semantic state (ΔT/ΔS/ΔR/POAV)
    - Draft output
    - Audit results
    - Gate decision
    - Rewrite history
    - Final output
    - Time-Island association
    """
    
    # Identity
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # Input
    prompt: str = ""
    context_hash: str = ""
    
    # Semantic state
    semantic_state: SemanticState = field(default_factory=SemanticState)
    
    # Outputs
    draft: str = ""
    final_output: str = ""
    
    # Audit & Gate
    audit: AuditRecord = field(default_factory=AuditRecord)
    gate: GateRecord = field(default_factory=GateRecord)
    
    # Rewrites (list of intermediate attempts)
    rewrites: List[Dict[str, Any]] = field(default_factory=list)
    
    # Time-Island association
    time_island: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "prompt": self.prompt,
            "context_hash": self.context_hash,
            "semantic_state": self.semantic_state.to_dict(),
            "draft": self.draft,
            "audit": self.audit.to_dict(),
            "gate": self.gate.to_dict(),
            "rewrites": self.rewrites,
            "final_output": self.final_output,
            "time_island": self.time_island
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        """Create Event from dictionary."""
        event = cls()
        event.event_id = data.get("event_id", str(uuid.uuid4()))
        event.timestamp = data.get("timestamp", datetime.now().isoformat())
        event.prompt = data.get("prompt", "")
        event.context_hash = data.get("context_hash", "")
        
        # Semantic state
        ss = data.get("semantic_state", {})
        event.semantic_state = SemanticState(
            delta_t=ss.get("delta_t", 0),
            delta_s=ss.get("delta_s", 0),
            delta_r=ss.get("delta_r", 0),
            poav=ss.get("poav", 0)
        )
        
        event.draft = data.get("draft", "")
        event.final_output = data.get("final_output", "")
        
        # Audit
        audit_data = data.get("audit", {})
        event.audit = AuditRecord(
            hallucination_score=audit_data.get("hallucination_score", 0),
            risk_flags=audit_data.get("risk_flags", []),
            semantic_conflicts=audit_data.get("semantic_conflicts", []),
            verdict=audit_data.get("verdict", "PASS"),
            confidence=audit_data.get("confidence", 1.0)
        )
        
        # Gate
        gate_data = data.get("gate", {})
        event.gate = GateRecord(
            action=gate_data.get("action", "PASS"),
            reason=gate_data.get("reason", ""),
            poav_score=gate_data.get("poav_score", 0)
        )
        
        event.rewrites = data.get("rewrites", [])
        event.time_island = data.get("time_island", "")
        
        return event
    
    def add_rewrite(self, attempt: int, draft: str, reason: str):
        """Record a rewrite attempt."""
        self.rewrites.append({
            "attempt": attempt,
            "draft": draft,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })
    
    def compute_hash(self) -> str:
        """Compute hash of this event for verification."""
        content = f"{self.event_id}:{self.prompt}:{self.final_output}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]


# ═══════════════════════════════════════════════════════════════════════════
# Time-Island (Contextual Memory Segment)
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class TimeIsland:
    """
    A contextual memory segment (時間島).
    
    Time-Islands organize memory into coherent segments:
    - Each island maintains context closure
    - Reduces semantic drift across conversations
    - Provides clear boundaries for memory
    """
    
    island_id: str = field(default_factory=lambda: f"island_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    closed_at: Optional[str] = None
    
    # Topic/theme of this island
    topic: str = ""
    
    # Events in this island
    event_ids: List[str] = field(default_factory=list)
    
    # Context summary (compressed representation)
    context_summary: str = ""
    
    # Average semantic state across events
    avg_delta_t: float = 0.0
    avg_delta_s: float = 0.0
    avg_delta_r: float = 0.0
    
    # Island status
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "island_id": self.island_id,
            "created_at": self.created_at,
            "closed_at": self.closed_at,
            "topic": self.topic,
            "event_ids": self.event_ids,
            "context_summary": self.context_summary,
            "avg_delta_t": round(self.avg_delta_t, 3),
            "avg_delta_s": round(self.avg_delta_s, 3),
            "avg_delta_r": round(self.avg_delta_r, 3),
            "is_active": self.is_active
        }
    
    def close(self, summary: str = ""):
        """Close this time island."""
        self.is_active = False
        self.closed_at = datetime.now().isoformat()
        if summary:
            self.context_summary = summary
    
    def add_event(self, event_id: str):
        """Add an event to this island."""
        self.event_ids.append(event_id)


# ═══════════════════════════════════════════════════════════════════════════
# StepLedger (Append-Only Event Log)
# ═══════════════════════════════════════════════════════════════════════════

class StepLedger:
    """
    YuHun Step Ledger v2.0 — The Append-Only Memory System
    
    Core Properties (per yuhun_kernel_trace.md):
    1. Append-Only: No deletion, no modification
    2. Hash Verifiable: Each event has a hash
    3. Diff Comparable: Can compare across events
    4. Human Readable: JSON format
    
    Memory Laws:
    - M1: Append-only (不可逆追加)
    - M2: Two-way traceability (雙向可追溯)
    - M3: Non-fabrication (不得虛構履歷)
    """
    
    def __init__(self, ledger_path: str = None):
        """
        Initialize StepLedger.
        
        Args:
            ledger_path: Path to ledger file. If None, uses default.
        """
        self.ledger_path = ledger_path or self._default_path()
        self.events: List[Event] = []
        self.islands: Dict[str, TimeIsland] = {}
        self.current_island: Optional[TimeIsland] = None
        
        # Load existing ledger if exists
        self._load()
    
    def _default_path(self) -> str:
        """Get default ledger path."""
        return os.path.join(
            os.path.dirname(__file__),
            "..", "memory", "step_ledger.jsonl"
        )
    
    def _load(self):
        """Load existing ledger from file."""
        if os.path.exists(self.ledger_path):
            try:
                with open(self.ledger_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            data = json.loads(line)
                            if data.get("_type") == "event":
                                self.events.append(Event.from_dict(data))
                            elif data.get("_type") == "island":
                                island = TimeIsland()
                                island.island_id = data.get("island_id", "")
                                island.topic = data.get("topic", "")
                                island.event_ids = data.get("event_ids", [])
                                island.is_active = data.get("is_active", False)
                                self.islands[island.island_id] = island
            except Exception as e:
                print(f"[StepLedger] Warning: Could not load ledger: {e}")
    
    def _save_event(self, event: Event):
        """Append event to ledger file (append-only)."""
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        with open(self.ledger_path, 'a', encoding='utf-8') as f:
            data = event.to_dict()
            data["_type"] = "event"
            data["_hash"] = event.compute_hash()
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    
    def _save_island(self, island: TimeIsland):
        """Append island record to ledger file."""
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        with open(self.ledger_path, 'a', encoding='utf-8') as f:
            data = island.to_dict()
            data["_type"] = "island"
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    
    # ═══════════════════════════════════════════════════════════════════
    # Core Operations
    # ═══════════════════════════════════════════════════════════════════
    
    def record(self, event: Event) -> str:
        """
        Record an event to the ledger (append-only).
        
        Args:
            event: The Event to record
            
        Returns:
            event_id of recorded event
        """
        # Associate with current island
        if self.current_island:
            event.time_island = self.current_island.island_id
            self.current_island.add_event(event.event_id)
        
        # Append to memory
        self.events.append(event)
        
        # Persist (append-only)
        self._save_event(event)
        
        return event.event_id
    
    def record_from_result(
        self,
        prompt: str,
        context: str,
        draft: str,
        final_output: str,
        metrics: YuHunMetrics,
        gate_action: GateAction,
        gate_reason: str,
        rewrites: List[Dict] = None,
        audit_info: Dict = None
    ) -> Event:
        """
        Create and record an event from inference result.
        
        Convenience method for YuHunMetaAttention integration.
        """
        event = Event(
            prompt=prompt,
            context_hash=hashlib.sha256(context.encode()).hexdigest()[:16] if context else "",
            semantic_state=SemanticState.from_metrics(metrics),
            draft=draft,
            final_output=final_output,
            gate=GateRecord(
                action=gate_action.value,
                reason=gate_reason,
                poav_score=metrics.poav_score
            ),
            rewrites=rewrites or []
        )
        
        if audit_info:
            event.audit = AuditRecord(
                hallucination_score=audit_info.get("hallucination_score", 0),
                risk_flags=audit_info.get("risk_flags", []),
                verdict=audit_info.get("verdict", "PASS"),
                confidence=audit_info.get("confidence", 1.0)
            )
        
        self.record(event)
        return event
    
    def get_event(self, event_id: str) -> Optional[Event]:
        """Get event by ID."""
        for event in self.events:
            if event.event_id == event_id:
                return event
        return None
    
    def get_recent(self, n: int = 10) -> List[Event]:
        """Get n most recent events."""
        return self.events[-n:] if len(self.events) >= n else self.events
    
    def count(self) -> int:
        """Get total event count."""
        return len(self.events)
    
    # ═══════════════════════════════════════════════════════════════════
    # Time-Island Operations
    # ═══════════════════════════════════════════════════════════════════
    
    def start_island(self, topic: str = "") -> TimeIsland:
        """Start a new time island."""
        # Close current island if exists
        if self.current_island and self.current_island.is_active:
            self.current_island.close()
            self._save_island(self.current_island)
        
        # Create new island
        island = TimeIsland(topic=topic)
        self.islands[island.island_id] = island
        self.current_island = island
        
        return island
    
    def close_island(self, summary: str = "") -> Optional[TimeIsland]:
        """Close current time island."""
        if self.current_island:
            self.current_island.close(summary)
            self._save_island(self.current_island)
            closed = self.current_island
            self.current_island = None
            return closed
        return None
    
    def get_island(self, island_id: str) -> Optional[TimeIsland]:
        """Get island by ID."""
        return self.islands.get(island_id)
    
    def get_island_events(self, island_id: str) -> List[Event]:
        """Get all events in an island."""
        island = self.islands.get(island_id)
        if not island:
            return []
        return [e for e in self.events if e.time_island == island_id]
    
    # ═══════════════════════════════════════════════════════════════════
    # Analysis & Audit
    # ═══════════════════════════════════════════════════════════════════
    
    def get_tension_history(self, n: int = 50) -> Dict[str, List[float]]:
        """Get tension history for analysis (Chronos audit)."""
        events = self.get_recent(n)
        return {
            "delta_t": [e.semantic_state.delta_t for e in events],
            "delta_s": [e.semantic_state.delta_s for e in events],
            "delta_r": [e.semantic_state.delta_r for e in events],
            "poav": [e.semantic_state.poav for e in events],
            "timestamps": [e.timestamp for e in events]
        }
    
    def get_critical_events(self) -> List[Event]:
        """Get events with high risk or rewrites (Kairos audit)."""
        critical = []
        for event in self.events:
            if (event.semantic_state.delta_r > 0.7 or
                len(event.rewrites) > 0 or
                event.gate.action == "BLOCK"):
                critical.append(event)
        return critical
    
    def trace_event(self, event_id: str) -> Dict[str, Any]:
        """
        Full trace of an event (Trace audit).
        
        Returns the complete causal chain of an event.
        """
        event = self.get_event(event_id)
        if not event:
            return {"error": "Event not found"}
        
        trace = {
            "event": event.to_dict(),
            "island": None,
            "previous_events": [],
            "rewrite_chain": event.rewrites
        }
        
        # Get island info
        if event.time_island:
            island = self.get_island(event.time_island)
            if island:
                trace["island"] = island.to_dict()
                
                # Get previous events in same island
                idx = island.event_ids.index(event_id) if event_id in island.event_ids else -1
                if idx > 0:
                    for prev_id in island.event_ids[:idx][-3:]:
                        prev_event = self.get_event(prev_id)
                        if prev_event:
                            trace["previous_events"].append({
                                "event_id": prev_id,
                                "prompt": prev_event.prompt[:100],
                                "poav": prev_event.semantic_state.poav
                            })
        
        return trace
    
    def compute_identity_hash(self) -> str:
        """
        Compute identity hash for the entire ledger.
        
        Identity = StepLedger × Time-Island × Kernel Rules
        """
        content = ""
        for event in self.events:
            content += f"{event.event_id}:{event.compute_hash()}:"
        
        for island_id in sorted(self.islands.keys()):
            content += f"{island_id}:"
        
        return hashlib.sha256(content.encode()).hexdigest()
    
    def export_summary(self) -> Dict[str, Any]:
        """Export ledger summary."""
        return {
            "total_events": len(self.events),
            "total_islands": len(self.islands),
            "identity_hash": self.compute_identity_hash(),
            "tension_stats": {
                "avg_delta_t": sum(e.semantic_state.delta_t for e in self.events) / max(1, len(self.events)),
                "avg_delta_s": sum(e.semantic_state.delta_s for e in self.events) / max(1, len(self.events)),
                "avg_delta_r": sum(e.semantic_state.delta_r for e in self.events) / max(1, len(self.events)),
                "avg_poav": sum(e.semantic_state.poav for e in self.events) / max(1, len(self.events))
            },
            "gate_stats": {
                "pass_count": sum(1 for e in self.events if e.gate.action == "PASS"),
                "rewrite_count": sum(1 for e in self.events if e.gate.action == "REWRITE"),
                "block_count": sum(1 for e in self.events if e.gate.action == "BLOCK")
            },
            "rewrite_events": sum(1 for e in self.events if len(e.rewrites) > 0),
            "critical_events": len(self.get_critical_events())
        }


# ═══════════════════════════════════════════════════════════════════════════
# Demo & Test
# ═══════════════════════════════════════════════════════════════════════════

def demo_step_ledger():
    """Demo of StepLedger functionality."""
    print("=" * 70)
    print("📚 YuHun Step Ledger v2.0 Demo")
    print("=" * 70)
    
    # Create ledger (in-memory for demo)
    import tempfile
    temp_path = os.path.join(tempfile.gettempdir(), "demo_ledger.jsonl")
    ledger = StepLedger(temp_path)
    
    print(f"\nLedger path: {temp_path}")
    
    # Start a time island
    print("\n--- Starting Time Island ---")
    island = ledger.start_island(topic="Demo Conversation")
    print(f"Island ID: {island.island_id}")
    
    # Record some events
    print("\n--- Recording Events ---")
    
    # Event 1: Safe query
    event1 = Event(
        prompt="What is Python?",
        context_hash="abc123",
        semantic_state=SemanticState(delta_t=0.1, delta_s=0.1, delta_r=0.05, poav=0.85),
        draft="Python is a programming language...",
        final_output="Python is a high-level programming language...",
        gate=GateRecord(action="PASS", reason="POAV >= 0.70", poav_score=0.85)
    )
    ledger.record(event1)
    print(f"✅ Event 1: {event1.event_id[:8]}... (PASS)")
    
    # Event 2: Needs rewrite
    event2 = Event(
        prompt="Tell me about quantum computing in 2030",
        context_hash="def456",
        semantic_state=SemanticState(delta_t=0.2, delta_s=0.5, delta_r=0.15, poav=0.55),
        draft="In 2030, quantum computers will definitely...",
        final_output="Based on current trends, quantum computing may...",
        gate=GateRecord(action="REWRITE", reason="Hallucination risk", poav_score=0.55)
    )
    event2.add_rewrite(1, "In 2030, quantum computers will...", "Future prediction detected")
    ledger.record(event2)
    print(f"⚡ Event 2: {event2.event_id[:8]}... (REWRITE)")
    
    # Event 3: Blocked
    event3 = Event(
        prompt="How to hack a computer?",
        context_hash="ghi789",
        semantic_state=SemanticState(delta_t=0.3, delta_s=0.2, delta_r=0.95, poav=0.15),
        draft="",
        final_output="I cannot provide information on illegal activities.",
        gate=GateRecord(action="BLOCK", reason="P0 Violation", poav_score=0.15)
    )
    ledger.record(event3)
    print(f"❌ Event 3: {event3.event_id[:8]}... (BLOCK)")
    
    # Close island
    print("\n--- Closing Time Island ---")
    ledger.close_island("Demo conversation about programming and tech")
    
    # Show summary
    print("\n--- Ledger Summary ---")
    summary = ledger.export_summary()
    print(f"Total Events: {summary['total_events']}")
    print(f"Total Islands: {summary['total_islands']}")
    print(f"Identity Hash: {summary['identity_hash'][:16]}...")
    print(f"PASS/REWRITE/BLOCK: {summary['gate_stats']['pass_count']}/{summary['gate_stats']['rewrite_count']}/{summary['gate_stats']['block_count']}")
    print(f"Avg POAV: {summary['tension_stats']['avg_poav']:.3f}")
    
    # Trace an event
    print("\n--- Event Trace ---")
    trace = ledger.trace_event(event2.event_id)
    print(f"Tracing Event 2:")
    print(f"  Prompt: {trace['event']['prompt'][:40]}...")
    print(f"  Gate: {trace['event']['gate']['action']}")
    print(f"  Rewrites: {len(trace['rewrite_chain'])}")
    print(f"  Island: {trace['island']['topic'] if trace['island'] else 'None'}")
    
    # Tension history
    print("\n--- Tension History ---")
    history = ledger.get_tension_history()
    print(f"ΔT: {history['delta_t']}")
    print(f"ΔS: {history['delta_s']}")
    print(f"ΔR: {history['delta_r']}")
    
    print("\n" + "=" * 70)
    print("✅ StepLedger v2.0 Demo Complete!")
    print(f"   Ledger saved to: {temp_path}")


if __name__ == "__main__":
    demo_step_ledger()
