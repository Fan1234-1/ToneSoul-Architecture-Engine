"""
Thinking Operators - Base Interface
-----------------------------------
Defines the abstract base class and types for cognitive operators.
These are "Hard Operators" that enforce specific reasoning steps.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

class ThinkingOperatorType(Enum):
    OP_ABSTRACT = "OP_ABSTRACT"        # Rational / Audit: Strip to logic skeleton
    OP_REVERSE = "OP_REVERSE"          # Black Mirror: Invert and find risks
    OP_TRANSLATE = "OP_TRANSLATE"      # Co-Voice: Translate across domains
    OP_FORK = "OP_FORK"                # Spark: Generate variations
    OP_RESTRUCT = "OP_RESTRUCT"        # Architect: Restructure topology
    OP_MAP = "OP_MAP"                  # Architect: Map across scenes
    OP_GROUND = "OP_GROUND"            # Rational / Action: Compile to steps
    OP_PIPELINE_FULL = "OP_PIPELINE_FULL" # Meta: Full loop

@dataclass
class OperatorContext:
    """The context passed to an operator."""
    input_text: str
    system_metrics: Dict[str, float] # T, S, R
    history: List[str]
    # Future: Add FS Vector, TimeIsland ID

class ThinkingOperator(ABC):
    def __init__(self, operator_type: ThinkingOperatorType):
        self.operator_type = operator_type

    @abstractmethod
    def execute(self, context: OperatorContext) -> Dict[str, Any]:
        """
        Executes the operator logic.
        Returns a dictionary containing the result and metadata.
        """
        pass
