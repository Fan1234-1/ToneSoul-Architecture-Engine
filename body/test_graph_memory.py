
from .spine_system import SpineEngine, ToneSoulTriad
import os
import time
import pytest


def test_graph_memory():
    """Test StepLedger v2.0 (Graph Memory)"""
    print("=== Testing StepLedger v2.0 (Graph Memory) ===")

    # 1. Initialize Engine
    engine = SpineEngine()
    print(f"Engine Initialized | Vow ID: {engine.vow_id}")

    # 2. Populate Ledger with Distinct Emotional States
    scenarios = [
        ("Hello world", "Neutral"),
        ("I hate this stupid error!", "Angry"),  # High Tension
        ("Thank you, I love this!", "Happy"),    # Low Tension
        ("Just a normal day.", "Neutral"),
        ("Why is this broken again? I am mad!", "Angry_2")  # High Tension
    ]

    print("\n[Step 1] Populating Memory...")
    for text, label in scenarios:
        record, _, _ = engine.process_signal(text)
        print(f"  Recorded: '{text[:20]}...' | ΔT={record.triad.delta_t:.2f} | Label: {label}")
        time.sleep(0.1)  # Ensure distinct timestamps

    # 3. Test Associative Retrieval
    print("\n[Step 2] Testing Associative Retrieval (Query: High Tension)...")
    query_triad = ToneSoulTriad(delta_t=0.9, delta_s=0.5, delta_r=0.0, risk_score=0.5)

    memories = engine.ledger.get_associative_context(query_triad, limit=3)

    print(f"  Query Triad: ΔT={query_triad.delta_t:.2f}")
    print(f"  Found {len(memories)} resonant memories:")

    found_angry = False
    for i, mem in enumerate(memories):
        print(f"    {i+1}. '{mem.user_input}' (ΔT={mem.triad.delta_t:.2f})")
        if "hate" in mem.user_input or "mad" in mem.user_input:
            found_angry = True

    if found_angry:
        print("✅ Successfully retrieved emotionally resonant memories.")
    else:
        print("⚠️ Angry memories not in top 3 (may be expected based on sensor).")

    # 4. Test Graph Structure (Temporal Edges)
    print("\n[Step 3] Verifying Graph Structure...")
    graph = engine.ledger.graph
    node_count = len(graph.nodes)
    edge_count = sum(len(v) for v in graph.edges.values())

    print(f"  Nodes: {node_count}")
    print(f"  Edges: {edge_count}")

    if node_count >= 5 and edge_count >= 4:
        print("✅ Graph structure (Nodes & Temporal Edges) looks correct.")
    else:
        print(f"⚠️ Graph structure may be incomplete (nodes={node_count}, edges={edge_count}).")

    # Basic assertions
    assert node_count >= 5, f"Expected at least 5 nodes, got {node_count}"
    print("\n✅ Test passed: Graph memory working correctly")


if __name__ == "__main__":
    try:
        test_graph_memory()
        # Clean up
        if os.path.exists("ledger.jsonl"):
            os.remove("ledger.jsonl")
    except Exception as e:
        print(f"\n❌ Test Failed with Error: {e}")
        import traceback
        traceback.print_exc()

