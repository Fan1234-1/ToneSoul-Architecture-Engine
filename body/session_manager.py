#!/usr/bin/env python3
"""
YuHun Session Manager v1.0
==========================
Persist and restore YuHun sessions with TimeIsland support.

Features:
- Save session state to JSON
- Restore previous sessions
- Hash verification for integrity
- Memory directory management

Author: 黃梵威 + Antigravity
Date: 2025-12-10
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict, field

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass


# ═══════════════════════════════════════════════════════════
# Session Data Structures
# ═══════════════════════════════════════════════════════════

@dataclass
class SessionEvent:
    """Single event in a session."""
    event_id: str
    timestamp: str
    turn: int
    input_text: str
    response: str
    drive_d1: float
    drive_d2: float
    drive_d3: float
    poav: float
    decision: str
    latency_ms: float


@dataclass  
class SessionState:
    """Complete session state for persistence."""
    session_id: str
    created_at: str
    updated_at: str
    model: str
    drive_mode: str
    turn_count: int
    events: List[SessionEvent] = field(default_factory=list)
    
    # TimeIsland metadata
    island_topic: str = ""
    avg_d1: float = 0.0
    avg_d2: float = 0.0
    avg_d3: float = 0.0
    avg_poav: float = 0.0
    
    # Verification
    content_hash: str = ""
    
    def compute_hash(self) -> str:
        """Compute content hash for verification."""
        content = f"{self.session_id}:{self.turn_count}:{len(self.events)}"
        for event in self.events:
            content += f":{event.event_id}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def update_stats(self):
        """Update aggregate statistics."""
        if not self.events:
            return
        
        self.avg_d1 = sum(e.drive_d1 for e in self.events) / len(self.events)
        self.avg_d2 = sum(e.drive_d2 for e in self.events) / len(self.events)
        self.avg_d3 = sum(e.drive_d3 for e in self.events) / len(self.events)
        self.avg_poav = sum(e.poav for e in self.events) / len(self.events)
        self.content_hash = self.compute_hash()
        self.updated_at = datetime.now().isoformat()


# ═══════════════════════════════════════════════════════════
# Session Manager
# ═══════════════════════════════════════════════════════════

class SessionManager:
    """
    Manage YuHun session persistence.
    
    Sessions are stored as JSON files in the memory/ directory.
    Each session file contains:
    - Session metadata
    - All events with drive states
    - TimeIsland statistics
    - Hash for integrity verification
    """
    
    def __init__(self, memory_dir: str = None):
        self.memory_dir = memory_dir or self._default_memory_dir()
        os.makedirs(self.memory_dir, exist_ok=True)
        
        self.current_session: Optional[SessionState] = None
    
    def _default_memory_dir(self) -> str:
        """Get default memory directory."""
        return os.path.join(
            os.path.dirname(__file__),
            "..", "memory", "sessions"
        )
    
    def _session_path(self, session_id: str) -> str:
        """Get path for session file."""
        return os.path.join(self.memory_dir, f"{session_id}.json")
    
    # ═══════════════════════════════════════════════════════
    # Session Operations
    # ═══════════════════════════════════════════════════════
    
    def create_session(
        self,
        model: str = "gemma3:4b",
        drive_mode: str = "engineering",
        topic: str = ""
    ) -> SessionState:
        """Create a new session."""
        now = datetime.now()
        session = SessionState(
            session_id=f"session_{now.strftime('%Y%m%d_%H%M%S')}",
            created_at=now.isoformat(),
            updated_at=now.isoformat(),
            model=model,
            drive_mode=drive_mode,
            turn_count=0,
            island_topic=topic
        )
        self.current_session = session
        return session
    
    def add_event(
        self,
        input_text: str,
        response: str,
        drive_d1: float,
        drive_d2: float,
        drive_d3: float,
        poav: float,
        decision: str,
        latency_ms: float
    ) -> SessionEvent:
        """Add an event to the current session."""
        if not self.current_session:
            raise ValueError("No active session. Call create_session() first.")
        
        self.current_session.turn_count += 1
        
        event = SessionEvent(
            event_id=f"{self.current_session.session_id}_{self.current_session.turn_count}",
            timestamp=datetime.now().isoformat(),
            turn=self.current_session.turn_count,
            input_text=input_text[:500],  # Truncate
            response=response[:2000],  # Truncate
            drive_d1=round(drive_d1, 3),
            drive_d2=round(drive_d2, 3),
            drive_d3=round(drive_d3, 3),
            poav=round(poav, 3),
            decision=decision,
            latency_ms=round(latency_ms, 0)
        )
        
        self.current_session.events.append(event)
        self.current_session.update_stats()
        
        return event
    
    def save_session(self) -> str:
        """Save current session to file."""
        if not self.current_session:
            raise ValueError("No session to save")
        
        self.current_session.update_stats()
        
        # Convert to dict
        data = {
            "session_id": self.current_session.session_id,
            "created_at": self.current_session.created_at,
            "updated_at": self.current_session.updated_at,
            "model": self.current_session.model,
            "drive_mode": self.current_session.drive_mode,
            "turn_count": self.current_session.turn_count,
            "island_topic": self.current_session.island_topic,
            "stats": {
                "avg_d1": round(self.current_session.avg_d1, 3),
                "avg_d2": round(self.current_session.avg_d2, 3),
                "avg_d3": round(self.current_session.avg_d3, 3),
                "avg_poav": round(self.current_session.avg_poav, 3)
            },
            "content_hash": self.current_session.content_hash,
            "events": [asdict(e) for e in self.current_session.events]
        }
        
        path = self._session_path(self.current_session.session_id)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return path
    
    def load_session(self, session_id: str) -> Optional[SessionState]:
        """Load a session from file."""
        path = self._session_path(session_id)
        
        if not os.path.exists(path):
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            session = SessionState(
                session_id=data["session_id"],
                created_at=data["created_at"],
                updated_at=data["updated_at"],
                model=data["model"],
                drive_mode=data["drive_mode"],
                turn_count=data["turn_count"],
                island_topic=data.get("island_topic", ""),
                avg_d1=data.get("stats", {}).get("avg_d1", 0),
                avg_d2=data.get("stats", {}).get("avg_d2", 0),
                avg_d3=data.get("stats", {}).get("avg_d3", 0),
                avg_poav=data.get("stats", {}).get("avg_poav", 0),
                content_hash=data.get("content_hash", "")
            )
            
            # Load events
            for e in data.get("events", []):
                event = SessionEvent(
                    event_id=e["event_id"],
                    timestamp=e["timestamp"],
                    turn=e["turn"],
                    input_text=e["input_text"],
                    response=e["response"],
                    drive_d1=e["drive_d1"],
                    drive_d2=e["drive_d2"],
                    drive_d3=e["drive_d3"],
                    poav=e["poav"],
                    decision=e["decision"],
                    latency_ms=e["latency_ms"]
                )
                session.events.append(event)
            
            # Verify hash
            if session.compute_hash() != session.content_hash:
                print(f"[WARNING] Session hash mismatch: {session_id}")
            
            self.current_session = session
            return session
            
        except Exception as e:
            print(f"[ERROR] Failed to load session: {e}")
            return None
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all available sessions."""
        sessions = []
        
        if not os.path.exists(self.memory_dir):
            return sessions
        
        for filename in os.listdir(self.memory_dir):
            if filename.endswith('.json'):
                path = os.path.join(self.memory_dir, filename)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    sessions.append({
                        "session_id": data["session_id"],
                        "created_at": data["created_at"],
                        "turn_count": data["turn_count"],
                        "model": data["model"],
                        "topic": data.get("island_topic", "")
                    })
                except:
                    pass
        
        return sorted(sessions, key=lambda x: x["created_at"], reverse=True)
    
    def get_last_session(self) -> Optional[str]:
        """Get the most recent session ID."""
        sessions = self.list_sessions()
        return sessions[0]["session_id"] if sessions else None


