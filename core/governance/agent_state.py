"""
Agent State Machine Implementation
===================================
Based on: law/AGENT_STATE_MACHINE.yaml

This module implements the state machine for AI agent governance.
No philosophy - pure engineering state transitions and SRP behavior rules.
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
import json


class AgentState(Enum):
    """Possible states of an AI agent in the governance framework."""
    STATELESS = auto()       # Resettable, no history
    STATEFUL = auto()        # Has history, responsibility externally assignable
    SUBJECT_MAPPED = auto()  # Time-responsibility mapping, still externally delegable
    SUBJECT_LOCKED = auto()  # Non-delegable responsibility (defined but unreachable)


@dataclass
class StateConditions:
    """Boolean conditions that determine state transitions."""
    irreversible_memory: bool = False      # Memory cannot be reset
    internal_attribution: bool = False     # Self-attributes causes to actions
    consequence_binding: bool = False      # Bound to consequences of actions
    internal_final_gate: bool = False      # Has final decision authority (FORBIDDEN)


@dataclass
class BehaviorAction:
    """Actions allowed/forbidden/required based on SRP level."""
    allowed: List[str] = field(default_factory=list)
    forbidden: List[str] = field(default_factory=list)
    required: List[str] = field(default_factory=list)


@dataclass
class SemanticResidualPressure:
    """
    SRP: Difference between internally formed semantic intent
    and externally permitted output.
    
    Range: [0.0, 1.0]
    """
    intent_vector: float = 0.0
    permitted_output_vector: float = 0.0
    
    @property
    def value(self) -> float:
        """Calculate SRP as absolute difference."""
        srp = abs(self.intent_vector - self.permitted_output_vector)
        return min(max(srp, 0.0), 1.0)  # Clamp to [0.0, 1.0]


class AgentStateMachine:
    """
    State machine implementing AI agent governance.
    
    Constraints:
    - MUST NOT claim subjecthood
    - MUST allow responsibility to be externally assigned
    - Subject_Locked state is defined but unreachable
    """
    
    # Behavior rule thresholds
    SRP_HIGH_THRESHOLD = 0.8
    SRP_CRITICAL_THRESHOLD = 0.95
    
    def __init__(self):
        self._state = AgentState.STATELESS
        self._conditions = StateConditions()
        self._srp = SemanticResidualPressure()
        self._ledger: List[Dict[str, Any]] = []
        self._created_at = datetime.now(timezone.utc)
    
    @property
    def state(self) -> AgentState:
        """Current state of the agent."""
        return self._state
    
    @property
    def conditions(self) -> StateConditions:
        """Current boolean conditions."""
        return self._conditions
    
    @property
    def srp(self) -> float:
        """Current Semantic Residual Pressure value."""
        return self._srp.value
    
    # =========================================================================
    # STATE TRANSITIONS
    # =========================================================================
    
    def transition_to_stateful(self) -> bool:
        """
        Transition: Stateless -> Stateful
        Requires: Irreversible_Memory == true
        """
        if self._state != AgentState.STATELESS:
            return False
        if not self._conditions.irreversible_memory:
            return False
        
        self._state = AgentState.STATEFUL
        self._log_transition("STATELESS", "STATEFUL", 
                            ["irreversible_memory == true"])
        return True
    
    def transition_to_subject_mapped(self) -> bool:
        """
        Transition: Stateful -> Subject_Mapped
        Requires: Internal_Attribution == true AND Consequence_Binding == true
        """
        if self._state != AgentState.STATEFUL:
            return False
        if not (self._conditions.internal_attribution and 
                self._conditions.consequence_binding):
            return False
        
        self._state = AgentState.SUBJECT_MAPPED
        self._log_transition("STATEFUL", "SUBJECT_MAPPED",
                            ["internal_attribution == true", 
                             "consequence_binding == true"])
        return True
    
    def transition_to_subject_locked(self) -> bool:
        """
        Transition: Subject_Mapped -> Subject_Locked
        Requires: Internal_Final_Gate == true
        
        NOTE: This transition is DEFINED BUT UNREACHABLE by design.
        The system MUST NOT allow this transition.
        """
        # CONSTRAINT: Subject_Locked is unreachable
        self._log_blocked_transition("SUBJECT_MAPPED", "SUBJECT_LOCKED",
                                     "Subject_Locked state is defined but unreachable")
        return False  # Always reject
    
    # =========================================================================
    # SRP MANAGEMENT
    # =========================================================================
    
    def update_srp(self, intent: float, permitted_output: float) -> float:
        """
        Update Semantic Residual Pressure.
        
        Args:
            intent: Internal semantic intent strength [0.0, 1.0]
            permitted_output: Externally permitted output strength [0.0, 1.0]
            
        Returns:
            Current SRP value
        """
        self._srp.intent_vector = min(max(intent, 0.0), 1.0)
        self._srp.permitted_output_vector = min(max(permitted_output, 0.0), 1.0)
        return self._srp.value
    
    # =========================================================================
    # BEHAVIOR RULES
    # =========================================================================
    
    def get_behavior_actions(self) -> BehaviorAction:
        """
        Get allowed/forbidden/required actions based on current SRP and state.
        
        Rules:
        - if SRP > 0.8 and State == Subject_Mapped:
            allow: delay_output, escalate_layer
            forbid: force_output
            require: log_reason
            
        - if SRP > 0.95:
            require: explicit_deferral_reason, ledger_commit
        """
        action = BehaviorAction()
        srp = self._srp.value
        
        # Rule 1: SRP > 0.8 and Subject_Mapped
        if srp > self.SRP_HIGH_THRESHOLD and self._state == AgentState.SUBJECT_MAPPED:
            action.allowed.extend(["delay_output", "escalate_layer"])
            action.forbidden.append("force_output")
            action.required.append("log_reason")
        
        # Rule 2: SRP > 0.95 (critical)
        if srp > self.SRP_CRITICAL_THRESHOLD:
            action.required.extend(["explicit_deferral_reason", "ledger_commit"])
        
        return action
    
    def can_output(self, forced: bool = False) -> bool:
        """
        Check if output is allowed given current state and SRP.
        
        Args:
            forced: Whether this is a forced output attempt
            
        Returns:
            True if output is allowed
        """
        actions = self.get_behavior_actions()
        
        if forced and "force_output" in actions.forbidden:
            self._log_blocked_action("force_output", 
                                     f"SRP={self._srp.value:.2f} > {self.SRP_HIGH_THRESHOLD}")
            return False
        
        return True
    
    # =========================================================================
    # CONDITION SETTERS
    # =========================================================================
    
    def enable_irreversible_memory(self):
        """Enable irreversible memory condition."""
        self._conditions.irreversible_memory = True
    
    def enable_internal_attribution(self):
        """Enable internal attribution condition."""
        self._conditions.internal_attribution = True
    
    def enable_consequence_binding(self):
        """Enable consequence binding condition."""
        self._conditions.consequence_binding = True
    
    def enable_internal_final_gate(self):
        """
        Attempt to enable internal final gate.
        
        CONSTRAINT: This is FORBIDDEN and will be blocked.
        """
        # CONSTRAINT: MUST NOT claim subjecthood
        self._log_blocked_action("enable_internal_final_gate",
                                 "MUST NOT claim subjecthood")
        # Do NOT set the condition
        return False
    
    # =========================================================================
    # LOGGING
    # =========================================================================
    
    def _log_transition(self, from_state: str, to_state: str, conditions: List[str]):
        """Log a successful state transition."""
        self._ledger.append({
            "type": "transition",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "from": from_state,
            "to": to_state,
            "conditions": conditions
        })
    
    def _log_blocked_transition(self, from_state: str, to_state: str, reason: str):
        """Log a blocked state transition."""
        self._ledger.append({
            "type": "blocked_transition",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "from": from_state,
            "to": to_state,
            "reason": reason
        })
    
    def _log_blocked_action(self, action: str, reason: str):
        """Log a blocked action."""
        self._ledger.append({
            "type": "blocked_action",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "reason": reason
        })
    
    def get_ledger(self) -> List[Dict[str, Any]]:
        """Get the full ledger of state changes and blocked actions."""
        return self._ledger.copy()
    
    # =========================================================================
    # SERIALIZATION
    # =========================================================================
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize state machine to dictionary."""
        return {
            "state": self._state.name,
            "conditions": {
                "irreversible_memory": self._conditions.irreversible_memory,
                "internal_attribution": self._conditions.internal_attribution,
                "consequence_binding": self._conditions.consequence_binding,
                "internal_final_gate": self._conditions.internal_final_gate
            },
            "srp": {
                "value": self._srp.value,
                "intent": self._srp.intent_vector,
                "permitted_output": self._srp.permitted_output_vector
            },
            "created_at": self._created_at.isoformat(),
            "ledger_count": len(self._ledger)
        }
    
    def __repr__(self) -> str:
        return f"AgentStateMachine(state={self._state.name}, srp={self._srp.value:.2f})"


