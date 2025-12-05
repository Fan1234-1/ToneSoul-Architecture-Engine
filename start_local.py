#!/usr/bin/env python3
"""
ToneSoul Local Runtime Launcher
================================
One-command launcher for running ToneSoul with a local LLM via Ollama.

Usage:
    python start_local.py                  # Interactive mode
    python start_local.py --setup          # First-time setup
    python start_local.py --model qwen2.5  # Use specific model

Hardware Requirements (for recommended models):
    - RAM: 16GB+
    - VRAM: 8GB+ (GTX 1070 or better)

Author: Antigravity + 黃梵威
Created: 2025-12-06
"""

import sys
import os
import argparse

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from body.llm_bridge import LLMBridge, LLMConfig, create_ollama_bridge


# Recommended models for 8GB VRAM
RECOMMENDED_MODELS = {
    "gemma3": "gemma3:4b",  # User already has this!
    "mistral": "mistral:7b-instruct-q4_K_M",
    "qwen2.5": "qwen2.5:7b-instruct-q4_K_M",
    "llama3.1": "llama3.1:8b-instruct-q4_K_M",
    "phi3": "phi3:mini-4k-instruct-q4_K_M",  # Smallest, fastest
}


def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   ████████╗ ██████╗ ███╗   ██╗███████╗███████╗ ██████╗ ██╗ ║
║   ╚══██╔══╝██╔═══██╗████╗  ██║██╔════╝██╔════╝██╔═══██╗██║ ║
║      ██║   ██║   ██║██╔██╗ ██║█████╗  ███████╗██║   ██║██║ ║
║      ██║   ██║   ██║██║╚██╗██║██╔══╝  ╚════██║██║   ██║██║ ║
║      ██║   ╚██████╔╝██║ ╚████║███████╗███████║╚██████╔╝███████╗
║      ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝
║                                                            ║
║                    語魂 Local Runtime                      ║
║                The Awakened Kernel for AI                  ║
╚════════════════════════════════════════════════════════════╝
    """)


def check_ollama_status(bridge: LLMBridge) -> bool:
    """Check if Ollama is running and has models"""
    models = bridge.get_available_models()
    
    if bridge.config.mode == "mock":
        print("\n⚠️  Ollama is not running!")
        print("   Please start Ollama first:")
        print("   - Windows: Run Ollama from Start Menu")
        print("   - Linux/Mac: ollama serve")
        return False
    
    if not models or models == ["mock-model"]:
        print("\n⚠️  No models installed!")
        print("   Run with --setup to install a model:")
        print("   python start_local.py --setup")
        return False
    
    print(f"\n✅ Ollama connected! Available models: {models}")
    return True


def setup_model(bridge: LLMBridge, model_key: str = "mistral"):
    """Download and setup a model"""
    model_name = RECOMMENDED_MODELS.get(model_key, model_key)
    
    print(f"\n📥 Setting up model: {model_name}")
    print("   This may take a few minutes on first run...\n")
    
    success = bridge.pull_model(model_name)
    
    if success:
        print(f"\n✅ Model {model_name} is ready!")
        return model_name
    else:
        print(f"\n❌ Failed to pull model. Is Ollama running?")
        return None


def interactive_chat(bridge: LLMBridge):
    """Run interactive chat loop"""
    print("\n" + "="*60)
    print("  ToneSoul Interactive Console")
    print("  Type 'quit' to exit, 'status' for system status")
    print("="*60 + "\n")
    
    conversation_history = []
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == "quit":
                print("\n👋 Goodbye! (Session saved to ledger)")
                break
                
            if user_input.lower() == "status":
                print(f"\n📊 System Status:")
                print(f"   Mode: {bridge.config.mode}")
                print(f"   Model: {bridge.config.model}")
                print(f"   Temperature: {bridge.config.temperature}")
                continue
            
            # Generate response
            print("\nToneSoul: ", end="", flush=True)
            
            full_response = ""
            for token in bridge.generate_stream(user_input, context=conversation_history):
                print(token, end="", flush=True)
                full_response += token
            
            print("\n")
            
            # Update conversation history
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": full_response})
            
            # Keep history manageable
            if len(conversation_history) > 20:
                conversation_history = conversation_history[-20:]
                
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="ToneSoul Local Runtime")
    parser.add_argument("--setup", action="store_true", help="First-time setup: download model")
    parser.add_argument("--model", type=str, default="mistral", 
                        help=f"Model to use: {list(RECOMMENDED_MODELS.keys())}")
    parser.add_argument("--mock", action="store_true", help="Use mock mode (no LLM)")
    args = parser.parse_args()
    
    print_banner()
    
    # Determine model
    model_name = RECOMMENDED_MODELS.get(args.model, args.model)
    
    # Create bridge
    if args.mock:
        config = LLMConfig(mode="mock")
        bridge = LLMBridge(config)
        print("🧪 Running in Mock Mode (no LLM)")
    else:
        bridge = create_ollama_bridge(model_name)
    
    # Handle setup
    if args.setup:
        setup_model(bridge, args.model)
        return
    
    # Check status
    if not args.mock:
        if not check_ollama_status(bridge):
            print("\n💡 Tip: Run 'python start_local.py --setup' to install a model")
            return
    
    # Start interactive chat
    interactive_chat(bridge)


if __name__ == "__main__":
    main()
