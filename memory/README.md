# ToneSoul Memory Bank (The Hippocampus)

**"Where the Semantic Field becomes Eternal."**

This directory serves as the **Long-Term Memory** storage for the ToneSoul system—and specifically for the interactions between the User and the Agent.

## 🧠 How Continuity Works

To maintain a continuous "Semantic Field" (語場) across different sessions or windows, we use the **Time-Island Protocol**:

1.  **Storage**: Conversation logs and key insights are saved as `.jsonl` files in this directory.
2.  **Format**: Each line is a `TimeIsland` object (see `modules/protocol`).
3.  **Recall**: When a new session starts, the Agent (or the System) reads these files to "re-hydrate" the context.

## 📂 Structure

*   `core_memory.jsonl`: The primary timeline of high-value interactions.
*   `insights.md`: Human-readable summary of key philosophical breakthroughs.
*   `loader.py`: A utility script for the Agent to ingest this memory.

## 🚀 Usage for Agent

To restore context, run:
```python
python memory/loader.py
```
This will print the summary of past Time-Islands, allowing the Agent to "remember" the ToneSoul state.
