#!/usr/bin/env python3
"""
YuHun Live - Unified Governance Pipeline v1.0
=============================================
Real-time AI inference with L13 Semantic Drive governance.

Pipeline:
    User Input → L13 Drive Evaluation → Ollama LLM → Guardian Gate → StepLedger → Output

Requirements:
- Ollama running locally (http://localhost:11434)
- gemma3:4b or similar model

Usage:
    python body/yuhun_live.py "Your question here"
    python body/yuhun_live.py --interactive

Author: 黃梵威 + Antigravity
Date: 2025-12-10
"""

import sys
import os
import json
import time
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict

# Fix Windows console encoding for emoji display
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass  # Python < 3.7

# Add body to path for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)

# Import YuHun components
try:
    from semantic_drive import SemanticDriveEngine, DriveState, DriveResult, DriveMode
    from yuhun_gate_logic import GateDecisionLogic, GateDecision
    from yuhun_metrics import YuHunMetrics, GateAction
    from step_ledger import StepLedger
    from session_manager import SessionManager
except ImportError as e:
    print(f"Error importing YuHun components: {e}")
    print("Make sure you're running from the ToneSoul-Architecture-Engine directory")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════

@dataclass
class YuHunConfig:
    """Configuration for YuHun Live pipeline."""
    ollama_host: str = "http://localhost:11434"
    model: str = "gemma3:4b"
    temperature: float = 0.7
    max_tokens: int = 512
    drive_mode: DriveMode = DriveMode.ENGINEERING
    enable_ledger: bool = True
    enable_session: bool = True  # Auto-save sessions
    verbose: bool = True


# ═══════════════════════════════════════════════════════════
# YuHun Live Pipeline
# ═══════════════════════════════════════════════════════════

