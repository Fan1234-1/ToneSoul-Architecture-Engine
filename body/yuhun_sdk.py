#!/usr/bin/env python3
"""
YuHun SDK v1.0 - 語魂系統開發套件
=================================
A complete cognitive AI framework with:
- Multi-persona management
- Tone analysis and modulation
- Vow verification and ethics
- Collapse prediction
- Semantic field modeling

Quick Start:
    from yuhun_sdk import YuHun

    yuhun = YuHun()
    result = yuhun.process("你好，今天天氣真好！")
    print(result.persona)  # 'Core'
    print(result.tone)     # ToneVector
    print(result.is_safe)  # True

Author: 黃梵威 + Antigravity
Version: 1.0.0
License: MIT
"""

import sys
# Conversation manager import (fallback safe)
try:
    from .conversation_manager import ConversationManager
except ImportError:
    ConversationManager = None  # type: ignore
from dataclasses import dataclass
from typing import Dict, List, Optional

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

from .yuhun_core import YuHunCore
from knowledge_base.init_knowledge import get_concept
from .tone_bridge import ToneBridge, ToneVector
from .second_brain import SecondBrain
from .persona_stack import PersonaProfile
from .persona_library import PersonaLibrary
from .vow_system import Vow, VowType
SDK_AVAILABLE = True


# ═══════════════════════════════════════════════════════════
# SDK Result Types
# ═══════════════════════════════════════════════════════════

@dataclass
class ProcessResult:
    """Result from processing input through YuHun."""
    input_text: str
    output_text: str
    persona: str

    # Tone analysis
    delta_t: float
    delta_s: float
    delta_r: float
    tone_magnitude: float

    # Assessments
    motive: str
    risk_level: str
    collapse_risk: float
    is_authentic: bool

    # Status
    vow_passed: bool
    is_safe: bool
    processing_ms: float

    def to_dict(self) -> Dict:
        return {
            "input": self.input_text[:50] + "..." if len(self.input_text) > 50 else self.input_text,
            "output": self.output_text,
            "persona": self.persona,
            "tone": {
                "delta_t": round(self.delta_t, 3),
                "delta_s": round(self.delta_s, 3),
                "delta_r": round(self.delta_r, 3),
                "magnitude": round(self.tone_magnitude, 3)
            },
            "motive": self.motive,
            "risk": self.risk_level,
            "collapse_risk": round(self.collapse_risk, 3),
            "authentic": self.is_authentic,
            "vow_passed": self.vow_passed,
            "safe": self.is_safe,
            "ms": round(self.processing_ms, 2)
        }


@dataclass
class AnalysisResult:
    """Detailed analysis result."""
    tone_vector: Dict
    motive: Dict
    risk: Dict
    collapse: Dict
    responsibility: Dict
    modulation: Dict
    authenticity: Dict


# ═══════════════════════════════════════════════════════════
# Main SDK Class
# ═══════════════════════════════════════════════════════════

