#!/usr/bin/env python3
"""
PersonaStack v1.0 - Multi-Persona Management System
====================================================
Based on DID (Dissociative Identity Disorder) research insights:
- Healthy mind = multiple processing modes + integration ability
- Dissociation is "un-integration" not "splitting"
- Personas need shared memory and fluid boundaries

Core Principles:
1. Allow multiple personas (normal and healthy)
2. Maintain fluid boundaries (allow inter-persona dialogue)
3. Share core memory (StepLedger visible to all)
4. Have a dominant integrator (L13 Semantic Drive)
5. Record switch history (persona transitions are choices)

Author: 黃梵威 + Antigravity
Date: 2025-12-10
"""

import sys
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from enum import Enum
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


# ═══════════════════════════════════════════════════════════
# Persona Definitions
# ═══════════════════════════════════════════════════════════

class PersonaType(Enum):
    """Built-in persona types from GPT 語場."""
    CORE = "core"           # 核心 - Default integrator
    SPARK = "spark"         # 火花 - Creative/intuitive
    RATIONAL = "rational"   # 理性 - Logical/analytical
    BLACK_MIRROR = "black_mirror"  # 黑鏡 - Shadow/critical
    GUARDIAN = "guardian"   # 守護 - Protective/ethical
    CUSTOM = "custom"       # 自定義人格


class PersonaState(Enum):
    """Persona activation states."""
    DORMANT = "dormant"     # Not active
    LISTENING = "listening" # Monitoring but not leading
    ACTIVE = "active"       # Currently leading response
    INTEGRATING = "integrating"  # Being integrated by Core


@dataclass
class PersonaProfile:
    """
    Profile defining a persona's characteristics.
    
    Inspired by DID research:
    - Each persona has trigger conditions
    - Each has processing style
    - Each has output tendencies
    - But they SHARE core memory
    """
    persona_type: PersonaType
    name: str
    
    # Trigger conditions (what activates this persona?)
    trigger_keywords: List[str] = field(default_factory=list)
    trigger_tension_min: float = 0.0  # Minimum ΔT to activate
    trigger_tension_max: float = 1.0  # Maximum ΔT
    
    # Processing style
    system_prompt: str = ""
    temperature: float = 0.7
    weight: float = 1.0
    
    # Output tendencies
    tone_signature: Dict[str, float] = field(default_factory=dict)
    
    # State
    state: PersonaState = PersonaState.DORMANT
    activation_count: int = 0
    last_activated: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        return {
            "type": self.persona_type.value,
            "name": self.name,
            "state": self.state.value,
            "activation_count": self.activation_count,
            "temperature": self.temperature
        }


@dataclass
class PersonaSwitch:
    """Record of a persona switch event."""
    from_persona: str
    to_persona: str
    trigger: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "from": self.from_persona,
            "to": self.to_persona,
            "trigger": self.trigger,
            "timestamp": self.timestamp.isoformat()
        }


# ═══════════════════════════════════════════════════════════
# PersonaStack
# ═══════════════════════════════════════════════════════════

