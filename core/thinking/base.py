from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import time

@dataclass
class OperatorContext:
    """Context passed to a Thinking Operator."""
    input_text: str
    system_metrics: Dict[str, float] # e.g., Triad (T, S, R)
    history: List[str]
    global_memory: Any = None # Reference to StepLedger or Graph

@dataclass
class OperationResult:
    """Result produced by a Thinking Operator."""
    operator_id: str
    output: Any # The result (text, plan, list of ideas, etc.)
    meta: Dict[str, Any] # Execution time, confidence, etc.
    logs: List[str] # Internal monologue steps

class ThinkingOperator(ABC):
    """
    Abstract Base Class for ToneSoul Thinking Operators.
    Represents a discrete cognitive function (System-2).
    """
    
    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier for the operator (e.g., 'ABSTRACTION')."""
        pass

    @abstractmethod
    def execute(self, context: OperatorContext) -> OperationResult:
        """
        Executes the cognitive function.
        
        Args:
            context: The input context and system state.
            
        Returns:
            OperationResult containing the output and logs.
        """
        pass

    def log_to_ledger(self, result: OperationResult, ledger: Any):
        """
        Logs the operation result to the StepLedger.
        Can be overridden for custom logging behavior.
        """
        # Default implementation assumes ledger has an append method
        # In a real system, this would format the result into a StepRecord
        pass
