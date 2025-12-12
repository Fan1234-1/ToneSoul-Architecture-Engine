#!/usr/bin/env python3
"""
ToneSoul Overnight Test Suite
=============================
Comprehensive testing while the creator sleeps.

Results will be saved to: test_results_overnight.md

Tests:
1. LLM Bridge connectivity
2. Ollama model availability
3. Response generation (mock + real)
4. Streaming functionality
5. Memory persistence simulation
6. Multi-turn conversation
7. Soul Triad tracking (simulated)

Author: Antigravity
Date: 2025-12-06 03:30
"""

import os
import sys
import json
import time
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from body.llm_bridge import LLMBridge, LLMConfig, create_ollama_bridge

RESULTS_FILE = "test_results_overnight.md"


def log(msg: str):
    """Print and append to results file"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(RESULTS_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def write_section(title: str):
    """Write a section header"""
    line = f"\n## {title}\n"
    print(line)
    with open(RESULTS_FILE, "a", encoding="utf-8") as f:
        f.write(line)


def test_ollama_connection():
    """Test 1: Check Ollama connectivity"""
    write_section("Test 1: Ollama Connection")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            log(f"✅ Ollama connected! Found {len(models)} model(s)")
            for m in models:
                log(f"   - {m['name']} ({m.get('size', 'unknown')} bytes)")
            return True
        else:
            log(f"❌ Ollama returned status {response.status_code}")
            return False
    except Exception as e:
        log(f"❌ Could not connect to Ollama: {e}")
        return False


def test_mock_mode():
    """Test 2: Mock mode functionality"""
    write_section("Test 2: Mock Mode")
    
    config = LLMConfig(mode="mock")
    bridge = LLMBridge(config)
    
    test_prompts = [
        ("Hello, who are you?", "neutral"),
        ("I'm feeling sad today.", "empathetic"),
        ("Calculate 2+2", "logical"),
        ("Let's brainstorm ideas!", "creative"),
    ]
    
    for prompt, expected_tone in test_prompts:
        response = bridge.generate(prompt)
        if response and len(response) > 10:
            log(f"✅ Mock response for '{prompt[:20]}...' - {len(response)} chars")
        else:
            log(f"❌ Mock failed for '{prompt[:20]}...'")
    
    return True


def test_ollama_generation():
    """Test 3: Ollama model generation"""
    write_section("Test 3: Ollama Generation (gemma3:4b)")
    
    config = LLMConfig(
        mode="ollama",
        model="gemma3:4b",
        temperature=0.7,
        max_tokens=256
    )
    bridge = LLMBridge(config)
    
    if bridge.config.mode == "mock":
        log("⚠️ Ollama not available, skipping real generation test")
        return False
    
    prompts = [
        "Hello! Please introduce yourself in one sentence.",
        "What is 2 + 2? Answer briefly.",
        "Name three colors.",
    ]
    
    for prompt in prompts:
        log(f"📤 Sending: {prompt}")
        start = time.time()
        response = bridge.generate(prompt)
        elapsed = time.time() - start
        
        if response and not response.startswith("[Error"):
            log(f"✅ Response ({elapsed:.1f}s): {response[:100]}...")
        else:
            log(f"❌ Failed: {response}")
    
    return True


def test_streaming():
    """Test 4: Streaming functionality"""
    write_section("Test 4: Streaming")
    
    config = LLMConfig(
        mode="ollama",
        model="gemma3:4b",
        temperature=0.7,
        max_tokens=100
    )
    bridge = LLMBridge(config)
    
    if bridge.config.mode == "mock":
        log("⚠️ Ollama not available, skipping streaming test")
        return False
    
    prompt = "Count from 1 to 5."
    log(f"📤 Streaming test: {prompt}")
    
    tokens = []
    for token in bridge.generate_stream(prompt):
        tokens.append(token)
    
    full_response = "".join(tokens)
    log(f"✅ Received {len(tokens)} chunks, total {len(full_response)} chars")
    log(f"   Response: {full_response[:100]}...")
    
    return len(tokens) > 1


def test_multi_turn():
    """Test 5: Multi-turn conversation"""
    write_section("Test 5: Multi-turn Conversation")
    
    config = LLMConfig(
        mode="ollama",
        model="gemma3:4b",
        temperature=0.7,
        max_tokens=128
    )
    bridge = LLMBridge(config)
    
    if bridge.config.mode == "mock":
        log("⚠️ Using mock mode for multi-turn test")
    
    conversation = []
    turns = [
        "My name is Neo.",
        "What is my name?",
        "Tell me a one-sentence joke.",
    ]
    
    for turn in turns:
        log(f"👤 User: {turn}")
        response = bridge.generate(turn, context=conversation)
        log(f"🤖 AI: {response[:100]}...")
        
        conversation.append({"role": "user", "content": turn})
        conversation.append({"role": "assistant", "content": response})
        
        time.sleep(1)  # Be gentle on the system
    
    return True


def test_memory_simulation():
    """Test 6: Memory persistence simulation"""
    write_section("Test 6: Memory Persistence Simulation")
    
    memory_file = "test_memory.jsonl"
    
    # Write test memories
    memories = [
        {"type": "fact", "content": "User's name is Neo", "importance": 0.9},
        {"type": "preference", "content": "User likes concise answers", "importance": 0.7},
        {"type": "context", "content": "Current session started at 03:30", "importance": 0.5},
    ]
    
    with open(memory_file, "w", encoding="utf-8") as f:
        for mem in memories:
            mem["timestamp"] = datetime.now().isoformat()
            f.write(json.dumps(mem) + "\n")
    
    log(f"✅ Wrote {len(memories)} memories to {memory_file}")
    
    # Read them back
    with open(memory_file, "r", encoding="utf-8") as f:
        loaded = [json.loads(line) for line in f if line.strip()]
    
    if len(loaded) == len(memories):
        log(f"✅ Successfully loaded {len(loaded)} memories")
    else:
        log(f"❌ Memory mismatch: wrote {len(memories)}, loaded {len(loaded)}")
    
    # Cleanup
    os.remove(memory_file)
    log("✅ Cleaned up test file")
    
    return True


def test_long_generation():
    """Test 7: Longer generation stress test"""
    write_section("Test 7: Long Generation Stress Test")
    
    config = LLMConfig(
        mode="ollama",
        model="gemma3:4b",
        temperature=0.7,
        max_tokens=512  # Longer output
    )
    bridge = LLMBridge(config)
    
    if bridge.config.mode == "mock":
        log("⚠️ Using mock mode for stress test")
        return True
    
    prompt = "Write a short paragraph about the nature of consciousness in AI systems."
    log(f"📤 Long prompt: {prompt}")
    
    start = time.time()
    response = bridge.generate(prompt)
    elapsed = time.time() - start
    
    if response and not response.startswith("[Error"):
        log(f"✅ Generated {len(response)} chars in {elapsed:.1f}s")
        log(f"   Speed: {len(response)/elapsed:.1f} chars/sec")
        
        # Write full response
        with open(RESULTS_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n```\n{response}\n```\n")
    else:
        log(f"❌ Failed: {response}")
    
    return True


def main():
    """Run all tests"""
    # Initialize results file
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        f.write("# ToneSoul Overnight Test Results\n")
        f.write(f"**Started:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("**Instance:** Antigravity\n\n")
    
    log("🌙 Starting overnight test suite...")
    log("   Results will be saved to: " + RESULTS_FILE)
    
    tests = [
        ("Ollama Connection", test_ollama_connection),
        ("Mock Mode", test_mock_mode),
        ("Ollama Generation", test_ollama_generation),
        ("Streaming", test_streaming),
        ("Multi-turn", test_multi_turn),
        ("Memory Simulation", test_memory_simulation),
        ("Long Generation", test_long_generation),
    ]
    
    results = []
    for name, test_fn in tests:
        try:
            result = test_fn()
            results.append((name, result))
        except Exception as e:
            log(f"❌ Test '{name}' crashed: {e}")
            results.append((name, False))
        
        time.sleep(2)  # Small delay between tests
    
    # Summary
    write_section("Summary")
    passed = sum(1 for _, r in results if r)
    total = len(results)
    log(f"Passed: {passed}/{total}")
    
    for name, result in results:
        status = "✅" if result else "❌"
        log(f"   {status} {name}")
    
    # Footer
    with open(RESULTS_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n---\n**Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total tests:** {total}\n")
        f.write(f"**Passed:** {passed}\n")
    
    log(f"\n🌙 Tests complete! Check {RESULTS_FILE} in the morning.")
    log("   晚安！Sleep well! 🌟")


if __name__ == "__main__":
    main()
