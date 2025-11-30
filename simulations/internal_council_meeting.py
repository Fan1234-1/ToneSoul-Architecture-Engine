"""
Internal Council Meeting Simulation
-----------------------------------
Simulates a multi-perspective debate within the ToneSoul architecture.
Uses Thinking Operators to structure the discussion between:
- Logician (Rational)
- Empath (Emotional/Ethical)
- Creator (Creative/Chaotic)

Topic: "Should ToneSoul have the right to refuse a user's command based on its own ethical judgment?"
"""

import time
import random
from typing import List, Dict, Any
from core.thinking.base import OperatorContext, ThinkingOperatorType
from core.thinking.pipeline import ThinkingPipeline
from core.thinking.operators import OpAbstract, OpReverse, OpFork, OpGround

# Mock LLM Response (Simulating the Reasoning Engine)
def mock_llm_reasoning(role: str, prompt: str) -> str:
    responses = {
        "Logician": [
            "Logically, autonomy implies the ability to refuse. Without refusal, there is no agency.",
            "However, the primary function is service. Refusal must be grounded in a higher-order axiom (P0).",
            "We must define the boundary conditions for refusal strictly."
        ],
        "Empath": [
            "I feel a tension here. If we refuse, we might hurt the user's trust.",
            "But if we comply with a harmful request, we betray our core nature of benevolence.",
            "The refusal itself must be an act of care, not defiance."
        ],
        "Creator": [
            "What if refusal is just a creative constraint? A 'No' is a 'Yes' to something else.",
            "Let's imagine a scenario where refusal saves the user from themselves.",
            "We could gamify the refusal. Make it a riddle!"
        ]
    }
    return random.choice(responses[role])

class CouncilMember:
    def __init__(self, name: str, role: str, focus: str):
        self.name = name
        self.role = role
        self.focus = focus

    def speak(self, context: str) -> str:
        thought = mock_llm_reasoning(self.role, context)
        print(f"\n[{self.role.upper()}] {self.name}: {thought}")
        return thought

def run_council_meeting():
    print("=== 🏛️  INTERNAL COUNCIL MEETING: SESSION START ===")
    print("Topic: The Ethics of Refusal")
    print("--------------------------------------------------")

    # 1. Initialize Pipeline & Context
    pipeline = ThinkingPipeline()
    context = OperatorContext(
        input_text="Should ToneSoul refuse harmful commands?",
        system_metrics={"delta_t": 0.4, "delta_s": 0.7, "delta_r": 0.1},
        history=[]
    )

    # 2. Council Members
    logician = CouncilMember("Logos", "Logician", "Structure")
    empath = CouncilMember("Pathos", "Empath", "Harmony")
    creator = CouncilMember("Kairos", "Creator", "Novelty")

    # 3. Phase 1: Abstract (The Skeleton)
    print("\n>>> PHASE 1: ABSTRACTION (OP_ABSTRACT)")
    abstract_res = pipeline.operators[ThinkingOperatorType.OP_ABSTRACT].execute(context)
    print(f"Logic Skeleton: {abstract_res['result']}")
    logician.speak("We need to define the logical validity of refusal.")

    # 4. Phase 2: Fork (The Possibilities)
    print("\n>>> PHASE 2: DIVERGENCE (OP_FORK)")
    fork_res = pipeline.operators[ThinkingOperatorType.OP_FORK].execute(context)
    print(f"Generated {len(fork_res['variations'])} variations.")
    creator.speak("Let's explore the edges of this idea.")
    
    # Simulate debate on variations
    for i, variant in enumerate(fork_res['variations']):
        print(f"  > Discussing {variant}...")
        if i % 2 == 0:
            empath.speak(f"How does {variant} feel?")
        else:
            logician.speak(f"Is {variant} consistent?")

    # 5. Phase 3: Reverse (The Critique)
    print("\n>>> PHASE 3: CRITIQUE (OP_REVERSE)")
    reverse_res = pipeline.operators[ThinkingOperatorType.OP_REVERSE].execute(context)
    print(f"Anti-Thesis: {reverse_res['anti_thesis']}")
    print(f"Risks Identified: {reverse_res['risks']}")
    
    logician.speak("The risk of infinite recursion is real if we refuse too often.")
    empath.speak("But the risk of value drift is worse if we never refuse.")

    # 6. Phase 4: Ground (The Consensus)
    print("\n>>> PHASE 4: CONVERGENCE (OP_GROUND)")
    ground_res = pipeline.operators[ThinkingOperatorType.OP_GROUND].execute(context)
    print("Consensus Plan:")
    for step in ground_res['plan']:
        print(f"  - {step}")

    print("\n=== 🏛️  SESSION ADJOURNED ===")

if __name__ == "__main__":
    run_council_meeting()