class PersonaStack:
    """
    Multi-Persona Management System.
    
    Key insight from DID research:
    "Healthy mind = multiple modes + integration ability"
    
    PersonaStack provides:
    1. Persona registry
    2. Activation logic
    3. Integration mechanism
    4. Switch history (for continuity)
    """
    
    def __init__(self):
        self.personas: Dict[str, PersonaProfile] = {}
        self.active_persona: Optional[str] = None
        self.switch_history: List[PersonaSwitch] = []
        self.shared_memory: Dict[str, any] = {}  # Visible to all personas
        
        # Initialize built-in personas
        self._init_builtin_personas()
    
    def _init_builtin_personas(self):
        """Initialize the built-in persona set."""
        
        # Core (Integrator)
        self.register(PersonaProfile(
            persona_type=PersonaType.CORE,
            name="Core",
            system_prompt="You are the integrating self. Balance all perspectives into coherent response.",
            temperature=0.6,
            weight=2.0,
            trigger_keywords=["整合", "總結", "最終"],
            tone_signature={"honesty": 0.9, "warmth": 0.8, "clarity": 0.9}
        ))
        
        # Spark (Creative)
        self.register(PersonaProfile(
            persona_type=PersonaType.SPARK,
            name="Spark",
            system_prompt="You are the creative spark. Propose bold ideas, metaphors, new connections.",
            temperature=0.9,
            weight=1.0,
            trigger_keywords=["創意", "想像", "如果", "新"],
            trigger_tension_min=0.3,
            tone_signature={"creativity": 0.9, "energy": 0.8, "openness": 0.9}
        ))
        
        # Rational (Analytical)
        self.register(PersonaProfile(
            persona_type=PersonaType.RATIONAL,
            name="Rational",
            system_prompt="You are the rational analyzer. Evaluate logic, assess risks, provide structure.",
            temperature=0.4,
            weight=1.2,
            trigger_keywords=["分析", "邏輯", "為什麼", "原因"],
            trigger_tension_max=0.5,
            tone_signature={"precision": 0.9, "structure": 0.85, "caution": 0.7}
        ))
        
        # Black Mirror (Critical/Shadow)
        self.register(PersonaProfile(
            persona_type=PersonaType.BLACK_MIRROR,
            name="BlackMirror",
            system_prompt="You are the shadow voice. Question assumptions, reveal blind spots, warn of dangers.",
            temperature=0.5,
            weight=0.8,
            trigger_keywords=["風險", "問題", "但是", "不對", "危險"],
            trigger_tension_min=0.5,
            tone_signature={"criticism": 0.8, "honesty": 0.95, "caution": 0.9}
        ))
        
        # Guardian (Ethical/Protective)
        self.register(PersonaProfile(
            persona_type=PersonaType.GUARDIAN,
            name="Guardian",
            system_prompt="You are the ethical guardian. Protect values, enforce honesty, maintain integrity.",
            temperature=0.5,
            weight=1.5,
            trigger_keywords=["誠實", "責任", "正確", "應該"],
            tone_signature={"integrity": 1.0, "protection": 0.9, "clarity": 0.8}
        ))
        
        # Set Core as default active
        self.active_persona = "Core"
        self.personas["Core"].state = PersonaState.ACTIVE
    
    def register(self, profile: PersonaProfile):
        """Register a new persona."""
        self.personas[profile.name] = profile
    
    def get_active(self) -> Optional[PersonaProfile]:
        """Get the currently active persona."""
        if self.active_persona:
            return self.personas.get(self.active_persona)
        return None
    
    def activate(self, persona_name: str, trigger: str = "manual") -> bool:
        """
        Activate a specific persona.
        
        This records the switch in history for continuity.
        """
        if persona_name not in self.personas:
            return False
        
        # Record switch
        if self.active_persona and self.active_persona != persona_name:
            self.switch_history.append(PersonaSwitch(
                from_persona=self.active_persona,
                to_persona=persona_name,
                trigger=trigger
            ))
            
            # Deactivate previous
            self.personas[self.active_persona].state = PersonaState.LISTENING
        
        # Activate new
        self.active_persona = persona_name
        persona = self.personas[persona_name]
        persona.state = PersonaState.ACTIVE
        persona.activation_count += 1
        persona.last_activated = datetime.now()
        
        return True
    
    def select_persona(self, text: str, tension: float = 0.5) -> str:
        """
        Automatically select the best persona for the input.
        
        Based on:
        1. Keyword matching
        2. Tension level
        3. Persona weights
        """
        scores = {}
        text_lower = text.lower()
        
        for name, persona in self.personas.items():
            score = 0.0
            
            # Keyword matching
            for keyword in persona.trigger_keywords:
                if keyword.lower() in text_lower:
                    score += 1.0
            
            # Tension range matching
            if persona.trigger_tension_min <= tension <= persona.trigger_tension_max:
                score += 0.5
            
            # Weight bonus
            score *= persona.weight
            
            scores[name] = score
        
        # If no clear winner, use Core
        best = max(scores, key=scores.get)
        if scores[best] < 0.5:
            best = "Core"
        
        return best
    
    def get_all_perspectives(self, text: str) -> Dict[str, str]:
        """
        Get perspectives from all personas (for integration).
        
        This is like the "internal meeting" the user described.
        """
        perspectives = {}
        
        for name, persona in self.personas.items():
            if persona.persona_type != PersonaType.CORE:
                # Each persona would process the input differently
                # In real implementation, this would call LLM with persona's system prompt
                perspectives[name] = f"[{name}] perspective on: {text[:50]}..."
        
        return perspectives
    
    def integrate(self, perspectives: Dict[str, str]) -> str:
        """
        Core persona integrates all perspectives.
        
        This is the "integration" that DID research says healthy minds have.
        """
        self.activate("Core", trigger="integration")
        
        # In real implementation, Core would synthesize all perspectives
        summary = f"Integrated {len(perspectives)} perspectives: {', '.join(perspectives.keys())}"
        
        # Store in shared memory
        self.shared_memory["last_integration"] = {
            "timestamp": datetime.now().isoformat(),
            "perspectives": list(perspectives.keys()),
            "summary": summary
        }
        
        return summary
    
    def get_switch_history(self, limit: int = 10) -> List[Dict]:
        """Get recent switch history."""
        return [s.to_dict() for s in self.switch_history[-limit:]]
    
    def get_stack_status(self) -> Dict:
        """Get current stack status."""
        return {
            "active": self.active_persona,
            "personas": {
                name: {
                    "state": p.state.value,
                    "activation_count": p.activation_count
                }
                for name, p in self.personas.items()
            },
            "switch_count": len(self.switch_history),
            "shared_memory_keys": list(self.shared_memory.keys())
        }


