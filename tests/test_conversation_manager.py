import pytest
from body.conversation_manager import ConversationManager
from body.persona_library import PersonaLibrary

def test_set_and_reset_goal():
    cm = ConversationManager()
    cm.set_goal('creative', 'Test creative goal')
    assert cm.current_goal is not None
    assert cm.current_goal.name == 'creative'
    cm.current_goal = None
    assert cm.current_goal is None

def test_add_feedback_and_strategy_selection():
    cm = ConversationManager()
    cm.set_goal('creative')
    cm.add_feedback('tone_analysis', 0.8, 'Good tone')
    profile = cm.choose_strategy()
    assert profile is not None
    # Spark persona should be selected for creative goal
    assert profile.name == '火花' or profile.name == 'Spark'
