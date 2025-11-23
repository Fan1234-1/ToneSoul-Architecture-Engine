  to decide when to answer directly and when to invoke guardian mode.
- **Time‑Island Memory** – a memory subsystem that isolates interactions
  into chronological islands, preserving context while preventing
  retroactive tampering.  It stores VowObjects that attach a
  responsibility score to every statement.
- **P0 Guardian Protocol** – a constitutional safety layer that
  intercepts high‑risk outputs.  It embodies the principle that safety
  and ethics (P0) always outrank factual accuracy (P1) and other goals.

## Architecture

At a high level the system flows through three modules:


## Repository Structure

The repository is organized as a monorepo with several layers:

## Repository Structure (The Monolith)

This repository is the **Single Source of Truth** for the ToneSoul ecosystem.

### The Core (Python)
- `core/`: The Main Engine (`ToneSoul_Core_Architecture.py`).
- `body/`: Physiological systems (Ledger, Guardian).
- `simulations/`: Stress tests.

### The Soul (Philosophy & Law)
- `soul/`: **[Migrated]** Contains the complete `Philosophy-of-AI` archives.
- `law/`: **[Migrated]** Contains the `AI-Ethics` constitution and `constitution.json`.

### The Modules (Polyglot Extensions)
- `modules/spine-ts/`: **[Migrated]** The TypeScript implementation of the Spine System (`ai-soul-spine-system`).
- `modules/codex/`: **[Migrated]** The Reference Codex (`tonesoul-codex`).
- `modules/integrity/`: **[Migrated]** The Integrity Protocol (`tone-soul-integrity`).

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+ (for TS modules)
- Make

### Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Full Verification (The Grand Test)**
   This command tests BOTH the Python Engine and the TypeScript Spine.
   ```bash
   make test-all
   ```

3. **Interactive Mode**
   ```bash
   python body/spine_system.py
   ```

## Governance
This repository is legally bound by the **AI-Ethics Constitution**.
- **Source of Truth**: `law/constitution.json` (Derived from `AI-Ethics/tonesoul_config.yaml`)
- **Enforcement**: All commits must pass the `make verify` gate.