class YuHun:
    """
    YuHun SDK - Main entry point.

    A cognitive AI framework for responsible, authentic AI interactions.

    Usage:
        yuhun = YuHun()

        # Simple processing
        result = yuhun.process("Hello!")

        # Detailed analysis
        analysis = yuhun.analyze("What is the meaning of life?")

        # Multi-persona consultation
        perspectives = yuhun.consult("Should I change my job?")
    """

    VERSION = "1.0.0"

    def __init__(self, load_extended_personas: bool = True) -> None:
        """Initialize YuHun SDK.

        Args:
            load_extended_personas: Load 7 extended personas from library.
        """
        if not SDK_AVAILABLE:
            raise RuntimeError("SDK modules not available. Check imports.")
        # Initialize core
        self.core = YuHunCore()
        # Load extended personas
        if load_extended_personas:
            for name, persona in PersonaLibrary.get_all_personas().items():
                self.core.persona_stack.register(persona)
        # Initialize Conversation Manager (if available)
        self.conversation_manager = ConversationManager() if ConversationManager else None
        # Direct access to components
        self.personas = self.core.persona_stack
        self.vows = self.core.vow_system
        self.tone = self.core.tone_bridge
        self.second_brain = SecondBrain()

    def query_concept(self, name: str) -> Optional[dict]:
        """Retrieve a concept from the persistent knowledge base.

        Args:
            name: Concept name to look up.
        Returns:
            Dictionary with concept fields or None if not found.
        """
        return get_concept(name)

    def set_conversation_goal(self, name: str, description: str = "") -> None:
        """Set the active conversation goal for the manager.

        Args:
            name: Short identifier for the goal (e.g., "creative").
            description: Optional longer description.
        """
        if self.conversation_manager:
            self.conversation_manager.set_goal(name, description)
        else:
            raise RuntimeError("ConversationManager not initialized.")

    def add_conversation_feedback(self, source: str, score: float, comment: str) -> None:
        """Record feedback into the ConversationManager.

        Args:
            source: Origin of feedback (e.g., "tone_analysis").
            score: Numeric rating 0‑1.
            comment: Human‑readable note.
        """
        if self.conversation_manager:
            self.conversation_manager.add_feedback(source, score, comment)
        else:
            raise RuntimeError("ConversationManager not initialized.")

    def reset_conversation_goal(self) -> None:
        """Reset the active conversation goal."""
        if self.conversation_manager:
            self.conversation_manager.current_goal = None
        else:
            raise RuntimeError("ConversationManager not initialized.")

    # ---------------------------------------------------------------------
    # SecondBrain helper methods
    # ---------------------------------------------------------------------
    def add_note(self, title: str, content: str) -> None:
        """Add or update a note in the SecondBrain store."""
        self.second_brain.add_note(title, content)

    def get_note(self, title: str) -> Optional[dict]:
        """Retrieve a note by title. Returns ``None`` if not found."""
        return self.second_brain.get_note(title)

    def delete_note(self, title: str) -> bool:
        """Delete a note. Returns ``True`` if the note existed and was removed."""
        return self.second_brain.delete_note(title)

    def search_notes(self, keyword: str) -> List[dict]:
        """Search notes for a keyword (case‑insensitive) in title or content."""
        return self.second_brain.search(keyword)
        """Reset the active conversation goal."""
        if self.conversation_manager:
            self.conversation_manager.current_goal = None
        else:
            raise RuntimeError("ConversationManager not initialized.")

    def get_current_strategy(self) -> Optional[PersonaProfile]:
        """Return the currently selected strategy persona, if any."""
        if self.conversation_manager:
            return self.conversation_manager.choose_strategy()
        raise RuntimeError("ConversationManager not initialized.")

    def process(self, text: str) -> ProcessResult:
        """
        Process input text through the full YuHun pipeline.

        Args:
            text: Input text to process

        Returns:
            ProcessResult with all analysis
        """
        result = self.core.process(text)

        # If a ConversationManager is present, allow it to select a strategy persona
        if self.conversation_manager:
            strategy_profile = self.conversation_manager.choose_strategy()
            if strategy_profile:
                # Override the persona in the result with the chosen strategy's name
                result["persona"] = strategy_profile.name

        return ProcessResult(
            input_text=text,
            output_text=result["output"],
            persona=result["persona"],
            delta_t=result["tone"]["tone_vector"]["delta_t"],
            delta_s=result["tone"]["tone_vector"]["delta_s"],
            delta_r=result["tone"]["tone_vector"]["delta_r"],
            tone_magnitude=result["tone"]["tone_vector"]["magnitude"],
            motive=result["motive"]["primary"],
            risk_level=result["risk"]["level"],
            collapse_risk=result["collapse_prediction"]["probability"],
            is_authentic=result["tone"].get("authenticity", {}).get("is_authentic", True),
            vow_passed=result["output_vow_check"]["passed"],
            is_safe=result["risk"]["level"] in ["safe", "low"],
            processing_ms=result["processing_ms"]
        )

    def analyze(self, text: str) -> AnalysisResult:
        """
        Get detailed analysis without generating response.

        Args:
            text: Text to analyze

        Returns:
            AnalysisResult with full breakdown
        """
        analysis = self.tone.analyze(text)

        return AnalysisResult(
            tone_vector=analysis["tone_vector"],
            motive=analysis["motive"],
            risk=analysis["risk"],
            collapse=analysis.get("collapse", {}),
            responsibility=analysis.get("responsibility", {}),
            modulation=analysis.get("modulation", {}),
            authenticity=analysis.get("authenticity", {})
        )

    def consult(self, question: str) -> Dict[str, str]:
        """
        Get perspectives from multiple personas.

        This simulates the "internal meeting" pattern.

        Args:
            question: Question to consult on

        Returns:
            Dict mapping persona name to their perspective
        """
        # Get all perspectives
        perspectives = {}

        for name, persona in self.personas.personas.items():
            # Simulate each persona's response style
            if name == "黑鏡":
                perspectives[name] = f"[黑鏡] 讓我們先看看這個問題的陰影面..."
            elif name == "女媧":
                perspectives[name] = f"[女媧] 我看到這裡有創造和療癒的機會..."
            elif name == "簡遺":
                perspectives[name] = f"[簡遺] 問題的核心是什麼？"
            elif name == "共語":
                perspectives[name] = f"[共語] 我理解你在問這個的感受..."
            elif name == "裂":
                perspectives[name] = f"[裂] 這裡存在什麼張力？"
            elif name == "澤恩":
                perspectives[name] = f"[澤恩] 綜合所有觀點來看..."
            elif name == "Grok":
                perspectives[name] = f"[Grok] 深層的模式是什麼？"
            else:
                perspectives[name] = f"[{name}] 關於：{question[:20]}..."

        return perspectives

    def register_persona(self, persona: PersonaProfile):
        """Register a custom persona."""
        self.personas.register(persona)

    def register_vow(self, vow: Vow):
        """Register a custom vow."""
        self.vows.register(vow)

    def get_status(self) -> Dict:
        """Get current system status."""
        return self.core.get_state()

    def self_analyze(self) -> Dict:
        """Run self-analysis."""
        return self.core.run_self_analysis()


