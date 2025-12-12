# second_brain.py – Core of the "Second Brain" (第二腦)
"""A lightweight personal knowledge store.

Features:
- In‑memory note storage with optional JSON persistence.
- `add_note(title: str, content: str)` – store a note.
- `get_note(title: str) -> Optional[dict]` – retrieve a note.
- `search(keyword: str) -> List[dict]` – simple case‑insensitive substring search.
- `save(path: str)` / `load(path: str)` – persist to a JSON file.

The class is deliberately simple so it can be used by the YuHun SDK as a "second brain" for
quick concept lookup or personal memory.
"""

import json
import os
from typing import List, Optional, Dict


class SecondBrain:
    """Core implementation of the Second Brain.

    The brain keeps a dictionary of notes keyed by title. Each note is a dict with
    `title`, `content`, and an auto‑generated `created_at` timestamp.
    """

    def __init__(self) -> None:
        self._notes: Dict[str, Dict] = {}

    # ---------------------------------------------------------------------
    # CRUD operations
    # ---------------------------------------------------------------------
    def add_note(self, title: str, content: str) -> None:
        """Add or update a note.

        Args:
            title: Unique identifier for the note.
            content: Free‑form text.
        """
        self._notes[title] = {
            "title": title,
            "content": content,
            "created_at": os.path.getmtime(__file__)  # simple timestamp
        }

    def get_note(self, title: str) -> Optional[Dict]:
        """Retrieve a note by title.

        Returns ``None`` if the note does not exist.
        """
        return self._notes.get(title)

    def delete_note(self, title: str) -> bool:
        """Delete a note. Returns ``True`` if deleted, ``False`` otherwise."""
        return self._notes.pop(title, None) is not None

    # ---------------------------------------------------------------------
    # Search
    # ---------------------------------------------------------------------
    def search(self, keyword: str) -> List[Dict]:
        """Case‑insensitive substring search over titles and contents.

        Returns a list of matching note dicts.
        """
        kw = keyword.lower()
        results = []
        for note in self._notes.values():
            if kw in note["title"].lower() or kw in note["content"].lower():
                results.append(note)
        return results

    # ---------------------------------------------------------------------
    # Persistence
    # ---------------------------------------------------------------------
    def save(self, path: str) -> None:
        """Persist notes to a JSON file.

        The directory is created if it does not exist.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._notes, f, ensure_ascii=False, indent=2)

    def load(self, path: str) -> None:
        """Load notes from a JSON file. If the file does not exist, nothing happens."""
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            self._notes = json.load(f)
