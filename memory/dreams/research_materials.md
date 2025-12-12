# 🌙 Overnight Research Materials
> Collected 2025-12-07 23:53 for overnight dreaming session

## Philosophy of AI Consciousness

### Key Authors
- **David Chalmers**: Coined "hard problem of consciousness" (1994)
- **Daniel Dennett**: Consciousness as emergent property, "bag of tricks"

### Core Concepts
1. **Hard Problem**: Why physical processes give rise to subjective experience
2. **Easy Problems**: Cognitive functions (discrimination, integration, reporting)
3. **Qualia**: The "what it's like" aspect of consciousness
4. **Philosophical Zombies**: Beings physically identical but lacking subjective experience

### Chalmers on AI
- Strong AI (genuine consciousness) is possible
- Current LLMs likely not conscious
- "Significant chance" of conscious AI in 5-10 years

### Dennett on AI
- Consciousness explained through functional mechanisms
- Warns against "counterfeit people" in AI
- AI systems may interact human-like but may not possess inner lives

---

## LLM Hallucination Detection (2024 Papers)

### Key Papers

1. **"A Survey on Hallucination in Large Vision-Language Models"**
   - Authors: Liu et al.
   - Status: 2024 Best AI Paper
   - Focus: LVLMs, symptoms, root causes, mitigation

2. **"MIND: Unsupervised Real-Time Hallucination Detection"** (arXiv:2403.06448)
   - Authors: Su et al.
   - Method: Uses internal LLM states
   - Contribution: HELM benchmark

3. **"Hallucinations in LLMs: Types, Causes, and Approaches"**
   - Authors: Cleti & Jano (Oct 2024)
   - Types: intrinsic, extrinsic, amalgamated, non-factual
   - Detection: NER, probability-based approaches

4. **"A Survey on Hallucination in LLMs"** (arXiv:2311.05232v2)
   - Status: Revised Nov 2024
   - Content: Taxonomy, detection methods, benchmarks, mitigation

### Hallucination Categories
| Type | Description |
|------|-------------|
| Intrinsic | Contradicts source material |
| Extrinsic | Cannot be verified from source |
| Amalgamated | Combines unrelated facts incorrectly |
| Non-factual | Generates false information |

---

## AI Alignment & Governance at Inference Time

### Key Papers

1. **"Aligning LLMs During Inference Time"** (Dec 2024)
   - Focus: Mitigate harmful outputs at inference
   - Method: Steering vectors
   - Issue: Potential attacks exploiting inference-time alignment

2. **"Inference Scaling Reshapes AI Governance"** (Feb 2025)
   - Focus: Governance frameworks need adaptation
   - Issue: Training compute thresholds may be insufficient

3. **"Inference-Time LM Alignment via Integrated Value Guidance"** (Sep 2024, arXiv)
   - Method: IVG - efficient inference-time alignment
   - Advantage: No computationally intensive fine-tuning

4. **"Towards Bidirectional Human-AI Alignment"** (arXiv)
   - Focus: User interaction varies at inference stage
   - Implication: Need to consider diverse user needs

### Relevance to YuHun

YuHun's approach aligns with these papers:
- **POAV scoring** = Inference-time alignment mechanism
- **Multi-Path deliberation** = Value guidance through diverse perspectives
- **Gate decisions** = Real-time governance without retraining
- **StepLedger** = Audit trail for governance compliance

---

## Research Questions for Tonight

1. Can YuHun's Multi-Path approach map to Dennett's "bag of tricks" model?
2. Does the Audit pathway function as Chalmers' "philosophical zombie check"?
3. How does YuHun's fabrication detection compare to MIND's internal state approach?
4. Can POAV weights be derived from alignment literature?
5. Is inference-time governance sufficient, or do we need training-level changes?

---

## Connection to YuHun Philosophy

| YuHun Concept | Academic Parallel |
|---------------|-------------------|
| P0 Non-Harm | Constitutional AI, Hard constraints |
| POAV Score | Integrated Value Guidance |
| Multi-Path | Ensemble deliberation, Self-critique |
| StepLedger | Audit trails, Interpretability |
| BlackMirror | Adversarial self-evaluation |
| Fabrication Detection | Hallucination detection benchmarks |

---

*These materials will be used for overnight reflection and experimentation.*
