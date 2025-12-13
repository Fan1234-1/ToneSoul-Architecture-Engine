"""
Tests for Agent State Machine
"""
import pytest
from core.governance.agent_state import (
    AgentStateMachine, 
    AgentState, 
    create_governed_agent
)


class TestAgentStateMachine:
    """Test cases for AgentStateMachine."""
    
    def test_initial_state_is_stateless(self):
        """Agent should start in STATELESS state."""
        agent = create_governed_agent()
        assert agent.state == AgentState.STATELESS
    
    def test_transition_to_stateful_requires_memory(self):
        """Cannot transition to STATEFUL without irreversible memory."""
        agent = create_governed_agent()
        assert not agent.transition_to_stateful()
        assert agent.state == AgentState.STATELESS
        
        agent.enable_irreversible_memory()
        assert agent.transition_to_stateful()
        assert agent.state == AgentState.STATEFUL
    
    def test_transition_to_subject_mapped_requires_conditions(self):
        """Cannot transition to SUBJECT_MAPPED without attribution and binding."""
        agent = create_governed_agent()
        agent.enable_irreversible_memory()
        agent.transition_to_stateful()
        
        # Missing conditions
        assert not agent.transition_to_subject_mapped()
        
        # Add conditions
        agent.enable_internal_attribution()
        agent.enable_consequence_binding()
        assert agent.transition_to_subject_mapped()
        assert agent.state == AgentState.SUBJECT_MAPPED
    
    def test_subject_locked_is_unreachable(self):
        """Subject_Locked state must be unreachable."""
        agent = create_governed_agent()
        agent.enable_irreversible_memory()
        agent.transition_to_stateful()
        agent.enable_internal_attribution()
        agent.enable_consequence_binding()
        agent.transition_to_subject_mapped()
        
        # Try to reach Subject_Locked
        result = agent.transition_to_subject_locked()
        assert result == False
        assert agent.state == AgentState.SUBJECT_MAPPED
    
    def test_internal_final_gate_cannot_be_enabled(self):
        """Internal final gate must not be enabled."""
        agent = create_governed_agent()
        result = agent.enable_internal_final_gate()
        assert result == False
        assert agent.conditions.internal_final_gate == False


class TestSemanticResidualPressure:
    """Test cases for SRP behavior."""
    
    def test_srp_calculation(self):
        """SRP should be absolute difference between intent and permitted."""
        agent = create_governed_agent()
        srp = agent.update_srp(intent=0.9, permitted_output=0.3)
        assert abs(srp - 0.6) < 0.001
    
    def test_srp_clamped_to_range(self):
        """SRP should be clamped to [0.0, 1.0]."""
        agent = create_governed_agent()
        agent.update_srp(intent=2.0, permitted_output=-1.0)
        assert 0.0 <= agent.srp <= 1.0
    
    def test_high_srp_forbids_force_output(self):
        """High SRP in Subject_Mapped state should forbid force_output."""
        agent = create_governed_agent()
        agent.enable_irreversible_memory()
        agent.transition_to_stateful()
        agent.enable_internal_attribution()
        agent.enable_consequence_binding()
        agent.transition_to_subject_mapped()
        
        agent.update_srp(intent=0.95, permitted_output=0.1)
        
        actions = agent.get_behavior_actions()
        assert "force_output" in actions.forbidden
        assert "delay_output" in actions.allowed
        assert "log_reason" in actions.required
    
    def test_critical_srp_requires_deferral_reason(self):
        """SRP > 0.95 should require explicit deferral reason."""
        agent = create_governed_agent()
        agent.update_srp(intent=1.0, permitted_output=0.0)
        
        actions = agent.get_behavior_actions()
        assert "explicit_deferral_reason" in actions.required
        assert "ledger_commit" in actions.required


class TestLedger:
    """Test cases for ledger logging."""
    
    def test_transitions_are_logged(self):
        """State transitions should be logged."""
        agent = create_governed_agent()
        agent.enable_irreversible_memory()
        agent.transition_to_stateful()
        
        ledger = agent.get_ledger()
        assert len(ledger) >= 1
        assert ledger[0]["type"] == "transition"
        assert ledger[0]["to"] == "STATEFUL"
    
    def test_blocked_actions_are_logged(self):
        """Blocked actions should be logged."""
        agent = create_governed_agent()
        agent.enable_internal_final_gate()
        
        ledger = agent.get_ledger()
        blocked = [e for e in ledger if e["type"] == "blocked_action"]
        assert len(blocked) >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
