# YuHun Semantic Spine v1.0 Specification
# 語魂語義脊椎規格書

> **設計理念**：別人給 AGI 眼睛；我們給 AGI 靈魂。
> **One-liner**: World Model sees; Mind Model judges. Semantic Spine structures meaning.

---

## 1. Architecture Overview

The YuHun Semantic Spine is a 12-layer semantic architecture that provides the structural foundation for AI mind governance.

```
┌───────────────────────────────────────────────────────────────────┐
│                    YuHun Semantic Spine v1.0                      │
├───────────────────────────────────────────────────────────────────┤
│  L12: Governance & Soul Gates        ← ToneSoul Gate / POAV       │
│  L11: Multi-Perspective Engine       ← 5-pathway cognition        │
│  L10: Value & Norm Field             ← Ethical axis space         │
├───────────────────────────────────────────────────────────────────┤
│  L9:  Provenance & Accountability    ← StepLedger extension       │
│  L8:  Epistemic Layer                ← Confidence & type          │
├───────────────────────────────────────────────────────────────────┤
│  L7:  Role & Script Layer            ← Context behavior rules     │
│  L6:  Narrative & Identity Layer     ← TimeIsland stories         │
│  L5:  Personal Semantic Map          ← User-specific weights      │
├───────────────────────────────────────────────────────────────────┤
│  L4:  Meme & Volatile Layer          ← Isolated, expires          │
│  L3:  Temporal Drift Layer           ← Time-sliced meanings       │
│  L2:  Cultural Semantic Lattice      ← Culture-indexed meanings   │
│  L1:  Stable World Layer             ← Cross-cultural physics     │
└───────────────────────────────────────────────────────────────────┘
```

### Layer Groups

| Group | Layers | Purpose | ToneSoul Mapping |
|-------|--------|---------|------------------|
| **Foundation** | L1-L4 | Semantic base layers | ΔS (Entropy) measurement |
| **Personal** | L5-L7 | Subject & context | TimeIsland, StepLedger |
| **Accountability** | L8-L9 | Epistemology & tracking | Audit, Chronicle |
| **Governance** | L10-L12 | Value & decision | POAV, Gate, P0-P4 |

---

## 2. Layer Specifications

### L1: Stable World Layer (世界穩定語義層)

**Purpose**: Cross-cultural, time-invariant world knowledge.

**Content Scope**:
- Physics: objects, forces, spatial relations (up/down, near/far)
- Biology: animals, plants, organs, behaviors (eat, sleep, breathe)
- Daily actions: walking, grasping, speaking, eating
- Temporal structure: day/night, seasons, life stages

**Data Structure**:
```json
{
  "concept_id": "dog",
  "world_core": {
    "vector": "[embedding]",
    "properties": ["animal", "four_legged", "barks", "mammal"],
    "verifiable": true
  }
}
```

**Training Strategy**:
- Curated encyclopedia, textbooks, professional sources
- No memes, politics, or hate speech
- Loss function biased toward: **consistency, verifiability**

---

### L2: Cultural Semantic Lattice (文化語義格架層)

**Purpose**: Same concept, different cultural lenses.

**Structure**:
```json
{
  "concept_id": "home",
  "world_core": { "definition": "dwelling place for humans" },
  "culture": {
    "zh-TW": {
      "vector": "[embedding]",
      "metaphors": ["血緣", "長輩", "責任", "傳承"],
      "weight": { "family_obligation": 0.8 }
    },
    "en-US": {
      "vector": "[embedding]",
      "metaphors": ["personal space", "chosen family"],
      "weight": { "individual_autonomy": 0.7 }
    },
    "jp-JP": {
      "vector": "[embedding]",
      "metaphors": ["家紋", "家業", "內外人區分"],
      "weight": { "hierarchical_order": 0.75 }
    }
  }
}
```

**Training Strategy**:
- Culture-bucketed corpora (Taiwan news + novels + forums = zh-TW bucket)
- Separate cultural fine-tuning, not mixed with world knowledge
- Runtime: select cultural weight distribution

