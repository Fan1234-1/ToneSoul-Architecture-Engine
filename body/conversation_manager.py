#!/usr/bin/env python3
"""
Conversation Manager – handles goals, feedback, and strategy selection.
"""

import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

# Import PersonaLibrary for persona lookup (fallback if unavailable)
try:
    from .persona_library import PersonaLibrary, PersonaProfile
except ImportError:
    PersonaLibrary = None
    PersonaProfile = None


@dataclass
class Goal:
    """Simple container for a conversation goal."""
    name: str
    description: str = ""


class ConversationManager:
    """Manage conversation-level goals, collect feedback, and choose a strategy.

    The manager stores a Goal object, a feedback log, and can map a goal to a PersonaProfile.
    """

    def __init__(self):
        self.current_goal: Optional[Goal] = None
        self.feedback_log: List[Dict] = []  # each entry: {source, score, comment, timestamp}

    # ---------------------------------------------------------------------
    # Goal handling
    # ---------------------------------------------------------------------
    def set_goal(self, name: str, description: str = "") -> None:
        """Set the active conversation goal.

        Args:
            name: Short identifier for the goal (e.g. "creative", "high_security").
            description: Optional longer description.
        """
        self.current_goal = Goal(name=name.lower(), description=description)

    # ---------------------------------------------------------------------
    # Feedback handling
    # ---------------------------------------------------------------------
    def add_feedback(self, source: str, score: float, comment: str) -> None:
        """Record a piece of feedback.

        Args:
            source: Where the feedback comes from (e.g. "tone_analysis").
            score: Numeric rating, typically 0‑1.
            comment: Human‑readable note.
        """
        entry = {
            "source": source,
            "score": score,
            "comment": comment,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        self.feedback_log.append(entry)

    # ---------------------------------------------------------------------
    # Strategy selection
    # ---------------------------------------------------------------------
    def choose_strategy(self) -> Optional[PersonaProfile]:
        """Select a PersonaProfile based on the current goal and feedback.

        Simple logic:
        * "creative" or "spark" -> Spark persona
        * "security" or "high" -> Zen persona
        * fallback -> BlackMirror persona
        """
        if not self.current_goal:
            return None
        goal_name = self.current_goal.name
        # Prefer Spark for creative goals
        if "creative" in goal_name or "spark" in goal_name or "創意" in goal_name:
            if PersonaLibrary:
                return PersonaLibrary.get_spark()
        # High‑security goal
        if "security" in goal_name or "high" in goal_name or "安全" in goal_name:
            if PersonaLibrary:
                return PersonaLibrary.get_zen()
        # Default fallback
        if PersonaLibrary:
            return PersonaLibrary.get_black_mirror()
        return None
