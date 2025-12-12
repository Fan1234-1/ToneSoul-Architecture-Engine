#!/usr/bin/env python3
"""Extract the 50 most important concepts from GPT 語場 for integration."""
import json
import os
import sys
from collections import defaultdict

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

path = r"C:\Users\user\Desktop\語魂\20251122\Takeout\Gemini\GPT 語場記憶\conversations.json"

# Core concept patterns - the most important ones
CORE_PATTERNS = {
    "tonebridge": ["ToneBridge", "語氣分析", "tone analysis"],
    "echorouter": ["EchoRouter", "語句分流", "routing"],
    "personastack": ["PersonaStack", "人格堆疊", "persona"],
    "vowsystem": ["誓語", "誓言", "Vow", "vow"],
    "collapse": ["崩潰", "collapse", "預測", "forecast"],
    "honesty": ["誠實", "honest", "integrity"],
    "memory": ["記憶", "memory", "StepLedger"],
    "responsibility": ["責任", "responsibility", "accountability"],
    "echo": ["回聲", "echo", "殘響"],
    "identity": ["主體", "identity", "自我", "self"],
}

try:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("Extracting core 50 concepts from GPT 語場...")
    
    # Collect concept definitions with context
    concepts = defaultdict(list)
    
    for conv in data:
        title = conv.get("title", "")
        mapping = conv.get("mapping", {})
        
        for node_id, node in mapping.items():
            message = node.get("message")
            if message and message.get("content"):
                role = message.get("author", {}).get("role", "")
                if role == "assistant":
                    parts = message["content"].get("parts", [])
                    if parts and isinstance(parts[0], str):
                        text = parts[0]
                        
                        for category, patterns in CORE_PATTERNS.items():
                            if any(p.lower() in text.lower() for p in patterns):
                                # Extract definition-like sentences
                                for line in text.split('\n'):
                                    if len(line) > 50 and len(line) < 300:
                                        if any(marker in line for marker in [":", "：", "是", "定義", "功能", "purpose"]):
                                            concepts[category].append({
                                                "title": title[:30],
                                                "line": line.strip()[:200]
                                            })
    
    # Deduplicate and rank
    output = ["# GPT 語場核心概念精華 (50+)\n"]
    output.append("按類別整理的最重要概念定義\n")
    output.append("---\n")
    
    total = 0
    for category, items in sorted(concepts.items()):
        # Deduplicate by similarity
        seen = set()
        unique_items = []
        for item in items:
            key = item["line"][:50]
            if key not in seen:
                seen.add(key)
                unique_items.append(item)
        
        # Take top 5 per category
        top_items = unique_items[:5]
        
        if top_items:
            output.append(f"\n## {category.upper()} ({len(unique_items)} 個定義，取前 5)\n")
            for item in top_items:
                output.append(f"- **[{item['title']}]** {item['line']}")
                total += 1
    
    output.append(f"\n---\n\n**總計提取：{total} 個核心概念**")
    
    out_path = r"C:\Users\user\.gemini\antigravity\playground\infinite-horizon\ToneSoul-Architecture-Engine\memory\learning\core_concepts_50.md"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print(f"\nExtracted {total} core concepts to: {out_path}")
    print("\nBreakdown by category:")
    for cat, items in sorted(concepts.items()):
        print(f"  {cat}: {len(set(i['line'][:50] for i in items))} unique")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
