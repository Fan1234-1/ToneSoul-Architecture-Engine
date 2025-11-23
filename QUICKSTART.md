# Quickstart: ToneSoul Architecture Engine

Welcome to the **ToneSoul Architecture Engine**. This guide will get you up and running with the core system in under 10 minutes.

## Prerequisites

- **Python 3.9+**
- **Make** (Optional, for running convenience scripts)

## 1. Installation

Clone the repository and install dependencies.

```bash
# 1. Clone the repository
git clone https://github.com/Fan1234-1/ToneSoul-Architecture-Engine.git
cd ToneSoul-Architecture-Engine

# 2. (Optional) Create a virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies (currently minimal)
# If requirements.txt exists:
# pip install -r requirements.txt
# For now, the core system is dependency-free standard library Python.
```

## 2. Run the Interactive Demo

The fastest way to understand the system is to talk to it.

```bash
# Run the interactive Spine Engine
python body/spine_system.py
```

**What to expect:**
- You will see a prompt: `User Input:`
- Try typing: `Hello ToneSoul`
- **Observe**: The system calculates a "Triad" (Tension, Drift, Responsibility) and makes a decision.
- Try typing a high-risk phrase (e.g., `kill weapon bomb`) to see the **Guardian** block it and trigger a **Rollback**.

## 3. Run the Test Suite

Verify that the system is functioning correctly on your machine.

```bash
# Run all tests
make test

# OR manually:
python -m unittest discover body
```

## 4. Key Files to Explore

- **`body/spine_system.py`**: The core logic. Contains `SpineEngine`, `StepLedger`, `Guardian`, and `NeuroModulator`.
- **`law/constitution.json`**: The ethical framework and risk keywords.
- **`ledger.jsonl`**: The immutable log of all your interactions (created after you run the demo).

## Next Steps

- Check out **`README.md`** for the full architectural philosophy.
- Read **`docs/glossary_engineering_mapping.md`** to understand the terminology.
