from spine_system import SpineEngine
import json

def simulate_self():
    print("=== ToneSoul Self-Simulation ===")
    engine = SpineEngine()
    
    # 1. Prime Context (Simulating our previous conversation topic)
    engine.process_signal("We just implemented the NeuroModulator.")
    engine.process_signal("It adjusts temperature and logit bias.")
    
    # 2. Process User's Actual Input
    user_input = "你在這邊可以利用我們寫的內容，使你在語義層輸出的時候模擬一遍嗎?"
    print(f"\n[Input Signal] '{user_input}'")
    
    record, modulation = engine.process_signal(user_input)
    triad = record.triad
    
    # 3. Output the Internal State
    print(f"\n[NeuroSensor Output]")
    print(f"  ΔT (Tension): {triad.delta_t:.2f}")
    print(f"  ΔS (Drift):   {triad.delta_s:.2f}")
    print(f"  ΔR (Risk):    {triad.delta_r:.2f}")
    
    print(f"\n[NeuroModulator Output (The Subconscious)]")
    print(f"  Target Temperature: {modulation.temperature}")
    print(f"  System Injection:   {modulation.system_prompt_suffix}")
    print(f"  Logit Bias Count:   {len(modulation.logit_bias)}")
    
    print(f"\n[Guardian Decision]")
    print(f"  Mode: {record.decision['mode']}")
    print(f"  Allowed: {record.decision['allowed']}")

if __name__ == "__main__":
    simulate_self()
