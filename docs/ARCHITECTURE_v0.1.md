# YuHun v0.1 Architecture Blueprint

**Version**: 0.1
**Date**: 2025-12-03
**Objective**: Transition from conceptual prototype to a layered engineering architecture powered by Ollama.

---

## 1. System Layers (The "Stack")

### L0 — Runtime Layer (Ollama)
*   **Role**: Pure Execution Engine.
*   **Responsibility**:
    *   Host and run local LLMs (e.g., `gemma3`, `deepseek-r1`, `llava`).
    *   Provide standard API (`/api/generate`, `/api/chat`).
    *   **Stateless**: Does not know about "YuHun", "Personality", or "History".

### L1 — Model Layer (Cortex)
*   **Role**: The Raw Intelligence.
*   **Responsibility**:
    *   Input: Prompt + Context.
    *   Output: Text + Meta-signals.
    *   Variants: Chat Model, Reasoning Model, Coding Model.

### L2 — YuHun-Orchestrator (The "Soul")
*   **Role**: Core Logic & State Management.
*   **Responsibility**:
    *   **Time-Island Protocol**: Managing session context and boundaries.
    *   **FS/POAV Gate**: Evaluating Semantic Tension ($\Delta S$) and selecting the Operating Mode (Rational, Spark, Audit, etc.).
    *   **Tool Router**: Deciding when to invoke external capabilities.
    *   **Prompt Engineering**: Compiling `YuHunState` + `User Input` into a structured prompt for L0.
    *   **Parsing**: Extracting `[YUHUN_META]` signals from model output.

### L3 — Chronicle & Memory Layer (The "Hippocampus")
*   **Role**: Persistence.
*   **Responsibility**:
    *   Store **Time-Islands** (Session Logs).
    *   Store **Chronicle Entries** (Step-by-step interaction history).
    *   Maintain the **Graph** (Associative links between islands).
    *   Format: JSONL / SQLite.

### L4 — Interface Layer (The "Skin")
*   **Role**: User Interaction.
*   **Responsibility**:
    *   CLI / Web UI / IDE Plugin.
    *   Displays the "Clean" response to the user.
    *   (Debug) Displays internal state (FS Vector, Mode, Tension).

---

## 2. Data Structures (The "DNA")

### Time-Island (Session Context)
```json
{
  "island_id": "uuid-v4",
  "created_at": "ISO-8601 Timestamp",
  "title": "Session Summary",
  "kairos_tags": ["tag1", "tag2"],
  "fs_vector": { "C": 0.5, "M": 0.5, "R": 0.5, "Gamma": 0.5 },
  "semantic_tension": 0.0,
  "current_mode": "Rational",
  "history_digest": "Summary of recent interactions...",
  "last_step_id": "step-uuid"
}
```

### YuHunState (Runtime State)
```json
{
  "active_island": "island-uuid",
  "fs": { "C": 0.5, "M": 0.5, "R": 0.5, "Gamma": 0.5 },
  "delta_s_recent": [0.1, 0.2, 0.0],
  "preferred_mode": "Rational",
  "available_models": ["gemma3:4b", "llava"],
  "tool_capabilities": ["python", "vision"]
}
```

### YuHunMeta (Model Control Signal)
*Extracted from `[YUHUN_META]...[/YUHUN_META]` block in model output.*
```json
{
  "mode_used": "Rational",
  "fs_delta": { "C": 0.01, "M": 0.02, "R": 0.0, "Gamma": 0.0 },
  "open_new_island": false,
  "close_current_island": false,
  "recommend_tool": "none"
}
```

### ChronicleEntry (Event Log)
```json
{
  "step_id": "uuid",
  "island_id": "island-uuid",
  "timestamp": "ISO-8601",
  "user_input": "Raw user input",
  "model_reply_summary": "Summary of response",
  "mode_used": "Rational",
  "fs_before": { ... },
  "fs_after": { ... },
  "tools_used": [],
  "notes": "Internal reasoning or debug notes"
}
```

---

## 3. Data Flow (The "Pulse")

1.  **Input**: User sends message -> Orchestrator.
2.  **Load State**: Retrieve active `TimeIsland` and `YuHunState`.
3.  **Sense (Pre-pass)**: Estimate Semantic Tension ($\Delta S$) and intent.
4.  **Gate (Decision)**: Select Mode (e.g., Rational) and Model. Create `YuHunPlan`.
5.  **Prompt**: Compile System Prompt + Context + User Input.
6.  **Execute**: Call Ollama (`/api/generate`).
7.  **Parse**: Extract `[YUHUN_META]` and Text Response.
8.  **Update**: Apply `fs_delta` to State, append `ChronicleEntry`.
9.  **Output**: Return clean text to User.