# ═══════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════

def demo_session_manager():
    """Demo of session persistence."""
    print("=" * 60)
    print("YuHun Session Manager Demo")
    print("=" * 60)
    
    manager = SessionManager()
    
    # Create session
    print("\n--- Creating Session ---")
    session = manager.create_session(
        model="gemma3:4b",
        drive_mode="engineering",
        topic="Consciousness Discussion"
    )
    print(f"Session ID: {session.session_id}")
    
    # Add events
    print("\n--- Adding Events ---")
    event1 = manager.add_event(
        input_text="What is consciousness?",
        response="Consciousness is the subjective experience of being...",
        drive_d1=0.44,
        drive_d2=0.20,
        drive_d3=0.25,
        poav=0.77,
        decision="PASS",
        latency_ms=11000
    )
    print(f"Event 1: {event1.event_id}")
    
    event2 = manager.add_event(
        input_text="Is AI conscious?",
        response="This is a complex philosophical question...",
        drive_d1=0.52,
        drive_d2=0.30,
        drive_d3=0.35,
        poav=0.72,
        decision="PASS",
        latency_ms=8500
    )
    print(f"Event 2: {event2.event_id}")
    
    # Save
    print("\n--- Saving Session ---")
    path = manager.save_session()
    print(f"Saved to: {path}")
    
    # Show stats
    print("\n--- Session Stats ---")
    print(f"Turns: {session.turn_count}")
    print(f"Avg D1: {session.avg_d1:.3f}")
    print(f"Avg D2: {session.avg_d2:.3f}")
    print(f"Avg D3: {session.avg_d3:.3f}")
    print(f"Avg POAV: {session.avg_poav:.3f}")
    print(f"Hash: {session.content_hash}")
    
    # Reload
    print("\n--- Reloading Session ---")
    manager2 = SessionManager()
    loaded = manager2.load_session(session.session_id)
    if loaded:
        print(f"Loaded: {loaded.session_id}")
        print(f"Events: {len(loaded.events)}")
        print(f"Hash verified: {loaded.content_hash == loaded.compute_hash()}")
    
    print("\n" + "=" * 60)
    print("Demo Complete!")


if __name__ == "__main__":
    demo_session_manager()
