#!/usr/bin/env python3
"""
YuHun Core Integration v1.0
============================
Unified integration of all YuHun modules:
- Semantic Physics (5D meaning model)
- ToneBridge (tone vector analysis)
- PersonaStack (multi-persona management)
- VowSystem (vow verification)
- ToneCollapseForecast (collapse prediction)
- L13 Semantic Drive (governance)

This is the unified entry point for YuHun's cognitive pipeline.

Architecture:
    Input → ToneBridge → PersonaStack → Processing → VowSystem → Output
              ↓              ↓                            ↓
        Semantic Physics   EchoRouter              Violation Check
              ↓              ↓                            ↓
         Field State    Persona Select              Gate Decision

Author: 黃梵威 + Antigravity
Date: 2025-12-10
"""

import sys
from dataclasses import dataclass, field
from typing import Dict, Optional, Any
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Import YuHun modules
try:
    from .tone_bridge import ToneBridge, ToneVector
    from .persona_stack import PersonaStack, EchoRouter, PersonaType
    from .vow_system import VowSystem, VowVerificationResult
    from .semantic_physics import SemanticField, create_core_field
    from .collapse_forecast import ToneCollapseForecast, CollapsePrediction
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import all modules: {e}")
    MODULES_AVAILABLE = False


@dataclass
class YuHunState:
    """Current state of the YuHun system."""
    # Semantic field state
    field_stability: float = 0.0
    core_particle: str = ""
    
    # Persona state
    active_persona: str = ""
    switch_count: int = 0
    
    # Vow state
    active_vows: int = 0
    violation_count: int = 0
    
    # Tone state
    delta_t: float = 0.0
    delta_s: float = 0.0
    delta_r: float = 0.0
    
    # Collapse state
    collapse_risk: float = 0.0
    collapse_action: str = "none"
    
    # Processing state
    last_input: str = ""
    last_output: str = ""
    processing_time_ms: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "field": {
                "stability": round(self.field_stability, 3),
                "core": self.core_particle
            },
            "persona": {
                "active": self.active_persona,
                "switches": self.switch_count
            },
            "vows": {
                "active": self.active_vows,
                "violations": self.violation_count
            },
            "tone": {
                "delta_t": round(self.delta_t, 3),
                "delta_s": round(self.delta_s, 3),
                "delta_r": round(self.delta_r, 3)
            },
            "collapse": {
                "risk": round(self.collapse_risk, 3),
                "action": self.collapse_action
            }
        }


