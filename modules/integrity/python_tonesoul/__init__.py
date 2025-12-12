"""Python ToneSoul Reference Implementation

2025年10月 Python Reference Implementation 初始化

This package provides core classes and functions for ToneSoul integrity system:
- ToneVector: Tone space vector representation
- CrossReflection: Cross-reflection analysis with temporal islands integration
- TemporalIslandsMemory: Temporal pattern memory system
- applyThresholdMapping: Threshold mapping utilities
"""

from .tonevector import ToneVector, applyThresholdMapping
from .crossreflection import CrossReflection
from .islands import TemporalIslandsMemory

__version__ = "0.1.0"
__all__ = [
    "ToneVector",
    "CrossReflection",
    "TemporalIslandsMemory",
    "applyThresholdMapping",
]
