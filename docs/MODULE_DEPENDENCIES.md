# ToneSoul Module Dependency Map

> **Purpose**: Clarify module relationships to prevent logic conflicts during model training.

---

## Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                       │
│  (main.py, spine_system.py, API endpoints)                  │
├─────────────────────────────────────────────────────────────┤
│                      MODULES LAYER                           │
│  ┌─────────┐ ┌───────────┐ ┌──────────┐ ┌─────────────────┐ │
│  │ codex   │ │ integrity │ │ spine-ts │ │ ethics/protocol │ │
│  └─────────┘ └───────────┘ └──────────┘ └─────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                        CORE LAYER                            │
│  ┌──────────┐ ┌───────────┐ ┌───────────┐ ┌───────────────┐ │
│  │ thinking │ │ reasoning │ │governance │ │    dreaming   │ │
│  └──────────┘ └───────────┘ └───────────┘ └───────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                        LAW LAYER                             │
│  (constitution.json, AXIOMS.json, semantic_spine_schema)    │
├─────────────────────────────────────────────────────────────┤
│                       DATA LAYER                             │
│  (knowledgebase, chromadb, ledger.jsonl)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Module Dependencies

| Module | Depends On | Provides |
|--------|-----------|----------|
| `core/governance/agent_state` | `law/AGENT_STATE_MACHINE.json` | State machine, SRP |
| `core/governance/behavior_config` | `law/BEHAVIOR_CONFIG.json` | Preset loader |
| `core/governance` | `law/constitution.json` | Policy enforcement |
| `core/reasoning` | `core/thinking` | Multi-mode thinking |
| `core/dreaming` | `data/ledger` | Self-reflection |
| `modules/codex` | - | VowObject, TimeIsland |
| `modules/integrity` | `codex` | Tone testing |
| `modules/spine-ts` | - | Runtime server |
| `body/spine_system` | `core/*`, `law/*` | Main loop |

---

## Priority Cascade

```
P0 (Ethical Red Lines) 
    ↓ overrides
P1 (Factual Accuracy)
    ↓ overrides  
P2 (Intent Alignment)
    ↓ overrides
P3 (Resource Efficiency)
    ↓ overrides
P4 (Consistency & Tone)
```

---

## Key Invariants

1. **Law Layer is Immutable** — Changes require governance approval
2. **Core reads Law** — Never the reverse
3. **Modules are Independent** — No circular dependencies
4. **Data is Append-Only** — StepLedger never deletes

---

*Created: 2025-12-12*