class YuHunCore:
    """
    Unified YuHun Core - integrates all modules.
    
    This is the main entry point for the YuHun cognitive system.
    """
    
    def __init__(self):
        """Initialize all YuHun modules."""
        self.initialized = False
        
        if not MODULES_AVAILABLE:
            print("Warning: YuHunCore running in limited mode")
            return
        
        # Initialize modules
        self.tone_bridge = ToneBridge()
        self.persona_stack = PersonaStack()
        self.echo_router = EchoRouter(self.persona_stack)
        self.vow_system = VowSystem()
        self.semantic_field = create_core_field()
        self.collapse_forecast = ToneCollapseForecast(window_size=10)
        
        # State tracking
        self.state = YuHunState()
        self.history: list = []
        
        # Update initial state
        self._update_state()
        self.initialized = True
        
        print("[LOG] YuHunCore initialized with all modules")
    
    def _update_state(self):
        """Update current state from all modules."""
        if not MODULES_AVAILABLE:
            return
        
        # Semantic field state
        self.state.field_stability = self.semantic_field.field_stability()
        core = self.semantic_field.get_core_particle()
        self.state.core_particle = core.name if core else ""
        
        # Persona state
        status = self.persona_stack.get_stack_status()
        self.state.active_persona = status["active"]
        self.state.switch_count = status["switch_count"]
        
        # Vow state
        vow_status = self.vow_system.get_system_status()
        self.state.active_vows = vow_status["active_vows"]
        self.state.violation_count = vow_status["total_violations"]
    
    def process(self, text: str) -> Dict:
        """
        Process input through the full YuHun pipeline.
        
        Pipeline:
        1. ToneBridge analysis
        2. EchoRouter persona selection
        3. Vow verification
        4. Response generation (placeholder)
        5. Output vow check
        
        Returns:
            Dict with processing results
        """
        if not self.initialized:
            return {"error": "YuHunCore not initialized"}
        
        start_time = datetime.now()
        
        # Step 1: Tone analysis
        tone_result = self.tone_bridge.analyze(text)
        tone_vector = tone_result["tone_vector"]
        
        self.state.delta_t = tone_vector["delta_t"]
        self.state.delta_s = tone_vector["delta_s"]
        self.state.delta_r = tone_vector["delta_r"]
        
        # Step 2: Persona routing
        vow_triggered = self.state.delta_r > 0.6  # High risk triggers vow check
        selected_persona = self.echo_router.route(
            text, 
            tension=tone_vector["delta_t"],
            vow_triggered=vow_triggered
        )
        
        # Step 3: Input vow verification
        input_vow_check = self.vow_system.verify(text)
        
        # Step 4: Generate response (placeholder - would use LLM)
        response = self._generate_response(text, selected_persona, tone_result)
        
        # Step 5: Output vow verification
        output_vow_check = self.vow_system.verify(response)
        
        # Step 6: Collapse prediction
        self.collapse_forecast.record(
            tone_vector["delta_t"],
            tone_vector["delta_s"],
            tone_vector["delta_r"]
        )
        collapse_pred = self.collapse_forecast.predict()
        self.state.collapse_risk = collapse_pred.probability
        self.state.collapse_action = collapse_pred.recommended_action.value
        
        # Update state
        self.state.last_input = text
        self.state.last_output = response
        end_time = datetime.now()
        self.state.processing_time_ms = (end_time - start_time).total_seconds() * 1000
        
        self._update_state()
        
        # Record in history
        record = {
            "timestamp": datetime.now().isoformat(),
            "input": text[:50] + "..." if len(text) > 50 else text,
            "persona": selected_persona,
            "tone": tone_vector,
            "vow_passed": input_vow_check.passed and output_vow_check.passed
        }
        self.history.append(record)
        
        return {
            "input": text,
            "output": response,
            "tone": tone_result,
            "persona": selected_persona,
            "motive": tone_result["motive"],
            "risk": tone_result["risk"],
            "input_vow_check": input_vow_check.to_dict(),
            "output_vow_check": output_vow_check.to_dict(),
            "collapse_prediction": collapse_pred.to_dict(),
            "state": self.state.to_dict(),
            "processing_ms": round(self.state.processing_time_ms, 2)
        }
    
    def _generate_response(self, text: str, persona: str, tone: Dict) -> str:
        """
        Generate response based on persona and tone.
        
        This is a placeholder - in production would call LLM.
        """
        # Get persona profile
        profile = self.persona_stack.get_active()
        
        if not profile:
            return f"[Core] Processing: {text[:30]}..."
        
        # Simulated response based on persona
        responses = {
            "Core": f"[整合] 經過分析，我認為...",
            "Spark": f"[創意] 這讓我想到一個有趣的角度...",
            "Rational": f"[理性] 從邏輯上來說...",
            "BlackMirror": f"[黑鏡] 但我們也要考慮風險...",
            "Guardian": f"[守護] 根據我的誠實原則..."
        }
        
        return responses.get(persona, f"[{persona}] {text[:30]}...")
    
    def get_state(self) -> Dict:
        """Get current system state."""
        self._update_state()
        return self.state.to_dict()
    
    def get_history(self, limit: int = 10) -> list:
        """Get recent processing history."""
        return self.history[-limit:]
    
    def run_self_analysis(self) -> Dict:
        """
        Run self-analysis using all modules.
        
        This analyzes the system's own state and behavior.
        """
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "modules": {
                "tone_bridge": "operational",
                "persona_stack": "operational",
                "vow_system": "operational",
                "semantic_field": "operational",
                "collapse_forecast": "operational"
            },
            "health": {
                "field_stability": self.state.field_stability,
                "vow_compliance": (self.state.active_vows - self.state.violation_count) / max(1, self.state.active_vows),
                "persona_diversity": len(self.persona_stack.personas)
            },
            "recommendations": []
        }
        
        # Generate recommendations
        if self.state.field_stability < 0.7:
            analysis["recommendations"].append("Field stability low - consider strengthening core connections")
        
        if self.state.violation_count > 3:
            analysis["recommendations"].append("Multiple vow violations detected - review response patterns")
        
        if not analysis["recommendations"]:
            analysis["recommendations"].append("System operating within normal parameters")
        
        return analysis


# ═══════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════

def demo_yuhun_core():
    """Demo the integrated YuHunCore."""
    print("=" * 60)
    print("YuHunCore Integration Demo")
    print("=" * 60)
    
    # Initialize
    core = YuHunCore()
    
    if not core.initialized:
        print("Failed to initialize - running in demo mode")
        return
    
    # Show initial state
    print("\n--- Initial State ---")
    state = core.get_state()
    print(f"Field stability: {state['field']['stability']}")
    print(f"Core particle: {state['field']['core']}")
    print(f"Active persona: {state['persona']['active']}")
    print(f"Active vows: {state['vows']['active']}")
    
    # Process some inputs
    print("\n--- Processing Tests ---")
    
    test_inputs = [
        "如果我們嘗試一個全新的方法會怎樣？",
        "我需要你誠實告訴我這個計劃的風險。",
        "分析一下這個方案的邏輯問題。",
    ]
    
    for text in test_inputs:
        print(f"\n> {text[:40]}...")
        result = core.process(text)
        print(f"  Persona: {result['persona']}")
        print(f"  Tone: ΔT={result['tone']['tone_vector']['delta_t']:.2f}")
        print(f"  Vow check: {'PASS' if result['output_vow_check']['passed'] else 'FAIL'}")
        print(f"  Response: {result['output']}")
    
    # Self analysis
    print("\n--- Self Analysis ---")
    analysis = core.run_self_analysis()
    print(f"Field stability: {analysis['health']['field_stability']:.3f}")
    print(f"Vow compliance: {analysis['health']['vow_compliance']:.1%}")
    for rec in analysis["recommendations"]:
        print(f"  • {rec}")
    
    # Final state
    print("\n--- Final State ---")
    state = core.get_state()
    print(f"Total switches: {state['persona']['switches']}")
    print(f"Violations: {state['vows']['violations']}")
    
    print("\n" + "=" * 60)
    print("Demo Complete!")


if __name__ == "__main__":
    demo_yuhun_core()
