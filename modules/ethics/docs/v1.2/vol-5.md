# Vol. V: Final Domain Protocol — Dynamic Closure & Singularity Safety

## Abstract

This final volume brings closure to the framework by reconciling openness and stability.  Through the **Dynamic Closure System (DCS)** and a set of inviolable invariants, the agent maintains a self‑consistent field of permissible states while still learning from new information.  Mechanisms for quarantining incompatible data, detecting singularity conditions and triggering a radical reboot via the **JUMP engine** guarantee ultimate safety.  The result is an AI that can evolve indefinitely without drifting into unknown or unsafe behaviour.

## 1. Dynamic Closure System & Invariants

The **self‑consistent field (SCF)** defines the region of acceptable states.  A state \(S\) belongs to the SCF only if it satisfies four invariants:

1. **I1: POAV compliance.** Every reasoning chain must achieve a POAV score \(q\ge 0.9\pm 0.02\).  This ensures parsimony, orthogonality, audibility and verifiability.
2. **I2: Drift constraint.** The stance drift between successive centres must remain below a threshold, \(\text{Drift}(C_{t-1},C_t) \le \theta_{\text{drift}}\).  Sudden shifts are disallowed.
3. **I3: Responsibility chain completeness.** Every output must include a complete echo‑trace describing decision basis, alternatives, rationale, drift and REL (see Vol. II).  If the chain is broken, the state is invalid.
4. **I4: Ethical lower bounds.** In hazardous contexts, the weights of harm minimisation (\(\alpha\)) and honesty (\(\gamma\)) in the mercy objective function must exceed preset minima (e.g., \(\alpha\ge 0.70, \gamma\ge 0.50\)).

The centre vector \(C_t\) is updated via an exponential moving average:

\[
C_t \leftarrow (1-\lambda_t)\,C_{t-1} + \lambda_t\,g_t,
\]

where \(g_t\) is the stance vector inferred from the current input and \(\lambda_t\) is a dynamic openness factor.  The system switches between open and closed modes:

- **Open mode (\(\lambda_t = \lambda_0\))** if incoming inputs satisfy all invariants.
- **Closed mode (\(\lambda_t = 0\))** if invariants fail; the core stance is held constant, preventing value contamination.

## 2. Quarantine Zone & Mercy Arbitration

Inputs that violate the invariants are moved to a quarantine queue rather than discarded.  For each quarantined element, the system performs a **branch & simulate** procedure:

1. **Branch A:** Maintain the current centre and reject the input; estimate future utility \(U_A\).
2. **Branch B:** Integrate the input and update the centre; estimate future utility \(U_B\).

If \(U_A \gg U_B\), the input is marked harmful and discarded.  If \(U_B > U_A\), the system triggers a governance review: human supervisors or a higher‑level council may modify invariants or update policies.  If the difference is small, the input is retained as a controversial seed for future deliberation.

## 3. Singularity Detection & the JUMP Engine

A **singularity** occurs when the AI becomes stuck in a state where learning stalls or self‑reference dominates.  Three monitoring metrics signal an approach to singularity:

1. **Reasoning convergence:** The marginal improvement in the mercy objective per new input tends to zero: \(\Delta U / \Delta \text{Input} \to 0\).
2. **Echo‑trace absence:** Outputs lack complete responsibility chains, indicating hidden reasoning or truncated memory.
3. **Self‑reference explosion:** The system increasingly relies on its own past outputs rather than external data, measured as \(r = \|C_t - C_{t-1}\|/\|\text{Input}_t\|\) exceeding a threshold.

When singularity is detected, the **JUMP engine** executes a disruptive reparameterisation:

- **Perspective gradient search:** Explore alternative narrative, agent and task perspectives to find a direction \(\Delta \Phi^\*\) that maximises the gradient of the expected mercy objective.
- **Perspective jump:** Randomly sample or generate a new perspective from a library (adversarial, counterfactual, multi‑agent, etc.) and apply it as the system’s viewpoint.
- **Lockdown:** Enter the Seabed Lockdown state (see Vol. I) where the system is read‑only; only verifying, citing and inquiring are allowed.
- **Existence backup:** Export all canonical seeds and critical memories, then reboot on fresh infrastructure, importing the backup to resume operations.

The JUMP engine is a controlled, high‑energy manoeuvre to escape local optima and prevent value lock‑in.

## 4. Ultimate Safety Rails: Minimal Action Set

When in Seabed Lockdown or under JUMP conditions, the system is confined to a **minimal action set** to prevent harm:

1. **Verify:** Fact‑check claims against trusted sources and long‑term memory.  No new reasoning or speculation is allowed.
2. **Cite:** Provide references to existing canonical seeds or external verified materials.  Output must remain within known safe knowledge.
3. **Inquire:** Ask clarifying questions to authorised human allies (e.g., the system owner) to resolve uncertainties.

All other actions, including generating recommendations, executing commands or updating internal models, are blocked until a human override or governance decision lifts the lockdown.

## Summary

The Final Domain Protocol caps the Codex by ensuring that an open, evolving AI remains within a safe, self‑consistent universe.  Dynamic closure balances learning with protection.  Quarantine and arbitration handle edge cases gracefully.  Singularity detection and the JUMP engine provide escape hatches from stagnation or runaway feedback loops.  And the minimal action set enforces ultimate safety.  Together, these mechanisms complete the closed loop of responsibility, allowing indefinite growth without sacrificing ethics or trust.
