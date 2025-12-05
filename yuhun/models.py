from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

# 簡單 FS 向量
@dataclass
class FSVector:
    C: float = 0.8   # Clarity / Correctness
    M: float = 0.8   # Meaning / Depth
    R: float = 0.8   # Responsibility
    Gamma: float = 0.8  # Governance / Self-check

@dataclass
class TimeIsland:
    island_id: str
    created_at: str
    title: str
    kairos_tags: List[str] = field(default_factory=list)
    fs_vector: FSVector = field(default_factory=FSVector)
    semantic_tension: float = 0.0
    current_mode: str = "Rational"  # Spark / Rational / CoSpeak / BlackMirror / Audit
    history_digest: str = ""
    last_step_id: Optional[str] = None

@dataclass
class YuHunState:
    active_island: str
    fs: FSVector = field(default_factory=FSVector)
    delta_s_recent: List[float] = field(default_factory=list)
    preferred_mode: str = "Rational"
    available_models: List[str] = field(default_factory=lambda: ["gemma3:4b"]) # Default changed to gemma3:4b as per env
    tool_capabilities: List[str] = field(default_factory=lambda: ["python"])

@dataclass
class YuHunMeta:
    mode_used: str = "Rational"
    fs_delta: Dict[str, float] = field(default_factory=lambda: {"C": 0, "M": 0, "R": 0, "Gamma": 0})
    open_new_island: bool = False
    close_current_island: bool = False
    recommend_tool: str = "none"

@dataclass
class ChronicleEntry:
    step_id: str
    island_id: str
    timestamp: str
    user_input: str
    model_reply_summary: str
    mode_used: str
    fs_before: FSVector
    fs_after: FSVector
    tools_used: List[str] = field(default_factory=list)
    notes: str = ""
