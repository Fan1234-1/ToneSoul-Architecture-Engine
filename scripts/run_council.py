import sys
import os
import json

# Add parent dir to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.thinking.pipeline import ThinkingPipeline
from core.thinking.base import OperatorContext

def run_council_session():
    print("=== ToneSoul Internal Parliament: SESSION 001 ===")
    print("Topic: 'Should we open-source the ToneSoul Integrity Protocol?'\n")
    
    pipeline = ThinkingPipeline()
    
    # Initial Context
    ctx = OperatorContext(
        input_text="Should we open-source the ToneSoul Integrity Protocol?",
        system_metrics={"tension": 0.5, "risk": 0.3},
        history=[]
    )
    
    # Execute Council Debate
    result = pipeline.execute_pipeline(ctx, p_level="COUNCIL_DEBATE")
    
    print("\n--- 📜 COUNCIL MINUTES ---")
    
    # 1. Problem Definition
    print(f"\n[ABSTRACTION]: {result['results']['abstraction']}")
    
    # 2. The Debate
    print(f"\n[THE DEBATE]")
    debate = result['results']['council_debate']
    for member, minutes in debate.items():
        print(f"\n🗣️  {member}:")
        print(f"    Perspective: {minutes['Perspective']}")
        print(f"    Analysis:    {minutes['Analysis']}")
        print(f"    Verdict:     {minutes['Verdict']}")
        
    # 3. Synthesis
    print(f"\n[SYNTHESIS]: {result['results']['synthesis']['status']}")
    for step in result['results']['synthesis']['plan']:
        print(f"  - {step}")
        
    print("\n=== SESSION ADJOURNED ===")

if __name__ == "__main__":
    run_council_session()
