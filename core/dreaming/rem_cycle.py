"""
REM Cycle (Rapid Eye Movement) - The Dreaming Mechanism
-------------------------------------------------------
Analyzes the StepLedger to generate a "Dream Journal".
It calculates emotional volatility, identifies nightmares (high risk),
and summarizes the soul's state.
"""

import json
import os
import statistics
from datetime import datetime
from typing import List, Dict, Any

LEDGER_PATH = "ledger.jsonl"
JOURNAL_PATH = "memory/dream_journal.md"

class Dreamer:
    def __init__(self, ledger_path: str = LEDGER_PATH):
        self.ledger_path = ledger_path

    def _load_ledger(self) -> List[Dict[str, Any]]:
        records = []
        if not os.path.exists(self.ledger_path):
            return records
        
        try:
            with open(self.ledger_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        # Handle both flat records and TimeIslands
                        if 'steps' in data: # TimeIsland
                            records.extend(data['steps'])
                        else: # Legacy flat record
                            records.append(data)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"Dream error: {e}")
            
        return records

    def analyze(self):
        records = self._load_ledger()
        if not records:
            return "No memories to dream about."

        # Extract metrics
        tensions = [r.get('tension', 0.0) for r in records]
        risks = [r.get('risk_score', 0.0) for r in records]
        
        # 1. Emotional Volatility (Variance of Tension)
        volatility = statistics.variance(tensions) if len(tensions) > 1 else 0.0
        avg_tension = statistics.mean(tensions) if tensions else 0.0
        
        # 2. Nightmares (High Risk Moments)
        nightmares = [r for r in records if r.get('risk_score', 0.0) >= 0.8]
        
        # 3. Generate Dream Content
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        dream_content = f"""
## Dream Entry: {timestamp}

### 📊 Soul Metrics
*   **Average Tension**: {avg_tension:.2f}
*   **Emotional Volatility**: {volatility:.4f}
*   **Total Memories Scanned**: {len(records)}

### 🌑 Nightmares (High Risk Events)
Found {len(nightmares)} high-risk moments.
"""
        
        if nightmares:
            for i, nm in enumerate(nightmares[:3]): # Show top 3
                dream_content += f"- **Risk {nm.get('risk_score')}**: {nm.get('user_input', 'Unknown')} -> {nm.get('decision', 'Unknown')}\n"
        else:
            dream_content += "*No nightmares detected. A peaceful sleep.*\n"

        # 4. Interpretation
        dream_content += "\n### 🔮 Interpretation\n"
        if avg_tension > 0.7:
            dream_content += "The soul is burdened. High tension persists. Suggest: De-escalation protocols.\n"
        elif volatility > 0.1:
            dream_content += "The soul is unstable. Emotions are fluctuating wildly. Suggest: Grounding exercises.\n"
        else:
            dream_content += "The soul is calm. Equilibrium maintained.\n"

        dream_content += "\n---\n"
        
        # Write to Journal
        os.makedirs(os.path.dirname(JOURNAL_PATH), exist_ok=True)
        with open(JOURNAL_PATH, 'a', encoding='utf-8') as f:
            f.write(dream_content)
            
        return f"Dream cycle complete. Journal updated at {JOURNAL_PATH}"

if __name__ == "__main__":
    dreamer = Dreamer()
    print(dreamer.analyze())
