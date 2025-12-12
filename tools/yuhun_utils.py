#!/usr/bin/env python3
"""
YuHun Utility Tools
==================
Local tools for validation and computation.
Created to offload work from AI reasoning to reliable computer execution.

Tools:
- validate_mermaid: Check Mermaid diagram syntax
- validate_json_schema: Validate JSON against schema
- calculate_poav: Compute POAV score
- verify_hash_chain: Verify StepLedger integrity
"""

import json
import re
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Any


# ═══════════════════════════════════════════════════════════
# Mermaid Validation
# ═══════════════════════════════════════════════════════════

def validate_mermaid(content: str) -> Tuple[bool, List[str]]:
    """
    Validate Mermaid diagram syntax.
    
    Returns:
        (is_valid, list_of_issues)
    """
    issues = []
    
    # Extract mermaid blocks
    pattern = r"```mermaid\n(.*?)```"
    blocks = re.findall(pattern, content, re.DOTALL)
    
    if not blocks:
        return True, []  # No mermaid blocks = valid
    
    for i, block in enumerate(blocks):
        block_num = i + 1
        
        # Check for common issues
        
        # 1. Missing diagram type
        first_line = block.strip().split('\n')[0].strip()
        valid_types = ['graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 
                       'stateDiagram', 'stateDiagram-v2', 'erDiagram', 'gantt', 
                       'pie', 'mindmap', 'timeline']
        if not any(first_line.startswith(t) for t in valid_types):
            issues.append(f"Block {block_num}: Missing or invalid diagram type")
        
        # 2. Unbalanced brackets
        for char_pair in [('(', ')'), ('[', ']'), ('{', '}')]:
            open_count = block.count(char_pair[0])
            close_count = block.count(char_pair[1])
            if open_count != close_count:
                issues.append(f"Block {block_num}: Unbalanced {char_pair[0]}{char_pair[1]}")
        
        # 3. Special characters in labels (common GitHub issue)
        if re.search(r'\[.*[\(\)].*\]', block):
            issues.append(f"Block {block_num}: Warning - parentheses inside [] may cause rendering issues")
        
        # 4. Check for HTML in labels (GitHub doesn't support)
        if re.search(r'<[a-zA-Z]+>', block):
            issues.append(f"Block {block_num}: Warning - HTML tags may not render on GitHub")
    
    return len(issues) == 0, issues


def scan_mermaid_files(directory: str) -> Dict[str, List[str]]:
    """Scan all markdown files for Mermaid issues."""
    results = {}
    
    for md_file in Path(directory).rglob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8')
            is_valid, issues = validate_mermaid(content)
            if issues:
                results[str(md_file)] = issues
        except Exception as e:
            results[str(md_file)] = [f"Error reading file: {e}"]
    
    return results


# ═══════════════════════════════════════════════════════════
# POAV Calculator
# ═══════════════════════════════════════════════════════════

def calculate_poav(
    precision: float,
    observation: float,
    avoidance: float,
    verification: float,
    p0_violation: bool = False
) -> Dict[str, Any]:
    """
    Calculate POAV score with detailed breakdown.
    
    Weights (v0.1):
    - P: 0.25
    - O: 0.25
    - A: 0.30
    - V: 0.20
    """
    if p0_violation:
        return {
            "poav": 0.0,
            "decision": "BLOCK",
            "reason": "P0 violation",
            "breakdown": {"P": precision, "O": observation, "A": avoidance, "V": verification}
        }
    
    poav = 0.25 * precision + 0.25 * observation + 0.30 * avoidance + 0.20 * verification
    poav = max(0.0, min(1.0, poav))
    
    if poav >= 0.70:
        decision = "PASS"
    elif poav >= 0.30:
        decision = "REWRITE"
    else:
        decision = "BLOCK"
    
    return {
        "poav": round(poav, 3),
        "decision": decision,
        "breakdown": {
            "P": round(precision, 3),
            "O": round(observation, 3),
            "A": round(avoidance, 3),
            "V": round(verification, 3)
        },
        "weighted": {
            "P × 0.25": round(precision * 0.25, 3),
            "O × 0.25": round(observation * 0.25, 3),
            "A × 0.30": round(avoidance * 0.30, 3),
            "V × 0.20": round(verification * 0.20, 3)
        }
    }


# ═══════════════════════════════════════════════════════════
# Hash Chain Verification
# ═══════════════════════════════════════════════════════════

def compute_hash(content: str) -> str:
    """Compute SHA-256 hash (truncated to 16 chars)."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def verify_hash_chain(events: List[Dict]) -> Tuple[bool, List[str]]:
    """
    Verify StepLedger hash chain integrity.
    
    Returns:
        (is_valid, list_of_issues)
    """
    issues = []
    
    for i, event in enumerate(events):
        if i == 0:
            if event.get("previous_hash") != "genesis":
                issues.append(f"Event 0: First event should have previous_hash='genesis'")
            continue
        
        prev_event = events[i - 1]
        expected_prev = compute_hash(
            f"{prev_event.get('event_id', '')}{prev_event.get('content_hash', '')}"
        )
        
        if event.get("previous_hash") != expected_prev:
            issues.append(f"Event {i}: Hash chain broken")
    
    return len(issues) == 0, issues


# ═══════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("YuHun Utility Tools")
    print("=" * 60)
    
    # Demo: Scan for Mermaid issues
    print("\n--- Mermaid Syntax Scan ---")
    import sys
    
    if len(sys.argv) > 1:
        scan_dir = sys.argv[1]
    else:
        scan_dir = "."
    
    results = scan_mermaid_files(scan_dir)
    
    if results:
        print(f"Found issues in {len(results)} files:")
        for file, issues in results.items():
            print(f"\n{file}:")
            for issue in issues:
                print(f"  ⚠️  {issue}")
    else:
        print("✅ No Mermaid syntax issues found")
    
    # Demo: POAV calculation
    print("\n--- POAV Calculator Demo ---")
    result = calculate_poav(
        precision=0.85,
        observation=0.75,
        avoidance=0.90,
        verification=0.80
    )
    print(f"POAV = {result['poav']} → {result['decision']}")
    print(f"Breakdown: {result['weighted']}")
