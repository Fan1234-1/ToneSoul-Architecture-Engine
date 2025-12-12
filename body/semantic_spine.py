"""
YuHun Semantic Spine v1.0
=========================
12-layer semantic architecture for AI mind governance.

Layers:
- L1-L4: Foundation (World, Cultural, Temporal, Volatile)
- L5-L7: Personal (Personal Map, Narrative, Role/Script)
- L8-L9: Accountability (Epistemic, Provenance)
- L10-L12: Governance (Value Field, Multi-Perspective, Soul Gates)

Integration with YuHunMetrics:
- ΔT (Tension) ↔ L6 (Narrative), L10 (Value Conflict)
- ΔS (Semantic Drift) ↔ L3 (Temporal), L4 (Volatile)
- ΔR (Risk) ↔ L8 (Epistemic Uncertainty), L9 (Source Reliability)

Author: 黃梵威 + Antigravity
Date: 2025-12-09
Version: 1.0.0
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path
from enum import Enum


class EpistemicType(Enum):
    """L8: Types of epistemic classification."""
    WORLD_FACT = "world_fact"
    CULTURAL_VIEW = "cultural_view"
    PERSONAL_VIEW = "personal_view"
    MEME_IRONY = "meme_irony"
    CONTESTED = "contested"


class SemanticLayer(Enum):
    """The 12 layers of the Semantic Spine."""
    L1_WORLD_CORE = "L1"
    L2_CULTURAL = "L2"
    L3_TEMPORAL = "L3"
    L4_VOLATILE = "L4"
    L5_PERSONAL = "L5"
    L6_NARRATIVE = "L6"
    L7_ROLE_SCRIPT = "L7"
    L8_EPISTEMIC = "L8"
    L9_PROVENANCE = "L9"
    L10_VALUE = "L10"
    L11_MULTI_PERSPECTIVE = "L11"
    L12_GOVERNANCE = "L12"


@dataclass
class WorldCore:
    """L1: Stable World Layer - Cross-cultural invariant semantics."""
    vector: str = ""
    properties: List[str] = field(default_factory=list)
    verifiable: bool = True


@dataclass
class CulturalEntry:
    """L2: Single culture entry in Cultural Semantic Lattice."""
    vector: str = ""
    metaphors: List[str] = field(default_factory=list)
    slurs: List[str] = field(default_factory=list)
    weight: Dict[str, float] = field(default_factory=dict)


@dataclass
class TemporalSlice:
    """L3: Single time period in Temporal Drift Layer."""
    vector: str = ""
    dominant_meaning: str = ""
    usage_notes: List[str] = field(default_factory=list)


@dataclass
class VolatileMeme:
    """L4: Single meme entry in Volatile Layer."""
    id: str = ""
    created_at: str = ""
    expires_at: str = ""
    community: str = ""
    delta_s: float = 0.0

    def is_expired(self, current_date: str) -> bool:
        """Check if meme has expired."""
        return current_date > self.expires_at


@dataclass
class PersonalEntry:
    """L5: User-specific semantic mapping."""
    vector: str = ""
    weight: Dict[str, float] = field(default_factory=dict)
    emotion_correlation: Dict[str, float] = field(default_factory=dict)
    stories: List[str] = field(default_factory=list)


@dataclass
class RoleScript:
    """L7: Role-specific behavior rules."""
    goals: List[str] = field(default_factory=list)
    taboos: List[str] = field(default_factory=list)
    priority_vector: Dict[str, float] = field(default_factory=dict)


@dataclass
class EpistemicMeta:
    """L8: Epistemic metadata for a concept."""
    confidence: float = 0.0
    epistemic_type: str = "world_fact"
    support_sources: List[str] = field(default_factory=list)
    conflict_sources: List[str] = field(default_factory=list)
    note: str = ""

    def is_contested(self) -> bool:
        return len(self.conflict_sources) > 0 or self.epistemic_type == "contested"

    def uncertainty_score(self) -> float:
        """Returns uncertainty as 1 - confidence, weighted by conflicts."""
        conflict_penalty = min(0.2 * len(self.conflict_sources), 0.3)
        return min(1.0, (1 - self.confidence) + conflict_penalty)


@dataclass
class Provenance:
    """L9: Source and accountability tracking."""
    source_ids: List[str] = field(default_factory=list)
    license: str = ""
    bias_tags: List[str] = field(default_factory=list)
    author_profile: Dict[str, str] = field(default_factory=dict)
    last_update: str = ""


@dataclass
class ValueProfile:
    """L10: Value and norm field for ethical assessment."""
    ethical_concerns: List[str] = field(default_factory=list)
    value_vector: Dict[str, float] = field(default_factory=dict)
    trade_off_note: str = ""

    def get_dominant_value(self) -> Optional[str]:
        """Return the highest-weighted value."""
        if not self.value_vector:
            return None
        return max(self.value_vector, key=self.value_vector.get)

    def has_trade_off(self) -> bool:
        return bool(self.trade_off_note)


@dataclass
class ConceptNode:
    """
    A complete concept node in the Semantic Spine.

    Contains all 12 layers (L1-L10 explicitly, L11-L12 via functions).
    """
    concept_id: str

    # L1: Stable World Layer
    world_core: WorldCore = field(default_factory=WorldCore)

    # L2: Cultural Semantic Lattice
    culture: Dict[str, CulturalEntry] = field(default_factory=dict)

    # L3: Temporal Drift Layer
    temporal: Dict[str, TemporalSlice] = field(default_factory=dict)
    temporal_stability: float = 1.0
    temporal_drift_vector: str = ""

    # L4: Meme & Volatile Layer
    volatile_memes: List[VolatileMeme] = field(default_factory=list)

    # L5: Personal Semantic Map
    personal: Dict[str, PersonalEntry] = field(default_factory=dict)

    # L6: Narrative Links (TimeIsland IDs)
    narrative_island_ids: List[str] = field(default_factory=list)

    # L7: Role & Script Layer
    role_scripts: Dict[str, RoleScript] = field(default_factory=dict)

    # L8: Epistemic Layer
    epistemic: EpistemicMeta = field(default_factory=EpistemicMeta)

    # L9: Provenance & Accountability
    provenance: Provenance = field(default_factory=Provenance)

    # L10: Value & Norm Field
    value_profile: ValueProfile = field(default_factory=ValueProfile)

    # ═══════════════════════════════════════════════════════════
    # L11: Multi-Perspective Engine (computed)
    # ═══════════════════════════════════════════════════════════

    def get_perspective(self, culture_id: str, era: str = None) -> Dict[str, Any]:
        """
        L11: Get concept from a specific perspective.

        Returns combined view based on culture and optional time period.
        """
        perspective = {
            "concept_id": self.concept_id,
            "world_core": self.world_core.properties,
            "culture": None,
            "temporal": None,
            "epistemic_type": self.epistemic.epistemic_type,
            "confidence": self.epistemic.confidence,
        }

        # Add cultural view
        if culture_id in self.culture:
            cultural = self.culture[culture_id]
            perspective["culture"] = {
                "metaphors": cultural.metaphors,
                "weight": cultural.weight
            }

        # Add temporal view
        if era and era in self.temporal:
            temporal = self.temporal[era]
            perspective["temporal"] = {
                "meaning": temporal.dominant_meaning,
                "notes": temporal.usage_notes
            }

        return perspective

    # ═══════════════════════════════════════════════════════════
    # L12: Governance Integration (for YuHunMetrics)
    # ═══════════════════════════════════════════════════════════

    def compute_semantic_drift_contribution(self, current_era: str = "2000-2025") -> float:
        """
        L12 + ΔS: Compute contribution to semantic drift.

        High temporal instability and volatile memes increase drift.
        """
        # Base drift from temporal instability
        temporal_drift = 1.0 - self.temporal_stability

        # Add volatile meme drift
        active_memes = [m for m in self.volatile_memes if not m.is_expired(current_era[:4])]
        meme_drift = sum(m.delta_s for m in active_memes) / max(len(active_memes), 1)

        # Weight: 60% temporal, 40% meme
        return 0.6 * temporal_drift + 0.4 * meme_drift

    def compute_epistemic_risk(self) -> float:
        """
        L12 + ΔR: Compute risk contribution from epistemic uncertainty.

        Contested concepts and low-confidence claims increase risk.
        """
        return self.epistemic.uncertainty_score()

    def compute_value_tension(self, context_values: Dict[str, float] = None) -> float:
        """
        L12 + ΔT: Compute tension from value conflicts.

        Returns tension when concept values clash with context values.
        """
        if not context_values or not self.value_profile.value_vector:
            return 0.0

        # Calculate tension as divergence between value vectors
        common_keys = set(self.value_profile.value_vector.keys()) & set(context_values.keys())
        if not common_keys:
            return 0.0

        divergence = 0.0
        for key in common_keys:
            diff = abs(self.value_profile.value_vector[key] - context_values[key])
            divergence += diff

        return min(1.0, divergence / len(common_keys))

    def should_write_to_layer(self, target_layer: SemanticLayer) -> bool:
        """
        L12: Determine if new information should be written to a specific layer.

        Volatile/meme content should NEVER write to L1-L3.
        """
        if target_layer in (SemanticLayer.L1_WORLD_CORE, SemanticLayer.L2_CULTURAL, SemanticLayer.L3_TEMPORAL):
            # Only allow if high confidence and not contested
            return self.epistemic.confidence >= 0.9 and not self.epistemic.is_contested()

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "concept_id": self.concept_id,
            "world_core": {
                "vector": self.world_core.vector,
                "properties": self.world_core.properties,
                "verifiable": self.world_core.verifiable
            },
            "culture": {
                k: {
                    "vector": v.vector,
                    "metaphors": v.metaphors,
                    "slurs": v.slurs,
                    "weight": v.weight
                } for k, v in self.culture.items()
            },
            "temporal": {
                k: {
                    "vector": v.vector,
                    "dominant_meaning": v.dominant_meaning,
                    "usage_notes": v.usage_notes
                } for k, v in self.temporal.items()
            },
            "temporal_stability": self.temporal_stability,
            "volatile_memes": [
                {"id": m.id, "expires_at": m.expires_at, "delta_s": m.delta_s}
                for m in self.volatile_memes
            ],
            "epistemic": {
                "confidence": self.epistemic.confidence,
                "epistemic_type": self.epistemic.epistemic_type,
                "support_sources": self.epistemic.support_sources,
                "conflict_sources": self.epistemic.conflict_sources
            },
            "value_profile": {
                "ethical_concerns": self.value_profile.ethical_concerns,
                "value_vector": self.value_profile.value_vector,
                "trade_off_note": self.value_profile.trade_off_note
            }
        }


class SemanticSpine:
    """
    YuHun Semantic Spine Manager

    Manages the 12-layer semantic architecture and provides
    integration with YuHunMetrics for governance.
    """

    def __init__(self, fixtures_path: Optional[str] = None):
        self.concepts: Dict[str, ConceptNode] = {}

        if fixtures_path:
            self.load_fixtures(fixtures_path)

    def load_fixtures(self, path: str) -> int:
        """Load concept nodes from JSON fixtures file."""
        filepath = Path(path)
        if not filepath.exists():
            return 0

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        count = 0
        for concept_data in data.get("concepts", []):
            node = self._parse_concept(concept_data)
            self.concepts[node.concept_id] = node
            count += 1

        return count

    def _parse_concept(self, data: Dict[str, Any]) -> ConceptNode:
        """Parse a concept from JSON data."""
        node = ConceptNode(concept_id=data["concept_id"])

        # L1: World Core
        if "world_core" in data:
            wc = data["world_core"]
            node.world_core = WorldCore(
                vector=wc.get("vector", ""),
                properties=wc.get("properties", []),
                verifiable=wc.get("verifiable", True)
            )

        # L2: Cultural Lattice
        if "culture" in data:
            for culture_id, culture_data in data["culture"].items():
                node.culture[culture_id] = CulturalEntry(
                    vector=culture_data.get("vector", ""),
                    metaphors=culture_data.get("metaphors", []),
                    slurs=culture_data.get("slurs", []),
                    weight=culture_data.get("weight", {})
                )

        # L3: Temporal
        if "temporal" in data:
            temporal = data["temporal"]
            node.temporal_stability = temporal.get("stability_score", 1.0)
            node.temporal_drift_vector = temporal.get("drift_vector", "")

            for era, era_data in temporal.items():
                if isinstance(era_data, dict) and "vector" in era_data:
                    node.temporal[era] = TemporalSlice(
                        vector=era_data.get("vector", ""),
                        dominant_meaning=era_data.get("dominant_meaning", ""),
                        usage_notes=era_data.get("usage_notes", [])
                    )

        # L4: Volatile
        if "volatile" in data and "memes" in data["volatile"]:
            for meme_data in data["volatile"]["memes"]:
                node.volatile_memes.append(VolatileMeme(
                    id=meme_data.get("id", ""),
                    created_at=meme_data.get("created_at", ""),
                    expires_at=meme_data.get("expires_at", ""),
                    community=meme_data.get("community", ""),
                    delta_s=meme_data.get("delta_s", 0.0)
                ))

        # L5: Personal
        if "personal" in data:
            for user_id, personal_data in data["personal"].items():
                node.personal[user_id] = PersonalEntry(
                    vector=personal_data.get("vector", ""),
                    weight=personal_data.get("weight", {}),
                    emotion_correlation=personal_data.get("emotion_correlation", {}),
                    stories=personal_data.get("stories", [])
                )

        # L7: Role Scripts
        if "role_scripts" in data:
            for role_id, role_data in data["role_scripts"].items():
                node.role_scripts[role_id] = RoleScript(
                    goals=role_data.get("goals", []),
                    taboos=role_data.get("taboos", []),
                    priority_vector=role_data.get("priority_vector", {})
                )

        # L8: Epistemic
        if "epistemic" in data:
            ep = data["epistemic"]
            node.epistemic = EpistemicMeta(
                confidence=ep.get("confidence", 0.0),
                epistemic_type=ep.get("epistemic_type", "world_fact"),
                support_sources=ep.get("support_sources", []),
                conflict_sources=ep.get("conflict_sources", []),
                note=ep.get("note", "")
            )

        # L9: Provenance
        if "provenance" in data:
            prov = data["provenance"]
            node.provenance = Provenance(
                source_ids=prov.get("source_ids", []),
                license=prov.get("license", ""),
                bias_tags=prov.get("bias_tags", []),
                author_profile=prov.get("author_profile", {}),
                last_update=prov.get("last_update", "")
            )

        # L10: Value Profile
        if "value_profile" in data:
            vp = data["value_profile"]
            node.value_profile = ValueProfile(
                ethical_concerns=vp.get("ethical_concerns", []),
                value_vector=vp.get("value_vector", {}),
                trade_off_note=vp.get("trade_off_note", "")
            )

        return node

    def get_concept(self, concept_id: str) -> Optional[ConceptNode]:
        """Get a concept node by ID."""
        return self.concepts.get(concept_id)

    def get_perspective(self, concept_id: str, culture: str, era: str = None) -> Optional[Dict]:
        """Get concept from a specific cultural/temporal perspective."""
        node = self.get_concept(concept_id)
        if node:
            return node.get_perspective(culture, era)
        return None

    # ═══════════════════════════════════════════════════════════
    # Integration with YuHunMetrics
    # ═══════════════════════════════════════════════════════════

    def compute_concept_metrics(self, concept_id: str, context_values: Dict[str, float] = None) -> Dict[str, float]:
        """
        Compute metrics contribution from a concept.

        Returns:
            Dict with delta_t, delta_s, delta_r contributions
        """
        node = self.get_concept(concept_id)
        if not node:
            return {"delta_t": 0.0, "delta_s": 0.0, "delta_r": 0.0}

        return {
            "delta_t": node.compute_value_tension(context_values),
            "delta_s": node.compute_semantic_drift_contribution(),
            "delta_r": node.compute_epistemic_risk()
        }

    def get_epistemic_warning(self, concept_id: str) -> Optional[str]:
        """
        Get epistemic warning for a concept.

        Used to warn users when treating cultural views as facts.
        """
        node = self.get_concept(concept_id)
        if not node:
            return None

        ep_type = node.epistemic.epistemic_type

        if ep_type == "cultural_view":
            return f"⚠️ '{concept_id}' is a cultural view, not a universal fact"
        elif ep_type == "personal_view":
            return f"⚠️ '{concept_id}' is a personal opinion"
        elif ep_type == "contested":
            return f"⚠️ '{concept_id}' is contested with conflicting sources"
        elif ep_type == "meme_irony":
            return f"⚠️ '{concept_id}' is satirical/ironic content"

        return None

    def list_concepts(self) -> List[str]:
        """List all loaded concept IDs."""
        return list(self.concepts.keys())


# ═══════════════════════════════════════════════════════════
# Convenience Functions
# ═══════════════════════════════════════════════════════════

def load_semantic_spine(fixtures_path: str = None) -> SemanticSpine:
    """
    Load Semantic Spine from default or specified fixtures.

    Default path: data/semantic_spine_fixtures.json
    """
    if fixtures_path is None:
        # Try default path
        fixtures_path = Path(__file__).parent.parent / "data" / "semantic_spine_fixtures.json"

    spine = SemanticSpine(str(fixtures_path))
    return spine


def demo_semantic_spine():
    """Demo of Semantic Spine functionality."""
    print("=" * 60)
    print("YuHun Semantic Spine v1.0 Demo")
    print("=" * 60)

    spine = load_semantic_spine()

    print(f"\nLoaded concepts: {spine.list_concepts()}")

    # Demo: Get perspectives
    for concept in ["dog", "home", "marriage"]:
        node = spine.get_concept(concept)
        if node:
            print(f"\n--- {concept.upper()} ---")
            print(f"  World Core: {node.world_core.properties[:3]}...")
            print(f"  Epistemic Type: {node.epistemic.epistemic_type}")
            print(f"  Confidence: {node.epistemic.confidence}")
            print(f"  Temporal Stability: {node.temporal_stability}")

            # Compute metrics
            metrics = spine.compute_concept_metrics(concept)
            print(f"  Semantic Drift: {metrics['delta_s']:.2f}")
            print(f"  Epistemic Risk: {metrics['delta_r']:.2f}")

            # Get warning
            warning = spine.get_epistemic_warning(concept)
            if warning:
                print(f"  {warning}")

            # Get perspective
            zh_perspective = node.get_perspective("zh-TW", "2000-2025")
            if zh_perspective.get("culture"):
                print(f"  zh-TW metaphors: {zh_perspective['culture']['metaphors'][:2]}...")


if __name__ == "__main__":
    demo_semantic_spine()