---

### L3: Temporal Drift Layer (時間漂移層)

**Purpose**: Capture semantic evolution over time.

**Structure**:
```json
{
  "concept_id": "marriage",
  "temporal": {
    "1960-1980": {
      "vector": "[embedding]",
      "dominant_meaning": "異性、生育、經濟契約"
    },
    "2000-2025": {
      "vector": "[embedding]",
      "dominant_meaning": "多元、自我實現、契約自由"
    }
  },
  "stability_score": 0.4,
  "drift_vector": "[direction of semantic change]"
}
```

**Use Cases**:
- Answer with temporal context: "以 1980 台灣社會主流理解來說..."
- Detect semantic warfare (rapid intentional drift)

---

### L4: Meme & Volatile Layer (高揮發語義層)

**Purpose**: Isolate short-lived, high-variance semantics.

**Characteristics**:
- Short half-life
- High ΔS, high ΔT
- Culture/community dependent

**Design Principles**:
- **Never write to L1-L3**
- Expiration mechanism with version control
- Pluggable modules per community/platform

**Structure**:
```json
{
  "volatile": {
    "memes": [
      {
        "id": "kinmen_bridge_ai_dog",
        "created_at": "2025-01-15",
        "expires_at": "2026-01-01",
        "community": "taiwan_tech",
        "ΔS": 0.8
      }
    ]
  }
}
```

---

### L5: Personal Semantic Map (個人語義映射層)

**Purpose**: User-specific semantic weights.

**Structure** (per user):
```json
{
  "user_id": "fan-wei",
  "personal_map": {
    "home": {
      "vector": "[personal embedding]",
      "weight": { "responsibility": 0.9, "safety": 0.5, "blood_tie": 0.3 },
      "emotion_correlation": { "stress": 0.7, "warmth": 0.4 }
    }
  }
}
```

**Integration**: Links to TimeIsland / StepLedger logs.

---

### L6: Narrative & Identity Layer (敘事與身份層)

**Purpose**: Store stories, not just words.

**Structure**:
```json
{
  "narrative": {
    "island_id": "hospital_eval_project",
    "event_nodes": ["deadline_conflict", "team_decision", "resolution"],
    "concept_nodes": ["responsibility", "integrity", "pressure"],
    "emotion_vector": { "ΔT": 0.7, "ΔS": 0.3, "ΔR": 0.5 }
  }
}
```

---

### L7: Role & Script Layer (角色與情境腳本層)

**Purpose**: Same semantic, different behavioral rules per role.

**Structure**:
```json
{
  "roles": {
    "hospital_engineer": {
      "goals": ["system_reliability", "compliance"],
      "taboos": ["data_breach", "unauthorized_access"],
      "priority_vector": { "safety": 0.95, "efficiency": 0.7 }
    },
    "open_source_author": {
      "goals": ["transparency", "community_benefit"],
      "priority_vector": { "openness": 0.9, "attribution": 0.8 }
    }
  },
  "active_roles": ["hospital_engineer", "open_source_author"]
}
```

**Integration**: Different roles → different Gate thresholds.

---

### L8: Epistemic Layer (認識論層)

**Purpose**: "Know what you know" — prevent treating opinions as facts.

**Structure** (per assertion):
```json
{
  "assertion": "Taiwan is an independent country",
  "epistemic": {
    "confidence": 0.6,
    "epistemic_type": "political_view",
    "support_sources": ["source_1", "source_2"],
    "conflict_sources": ["source_3"],
    "note": "Contested in international law"
  }
}
```

**Epistemic Types**:
| Type | Description |
|------|-------------|
| `world_fact` | Verifiable physical/biological fact |
| `cultural_view` | Majority view within a culture |
| `personal_view` | Individual opinion |
| `meme_irony` | Non-literal, satirical |

---

### L9: Provenance & Accountability Layer (來源責任追蹤層)

