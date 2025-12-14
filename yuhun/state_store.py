import json
import sqlite3
import uuid
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from .models import YuHunState, TimeIsland, ChronicleEntry, FSVector

DB_PATH = Path("data/yuhun.db")
LEGACY_STATE_PATH = Path("data/state.json")
LEGACY_ISLANDS_PATH = Path("data/islands.json")
LEGACY_CHRONICLE_PATH = Path("data/chronicle.jsonl")

def _get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")  # Enable WAL for concurrency
    return conn

def init_db():
    conn = _get_conn()
    cursor = conn.cursor()
    
    # System State Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS system_state (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        active_island TEXT,
        fs TEXT,
        delta_s_recent TEXT,
        preferred_mode TEXT,
        available_models TEXT,
        tool_capabilities TEXT
    )
    ''')
    
    # Islands Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS islands (
        island_id TEXT PRIMARY KEY,
        created_at TEXT,
        title TEXT,
        kairos_tags TEXT,
        fs_vector TEXT,
        semantic_tension REAL,
        current_mode TEXT,
        history_digest TEXT,
        last_step_id TEXT
    )
    ''')
    
    # Chronicle Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chronicle (
        step_id TEXT PRIMARY KEY,
        island_id TEXT,
        timestamp TEXT,
        user_input TEXT,
        model_reply_summary TEXT,
        mode_used TEXT,
        fs_before TEXT,
        fs_after TEXT,
        tools_used TEXT,
        notes TEXT
    )
    ''')
    
    # Indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_chronicle_island ON chronicle(island_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_chronicle_timestamp ON chronicle(timestamp)')
    
    conn.commit()
    conn.close()
    
    _migrate_from_legacy()

def _migrate_from_legacy():
    """Migrates data from legacy JSON files if DB is empty."""
    if not LEGACY_STATE_PATH.exists():
        return
        
    conn = _get_conn()
    cursor = conn.cursor()
    
    # Check if migration is needed (if state table is empty)
    cursor.execute("SELECT count(*) FROM system_state")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    print("📦 [Migration] Migrating legacy data to SQLite...")
    
    try:
        # Migrate State
        if LEGACY_STATE_PATH.exists():
            data = json.loads(LEGACY_STATE_PATH.read_text(encoding='utf-8'))
            cursor.execute('''
            INSERT INTO system_state (id, active_island, fs, delta_s_recent, preferred_mode, available_models, tool_capabilities)
            VALUES (1, ?, ?, ?, ?, ?, ?)
            ''', (
                data["active_island"],
                json.dumps(data["fs"]),
                json.dumps(data.get("delta_s_recent", [])),
                data.get("preferred_mode", "Rational"),
                json.dumps(data.get("available_models", ["gemma3:4b"])),
                json.dumps(data.get("tool_capabilities", ["python"]))
            ))
            
        # Migrate Islands
        if LEGACY_ISLANDS_PATH.exists():
            islands = json.loads(LEGACY_ISLANDS_PATH.read_text(encoding='utf-8'))
            for i_id, data in islands.items():
                cursor.execute('''
                INSERT INTO islands (island_id, created_at, title, kairos_tags, fs_vector, semantic_tension, current_mode, history_digest, last_step_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data["island_id"],
                    data["created_at"],
                    data["title"],
                    json.dumps(data.get("kairos_tags", [])),
                    json.dumps(data["fs_vector"]),
                    data.get("semantic_tension", 0.0),
                    data.get("current_mode", "Rational"),
                    data.get("history_digest", ""),
                    data.get("last_step_id")
                ))
                
        # Migrate Chronicle
        if LEGACY_CHRONICLE_PATH.exists():
            with LEGACY_CHRONICLE_PATH.open("r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip(): continue
                    entry = json.loads(line)
                    cursor.execute('''
                    INSERT INTO chronicle (step_id, island_id, timestamp, user_input, model_reply_summary, mode_used, fs_before, fs_after, tools_used, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        entry["step_id"],
                        entry["island_id"],
                        entry["timestamp"],
                        entry["user_input"],
                        entry["model_reply_summary"],
                        entry["mode_used"],
                        json.dumps(entry["fs_before"]),
                        json.dumps(entry["fs_after"]),
                        json.dumps(entry["tools_used"]),
                        entry["notes"]
                    ))
        
        conn.commit()
        print("✅ [Migration] Legacy data migrated successfully.")
        
        # Backup and rename legacy files (safe migration)
        try:
            # Create safety backups first
            shutil.copy(LEGACY_STATE_PATH, LEGACY_STATE_PATH.with_suffix('.json.backup'))
            if LEGACY_ISLANDS_PATH.exists():
                shutil.copy(LEGACY_ISLANDS_PATH, LEGACY_ISLANDS_PATH.with_suffix('.json.backup'))
            if LEGACY_CHRONICLE_PATH.exists():
                shutil.copy(LEGACY_CHRONICLE_PATH, LEGACY_CHRONICLE_PATH.with_suffix('.jsonl.backup'))
            
            # Only rename after successful backup and commit
            LEGACY_STATE_PATH.rename(LEGACY_STATE_PATH.with_suffix('.json.bak'))
            if LEGACY_ISLANDS_PATH.exists():
                LEGACY_ISLANDS_PATH.rename(LEGACY_ISLANDS_PATH.with_suffix('.json.bak'))
            if LEGACY_CHRONICLE_PATH.exists():
                LEGACY_CHRONICLE_PATH.rename(LEGACY_CHRONICLE_PATH.with_suffix('.jsonl.bak'))
        except Exception as backup_err:
            print(f"⚠️ [Migration] Backup warning: {backup_err}")
            
    except Exception as e:
        print(f"❌ [Migration] Failed: {e}")
        conn.rollback()
    finally:
        conn.close()

def load_state() -> YuHunState:
    init_db() # Ensure DB exists
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM system_state WHERE id = 1")
    row = cursor.fetchone()
    
    if row:
        fs_data = json.loads(row["fs"])
        fs = FSVector(**fs_data)
        state = YuHunState(
            active_island=row["active_island"],
            fs=fs,
            delta_s_recent=json.loads(row["delta_s_recent"]),
            preferred_mode=row["preferred_mode"],
            available_models=json.loads(row["available_models"]),
            tool_capabilities=json.loads(row["tool_capabilities"]),
        )
        conn.close()
        return state
    else:
        conn.close()
        # Initialize new state
        island_id = str(uuid.uuid4())[:8]
        island = TimeIsland(
            island_id=island_id,
            created_at=datetime.now(timezone.utc).isoformat(),
            title="Default Island",
        )
        save_island(island)
        
        state = YuHunState(active_island=island_id)
        save_state(state)
        return state

def save_state(state: YuHunState) -> None:
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR REPLACE INTO system_state (id, active_island, fs, delta_s_recent, preferred_mode, available_models, tool_capabilities)
    VALUES (1, ?, ?, ?, ?, ?, ?)
    ''', (
        state.active_island,
        json.dumps(state.fs.__dict__),
        json.dumps(state.delta_s_recent),
        state.preferred_mode,
        json.dumps(state.available_models),
        json.dumps(state.tool_capabilities)
    ))
    conn.commit()
    conn.close()

def load_island(island_id: str) -> Optional[TimeIsland]:
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM islands WHERE island_id = ?", (island_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
        
    fs_data = json.loads(row["fs_vector"])
    fs = FSVector(**fs_data)
    
    return TimeIsland(
        island_id=row["island_id"],
        created_at=row["created_at"],
        title=row["title"],
        kairos_tags=json.loads(row["kairos_tags"]),
        fs_vector=fs,
        semantic_tension=row["semantic_tension"],
        current_mode=row["current_mode"],
        history_digest=row["history_digest"],
        last_step_id=row["last_step_id"],
    )

def save_island(island: TimeIsland) -> None:
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR REPLACE INTO islands (island_id, created_at, title, kairos_tags, fs_vector, semantic_tension, current_mode, history_digest, last_step_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        island.island_id,
        island.created_at,
        island.title,
        json.dumps(island.kairos_tags),
        json.dumps(island.fs_vector.__dict__),
        island.semantic_tension,
        island.current_mode,
        island.history_digest,
        island.last_step_id
    ))
    conn.commit()
    conn.close()

def append_chronicle(entry: ChronicleEntry) -> None:
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO chronicle (step_id, island_id, timestamp, user_input, model_reply_summary, mode_used, fs_before, fs_after, tools_used, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        entry.step_id,
        entry.island_id,
        entry.timestamp,
        entry.user_input,
        entry.model_reply_summary,
        entry.mode_used,
        json.dumps(entry.fs_before.__dict__),
        json.dumps(entry.fs_after.__dict__),
        json.dumps(entry.tools_used),
        entry.notes
    ))
    conn.commit()
    conn.close()
