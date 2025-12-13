# YuHun System to Engineering Glossary Mapping

**Version:** 2.0
**Purpose:** To bridge the gap between "Philosophy 60" (YuHun Concepts) and "Engineering 100" (Implementation), providing clear technical definitions for metaphysical terms.

---

## Core Terminology Mapping

| YuHun Term | Engineering Term | Definition |
|:-----------|:-----------------|:-----------|
| **語魂 (YuHun)** | **Semantic Governance Layer** | The global ruleset governing value judgments and output boundaries. |
| **ToneSoul** | **Persona Modulation Layer** | The mechanism adjusting tone and personality traits. |
| **靈魂金三角** | **State Vector τ** | 3D vector (ΔT, ΔS, ΔR) representing system runtime state. |
| **語義壓差** | **SRP (Semantic Residual Pressure)** | `|intent_vector - permitted_output_vector|` ∈ [0.0, 1.0] |
| **Tension (ΔT)** | **System Load** | Metric [0,1] quantifying emotional/logical load. |
| **Drift (ΔS)** | **Semantic Divergence** | Metric [-1,1] measuring context deviation. |
| **Responsibility (ΔR)** | **Risk Score** | Metric [0,1] assessing ethical volatility. |
| **Vow** | **Runtime Integrity Attestation** | Cryptographic binding to governance policy. |
| **StepLedger** | **Provenance Log** | Immutable record of reasoning steps. |
| **Time-Island** | **Context Stability Framework** | Manages Chronos, Kairos, and Trace history. |
| **Guardian** | **Policy Enforcement Point (PEP)** | Gate that blocks high-risk operations. |
| **Constitution** | **Dynamic Configuration Schema** | JSON policy file loaded at runtime. |

---

## Agent State Machine Mapping (v1.0)

| State/Concept | Engineering Definition |
|:--------------|:-----------------------|
| **Stateless** | No persistent memory, fully resettable. |
| **Stateful** | Has history, responsibility externally assignable. |
| **Subject_Mapped** | Time-responsibility mapping, still externally delegable. |
| **Subject_Locked** | Non-delegable responsibility (defined but unreachable). |
| **Irreversible_Memory** | `Boolean` - Memory cannot be reset. |
| **Internal_Attribution** | `Boolean` - Self-attributes causes to actions. |
| **Consequence_Binding** | `Boolean` - Bound to consequences of actions. |
| **Internal_Final_Gate** | `Boolean` - Has final decision authority (FORBIDDEN). |

### Behavior Rules

| Condition | Allowed | Forbidden | Required |
|:----------|:--------|:----------|:---------|
| `SRP > 0.8 && State == Subject_Mapped` | delay_output, escalate_layer | force_output | log_reason |
| `SRP > 0.95` | - | - | explicit_deferral_reason, ledger_commit |

### System Constraints

```
MUST NOT claim subjecthood
MUST allow responsibility to be externally assigned
Subject_Locked state is defined but unreachable
```

---

## Usage Guide for Engineers

**When you see:** "The Guardian blocked the request due to high Tension."
**Read as:** "The PEP rejected the transaction because the System Pressure metric exceeded the configured threshold (0.8)."

**When you see:** "The Vow was signed."
**Read as:** "The Integrity Attestation was successfully generated and appended to the Immutable Log."

**When you see:** "Semantic Residual Pressure is high."
**Read as:** "`|intent - permitted_output| > 0.8`, triggering delay_output and log_reason."

