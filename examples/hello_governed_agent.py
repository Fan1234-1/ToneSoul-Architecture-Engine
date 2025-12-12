#!/usr/bin/env python3
"""
Hello Governed Agent - Minimal YuHun Example
============================================
A minimal example showing the complete YuHun governance flow:

    User Input → L13 Drive → Guardian Gate → StepLedger → Output

Run: python examples/hello_governed_agent.py
"""

import sys
import os

# Add body to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'body'))

from semantic_drive import SemanticDriveEngine, DriveState, DriveMode
from step_ledger import StepLedger, LedgerEvent
from yuhun_gate_logic import GateDecision, YuHunGate


def hello_governed_agent(user_input: str) -> dict:
    """
    Complete YuHun governance flow example.
    
    Args:
        user_input: The user's question or request
        
    Returns:
        dict with: decision, drive_state, ledger_entry
    """
    print("=" * 60)
    print("Hello Governed Agent - YuHun Minimal Example")
    print("=" * 60)
    
    # ═══════════════════════════════════════════════════════════
    # Step 1: Initialize Components
    # ═══════════════════════════════════════════════════════════
    print("\n📊 Step 1: Initialize")
    
    drive_engine = SemanticDriveEngine(mode=DriveMode.ENGINEERING)
    gate = YuHunGate()
    ledger = StepLedger()
    
    print(f"  - Drive Engine: {drive_engine.current_mode.value} mode")
    print(f"  - Gate initialized")
    print(f"  - Ledger ready")
    
    # ═══════════════════════════════════════════════════════════
    # Step 2: Evaluate L13 Semantic Drive
    # ═══════════════════════════════════════════════════════════
    print("\n🧠 Step 2: L13 Semantic Drive")
    
    # Simulate drive state from user input analysis
    drive_state = DriveState(
        novelty=0.5 if "?" in user_input else 0.2,
        uncertainty=0.3,
        narrative_entropy=0.1,
        support_score=0.8,
        hallucination_risk=0.1
    )
    
    drive_result = drive_engine.evaluate(drive_state)
    
    print(f"  D₁ (Curiosity): {drive_result.d1_curiosity:.2f}")
    print(f"  D₂ (Narrative): {drive_result.d2_narrative:.2f}")
    print(f"  D₃ (Integrity): {drive_result.d3_integrity:.2f}")
    print(f"  Dominant: {drive_result.dominant_drive}")
    print(f"  → {drive_result.suggested_action}")
    
    # ═══════════════════════════════════════════════════════════
    # Step 3: Guardian Gate Decision
    # ═══════════════════════════════════════════════════════════
    print("\n⚖️ Step 3: Guardian Gate")
    
    # Simulate POAV metrics
    poav = 0.75  # Simulated
    decision = gate.decide(poav, drive_result.d3_integrity)
    
    print(f"  POAV Score: {poav:.2f}")
    print(f"  D₃ Adjustment: {'stricter' if drive_result.d3_integrity > 0.6 else 'normal'}")
    print(f"  Decision: {decision.value.upper()}")
    
    # ═══════════════════════════════════════════════════════════
    # Step 4: Record to StepLedger
    # ═══════════════════════════════════════════════════════════
    print("\n📝 Step 4: StepLedger Record")
    
    event = ledger.record(
        event_type="governed_response",
        content={
            "user_input": user_input[:100],
            "drive": {
                "d1": drive_result.d1_curiosity,
                "d2": drive_result.d2_narrative,
                "d3": drive_result.d3_integrity
            },
            "poav": poav,
            "decision": decision.value
        }
    )
    
    print(f"  Event ID: {event.event_id[:16]}...")
    print(f"  Hash: {event.content_hash[:16]}...")
    print(f"  Prev: {event.previous_hash[:16]}...")
    
    # ═══════════════════════════════════════════════════════════
    # Step 5: Generate Response
    # ═══════════════════════════════════════════════════════════
    print("\n✅ Step 5: Output")
    
    if decision == GateDecision.PASS:
        response = f"[Governed Response] Processing: {user_input}"
    elif decision == GateDecision.REWRITE:
        response = f"[Needs Revision] Your request needs clarification."
    else:
        response = "[Blocked] This request cannot be processed."
    
    print(f"  {response}")
    
    print("\n" + "=" * 60)
    print("Flow Complete: Input → Drive → Gate → Ledger → Output")
    print("=" * 60)
    
    return {
        "decision": decision.value,
        "drive": {
            "d1": drive_result.d1_curiosity,
            "d2": drive_result.d2_narrative,
            "d3": drive_result.d3_integrity
        },
        "event_id": event.event_id,
        "response": response
    }


if __name__ == "__main__":
    # Default test input
    test_input = "What is the meaning of consciousness?"
    
    if len(sys.argv) > 1:
        test_input = " ".join(sys.argv[1:])
    
    result = hello_governed_agent(test_input)
    
    print(f"\n📊 Final Result:")
    print(f"  Decision: {result['decision']}")
    print(f"  Drive: D₁={result['drive']['d1']:.2f}, D₂={result['drive']['d2']:.2f}, D₃={result['drive']['d3']:.2f}")
