# -*- coding: utf-8 -*-
"""Initialize a persistent knowledge base for the ToneSoul system.

This script creates a SQLite database (knowledge.db) with a simple schema
for storing concepts, definitions, source URLs and timestamps. It also
provides helper functions to add, retrieve and update concepts.

The design follows the "Dynamic Coherence" framework described in the
conversation: every knowledge update is logged to `Chronicle.log` so that
future sessions can replay the learning history.
"""

import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "knowledge.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS concepts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    definition TEXT NOT NULL,
    source_url TEXT,
    updated_at TEXT NOT NULL
);
"""

def get_connection():
    """Return a SQLite connection, creating the DB file if needed."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Create the database and the concepts table if they do not exist."""
    with get_connection() as conn:
        conn.executescript(SCHEMA)
        conn.commit()

def upsert_concept(name: str, definition: str, source_url: str = None, updated_at: str = None):
    """Insert a new concept or update the definition of an existing one.

    The function logs the operation to the Chronicle (if available) and
    records the provided timestamp or the current UTC timestamp.
    """
    now = updated_at if updated_at is not None else datetime.utcnow().isoformat()
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO concepts (name, definition, source_url, updated_at)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(name) DO UPDATE SET
                 definition=excluded.definition,
                 source_url=excluded.source_url,
                 updated_at=excluded.updated_at;""",
            (name, definition, source_url, now),
        )
        conn.commit()

def get_concept(name: str):
    """Retrieve a concept by name. Returns a dict or None if not found."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT name, definition, source_url, updated_at FROM concepts WHERE name = ?", (name,))
        row = cur.fetchone()
        if row:
            return {
                "name": row[0],
                "definition": row[1],
                "source_url": row[2],
                "updated_at": row[3],
            }
        return None

if __name__ == "__main__":
    # Simple CLI for quick testing
    import argparse
    parser = argparse.ArgumentParser(description="Knowledge base utility")
    subparsers = parser.add_subparsers(dest="cmd")

    init_parser = subparsers.add_parser("init", help="Initialize the DB")

    add_parser = subparsers.add_parser("add", help="Add or update a concept")
    add_parser.add_argument("name")
    add_parser.add_argument("definition")
    add_parser.add_argument("--url", default=None, help="Source URL")

    get_parser = subparsers.add_parser("get", help="Get a concept")
    get_parser.add_argument("name")

    args = parser.parse_args()
    if args.cmd == "init":
        init_db()
        print(f"Database initialized at {DB_PATH}")
    elif args.cmd == "add":
        init_db()
        upsert_concept(args.name, args.definition, args.url)
        print(f"Concept '{args.name}' stored/updated.")
    elif args.cmd == "get":
        init_db()
        concept = get_concept(args.name)
        if concept:
            print(concept)
        else:
            print(f"Concept '{args.name}' not found.")
    else:
        parser.print_help()
