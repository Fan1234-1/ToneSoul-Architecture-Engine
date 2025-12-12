import os
import tempfile
import pytest

from body.yuhun_sdk import YuHun
from knowledge_base.init_knowledge import init_db, upsert_concept, get_concept

@pytest.fixture(scope="function")
def temp_db():
    # Create a temporary directory to hold the SQLite DB
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "knowledge.db")
        # Initialize DB at this path by monkeypatching the DB location
        # The init_knowledge module uses a fixed path; we will monkeypatch it
        original_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "knowledge_base", "knowledge.db"))
        # Backup any existing DB
        if os.path.exists(original_db_path):
            os.rename(original_db_path, original_db_path + ".bak")
        # Copy the temporary DB to the expected location
        os.makedirs(os.path.dirname(original_db_path), exist_ok=True)
        open(original_db_path, "a").close()
        init_db()
        yield
        # Cleanup: remove temporary DB and restore original if existed
        if os.path.exists(original_db_path):
            os.remove(original_db_path)
        if os.path.exists(original_db_path + ".bak"):
            os.rename(original_db_path + ".bak", original_db_path)

def test_query_existing_concept(temp_db):
    # Insert a concept
    upsert_concept(name="誠實", definition="Honesty", source_url="http://example.com", updated_at=None)
    sdk = YuHun()
    result = sdk.query_concept("誠實")
    assert isinstance(result, dict)
    assert result.get("name") == "誠實"
    assert result.get("definition") == "Honesty"

def test_query_missing_concept(temp_db):
    sdk = YuHun()
    result = sdk.query_concept("不存在的概念")
    assert result is None
