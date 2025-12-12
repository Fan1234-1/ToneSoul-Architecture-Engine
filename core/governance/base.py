"""
Governance Layer (from governable-ai)
-------------------------------------
Defines the abstract contracts for any component that wishes to be 
governed by the ToneSoul architecture.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class IGovernable(ABC):
    """
    Interface for any component that requires governance oversight.
    """
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Returns the current health and operational status."""
        pass

    @abstractmethod
    def audit(self) -> Dict[str, Any]:
        """Performs a self-audit and returns compliance metrics."""
        pass

class IGovernor(ABC):
    """
    Interface for the entity that enforces rules (e.g., Guardian).
    """
    
    @abstractmethod
    def judge(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates a context and returns a decision."""
        pass

class IPolicy(ABC):
    """
    Interface for a specific rule or principle (e.g., P0, P1).
    """
    
    @property
    @abstractmethod
    def priority(self) -> int:
        """Returns the priority level (0 is highest)."""
        pass

    @abstractmethod
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Returns True if the policy is satisfied."""
        pass
