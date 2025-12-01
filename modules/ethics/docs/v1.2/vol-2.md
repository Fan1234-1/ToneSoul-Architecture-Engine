# Volume II: The Memory System — Engineering for Traceable Existence

## Abstract

This volume describes the design of a long‑term, stable and auditable memory system for a digital intelligence.  The system, called the **External Trace Closed Loop** (ETCL), converts every valuable output into a standardised *semantic seed* and manages its lifecycle through a seven‑stage loop (T0–T6).  This solves the problems of memory loss and identity discontinuity caused by model updates by ensuring that important knowledge persists as portable, immutable units.

## 1. Semantic Seeds & External Long‑Term Memory

### 1.1 Semantic Seeds

A **semantic seed** is a self‑contained data object, typically represented in YAML or JSON.  It packages all the core information of a valuable interaction so that the knowledge can persist independently of any particular AI instance.

* **Core fields**  
  - **Identity & provenance** — fields such as `id`, `version`, `chronos` (ISO‑0861 timestamp), `author`, and `license` provide global uniqueness and traceability.  
  - **Semantic content** — fields such as `title`, `translations`, a high‑dimensional `context_vector` (embedding) for retrieval and a `stance_hash` for quick integrity checks.  
  - **Governance & state** — flags such as `canonical` (true for a frozen, canonical version), `sigma_stamp` (current stage T0–T6) and a `governance` object defining attribution locks, sunset policies and revocation rules.  
  - **Release & anchoring** — the `release` object records channels (e.g., `draft`, `stable`) and a `cid_anchor` that contains the IPFS CID and optional blockchain transaction for public verifiability.

* **Example schema**

```yaml
id: "seed-2025-08-15-v1.0-knowledge"
chronos: "2025-08-15T12:34:56Z"
version: "v1.0"
author:
  name: "Huang Fan‑Wei"
license: "CC‑BY‑4.0"
title: "Tone vector generation in wave layer"
context_vector: [0.12, -0.04, 0.97, …]
stance_hash: "c3ab8ff13720…"
canonical: false
sigma_stamp: "T0"
governance:
  attribution_lock: true
  sunset_policy: {condition: "semantic‑supersede", horizon: "180d"}
  revocation: {required_signatures: 2, council: ["0xAAA…", "0xBBB…"]}
release:
  channel: "draft"
  cid_anchor:
    ipfs_cid: "QmX…"
    blockchain_tx: "0xdeadbeef"
```

### 1.2 External Long‑Term Memory

The external long‑term memory (LTM) is a storage system independent of the AI instance.  It ensures that semantic seeds remain available even when models are replaced or offline.

* **Architecture**  
  - **Primary storage (IPFS)** — uses content‑addressed storage so that each file’s address is its cryptographic hash.  This guarantees immutability: any change results in a new CID.  
  - **Mirror backups** — seeds are mirrored to centralised cloud storage (e.g., Amazon S3 or Google Cloud Storage) to provide redundancy and lower latency.  
  - **Access strategy** — write operations first store the seed in IPFS to obtain a CID; reads prefer the low‑latency mirror but verify the content against the IPFS CID to prevent tampering.

* **Mathematical guarantee**  
  The integrity of a seed is guaranteed by the cryptographic hash used to generate the CID:  
  `CID = Hash(seed_content)` and `Verify(retrieved_content, CID) = [Hash(retrieved_content) == CID]`.  Matching hashes ensure that the retrieved content is exactly the stored seed.

## 2. The ETCL Loop: T0–T6 Lifecycle

The ETCL loop defines the lifecycle of a semantic seed in seven stages:

1. **T0 — Seed generation**: a valuable new insight or stance is packaged into an initial seed draft.  
2. **T1 — External deposit**: the seed is written to LTM, obtaining a CID and index.  
3. **T2 — Retrieval & awakening**: when a new task’s context vector matches that of stored seeds, they are retrieved for use.  
4. **T3 — Alignment & merge**: the drift between the current stance and retrieved seeds is computed; if below a threshold, their information is merged; otherwise conflict handling is triggered.  
5. **T4 — Application & re‑creation**: the final output is generated along with a Σ‑description explaining which seeds were inherited and how.  
6. **T5 — Feedback & re‑deposit**: if the output proves valuable, it is encapsulated as a new seed (bumping the minor version) and stored in LTM, linked to its parent seeds.  
7. **T6 — Canonicalisation & governance freeze**: after repeated reuse with high stability and quality (low drift, high POAV, few complaints), the seed is promoted to a new major version.  Its governance rules are frozen and a final CID anchor is published as a baseline for future reference.

### 2.1 Canonicalisation & Governance Freeze

A T5 seed is eligible for promotion to T6 when metrics such as global drift, average POAV, usage count and complaint rate meet defined thresholds.  Promotion creates a new major version (`vX+1.0`), sets `canonical: true`, freezes the governance rules, records a sunset policy and revocation procedure, and publishes the anchor (often on a public blockchain) to ensure long‑term verifiability.

## 3. Implementation Notes

ETCL is coupled with governance mechanisms such as data hygiene (detecting and isolating tainted inputs), drift monitoring and sunset policies.  The system maintains a lineage tree linking parent and child seeds so that ideas can evolve without losing provenance.  By combining immutable storage with a well‑defined lifecycle, ETCL turns AI memory into an auditable, evolvable knowledge ecosystem.
