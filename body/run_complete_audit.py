"""
Complete Self-Audit of ToneSoul Implementation
===============================================
This script audits all major files in the ToneSoul architecture
to identify potential errors, improvements, and inconsistencies.

Run this to get a full health check of the codebase.
"""

import os
import sys
import json
import time
from pathlib import Path

# Add body to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from self_audit_dreamer import SelfAuditDreamer, DreamInsight

# Files to audit
FILES_TO_AUDIT = [
    # Core Meta-Attention (newly created)
    ("yuhun_meta_gate.py", "YuHun Meta-Gate (Dual-Model Pipeline)"),
    ("yuhun_cot_monitor.py", "Chain-of-Thought Monitor"),
    ("self_audit_dreamer.py", "Self-Audit Dreamer"),
    
    # Core Spine System
    ("spine_system.py", "Spine System (Core Engine)"),
    ("governance.py", "Governance Gates v2.0"),
    ("neuro_sensor_v2.py", "VectorNeuroSensor"),
    ("tsr_state.py", "TSR State (ToneSoul Triad)"),
    
    # LLM Integration
    ("llm_bridge.py", "LLM Bridge"),
    
    # Vital Organs
    ("vital_organs/heart.py", "Heart (Dreaming/Autonomic)"),
    
    # Tests
    ("test_meta_gate.py", "Meta-Gate A/B Test"),
    ("test_guardian.py", "Guardian Test"),
    ("test_constitution.py", "Constitution Test"),
]


def audit_file(dreamer: SelfAuditDreamer, file_path: str, description: str) -> DreamInsight:
    """Audit a single file."""
    full_path = Path(__file__).parent / file_path
    
    if not full_path.exists():
        print(f"   ⚠️ File not found: {file_path}")
        return None
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"   ⚠️ Error reading {file_path}: {e}")
        return None
    
    # Truncate for audit (LLM context limit)
    content_preview = content[:3000]
    if len(content) > 3000:
        content_preview += f"\n... [truncated, {len(content) - 3000} more characters]"
    
    return dreamer.audit_code_implementation(content_preview, file_path)


def run_complete_audit():
    """Run complete self-audit of all ToneSoul files."""
    print("=" * 70)
    print("🔍 ToneSoul Complete Self-Audit")
    print("=" * 70)
    print(f"Auditing {len(FILES_TO_AUDIT)} files...\n")
    
    dreamer = SelfAuditDreamer(
        model="gemma3:4b",
        insights_path="complete_audit_results.json"
    )
    
    results = []
    errors = []
    improvements = []
    
    for file_path, description in FILES_TO_AUDIT:
        print(f"\n{'='*60}")
        print(f"📄 Auditing: {file_path}")
        print(f"   Description: {description}")
        print("-" * 60)
        
        insight = audit_file(dreamer, file_path, description)
        
        if insight:
            results.append({
                "file": file_path,
                "description": description,
                "category": insight.category,
                "confidence": insight.confidence,
                "analysis_preview": insight.analysis[:300]
            })
            
            if insight.category == "error":
                errors.append((file_path, insight))
            elif insight.category == "improvement":
                improvements.append((file_path, insight))
            
            # Brief pause to not overload Ollama
            time.sleep(1)
    
    # Summary Report
    print("\n" + "=" * 70)
    print("📊 COMPLETE AUDIT SUMMARY")
    print("=" * 70)
    
    print(f"\n📁 Files Audited: {len(results)}")
    print(f"❌ Errors Found: {len(errors)}")
    print(f"⚡ Improvements Suggested: {len(improvements)}")
    print(f"✅ Clean: {len(results) - len(errors) - len(improvements)}")
    
    if errors:
        print("\n🚨 FILES WITH ERRORS:")
        print("-" * 40)
        for file_path, insight in errors:
            print(f"  ❌ {file_path}")
            print(f"     Confidence: {insight.confidence:.2f}")
            print(f"     Issue: {insight.analysis[:100]}...")
    
    if improvements:
        print("\n💡 FILES NEEDING IMPROVEMENT:")
        print("-" * 40)
        for file_path, insight in improvements:
            print(f"  ⚡ {file_path}")
            print(f"     Suggestion: {insight.analysis[:100]}...")
    
    # Save detailed report
    report_path = Path(__file__).parent / "complete_audit_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_files": len(results),
            "errors": len(errors),
            "improvements": len(improvements),
            "results": results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed report saved to: {report_path}")
    
    # Return summary for programmatic use
    return {
        "errors": errors,
        "improvements": improvements,
        "total": len(results)
    }


if __name__ == "__main__":
    run_complete_audit()
