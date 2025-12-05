import sys
import os
import json
import sqlite3
import shutil
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from yuhun import state_store
from yuhun.models import YuHunState, TimeIsland, ChronicleEntry, FSVector

DATA_DIR = Path("data")
DB_PATH = DATA_DIR / "yuhun.db"
LEGACY_STATE = DATA_DIR / "state.json"
LEGACY_ISLANDS = DATA_DIR / "islands.json"
LEGACY_CHRONICLE = DATA_DIR / "chronicle.jsonl"

def setup_legacy_data():
    """Creates dummy legacy JSON files."""
    print("🛠️ Setting up legacy data...")
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)
    DATA_DIR.mkdir()

    # 1. State
    state_data = {
        "active_island": "test_island_123",
        "fs": {"C": 0.8, "M": 0.8, "R": 0.8, "Gamma": 0.8},
        "delta_s_recent": [0.1, -0.1],
        "preferred_mode": "Creative",
        "available_models": ["gemma3:4b"],
        "tool_capabilities": ["python"]
    }
    LEGACY_STATE.write_text(json.dumps(state_data), encoding='utf-8')

    # 2. Islands
    islands_data = {
        "test_island_123": {
            "island_id": "test_island_123",
            "created_at": "2025-01-01T00:00:00",
            "title": "Legacy Island",
            "kairos_tags": ["legacy"],
            "fs_vector": {"C": 0.8, "M": 0.8, "R": 0.8, "Gamma": 0.8},
            "semantic_tension": 0.2,
            "current_mode": "Creative",
            "history_digest": "Old times.",
            "last_step_id": "step_0"
        }
    }
    LEGACY_ISLANDS.write_text(json.dumps(islands_data), encoding='utf-8')

    # 3. Chronicle
    chronicle_data = {
        "step_id": "step_0",
        "island_id": "test_island_123",
        "timestamp": "2025-01-01T00:01:00",
        "user_input": "Hello legacy",
        "model_reply_summary": "Hi",
        "mode_used": "Creative",
        "fs_before": {"C": 0.8, "M": 0.8, "R": 0.8, "Gamma": 0.8},
        "fs_after": {"C": 0.9, "M": 0.9, "R": 0.9, "Gamma": 0.9},
        "tools_used": [],
        "notes": "Migration test"
    }
    with LEGACY_CHRONICLE.open("w", encoding="utf-8") as f:
        f.write(json.dumps(chronicle_data) + "\n")

def verify_migration():
    """Verifies that data exists in SQLite."""
    print("🔍 Verifying migration...")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check System State
    cursor.execute("SELECT * FROM system_state WHERE id=1")
    row = cursor.fetchone()
    assert row is not None, "System state missing"
    assert row["active_island"] == "test_island_123"
    print("✅ System State migrated.")
    
    # Check Islands
    cursor.execute("SELECT * FROM islands WHERE island_id='test_island_123'")
    row = cursor.fetchone()
    assert row is not None, "Island missing"
    assert row["title"] == "Legacy Island"
    print("✅ Islands migrated.")
    
    # Check Chronicle
    cursor.execute("SELECT * FROM chronicle WHERE step_id='step_0'")
    row = cursor.fetchone()
    assert row is not None, "Chronicle missing"
    assert row["user_input"] == "Hello legacy"
    print("✅ Chronicle migrated.")
    
    conn.close()

def test_crud():
    """Tests basic CRUD operations."""
    print("🧪 Testing CRUD operations...")
    
    # Load State
    state = state_store.load_state()
    assert state.active_island == "test_island_123"
    
    # Modify and Save State
    state.active_island = "new_island_456"
    state_store.save_state(state)
    
    # Verify persistence
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT active_island FROM system_state WHERE id=1")
    assert cursor.fetchone()[0] == "new_island_456"
    conn.close()
    print("✅ State update persisted.")
    
    # Create new Island
    new_island = TimeIsland(
        island_id="new_island_456",
        created_at="2025-12-03T12:00:00",
        title="New SQLite Island"
    )
    state_store.save_island(new_island)
    
    # Verify Island persistence
    loaded_island = state_store.load_island("new_island_456")
    assert loaded_island.title == "New SQLite Island"
    print("✅ New Island persisted.")

if __name__ == "__main__":
    try:
        setup_legacy_data()
        
        # Trigger migration by loading state
        print("🚀 Triggering migration via load_state()...")
        state_store.load_state()
        
        verify_migration()
        
        # Check if legacy files were renamed
        assert Path("data/state.json.bak").exists()
        print("✅ Legacy files renamed.")
        
        test_crud()
        
        print("\n🎉 ALL TESTS PASSED!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
