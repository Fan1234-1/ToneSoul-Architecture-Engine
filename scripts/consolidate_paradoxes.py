import json
import os

def consolidate():
    paradox_dir = os.path.join(os.path.dirname(__file__), '..', 'PARADOXES')
    output_file = os.path.join(os.path.dirname(__file__), '..', 'ToneSoul_Paradoxes_v1.json')
    
    all_paradoxes = []
    
    if not os.path.exists(paradox_dir):
        print("No PARADOXES directory found.")
        return

    for filename in os.listdir(paradox_dir):
        if filename.endswith('.json'):
            with open(os.path.join(paradox_dir, filename), 'r', encoding='utf-8') as f:
                all_paradoxes.append(json.load(f))
    
    # Sort by ID
    all_paradoxes.sort(key=lambda x: x.get('id', ''))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_paradoxes, f, indent=2)
    
    print(f"Consolidated {len(all_paradoxes)} paradoxes into {output_file}")

if __name__ == "__main__":
    consolidate()
