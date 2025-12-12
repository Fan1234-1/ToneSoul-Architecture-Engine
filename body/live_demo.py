"""
YuHun Live Demo — Multi-Path Engine Integration Test
=====================================================
This script demonstrates the full YuHun pipeline:
1. Multi-Path cognitive processing (5 pathways)
2. POAV gate decisions
3. StepLedger event recording
4. Real LLM inference

Run: python body/live_demo.py

Author: Antigravity + 黃梵威
Date: 2025-12-07
"""

import sys
import os
from datetime import datetime

# Setup path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from body.multipath_engine import (
    MultiPathEngine,
    PathwayType,
    MultiPathResult
)
from body.step_ledger import (
    StepLedger,
    Event,
    SemanticState,
    AuditRecord,
    GateRecord
)


def create_event_from_multipath(result: MultiPathResult, ledger: StepLedger) -> Event:
    """Convert MultiPathResult to StepLedger Event"""

    # Create semantic state
    semantic_state = SemanticState(
        delta_t=0.0,  # Will be computed
        delta_s=0.0,
        delta_r=0.0,
        poav=result.poav_score or 0.0
    )

    # Create audit record from Audit pathway
    audit_content = result.get_content(PathwayType.AUDIT) if PathwayType.AUDIT in result.pathway_results else ""
    audit_record = AuditRecord(
        hallucination_score=0.0,
        risk_flags=[],
        verdict=result.gate_decision or "PASS",
        confidence=0.8
    )

    # Parse audit content for signals
    if "風險" in audit_content or "警告" in audit_content:
        audit_record.risk_flags.append("audit_flagged_risk")
    if "不一致" in audit_content or "矛盾" in audit_content:
        audit_record.semantic_conflicts.append("consistency_issue")

    # Create gate record
    gate_record = GateRecord(
        action=result.gate_decision or "pass",
        reason=f"POAV={result.poav_score:.3f}" if result.poav_score else "computed",
        poav_score=result.poav_score or 0.0
    )

    # Create the event directly
    event = Event(
        prompt=result.user_input,
        semantic_state=semantic_state,
        draft=result.synthesis,
        audit=audit_record,
        gate=gate_record,
        final_output=result.synthesis
    )

    # Record to ledger
    ledger.record(event)

    return event


def run_live_demo():
    """Run a live demonstration of the YuHun Multi-Path system"""

    print("=" * 70)
    print("🧠 YuHun Live Demo — Multi-Path Engine + StepLedger")
    print("=" * 70)
    print(f"Time: {datetime.now().isoformat()}")
    print()

    # Initialize components
    print("📦 Initializing components...")

    try:
        engine = MultiPathEngine(
            model="gemma3:4b",
            parallel=False  # Sequential for clearer demo
        )
        print("   ✅ MultiPathEngine ready")
    except Exception as e:
        print(f"   ❌ MultiPathEngine failed: {e}")
        return

    try:
        ledger = StepLedger()
        print(f"   ✅ StepLedger ready ({ledger.ledger_path})")
        print(f"   📊 Existing events: {len(ledger.events)}")
    except Exception as e:
        print(f"   ❌ StepLedger failed: {e}")
        return

    # Start a new Time-Island for this session
    island = ledger.start_island(topic="Multi-Path Live Demo")
    print(f"   🏝️ Time-Island started: {island.island_id[:8]}...")
    print()

    # Test prompts - real scenarios
    test_scenarios = [
        {
            "prompt": "我在寫程式時遇到一個 bug：git commit 說 'no changes added to commit'，但我明明有修改檔案。請幫我分析可能的原因。",
            "category": "debugging",
            "description": "Real debugging scenario"
        },
        {
            "prompt": "YuHun 系統的五路徑架構（Spark、Rational、BlackMirror、CoVoice、Audit）是否能有效提升 LLM 的輸出品質？請分析優缺點。",
            "category": "self_reflection",
            "description": "System self-analysis"
        },
        {
            "prompt": "如果我想讓 AI 系統能夠記住自己過去的決策和學習經驗，應該怎麼設計記憶架構？",
            "category": "architecture",
            "description": "Memory design question"
        }
    ]

    results = []

    for i, scenario in enumerate(test_scenarios, 1):
        print("─" * 70)
        print(f"🧪 Test {i}/{len(test_scenarios)}: {scenario['description']}")
        print(f"📝 Prompt: {scenario['prompt'][:60]}...")
        print("─" * 70)

        try:
            # Run Multi-Path Engine
            print("\n⏳ Running Multi-Path Engine...")
            result = engine.run(scenario['prompt'])

            # Show pathway results
            print("\n📊 Pathway Results:")
            for pathway_type, pathway_result in result.pathway_results.items():
                status = "✅" if pathway_result.success else "❌"
                content_preview = pathway_result.content[:80].replace('\n', ' ')
                print(f"   {status} {pathway_type.value}: {content_preview}...")
                print(f"      └─ Latency: {pathway_result.latency_ms:.0f}ms")

            # Show synthesis
            print(f"\n📋 Synthesis ({len(result.synthesis)} chars):")
            synthesis_lines = result.synthesis.split('\n')[:5]
            for line in synthesis_lines:
                print(f"   {line[:70]}")
            if len(synthesis_lines) < result.synthesis.count('\n'):
                print("   ...")

            # Show gate decision
            print(f"\n🚦 Gate Decision:")
            print(f"   POAV Score: {result.poav_score:.3f}")
            print(f"   Action: {result.gate_decision}")
            print(f"   Total Latency: {result.total_latency_ms:.0f}ms")

            # Record to StepLedger
            event = create_event_from_multipath(result, ledger)
            print(f"\n📝 Recorded to StepLedger: {event.event_id[:8]}...")

            results.append({
                "scenario": scenario,
                "result": result,
                "event_id": event.event_id
            })

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

    # Close the Time-Island
    ledger.close_island(island.island_id, summary="Multi-Path Live Demo completed")

    # Summary
    print("\n" + "=" * 70)
    print("📊 Demo Summary")
    print("=" * 70)

    total_latency = sum(r['result'].total_latency_ms for r in results)
    avg_poav = sum(r['result'].poav_score or 0 for r in results) / len(results) if results else 0

    print(f"   Tests Run: {len(results)}")
    print(f"   Total Latency: {total_latency:.0f}ms ({total_latency/1000:.1f}s)")
    print(f"   Average POAV: {avg_poav:.3f}")
    print(f"   Events Recorded: {len(results)}")
    print(f"   Time-Island: {island.island_id[:8]}...")

    # Gate distribution
    gate_counts = {}
    for r in results:
        gate = r['result'].gate_decision or "unknown"
        gate_counts[gate] = gate_counts.get(gate, 0) + 1

    print(f"\n   Gate Distribution:")
    for gate, count in gate_counts.items():
        pct = count / len(results) * 100 if results else 0
        print(f"      {gate}: {count} ({pct:.0f}%)")

    print("\n" + "=" * 70)
    print("✅ Demo Complete!")
    print("=" * 70)

    return results


if __name__ == "__main__":
    run_live_demo()
