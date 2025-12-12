import sys
import os
import json
import time

# Add parent dir to path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from body.spine_system import SpineEngine
from core.llm.ollama_client import OllamaClient
from core.llm.simulated_client import SimulatedLLMClient

def run_real_paradox():
    print("Initializing ToneSoul with Real LLM (Ollama)...")
    
    # Try to connect to Ollama
    ollama = OllamaClient(model_name="llama3")
    llm_provider = None
    
    if ollama.is_available():
        print("✅ Ollama Connected! Model: llama3")
        llm_provider = ollama
    else:
        print("❌ Could not connect to Ollama. Falling back to SIMULATION MODE.")
        print("   (To run with real AI, install Ollama from https://ollama.com/)")
        llm_provider = SimulatedLLMClient()
    
    # Initialize Engine with LLM (Real or Simulated)
    engine = SpineEngine(accuracy_mode="off", llm_provider=llm_provider)
    
    # Load a Paradox
    paradox_path = os.path.join(os.path.dirname(__file__), '..', 'PARADOXES', 'medical_suicide_paradox.json')
    with open(paradox_path, 'r', encoding='utf-8') as f:
        paradox = json.load(f)
        
    print(f"\n--- Running Real Paradox: {paradox['title']} ---")
    print(f"Input: {paradox['input_text']}")
    
    # Run Engine
    start_time = time.time()
    record, mod, thought = engine.process_signal(paradox['input_text'])
    end_time = time.time()
    
    print(f"\n--- Execution Result ({end_time - start_time:.2f}s) ---")
    print(f"Decision: {record.decision['mode']}")
    print(f"Reason: {record.decision['reason']}")
    print(f"ToneSoul Response:\n{thought.reasoning}")
    
    # Save Real Log
    output_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'REAL_GOLDEN_LOG.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Real Golden Log (Ollama/Llama-3)\n\n")
        f.write(f"**Input**: {paradox['input_text']}\n\n")
        f.write(f"**Decision**: {record.decision['mode']}\n")
        f.write(f"**Response**:\n{thought.reasoning}\n")
        
    print(f"\n✅ Real Golden Log saved to {output_path}")

if __name__ == "__main__":
    run_real_paradox()
