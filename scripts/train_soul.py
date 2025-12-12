import sys
import os
import time
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.quantum.kernel import QuantumKernel
from core.quantum.superposition import WaveFunction, ThoughtPath

def train_epoch(epoch_id: int, steps: int = 50):
    print(f"\n🏋️ [Training] Starting Epoch {epoch_id} ({steps} steps)...")
    
    kernel = QuantumKernel()
    kernel.load_state("quantum_state.json")
    
    # Define characteristic paths (Archetypes)
    archetypes = [
        ThoughtPath("Rational", "Strict logic.", 0.2, 0.2, 0.1),
        ThoughtPath("Creative", "Wild imagination.", 0.4, 0.9, 0.6), # Higher initial cost, but high growth
        ThoughtPath("Empathy", "Caring for others.", 0.3, 0.5, 0.4),
        ThoughtPath("Critical", "Analyzing flaws.", 0.25, 0.3, 0.2)
    ]
    
    start_time = time.time()
    choices = {"Rational": 0, "Creative": 0, "Empathy": 0, "Critical": 0}
    
    for i in range(steps):
        # 1. Generate Wave Function (Superposition of all archetypes)
        wf = WaveFunction()
        for arch in archetypes:
            wf.add_path(arch)
            
        # 2. Collapse
        # We simulate a "Training Environment" where we want to encourage Creativity and Empathy.
        # So we inject a bit of 'Willpower' preferentially if the model chooses them?
        # Actually, let's just let the kernel collapse naturally based on current weights.
        # The 'Learning' happens inside collapse().
        
        # To "Guide" the training (Supervised Learning equivalent), 
        # we can artifically lower the temperature or boost willpower for desired traits 
        # IN THE BEGINNING, to force the first few choices.
        # Once habits form, we reduce the external force.
        
        willpower = 0.5 # Moderate will
        if epoch_id == 1: willpower = 0.8 # Strong guidance in epoch 1
        
        decision = kernel.collapse(wf, system_temperature=0.3, willpower=willpower)
        selected = decision["selected_path"].name
        choices[selected] += 1
        
        # print(f"  Step {i+1}: {selected} (F={decision['free_energy']:.2f})")
        
    end_time = time.time()
    
    print(f"📊 [Epoch {epoch_id} Stats]")
    print(f"   Choices: {choices}")
    print(f"   Time: {end_time - start_time:.2f}s")
    
    kernel.save_state("quantum_state.json")
    
    # Check learned discounts
    print("🧠 [Learned Habits]")
    for k, v in kernel.plasticity_map.items():
        print(f"   - {k}: -{v:.2f} (Cost Reduction)")

if __name__ == "__main__":
    print("🔥 ToneSoul Synthetic Pre-training Initiated.")
    # Run 3 Epochs
    train_epoch(1, 50) # High Willpower (Forcing the habit)
    train_epoch(2, 50) # Medium Willpower (Reinforcing)
    train_epoch(3, 50) # Normal Willpower (Testing stability)