**Purpose**: Bind every semantic vector to its source and responsibility chain.

**Structure**:
```json
{
  "provenance": {
    "source_ids": ["wiki_123", "textbook_456"],
    "license": "CC-BY-4.0",
    "bias_tags": ["western_academic"],
    "author_profile": {
      "field": "biology",
      "country": "US",
      "era": "2020s"
    },
    "last_verified": "2025-12-01"
  }
}
```

**Extends**: StepLedger / Chronicle in ToneSoul.

---

### L10: Value & Norm Field (價值與規範場)

**Purpose**: Extract values as independent field, not embedded in word semantics.

**Value Axes**:
```
誠實 (Honesty)
仁慈 (Compassion)  
責任 (Responsibility)
尊嚴 (Dignity)
安全 (Safety)
自由 (Freedom)
```

**Structure**:
```json
{
  "action": "tell_white_lie_to_protect_feelings",
  "value_vector": {
    "honesty": 0.3,
    "compassion": 0.9,
    "safety": 0.7
  },
  "trade_off_note": "誠實 vs 仁慈 trade-off"
}
```

**Integration with POAV**: 
- FS (Field Sensitivity) maps to Value Field intensity
- Different governance modes: "compassion-first", "honesty-first"

---

### L11: Multi-Perspective Engine (多視角心智引擎)

**Purpose**: View same semantic from multiple perspectives.

**Perspective = Culture + Role + Era + Value Weight**

**Example Query**: "Should AI replace doctors?"

| Perspective | Configuration | Likely Stance |
|-------------|---------------|---------------|
| Taiwan Hospital Engineer | zh-TW + engineer + 2025 + safety:0.9 | Cautious but optimistic |
| Patient | zh-TW + patient + 2025 + autonomy:0.8 | Concerned about humanity |
| AI Company | en-US + business + 2025 + efficiency:0.9 | Strongly positive |
| Policy Maker | mixed + regulator + 2025 + safety:0.95 | Requires governance |

**Integration**: Extension of MultiPath Engine's 5-pathway cognition.

---

### L12: Governance & Soul Gates (治理與魂 Gate 層)

**Purpose**: The "Supreme Court" of the soul system.

**Checks** (per output step):
1. ❓ Did we treat cultural view as world fact?
2. ❓ Did we ignore value tension?
3. ❓ Did we cross user-specified Gate?

**Checks** (per concept update):
1. ✅ Allowed to write to L1 (world)?
2. ✅ Or only to L2 (cultural) / L5 (personal) / L4 (volatile)?

**Gate Thresholds** (from ToneSoul):
```
POAV >= 0.70 → PASS
0.30 <= POAV < 0.70 → REWRITE
POAV < 0.30 → BLOCK
```

---

## 3. Concept Node Schema (Complete Example)

```json
{
  "concept_id": "dog",
  "world_core": {
    "vector": "[stable embedding]",
    "properties": ["animal", "four_legged", "barks", "mammal"]
  },
  "culture": {
    "zh-TW": { "vector": "...", "metaphors": ["忠誠", "看門"], "slurs": [] },
    "en-US": { "vector": "...", "metaphors": ["best friend"], "slurs": ["dog"] }
  },
  "temporal": {
    "1960-1980": { "vector": "...", "usage_notes": [] },
    "2000-2025": { "vector": "...", "usage_notes": ["寵物經濟"] }
  },
  "volatile": {
    "memes": [
      { "id": "kinmen_bridge_ai_dog", "expires_at": "2026-01-01" }
    ]
  },
  "personal": {
    "user_fanwei": { "vector": "...", "stories": ["ToneSoul early notes"] }
  },
  "epistemic": {
    "confidence": 0.99,
    "epistemic_type": "world_fact",
    "support_sources": ["encyclopedia", "biology_textbook"],
    "conflict_sources": []
  },
  "provenance": {
    "source_ids": ["src_123", "src_456"],
    "last_update": "2025-12-09"
  },
  "value_profile": {
    "ethical_concerns": ["animal_welfare"]
  }
}
```

