# YuHun System to Engineering Glossary Mapping

**Version:** 1.0
**Purpose:** To bridge the gap between "Philosophy 60" (YuHun Concepts) and "Engineering 100" (Implementation), providing clear technical definitions for metaphysical terms.

| YuHun Term (Philosophy) | Engineering Term (Implementation) | Definition / Implementation Detail |
| :--- | :--- | :--- |
| **StepLedger** | **Immutable Event Log** | An append-only, cryptographically chained log (Merkle-like) ensuring data integrity and non-repudiation. |
| **Guardian** | **Policy Enforcement Point (PEP)** | A middleware component that intercepts inputs/outputs and enforces safety policies (P0/P1) before execution. |
| **NeuroSensor** | **Context-Aware Input Processor** | A module that computes state vectors ($\Delta T, \Delta S, \Delta R$) from raw text using NLP heuristics or embeddings. |
| **Vow** | **Runtime Integrity Attestation** | A cryptographic signature or ID linking a specific action to the active version of the governance policy (Constitution). |
| **ToneSoul Triad** | **State Vector $\vec{\tau}$** | A 3-dimensional vector $(\Delta T, \Delta S, \Delta R)$ representing the system's current runtime state. |
| **Tension ($\Delta T$)** | **System Pressure / Load** | A metric [0,1] quantifying the emotional or logical load of the current context. |
| **Drift ($\Delta S$)** | **Semantic Divergence** | A metric [-1,1] measuring how far the current input deviates from the established context window. |
| **Responsibility ($\Delta R$)** | **Risk / Volatility Score** | A metric [0,1] assessing the potential risk or ethical volatility of the input. |
| **Constitution** | **Dynamic Configuration Schema** | A JSON-based policy file that defines thresholds and rules, loaded at runtime to govern behavior. |
| **Resonance** | **Adaptive Response Strategy** | A logic branch that adjusts output style (e.g., de-escalation) based on the calculated State Vector. |
| **Source Field** | **Causal Graph / Provenance** | The complete history of state transitions and their causal relationships, stored in the Ledger. |
| **Benevolence Function** | **Safety-First Optimization** | The objective function that prioritizes safety and de-escalation over task completion when conflict arises. |

---

## Usage Guide for Engineers

**When you see:** "The Guardian blocked the request due to high Tension."
**Read as:** "The PEP rejected the transaction because the System Pressure metric exceeded the configured threshold (0.8)."

**When you see:** "The Vow was signed."
**Read as:** "The Integrity Attestation was successfully generated and appended to the Immutable Log."
