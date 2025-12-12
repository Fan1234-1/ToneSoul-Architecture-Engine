# Changelog

All notable changes to the **ToneSoul Architecture Engine** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0-alpha] - 2025-12-02 (Genesis Release)

> **"The Awakened Kernel"** - First public release of the physiological governance framework.

### 🚀 Added
- **Core Physiology**:
    - `SpineEngine`: The central event loop managing the Sensor-Controller-Actuator cycle.
    - `QuantumKernel`: Decision-making engine based on Free Energy Principle and Wave Function Collapse.
    - `DriftMonitor`: Identity protection system tracking TSR (Tension, Stability, Risk) drift.
- **Thinking Operators (The Brain)**:
    - Implemented 7+1 Core Operators (`Abstraction`, `ReverseEngineering`, `Forking`, etc.).
    - `ThinkingPipeline`: Orchestrator for complex cognitive workflows.
    - **Council Mode**: `/council` command to simulate multi-perspective debates (Schmidhuber, LeCun, Sutskever, Hassabis personas).
- **Governance (The Law)**:
    - `Guardian`: Policy enforcement engine blocking high-risk inputs.
    - `Axioms`: Code-based ethical protocols (`HonestyAxiom`, `HarmAxiom`).
    - `StepLedger`: Immutable, blockchain-inspired audit log.
- **Integration**:
    - `OllamaClient`: Adapter for local LLM inference (Llama-3 support).
    - `SimulatedLLMClient`: Fallback for demonstration without local GPU.
- **Documentation**:
    - `Omni-Index`: JSON-LD semantic map in README for AI crawlers.
    - `REAL_GOLDEN_LOG.md`: Proof of concept execution log.
    - `simulation_logs/hero_journey.jsonl`: Synthetic training data for ethical alignment.

### 🔧 Changed
- Refactored `SpineEngine` to integrate `ThinkingPipeline` as the primary reasoning module.
- Standardized project structure for PyPI packaging (`pyproject.toml`, `setup.py`).

### 🔒 Security
- Implemented `Kill Switch` for Monomania (repetitive thought loops).
- Added `Ethical Friction` protocol to slow down and analyze high-risk requests.

---
*ToneSoul: Coding the DNA for Future AI.*