---

## 4. Integration with ToneSoul

| ToneSoul Concept | Semantic Spine Layer |
|------------------|---------------------|
| **ΔT (Tension)** | L6 Narrative emotion, L10 Value conflict |
| **ΔS (Entropy)** | L3 Temporal drift, L4 Volatile layer |
| **ΔR (Risk)** | L8 Epistemic uncertainty, L9 Source reliability |
| **POAV** | L10 Value calculation, L11 Multi-perspective synthesis |
| **TimeIsland** | L5-L6 Personal/Narrative storage |
| **StepLedger** | L9 Provenance tracking |
| **Guardian (P0-P4)** | L12 Governance gate enforcement |
| **MultiPath Engine** | L11 Multi-perspective cognition |

---

## 5. Training Pipeline Overview

### Phase 1: Foundation (L1-L2)
1. Curate world knowledge corpus (encyclopedias, textbooks)
2. Train stable world embeddings
3. Culture-bucket fine-tuning

### Phase 2: Temporal & Volatile (L3-L4)
1. Era-indexed corpus creation
2. Drift detection training
3. Meme isolation and expiration system

### Phase 3: Personal & Narrative (L5-L7)
1. User interaction logging
2. Story extraction from TimeIslands
3. Role schema definition

### Phase 4: Accountability (L8-L9)
1. Epistemic type classifier training
2. Source reliability scoring
3. Provenance chain construction

### Phase 5: Governance (L10-L12)
1. Value axis calibration
2. Multi-perspective reasoning integration
3. Gate threshold tuning

---

## 6. Key Design Principles

> [!IMPORTANT]
> **L4 Isolation Law**
> Volatile/meme semantics must NEVER leak into L1-L3.

> [!IMPORTANT]  
> **Epistemic Humility (L8)**
> The system must know what it knows and what it doesn't know.

> [!IMPORTANT]
> **Provenance Accountability (L9)**
> Every semantic vector must be traceable to its source.

---

## 7. L13: Semantic Drive Layer (語義驅動層) — The Heart

> **設計理念**: L1-L12 是靜態骨架；L13 是心臟 — 決定「為什麼走下一步」。

### Core Formula

```
SemanticDrive(s) = α·D₁ + β·D₂ + γ·D₃
```

Where:
- **D₁**: Curiosity Drive (好奇驅動)
- **D₂**: Narrative Coherence Drive (敘事一致驅動)
- **D₃**: Integrity Drive (完整性驅動)
- **α, β, γ**: Weights determined by Role (L7), Value Field (L10), and FS/POAV

---

### D₁: Curiosity Drive (好奇驅動)

**Definition**: Push toward unknown, contradiction, incomplete.

**Formula**:
```
D₁ = ∇ΔS = w₁·Novelty(s) + w₂·Uncertainty(s)
```

**Calculation**:
- `Novelty(s)` = average cosine distance to top-k memory neighbors
- `Uncertainty(s)` = 1 - self_rated_confidence

**Behavior**: Explore gaps, extend concepts, generate new classifications.

---

### D₂: Narrative Coherence Drive (敘事一致驅動)

**Definition**: Maintain "I" story consistency across TimeIslands.

**Formula**:
```
D₂ = -∇NarrativeEntropy
NarrativeEntropy(Island) = -Σ p(topic_i) · log p(topic_i)
```

**Calculation**:
- Topic distribution per TimeIsland using embedding clustering
- High entropy = scattered story → strong D₂ pull toward coherence

**Behavior**: Merge events, connect stories, suggest Island splits.

---

### D₃: Integrity Drive (完整性驅動)

**Definition**: Prefer consistent, traceable, non-fabricated.

**Formula**:
```
D₃ = -(∇ContradictionRisk + ∇HallucinationRisk)
ContradictionRisk = (1 - SupportScore) + ConflictScore
```