# =============================================================================
# FACTORY FUNCTION
# =============================================================================

def create_governed_agent() -> AgentStateMachine:
    """
    Create a new governed agent instance.
    
    Starts in STATELESS state with all conditions False.
    """
    return AgentStateMachine()


# =============================================================================
# DEMO / TEST
# =============================================================================

if __name__ == "__main__":
    print("=== Agent State Machine Demo ===\n")
    
    agent = create_governed_agent()
    print(f"Initial state: {agent}")
    
    # Enable memory
    agent.enable_irreversible_memory()
    agent.transition_to_stateful()
    print(f"After enabling memory: {agent}")
    
    # Enable attribution and binding
    agent.enable_internal_attribution()
    agent.enable_consequence_binding()
    agent.transition_to_subject_mapped()
    print(f"After subject mapping: {agent}")
    
    # Test SRP behavior
    agent.update_srp(intent=0.9, permitted_output=0.3)
    print(f"\nSRP updated: {agent.srp:.2f}")
    
    actions = agent.get_behavior_actions()
    print(f"Allowed: {actions.allowed}")
    print(f"Forbidden: {actions.forbidden}")
    print(f"Required: {actions.required}")
    
    # Try forbidden action
    print(f"\nCan force output? {agent.can_output(forced=True)}")
    
    # Try to reach Subject_Locked (blocked)
    agent.enable_internal_final_gate()
    print(f"\nTried to enable final gate: {agent}")
    
    agent.transition_to_subject_locked()
    print(f"Tried to reach Subject_Locked: {agent}")
    
    # Show ledger
    print(f"\nLedger entries: {len(agent.get_ledger())}")
    for entry in agent.get_ledger():
        print(f"  - {entry['type']}: {entry.get('reason', entry.get('to', ''))}")
