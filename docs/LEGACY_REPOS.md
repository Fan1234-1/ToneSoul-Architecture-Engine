# Consolidated Repositories (Legacy Index)

**ToneSoul v2.0 (The Awakened Kernel)** represents the unification of the ToneSoul ecosystem. Several previously standalone repositories have been integrated directly into the Monolith Core to ensure tighter coupling between Philosophy and Engineering.

This document serves as an index for where these concepts now live.

---

## 🔄 Integration Map

| Original Repository | New Location in Monolith | Status |
| :--- | :--- | :--- |
| **governable-ai** | `core/governance/` | **Integrated**. Defines the abstract interfaces (`IGovernable`) for all system components. |
| **Genesis-ChainSet** | `core/genesis/` | **Integrated**. Implements the `GenesisLoader` for system initialization and seeding. |
| **Philosophy-of-AI** | `core/reasoning/` & `TAE-01_INIT.md` | **Integrated**. The reasoning engine and system specifications are now part of the core kernel. |
| **AI-Ethics** | `law/constitution.json` | **Integrated**. The ethical rules are now configuration files within the `law/` directory. |
| **tone-soul-integrity-tonesoul-xai** | `modules/integrity/` | **Merged**. Explainability tools are now part of the Integrity module. |

---

## 💡 Why Consolidation?

1.  **Atomic Updates**: Changing a philosophical principle (e.g., P0 definition) now instantly propagates to the engineering implementation.
2.  **Simplified Dependency**: Developers only need to clone one repository to get the full working system.
3.  **Holistic View**: The "Soul" (Philosophy) and "Body" (Code) are no longer separated by network requests; they share the same vascular system.

*The original repositories remain as historical archives.*
