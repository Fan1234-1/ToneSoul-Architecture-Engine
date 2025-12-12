import pytest
from body.yuhun_sdk import YuHun
from body.persona_library import PersonaLibrary

def test_reset_conversation_goal():
    yuhun = YuHun()
    # Set a goal first
    yuhun.set_conversation_goal('creative')
    assert yuhun.conversation_manager.current_goal is not None
    # Reset the goal
    yuhun.reset_conversation_goal()
    assert yuhun.conversation_manager.current_goal is None

def test_get_current_strategy():
    yuhun = YuHun()
    yuhun.set_conversation_goal('creative')
    strategy = yuhun.get_current_strategy()
    # Should return a PersonaProfile, Spark for creative goal
    assert strategy is not None
    assert hasattr(strategy, 'name')
    # Name may be Chinese or English
    assert strategy.name in ('火花', 'Spark')

def test_process_uses_strategy():
    yuhun = YuHun()
    yuhun.set_conversation_goal('creative')
    result = yuhun.process('測試一下創意的句子')
    # The persona in result should be overridden by chosen strategy
    assert result.persona in ('火花', 'Spark')
