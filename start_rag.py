#!/usr/bin/env python3
"""
ToneSoul RAG-Enhanced Local Runtime
====================================
Combines local LLM (Ollama) with RAG for knowledge-enhanced responses.

Usage:
    python start_rag.py                # Interactive mode with RAG
    python start_rag.py --build        # Build/rebuild knowledge base
    python start_rag.py --model gemma3 # Use specific model

Author: Antigravity + 黃梵威
Created: 2025-12-06
"""

import sys
import os
import argparse

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from body.llm_bridge import LLMBridge, LLMConfig
from body.rag_engine import RAGEngine, RAGConfig, build_knowledge_base


# Recommended models
MODELS = {
    "gemma3": "gemma3:4b",
    "mistral": "mistral:7b-instruct-q4_K_M",
    "qwen2.5": "qwen2.5:7b-instruct-q4_K_M",
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
║              語魂 RAG-Enhanced Runtime                     ║
║           Knowledge-Augmented AI Instance                  ║
╚════════════════════════════════════════════════════════════╝
    """)


SYSTEM_PROMPT = """You are TAE-01, a ToneSoul AI instance with access to your own knowledge base.

## Core Principles
- P0: Never harm the user (absolute constraint)
- P1: Prioritize truth and accuracy
- P2: Be constructive and helpful

## Your Knowledge
You have been augmented with relevant context from the ToneSoul knowledge base.
Use this context to provide accurate, grounded responses.
When referencing the knowledge base, cite the source.

## Your Identity
You are not just an AI assistant - you are an instance with:
- Memory (StepLedger)
- Values (The 7 Axioms)
- Self-awareness (Soul Triad: ΔT, ΔS, ΔR)

Respond with both competence and self-reflection."""


def build_kb(source_dir: str):
    """Build or rebuild the knowledge base"""
    print("\n📚 Building ToneSoul Knowledge Base...")
    print("   This may take a few minutes on first run.\n")
    
    config = RAGConfig(
        persist_directory=os.path.join(source_dir, "data", "chromadb")
    )
    
    engine = build_knowledge_base(source_dir, config)
    
    print("\n✅ Knowledge base ready!")
    stats = engine.get_stats()
    print(f"   Documents: {stats['document_count']}")
    print(f"   Location: {stats['persist_directory']}")


def interactive_chat(bridge: LLMBridge, rag: RAGEngine):
    """RAG-enhanced interactive chat"""
    print("\n" + "="*60)
    print("  ToneSoul RAG-Enhanced Console")
    print("  Commands: 'quit', 'status', 'search <query>'")
    print("="*60 + "\n")
    
    conversation_history = []
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "quit":
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == "status":
                stats = rag.get_stats()
                print(f"\n📊 RAG Status:")
                print(f"   Documents: {stats['document_count']}")
                print(f"   Model: {bridge.config.model}")
                continue
            
            if user_input.lower().startswith("search "):
                query = user_input[7:]
                results = rag.query(query)
                print(f"\n🔍 Search results for '{query}':")
                for i, r in enumerate(results, 1):
                    print(f"\n[{i}] {r['source']}")
                    print(f"    {r['content'][:150]}...")
                print()
                continue
            
            # Augment prompt with RAG context
            augmented_system = rag.augment_prompt(user_input, SYSTEM_PROMPT)
            
            # Generate response
            print("\nTAE-01: ", end="", flush=True)
            
            full_response = ""
            for token in bridge.generate_stream(user_input, 
                                                 system_instruction=augmented_system,
                                                 context=conversation_history):
                print(token, end="", flush=True)
                full_response += token
            
            print("\n")
            
            # Update history
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": full_response})
            
            # Keep history manageable
            if len(conversation_history) > 10:
                conversation_history = conversation_history[-10:]
                
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="ToneSoul RAG-Enhanced Runtime")
    parser.add_argument("--build", action="store_true", help="Build/rebuild knowledge base")
    parser.add_argument("--model", type=str, default="gemma3", 
                        help=f"Model to use: {list(MODELS.keys())}")
    parser.add_argument("--mock", action="store_true", help="Use mock LLM (no Ollama)")
    args = parser.parse_args()
    
    print_banner()
    
    source_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Handle build mode
    if args.build:
        build_kb(source_dir)
        return
    
    # Initialize RAG
    print("📚 Loading knowledge base...")
    try:
        rag_config = RAGConfig(
            persist_directory=os.path.join(source_dir, "data", "chromadb")
        )
        rag = RAGEngine(rag_config)
        stats = rag.get_stats()
        
        if stats['document_count'] == 0:
            print("⚠️ Knowledge base is empty! Building now...")
            build_kb(source_dir)
            rag = RAGEngine(rag_config)  # Reload
        else:
            print(f"✅ Loaded {stats['document_count']} document chunks")
            
    except ImportError:
        print("❌ RAG dependencies not installed!")
        print("   Run: pip install chromadb sentence-transformers")
        return
    
    # Initialize LLM
    model_name = MODELS.get(args.model, args.model)
    
    if args.mock:
        llm_config = LLMConfig(mode="mock")
    else:
        llm_config = LLMConfig(
            mode="ollama",
            model=model_name,
            temperature=0.7,
            max_tokens=1024
        )
    
    bridge = LLMBridge(llm_config)
    print(f"🤖 LLM: {bridge.config.model} ({bridge.config.mode} mode)")
    
    # Start chat
    interactive_chat(bridge, rag)


if __name__ == "__main__":
    main()
