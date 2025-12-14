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
        from .vector_store import VectorStore
        self.vector_store = VectorStore()
        
        # We still keep loaded engrams for fast in-mem access if needed,
        # but primarily rely on vector store for search.
        self.engrams: List[Engram] = []
        # Load logic is now handled by vector_store internally (it loads numpy + json)
        # But to maintain compat with valid_memory checks, we might want to sync?
        # For now, let's trust vector_store.metadata as the source of truth.
        self._sync_mem_from_store()

    def _sync_mem_from_store(self):
        """Syncs local engram list from vector store metadata."""
        if self.vector_store.metadata:
            self.engrams = [Engram(**m) for m in self.vector_store.metadata]
        else:
            self.engrams = []

    def engrave(self, content: str, source_id: str = None, importance: float = 0.5, tags: List[str] = None):
        """
        Creates a new Engram and stores it in the Vector DB.
        """
        from ..brain.llm_client import llm_client
        
        # 1. Generate Embedding
        vector = llm_client.get_embedding(content)
        if not vector:
            print(f"⚠️ [Hippocampus] Failed to embed '{content[:30]}...'. Memory skipped.")
            return

        # 2. Create Engram Object
        engram = Engram(
            engram_id=str(uuid.uuid4()),
            content=content,
            source_record_id=source_id,
            importance=importance,
            timestamp=time.time(),
            tags=tags or []
        )
        
        # 3. Save to Vector Store
        self.vector_store.add(vector, asdict(engram))
        self.engrams.append(engram)
        
        print(f"🧠 [Hippocampus] Engraved (Vectorized): '{content[:30]}...' (Imp={importance:.2f})")

    def recall(self, query: str, limit: int = 3) -> List[Engram]:
        """
        Retrieves relevant Engrams based on query context using Vector Search.
        """
        from ..brain.llm_client import llm_client
        
        # 1. Embed Query
        query_vector = llm_client.get_embedding(query)
        if not query_vector:
            return []

        # 2. Search Vector DB
        # Lower threshold to find *something* if exists
        results = self.vector_store.search(query_vector, k=limit, threshold=0.3)
        
        engrams = []
        for meta, score in results:
            engram = Engram(**meta)
            # Boost score by importance? 
            # Vector score is cosine similarity [0,1].
            # Let's trust semantic similarity primarily.
            engrams.append(engram)
            print(f"🔍 [Recall] Found: '{engram.content[:30]}...' (Sim={score:.2f})")

        return engrams

    def consolidate(self, ledger_records: List[Any]):
        """
        Scans recent ledger records and extracts high-value memories.
        This is the 'Conscious Ingestion' process.
        """
        print("🧠 [Hippocampus] Consolidating memories...")
        count = 0
        for record in ledger_records:
            # Check for consolidation flag (heuristic: check existence)
            
            # Heuristic 1: Vow Objects
            if record.vow_object:
                try:
                    commitment = record.vow_object.get('vow_core', {}).get('commitment', 'Unknown Vow')
                    content = f"Vow taken: {commitment}"
                    if not self._exists(content):
                        self.engrave(content, record.record_id, importance=1.0, tags=["vow", "ethics"])
                        count += 1
                except Exception as e:
                    print(f"⚠️ [Hippocampus] Error extracting vow: {e}")

            # Heuristic 2: High Tension Events
            if record.triad.delta_t > 0.7:
                content = f"High stress event: {record.user_input} -> {record.decision['mode']}"
                if not self._exists(content):
                    self.engrave(content, record.record_id, importance=0.8, tags=["stress", "lesson"])
                    count += 1

            # Heuristic 3: Explicit User Facts
            lower_input = record.user_input.lower()
            if "my name is" in lower_input or "i like" in lower_input:
                 if not self._exists(record.user_input):
                    self.engrave(record.user_input, record.record_id, importance=0.9, tags=["user_fact"])
                    count += 1

        if count > 0:
            print(f"🧠 [Hippocampus] Consolidated {count} new semantic engrams.")
        else:
            print("🧠 [Hippocampus] No new significant memories found.")

    def _exists(self, content: str) -> bool:
        return any(e.content == content for e in self.engrams)

