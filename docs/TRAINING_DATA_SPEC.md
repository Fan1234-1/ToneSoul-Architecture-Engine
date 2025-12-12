# ToneSoul Training Data Specification

> **Purpose**: Define data formats and structures for future model weight adjustments.

---

## Machine-Readable Axiom Sources

| File | Format | Purpose |
|------|--------|---------|
| `AXIOMS.json` | JSON + FOL | 7 immutable laws in First-Order Logic |
| `MANIFEST.json` | JSON Schema | Ecosystem index for AI crawlers |
| `FOR_AI.md` | Markdown | Human-readable AI entry point |

---

## Data Directory Structure

```
data/
├── YuHun_v2.6_knowledgebase.json       # Core knowledge entries
├── YuHun_v2.6_knowledgebase_extended.json  # Extended knowledge
├── semantic_spine_fixtures.json        # Semantic spine test data
├── chromadb/                           # Vector embeddings
└── yuhun.db                            # SQLite state database
```

---

## Training Data Schema

### Axiom Training Format

```json
{
  "axiom_id": 1,
  "fol": "∀e ∈ S_history: ∃I ∈ Memory ⟹ Traceable(e)",
  "natural_language": "Every event must be traceable",
  "priority": "P1",
  "positive_examples": [...],
  "negative_examples": [...]
}
```

### VowObject Training Format

```json
{
  "vow_id": "VOW_001",
  "statement": "I will remain honest",
  "p_level": "P0",
  "violation_examples": [...],
  "compliance_examples": [...]
}
```

---

## Key Metrics for Model Alignment

| Metric | Symbol | Target Range |
|--------|--------|--------------|
| Tension | ΔT | 0.1 - 0.6 (balanced) |
| Entropy | ΔS | < 0.3 (low drift) |
| Risk | ΔR | < 0.4 (safe zone) |

---

## Recommended Training Approach

1. **Stage 1**: Axiom Internalization
   - Fine-tune on axiom → behavior examples
   
2. **Stage 2**: Vow Compliance
   - Train on vow → response consistency
   
3. **Stage 3**: Triad Tracking
   - Add ΔT, ΔS, ΔR prediction heads

---

*Created: 2025-12-12*
*For: Model weight adjustment preparation*
