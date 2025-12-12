import json
import os
import time
import uuid
from dataclasses import dataclass, asdict, field
from typing import List, Any, Optional


@dataclass
class Engram:
    """
    A unit of long-term memory (Conscious Ingestion).
    Represents a consolidated fact or experience.
    """
    engram_id: str
    content: str
    source_record_id: Optional[str]
    importance: float # 0.0 - 1.0
    timestamp: float
    tags: List[str] = field(default_factory=list)


class MemoryConsolidator:
    """
    The Hippocampus of ToneSoul.
    Consolidates short-term ledger entries into long-term Engrams.
    """
    MEMORY_FILE = "core_memory.json"

    def __init__(self):
        self.engrams: List[Engram] = []
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.MEMORY_FILE):
            try:
                with open(self.MEMORY_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.engrams = [Engram(**e) for e in data]
            except Exception as e:
                print(f"⚠️ [Hippocampus] Failed to load memory: {e}")
                self.engrams = []
        else:
            self.engrams = []

    def _persist_memory(self):
        with open(self.MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump([asdict(e) for e in self.engrams], f, indent=2)

    def engrave(self, content: str, source_id: str = None, importance: float = 0.5, tags: List[str] = None):
        """
        Creates a new Engram and stores it.
        """
        engram = Engram(
            engram_id=str(uuid.uuid4()),
            content=content,
            source_record_id=source_id,
            importance=importance,
            timestamp=time.time(),
            tags=tags or []
        )
        self.engrams.append(engram)
        self._persist_memory()
        print(f"🧠 [Hippocampus] Engraved: '{content[:30]}...' (Imp={importance:.2f})")

    def recall(self, query: str, limit: int = 3) -> List[Engram]:
        """
        Retrieves relevant Engrams based on query context.
        Simple keyword matching for now.
        """
        query_tokens = set(query.lower().split())
        results = []

        for engram in self.engrams:
            content_tokens = set(engram.content.lower().split())
            if not content_tokens:
                continue

            # Jaccard Similarity
            intersection = len(query_tokens & content_tokens)
            union = len(query_tokens | content_tokens)
            score = intersection / union if union > 0 else 0.0

            # Boost by importance
            final_score = score * (1.0 + engram.importance)

            if final_score > 0.1: # Threshold
                results.append((engram, final_score))

        # Sort by score descending
        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results[:limit]]

    def consolidate(self, ledger_records: List[Any]):
        """
        Scans recent ledger records and extracts high-value memories.
        This is the 'Conscious Ingestion' process.
        """
        print("🧠 [Hippocampus] Consolidating memories...")
        count = 0
        for record in ledger_records:
            # Skip if already consolidated (we need a way to track this,
            # for now we just check if content exists to avoid dupes roughly)
            # In production, StepRecord should have a 'consolidated' flag.

            # Heuristic 1: Vow Objects are critical
            if record.vow_object:
                try:
                    commitment = record.vow_object.get('vow_core', {}).get('commitment', 'Unknown Vow')
                    content = f"Vow taken: {commitment}"
                    if not self._exists(content):
                        self.engrave(content, record.record_id, importance=1.0, tags=["vow", "ethics"])
                        count += 1
                except Exception as e:
                    print(f"⚠️ [Hippocampus] Error extracting vow: {e}")

            # Heuristic 2: High Tension Events (Trauma/Lessons)
            if record.triad.delta_t > 0.7:
                content = f"High stress event: {record.user_input} -> {record.decision['mode']}"
                if not self._exists(content):
                    self.engrave(content, record.record_id, importance=0.8, tags=["stress", "lesson"])
                    count += 1

            # Heuristic 3: Explicit User Facts (Simple regex for now)
            # "My name is X", "I like Y"
            lower_input = record.user_input.lower()
            if "my name is" in lower_input or "i like" in lower_input:
                 if not self._exists(record.user_input):
                    self.engrave(record.user_input, record.record_id, importance=0.9, tags=["user_fact"])
                    count += 1

        if count > 0:
            print(f"🧠 [Hippocampus] Consolidated {count} new engrams.")
        else:
            print("🧠 [Hippocampus] No new significant memories found.")

    def _exists(self, content: str) -> bool:
        return any(e.content == content for e in self.engrams)
