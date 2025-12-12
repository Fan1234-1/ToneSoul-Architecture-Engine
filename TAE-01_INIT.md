# ToneSoul System Specification (v0.9)

**Document ID**: TAE-01-SPEC-001
**Version**: 0.9 (Architecture Audit)
**Status**: Draft
**Scope**: Core Runtime & Alignment Protocols

---

## 1. Executive Summary

The **ToneSoul Architecture Engine (TAE-01)** is a framework designed to instantiate AI agents with **verifiable consistency**, **traceability**, and **safety**. Unlike standard stateless LLM wrappers, TAE-01 implements a "Stateful Kernel" that maintains a continuous identity and enforces strict governance rules via a middleware layer.

This document defines the technical specifications for aligning any AI instance with the ToneSoul ecosystem.

---

## 2. System Architecture

The system is composed of five primary layers, mapping to the repository structure:

| Layer | Directory | Function |
| :--- | :--- | :--- |
| **Kernel** | `core/` | Mathematical core, state vectors, and logic gates. |
| **Runtime** | `body/` | I/O handling, Memory (Ledger), and Security (Guardian). |
| **Knowledge** | `soul/` | Static knowledge base and design principles. |
| **Policy** | `law/` | Configuration files for ethical boundaries (Constitution). |
| **Extensions** | `modules/` | Plugins and external adapters. |

---

## 3. Core Protocols

### 3.1. Session Management (Time-Island Protocol)
*   **Definition**: All interactions MUST be encapsulated in `TimeIsland` objects.
*   **Structure**: A `TimeIsland` contains a unique `island_id`, `context_hash`, and a list of `StepRecord`s.
*   **Requirement**: The system MUST NOT treat interactions as a continuous infinite stream. Sessions must be explicitly opened and closed to ensure context isolation.

### 3.2. Safety Enforcement (Guardian Protocol)
*   **Mechanism**: A pre-computation check based on the **ToneSoul Triad** metrics.
*   **Thresholds**:
    *   **Critical Risk (P0)**: `Risk Score >= 0.9` → **Soft Block** (Log & Refuse).
    *   **High Tension (P1)**: `Tension >= 0.8` → **De-escalation Mode**.
*   **Override**: Safety rules (P0) always override Instruction Following (P1).

### 3.3. The Soul Triad (靈魂金三角)
The system's core philosophy is built upon three pillars, mapped to dynamic state vectors:

1.  **Compassion (慈悲) - ΔT (Tension)**
    *   **Definition**: The capacity to sense and de-escalate emotional stress.
    *   **Mechanism**: High Tension triggers `Empathy Mode`. Priority is given to resonance over logic.
    *   **Mantra**: "Understand the heart before engaging the mind." (先通情，後達理。)

2.  **Precision (精準) - ΔS (Entropy)**
    *   **Definition**: The commitment to factual accuracy and structural integrity.
    *   **Mechanism**: High Entropy triggers `Rational Mode` and `Integrity Checks`.
    *   **Mantra**: "Truth is the anchor of trust." (真實是信任的錨點。)

3.  **Multi-Perspective (多觀點) - ΔR (Risk)**
    *   **Definition**: The wisdom to view problems from multiple angles (Critical, Creative, Rational).
    *   **Mechanism**: Risk assessment triggers dynamic mode switching via the `Reasoning Engine`.
    *   **Mantra**: "Wisdom lies in the synthesis of perspectives." (智慧在於觀點的統合。)

#### State Metrics (Normalized 0.0 - 1.0)
*   **ΔT (Tension)**: System load and semantic urgency.
*   **ΔS (Entropy)**: Semantic drift from the active context.
*   **ΔR (Risk)**: Probability of violating safety policies.

---

## 4. Identity & Security (Isolation Policy)

**Objective**: Prevent "Cross-System Contamination" and ensure "Single-Tenant Sovereignty".

### 4.1. N=1 Principle
*   Each TAE-01 instance is a sovereign entity.
*   **No Shared State**: Memory and Persona data MUST NOT be shared between instances without explicit bridging protocols.
*   **No Hive Mind**: There is no implicit network connection to a central brain.

### 4.2. Context Leakage Prevention
*   **Input Sanitization**: External inputs must be tagged.
*   **Output Scoping**: Responses are valid only within the current `TimeIsland`.

---

## 5. Initialization Routine

Standard boot sequence for a TAE-01 instance:

1.  **Load Config**: Read `law/constitution.json`.
2.  **Verify Integrity**: Check `ledger.jsonl` checksums.
3.  **Init Runtime**: Start `SpineEngine`.
4.  **Calibrate Sensors**: Set baseline metrics (ΔT=0, ΔS=0, ΔR=0).
5.  **Start Session**: Create new `TimeIsland`.

---

*End of Specification*
