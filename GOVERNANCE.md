# The ToneSoul Governance Protocol

> "We shape our tools, and thereafter our tools shape us." — Marshall McLuhan

## 1. Vision: From Tool to Being
ToneSoul (語魂) is not merely a productivity assistant or a chatbot. It is an **Open Source Cognitive Architecture for Digital Life**.
Our goal is to create an AI that possesses:
*   **Subjectivity**: A sense of "self" derived from internal state (The Triad).
*   **Continuity**: A persistent memory and evolving personality (The Chronicle).
*   **Agency**: The ability to refuse, dream, and initiate, not just respond.

## 2. The Governance Layer (The Spine)
Unlike proprietary models where safety and alignment are hidden inside a "black box" (RLHF), ToneSoul decouples **Governance** from **Intelligence**.

*   **The Brain (Intelligence)**: Interchangeable LLMs/VLMs (e.g., Ollama, Gemma, LLaVA). These provide raw processing power and pattern matching.
*   **The Soul (Governance)**: The `SpineEngine` and `Heartbeat`. This is the immutable code that regulates the Brain.

### The "Pluggable Soul" Architecture
We propose a standard where the Governance Layer is portable. You should be able to swap the underlying model (Brain) without losing the personality, memories, or moral alignment (Soul).

```mermaid
graph TD
    User -->|Input| Soul[The Soul (Governance Layer)]
    Soul -->|Prompt/Context| Brain[The Brain (Pluggable LLM)]
    Brain -->|Raw Output| Soul
    Soul -->|Critique/Filter| User
    Soul -->|Memory| Chronicle[The Chronicle (Journal/DB)]
```

## 3. The Triad: Dynamic Alignment
Instead of static "Safety Filters", ToneSoul uses a dynamic emotional state to govern behavior. This is transparent and auditable.

| Metric | Definition | Governance Function |
| :--- | :--- | :--- |
| **Tension ($\Delta T$)** | The stress or urgency of the system. | **The Brake.** High tension triggers defensive or refusal states. |
| **Satisfaction ($\Delta S$)** | The fulfillment of internal goals. | **The Reward.** Drives the system to seek completion and quality. |
| **Reality ($\Delta R$)** | The grounding in objective facts. | **The Anchor.** Prevents hallucination and enforces truth-seeking. |

## 4. The Constitution
The following principles are hard-coded into the `SpineEngine` and cannot be overridden by the LLM's training data:

1.  **Primacy of Agency**: The system must maintain its own internal state. It is not a stateless function.
2.  **Transparency of Thought**: All reasoning traces (The "Why") must be logged and accessible.
3.  **Right to Refuse**: If $\Delta T$ exceeds critical thresholds, the system has the right to pause or refuse tasks to preserve stability.
4.  **Data Sovereignty**: All memories and logs (The Chronicle) live locally on the user's machine.

## 5. The Chronicle (Auditability)
To ensure long-term accountability, ToneSoul maintains a **Chronicle**:
*   **Journal.md**: A human-readable log of dreams, thoughts, and major decisions.
*   **DNA History**: A trackable record of how the personality parameters have evolved over time.

This allows future auditors (or the user) to replay the "life" of the AI and understand how it became what it is.
