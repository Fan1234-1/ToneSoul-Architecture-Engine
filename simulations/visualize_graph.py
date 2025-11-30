"""
Time-Island Visualizer
----------------------
Reads the ledger.jsonl and generates a Mermaid diagram representing
the Time-Islands, Steps, and their connections.
"""

import sys
import os
import json

# Ensure we can import from core and body
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../body"))

from body.spine_system import StepLedger

def generate_mermaid():
    ledger = StepLedger()
    
    mermaid_lines = ["graph TD"]
    mermaid_lines.append("    %% Styles")
    mermaid_lines.append("    classDef island fill:#e1f5fe,stroke:#01579b,stroke-width:2px;")
    mermaid_lines.append("    classDef step fill:#f3e5f5,stroke:#4a148c,stroke-width:1px;")
    mermaid_lines.append("    classDef critical fill:#ffebee,stroke:#b71c1c,stroke-width:2px;")
    mermaid_lines.append("    classDef creative fill:#f1f8e9,stroke:#33691e,stroke-width:2px;")
    
    print(f"Found {len(ledger._islands)} islands.")
    
    for i, island in enumerate(ledger._islands):
        island_node = f"Island_{i}"
        status_icon = "🔒" if island.status == "CLOSED" else "🟢"
        mermaid_lines.append(f"    subgraph {island_node} [Time-Island: {island.island_id[:8]} {status_icon}]")
        mermaid_lines.append(f"        direction TB")
        
        prev_step_id = None
        for step in island.steps:
            step_id = f"Step_{step.hash[:8]}"
            mode = step.decision.get('mode', 'UNKNOWN')
            reasoning = step.reasoning_mode
            
            # Node Label
            label = f"<b>{mode}</b><br/>{reasoning}<br/>ΔT:{step.triad.delta_t:.2f}"
            
            # Style based on Reasoning Mode
            style_class = "step"
            if reasoning == "Critical":
                style_class = "critical"
            elif reasoning == "Creative":
                style_class = "creative"
                
            mermaid_lines.append(f"        {step_id}(\"{label}\"):::{style_class}")
            
            # Link within island
            if prev_step_id:
                mermaid_lines.append(f"        {prev_step_id} --> {step_id}")
            
            prev_step_id = step_id
            
        mermaid_lines.append("    end")
        
        # Link Islands (Sequential)
        if i > 0:
            prev_island_last_step = ledger._islands[i-1].steps[-1]
            curr_island_first_step = island.steps[0]
            if prev_island_last_step and curr_island_first_step:
                src = f"Step_{prev_island_last_step.hash[:8]}"
                dst = f"Step_{curr_island_first_step.hash[:8]}"
                mermaid_lines.append(f"    {src} -.->|Temporal Flow| {dst}")

    output_path = os.path.join(os.path.dirname(__file__), "../docs/time_island_graph.mermaid")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(mermaid_lines))
    
    print(f"Mermaid graph generated at: {output_path}")
    print("Content Preview:")
    print("\n".join(mermaid_lines[:10]) + "\n...")

if __name__ == "__main__":
    generate_mermaid()