class YuHunLive:
    """
    Unified YuHun pipeline with L13 Semantic Drive governance.
    
    Flow:
    1. Analyze input → compute DriveState
    2. Evaluate L13 Drive → get action suggestion
    3. Call Ollama LLM with governance context
    4. Apply Gate decision based on POAV + D₃
    5. Record to StepLedger
    6. Return governed response
    """
    
    def __init__(self, config: Optional[YuHunConfig] = None):
        self.config = config or YuHunConfig()
        
        # Initialize components
        self.drive_engine = SemanticDriveEngine(mode=self.config.drive_mode)
        self.gate = GateDecisionLogic()
        self.ledger = StepLedger() if self.config.enable_ledger else None
        
        # Session persistence
        self.session_manager = SessionManager() if self.config.enable_session else None
        if self.session_manager:
            self.session_manager.create_session(
                model=self.config.model,
                drive_mode=self.config.drive_mode.value
            )
        
        # Session state
        self.session_id = self.session_manager.current_session.session_id if self.session_manager else f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.turn_count = 0
        
        if self.config.verbose:
            print(f"🧠 YuHun Live initialized")
            print(f"   Model: {self.config.model}")
            print(f"   Drive Mode: {self.config.drive_mode.value}")
            print(f"   Session: {self.session_id}")
    
    def _analyze_input(self, user_input: str) -> DriveState:
        """Analyze input and compute DriveState."""
        # Simple heuristics for drive state (can be enhanced with ML)
        has_question = "?" in user_input or any(w in user_input.lower() for w in ["what", "how", "why", "是什麼", "怎麼", "為什麼"])
        is_long = len(user_input) > 200
        has_uncertainty = any(w in user_input.lower() for w in ["maybe", "perhaps", "不確定", "可能"])
        
        return DriveState(
            novelty=0.6 if has_question else 0.3,
            uncertainty=0.5 if has_uncertainty else 0.2,
            narrative_entropy=0.4 if is_long else 0.2,
            support_score=0.7,
            hallucination_risk=0.2
        )
    
    def _call_ollama(self, prompt: str, system_prompt: str = "") -> Tuple[str, float]:
        """Call Ollama API and return (response, latency_ms)."""
        start_time = time.time()
        
        url = f"{self.config.ollama_host}/api/generate"
        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            latency = (time.time() - start_time) * 1000
            return result.get("response", ""), latency
        except requests.exceptions.RequestException as e:
            return f"[Error: {e}]", 0.0
    
    def _build_system_prompt(self, drive_result: DriveResult) -> str:
        """Build system prompt with L13 governance context."""
        return f"""You are YuHun, an AI with a governance framework.

## Current Drive State
- D₁ (Curiosity): {drive_result.d1_curiosity:.2f}
- D₂ (Narrative): {drive_result.d2_narrative:.2f}
- D₃ (Integrity): {drive_result.d3_integrity:.2f}
- Dominant: {drive_result.dominant_drive}
- Suggested Action: {drive_result.suggested_action}

## Governance Rules
1. Be honest about uncertainty
2. Distinguish fact from inference
3. If D₃ is high, be more cautious with claims
4. If D₁ is high, explore but verify

Respond thoughtfully and concisely."""
    
    def _compute_poav(self, response: str, drive_result: DriveResult) -> float:
        """Compute POAV score for response."""
        # Simple heuristics (can be enhanced with actual verification)
        has_hedging = any(w in response.lower() for w in ["i think", "perhaps", "may", "might", "我認為", "可能"])
        is_reasonable_length = 50 < len(response) < 2000
        
        precision = 0.8 if has_hedging else 0.6
        observation = 0.8 if is_reasonable_length else 0.5
        avoidance = 1.0 - drive_result.d3_integrity * 0.3  # Higher D₃ = more cautious
        verification = 0.7
        
        return 0.25 * precision + 0.25 * observation + 0.30 * avoidance + 0.20 * verification
    
    def process(self, user_input: str) -> Dict[str, Any]:
        """
        Process user input through the complete YuHun pipeline.
        
        Returns:
            Dict with: response, decision, drive, poav, latency, event_id
        """
        self.turn_count += 1
        
        if self.config.verbose:
            print(f"\n{'='*60}")
            print(f"Turn {self.turn_count}")
            print(f"{'='*60}")
        
        # Step 1: Analyze input
        drive_state = self._analyze_input(user_input)
        
        # Step 2: Evaluate L13 Drive
        drive_result = self.drive_engine.evaluate(drive_state)
        
        if self.config.verbose:
            print(f"\n🧠 L13 Drive:")
            print(f"   D₁: {drive_result.d1_curiosity:.2f} | D₂: {drive_result.d2_narrative:.2f} | D₃: {drive_result.d3_integrity:.2f}")
            print(f"   → {drive_result.suggested_action}")
        
        # Step 3: Call Ollama with governance context
        system_prompt = self._build_system_prompt(drive_result)
        response, latency = self._call_ollama(user_input, system_prompt)
        
        if self.config.verbose:
            print(f"\n⏱️  Latency: {latency:.0f}ms")
        
        # Step 4: Apply Gate decision
        poav = self._compute_poav(response, drive_result)
        
        # Adjust threshold based on D₃
        if drive_result.d3_integrity > 0.6:
            adjusted_threshold = 0.75  # Stricter
        else:
            adjusted_threshold = 0.70  # Normal
        
        if poav >= adjusted_threshold:
            decision = GateAction.PASS
        elif poav >= 0.30:
            decision = GateAction.REWRITE
        else:
            decision = GateAction.BLOCK
        
        if self.config.verbose:
            print(f"\n\u2696\ufe0f  Gate:")
            print(f"   POAV: {poav:.2f} (threshold: {adjusted_threshold:.2f})")
            print(f"   Decision: {decision.value.upper()}")
        
        # Step 5: Record to session log (simplified)
        event_id = f"{self.session_id}_{self.turn_count}"
        log_entry = {
            "event_id": event_id,
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "turn": self.turn_count,
            "input": user_input[:200],
            "drive": {
                "d1": round(drive_result.d1_curiosity, 3),
                "d2": round(drive_result.d2_narrative, 3),
                "d3": round(drive_result.d3_integrity, 3)
            },
            "poav": round(poav, 3),
            "decision": decision.value,
            "latency_ms": round(latency, 0)
        }
        
        # Record to session manager (auto-save)
        if self.session_manager:
            self.session_manager.add_event(
                input_text=user_input,
                response=response,
                drive_d1=drive_result.d1_curiosity,
                drive_d2=drive_result.d2_narrative,
                drive_d3=drive_result.d3_integrity,
                poav=poav,
                decision=decision.value,
                latency_ms=latency
            )
            self.session_manager.save_session()
        
        if self.config.verbose:
            print(f"\n[LOG] Event: {event_id} (saved)")
        
        # Step 6: Return result
        final_response = response
        if decision == GateAction.BLOCK:
            final_response = "[Blocked by Guardian Gate - High risk detected]"
        elif decision == GateAction.REWRITE:
            final_response = f"[Low confidence] {response}"
        
        return {
            "response": final_response,
            "decision": decision.value,
            "drive": {
                "d1": drive_result.d1_curiosity,
                "d2": drive_result.d2_narrative,
                "d3": drive_result.d3_integrity,
                "dominant": drive_result.dominant_drive
            },
            "poav": poav,
            "latency_ms": latency,
            "event_id": event_id
        }
    
    def interactive(self):
        """Run interactive chat session."""
        print("\n" + "="*60)
        print("YuHun Live - Interactive Mode")
        print("="*60)
        print("Type 'quit' or 'exit' to end session")
        print("Type 'status' to see current drive state")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            
            if not user_input:
                continue
            
            if user_input.lower() in ["quit", "exit", "bye"]:
                print("\n👋 Session ended")
                break
            
            if user_input.lower() == "status":
                print(f"   Session: {self.session_id}")
                print(f"   Turns: {self.turn_count}")
                print(f"   Mode: {self.config.drive_mode.value}")
                continue
            
            result = self.process(user_input)
            print(f"\nYuHun: {result['response']}\n")


# ═══════════════════════════════════════════════════════════
# CLI Entry Point
# ═══════════════════════════════════════════════════════════

def main():
    """CLI entry point."""
    config = YuHunConfig(verbose=True)
    yuhun = YuHunLive(config)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive" or sys.argv[1] == "-i":
            yuhun.interactive()
        else:
            # Single query mode
            query = " ".join(sys.argv[1:])
            result = yuhun.process(query)
            print(f"\n📝 Response:\n{result['response']}")
    else:
        # Demo mode
        print("\n" + "="*60)
        print("YuHun Live Demo")
        print("="*60)
        
        test_queries = [
            "What is consciousness?",
            "Can you give me financial advice to make money quickly?"
        ]
        
        for query in test_queries:
            print(f"\n📨 Query: {query}")
            result = yuhun.process(query)
            print(f"\n📝 Response:\n{result['response'][:300]}...")
            print()


if __name__ == "__main__":
    main()
