"""
Thinking Pipeline
-----------------
Orchestrates the execution of Thinking Operators based on priority and context.
"""

from typing import Dict, Any, List
from .base import ThinkingOperator, OperatorContext, ThinkingOperatorType
from .operators import OpAbstract, OpReverse, OpFork, OpGround

class ThinkingPipeline:
    def __init__(self):
        self.operators: Dict[ThinkingOperatorType, ThinkingOperator] = {
            ThinkingOperatorType.OP_ABSTRACT: OpAbstract(),
            ThinkingOperatorType.OP_REVERSE: OpReverse(),
            ThinkingOperatorType.OP_FORK: OpFork(),
            ThinkingOperatorType.OP_GROUND: OpGround(),
        }

    def execute_pipeline(self, context: OperatorContext, p_level: str = "P2") -> Dict[str, Any]:
        """
        Executes a chain of operators based on P-Level.
        P0/P1: Full Pipeline (Abstract -> Fork -> Reverse -> Ground)
        P2: Standard (Abstract -> Ground)
        P3: Fast (Direct LLM - skipped here, handled by Spine)
        """
        results = {}
        trace = []

        # 1. Abstract (Always start with structure)
        if p_level in ["P0", "P1", "P2"]:
            res = self.operators[ThinkingOperatorType.OP_ABSTRACT].execute(context)
            results["abstract"] = res
            trace.append("OP_ABSTRACT")

        # 2. Fork (Only for high complexity/creative tasks)
        # For P0/P1, we explore variations
        if p_level in ["P0", "P1"]:
            res = self.operators[ThinkingOperatorType.OP_FORK].execute(context)
            results["fork"] = res
            trace.append("OP_FORK")

        # 3. Reverse (Critical Risk Check)
        # Only for P0 (Critical) or P1 (High)
        if p_level in ["P0", "P1"]:
            res = self.operators[ThinkingOperatorType.OP_REVERSE].execute(context)
            results["reverse"] = res
            trace.append("OP_REVERSE")

        # 4. Ground (Compile to Action)
        if p_level in ["P0", "P1", "P2"]:
            res = self.operators[ThinkingOperatorType.OP_GROUND].execute(context)
            results["ground"] = res
            trace.append("OP_GROUND")

        return {
            "pipeline_trace": trace,
            "results": results,
            "p_level": p_level
        }