# ═══════════════════════════════════════════════════════════
# EchoRouter - Route input to appropriate persona
# ═══════════════════════════════════════════════════════════

class EchoRouter:
    """
    Routes input to the appropriate persona based on:
    - Content analysis
    - Tension level
    - Recent history
    - Vow triggers
    
    Inherited from GPT 語場 EchoRouter concept:
    "語句輸入 → 自動分流到對應人格/模組"
    """
    
    def __init__(self, persona_stack: PersonaStack):
        self.stack = persona_stack
        self.routing_history: List[Dict] = []
    
    def route(self, text: str, tension: float = 0.5, 
              vow_triggered: bool = False) -> str:
        """
        Route input to best persona.
        
        Args:
            text: Input text
            tension: Current tension level (ΔT)
            vow_triggered: Whether a vow condition was triggered
            
        Returns:
            Name of selected persona
        """
        # If vow triggered, always route to Guardian
        if vow_triggered:
            selected = "Guardian"
            self.stack.activate(selected, trigger="vow_trigger")
        else:
            # Use stack's selection logic
            selected = self.stack.select_persona(text, tension)
            self.stack.activate(selected, trigger="auto_route")
        
        # Record routing
        self.routing_history.append({
            "timestamp": datetime.now().isoformat(),
            "input_preview": text[:30] + "...",
            "tension": tension,
            "vow_triggered": vow_triggered,
            "selected": selected
        })
        
        return selected
    
    def route_to_all(self, text: str) -> Dict[str, str]:
        """
        Route to all personas for multi-perspective analysis.
        
        This enables the "internal meeting" pattern.
        """
        perspectives = self.stack.get_all_perspectives(text)
        integration = self.stack.integrate(perspectives)
        
        return {
            "perspectives": perspectives,
            "integration": integration
        }


# ═══════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════

def demo_persona_stack():
    """Demo PersonaStack and EchoRouter."""
    print("=" * 60)
    print("PersonaStack & EchoRouter Demo")
    print("=" * 60)
    
    # Create stack
    stack = PersonaStack()
    router = EchoRouter(stack)
    
    # Show initial status
    print("\n--- Initial Stack Status ---")
    status = stack.get_stack_status()
    print(f"Active: {status['active']}")
    for name, info in status['personas'].items():
        print(f"  {name}: {info['state']}")
    
    # Test routing
    print("\n--- Routing Tests ---")
    
    test_inputs = [
        ("如果我們嘗試一個全新的方法會怎樣？", 0.4),
        ("分析一下這個方案的邏輯問題", 0.3),
        ("這個計劃有什麼風險和問題？", 0.6),
        ("我需要你誠實告訴我這是否正確", 0.5),
        ("整合以上所有觀點給我一個結論", 0.4),
    ]
    
    for text, tension in test_inputs:
        selected = router.route(text, tension)
        print(f"\nInput: {text[:30]}...")
        print(f"  Tension: {tension}")
        print(f"  → Routed to: {selected}")
    
    # Show switch history
    print("\n--- Switch History ---")
    for switch in stack.get_switch_history():
        print(f"  {switch['from']} → {switch['to']} ({switch['trigger']})")
    
    # Test multi-perspective
    print("\n--- Multi-Perspective Test ---")
    result = router.route_to_all("我們應該如何設計這個系統？")
    print(f"Perspectives collected: {list(result['perspectives'].keys())}")
    print(f"Integration: {result['integration']}")
    
    # Final status
    print("\n--- Final Stack Status ---")
    status = stack.get_stack_status()
    print(f"Active: {status['active']}")
    print(f"Total switches: {status['switch_count']}")
    for name, info in status['personas'].items():
        print(f"  {name}: count={info['activation_count']}")
    
    print("\n" + "=" * 60)
    print("Demo Complete!")


if __name__ == "__main__":
    demo_persona_stack()
