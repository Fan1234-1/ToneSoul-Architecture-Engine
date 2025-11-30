"""
ToneSoul Triad State Definition
-------------------------------
Extracted from spine_system.py to prevent circular imports.
"""

from dataclasses import dataclass

@dataclass
class ToneSoulTriad:
    delta_t: float
    delta_s: float
    delta_r: float
    risk_score: float