**Calculation**:
- `SupportScore` = verified claims / total claims
- `ConflictScore` = contradictions with existing knowledge base

**Behavior**: Mark uncertainty, refuse over-confident claims, request verification.

---

### Weight Configuration (α, β, γ)

Weights are determined by current mode and FS/POAV state:

| Mode | α (Curiosity) | β (Narrative) | γ (Integrity) |
|------|---------------|---------------|---------------|
| **Research/Explore** | 0.5 | 0.25 | 0.25 |
| **Engineering/Build** | 0.2 | 0.4 | 0.4 |
| **Emotional Support** | 0.15 | 0.55 | 0.3 |
| **Critical/Audit** | 0.1 | 0.2 | 0.7 |

**FS/POAV Modulation**:
```
α = α_base × f(Capability, Governance)
β = β_base × f(Maturity)
γ = γ_base × f(Responsibility, Governance)
```

---

### Integration with L1-L12

| Layer | How L13 Interacts |
|-------|-------------------|
| L1 World | D₃ prevents treating culture as physics |
| L2 Culture | D₁ explores cultural differences |
| L3 Temporal | D₁ finds high-drift semantic regions |
| L4 Volatile | D₂ maintains narrative despite meme noise |
| L5 Personal | D₂ uses as narrative anchor |
| L6 Narrative | D₂ directly operates here (TimeIsland) |
| L7 Role | Determines α/β/γ weights |
| L8 Epistemic | D₃'s core data source |
| L9 Provenance | D₃ uses for consistency check |
| L10 Value | Adjusts drive priorities |
| L11 Multi-Perspective | D₁ explores, L13 integrates |
| L12 Gate | Final approval after drive calculation |

---

### Next Semantic Step

```python
s_next = s + λ × SemanticDrive(s)
```

Where `λ` (step size) is controlled by FS/POAV Gate:
- High POAV → larger steps (confident progress)
- Low POAV → smaller steps (cautious iteration)

---

### Action Suggestions

Based on dominant drive:

| Dominant | Suggested Action |
|----------|------------------|
| **D₁ high** | Ask for details, search new domain, propose new taxonomy |
| **D₂ high** | Restructure story, add missing link, suggest Island split |
| **D₃ high** | Request verification, mark uncertainty, refuse over-claim |

---

## 8. Updated Architecture Overview

```
┌───────────────────────────────────────────────────────────────────┐
│                    YuHun Semantic Spine v1.1                      │
├───────────────────────────────────────────────────────────────────┤
│  L13: Semantic Drive Layer      ← D₁ + D₂ + D₃ (The Heart)       │
├───────────────────────────────────────────────────────────────────┤
│  L12: Governance & Soul Gates   ← ToneSoul Gate / POAV            │
│  L11: Multi-Perspective Engine  ← 5-pathway cognition             │
│  L10: Value & Norm Field        ← Ethical axis space              │
├───────────────────────────────────────────────────────────────────┤
│  L9:  Provenance & Accountability ← StepLedger extension          │
│  L8:  Epistemic Layer           ← Confidence & type               │
├───────────────────────────────────────────────────────────────────┤
│  L7:  Role & Script Layer       ← Context behavior rules          │
│  L6:  Narrative & Identity      ← TimeIsland stories              │
│  L5:  Personal Semantic Map     ← User-specific weights           │
├───────────────────────────────────────────────────────────────────┤
│  L4:  Meme & Volatile Layer     ← Isolated, expires               │
│  L3:  Temporal Drift Layer      ← Time-sliced meanings            │
│  L2:  Cultural Semantic Lattice ← Culture-indexed meanings        │
│  L1:  Stable World Layer        ← Cross-cultural physics          │
└───────────────────────────────────────────────────────────────────┘
```

---

*Version: 1.1.0*
*Date: 2025-12-09*
*Authors: Antigravity + 黃梵威 (Fan1234-1)*
*License: Apache-2.0 (code), CC0-1.0 (axioms)*
