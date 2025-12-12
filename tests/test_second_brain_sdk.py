import pytest
from body.yuhun_sdk import YuHun

def test_second_brain_crud():
    # Initialize YuHun without loading extended personas to speed up
    y = YuHun(load_extended_personas=False)
    # Add a note
    y.add_note('demo', 'hello world')
    note = y.get_note('demo')
    assert note is not None
    assert note['content'] == 'hello world'
    # Search for the note
    results = y.search_notes('hello')
    assert any(n['title'] == 'demo' for n in results)
    # Delete the note
    assert y.delete_note('demo') is True
    assert y.get_note('demo') is None
