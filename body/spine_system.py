"""
Spine system for the body layer of ToneSoul. Defines abstract interfaces for
an immutable StepLedger and a SoulTracer to trace responsibility across steps.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class StepRecord:
    """
    A single immutable record in the StepLedger.
    """
    step_id: str
    trace_id: str
    input_snapshot: Dict[str, Any]
    output_snapshot: Dict[str, Any]
    context_hash: str
    timestamp: float
    module_name: str

class StepLedger(ABC):
    """
    Abstract base class for an immutable ledger of steps.
    """

    @abstractmethod
    def append_step(
        self,
        trace_id: str,
        input_snapshot: Dict[str, Any],
        output_snapshot: Dict[str, Any],
        module_name: str,
    ) -> StepRecord:
        """Append an immutable step to the ledger and return the record."""
        pass

    @abstractmethod
    def get_steps(self, trace_id: Optional[str] = None) -> List[StepRecord]:
        """Retrieve all steps or filter by trace id."""
        pass

class SoulTracer:
    """
    Utility class to trace the chain of responsibility through the ledger.
    """

    def __init__(self, ledger: StepLedger):
        self._ledger = ledger

    def trace_responsibility(self, trace_id: str) -> List[StepRecord]:
        """
        Return the list of StepRecords associated with a trace_id to
        reconstruct the chain of responsibility.
        """
        return self._ledger.get_steps(trace_id=trace_id)