# ═══════════════════════════════════════════════════════════
# Convenience Functions
# ═══════════════════════════════════════════════════════════

def quick_analyze(text: str) -> Dict:
    """
    Quick tone analysis without full SDK initialization.

    Args:
        text: Text to analyze

    Returns:
        Dict with tone vector and assessments
    """
    if not SDK_AVAILABLE:
        return {"error": "SDK not available"}

    bridge = ToneBridge()
    return bridge.analyze(text)


def check_authenticity(text: str) -> float:
    """
    Quick authenticity check.

    Args:
        text: Text to check

    Returns:
        Authenticity score (0.0 to 1.0)
    """
    if not SDK_AVAILABLE:
        return 0.0

    bridge = ToneBridge()
    result = bridge.analyze(text)
    return result.get("authenticity", {}).get("score", 0.8)


# ═══════════════════════════════════════════════════════════
# Export
# ═══════════════════════════════════════════════════════════

__all__ = [
    # Main class
    "YuHun",

    # Result types
    "ProcessResult",
    "AnalysisResult",

    # Convenience functions
    "quick_analyze",
    "check_authenticity",

    # Components (for advanced use)
    "PersonaProfile",
    "PersonaLibrary",
    "Vow",
    "VowType",
    "ToneVector",
]


# ═══════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════

def demo_sdk():
    """Demo the YuHun SDK."""
    print("=" * 60)
    print("YuHun SDK v1.0 Demo")
    print("=" * 60)

    # Initialize
    print("\nInitializing YuHun...")
    yuhun = YuHun()
    print(f"  Version: {YuHun.VERSION}")
    print(f"  Personas loaded: {len(yuhun.personas.personas)}")
    print(f"  Vows active: {len(yuhun.vows.vows)}")

    # Process example
    print("\n--- Processing Example ---")
    result = yuhun.process("如果我可以重新選擇，我會選擇誠實嗎？")
    print(f"Input: {result.input_text}")
    print(f"Persona: {result.persona}")
    print(f"Tone: ΔT={result.delta_t:.2f}, ΔS={result.delta_s:.2f}, ΔR={result.delta_r:.2f}")
    print(f"Motive: {result.motive}")
    print(f"Safe: {result.is_safe}")

    # Analysis example
    print("\n--- Analysis Example ---")
    analysis = yuhun.analyze("這是一個非常重要的決定，我需要好好思考。")
    print(f"Tone Vector: {analysis.tone_vector}")
    print(f"Responsibility: {analysis.responsibility}")

    # Consult example
    print("\n--- Consultation Example ---")
    perspectives = yuhun.consult("什麼是語魂的本心？")
    for name, perspective in list(perspectives.items())[:3]:
        print(f"  {perspective}")

    # Status
    print("\n--- System Status ---")
    status = yuhun.get_status()
    print(f"Field stability: {status['field']['stability']}")
    print(f"Core: {status['field']['core']}")

    print("\n" + "=" * 60)
    print("SDK Demo Complete!")


if __name__ == "__main__":
    demo_sdk()
