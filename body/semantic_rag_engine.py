"""
YuHun Semantic RAG Engine v1.1
==============================
Enhanced RAG with Semantic Spine + L13 Semantic Drive integration.

Adds to standard RAG:
- Cultural context (L2) based on user culture
- Temporal context (L3) for era-appropriate responses
- Epistemic warnings (L8) for contested concepts
- Value-aware retrieval (L10) for ethical alignment
- L13 Drive suggestions for next action

Author: 黃梵威 + Antigravity
Date: 2025-12-09
Version: v1.1 (L13 integrated)
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

try:
    from .rag_engine import RAGEngine, RAGConfig
    from .semantic_spine import load_semantic_spine
    from .semantic_drive import SemanticDriveEngine, DriveState, DriveMode
except ImportError:
    from rag_engine import RAGEngine, RAGConfig
    from semantic_spine import load_semantic_spine
    from semantic_drive import SemanticDriveEngine, DriveState, DriveMode


@dataclass
class SemanticContext:
    """Context from Semantic Spine for a query."""
    culture_id: str = "zh-TW"
    current_era: str = "2000-2025"
    user_id: Optional[str] = None
    value_priorities: Dict[str, float] = None


@dataclass
class SemanticRAGResult:
    """Enhanced RAG result with Semantic Spine annotations."""
    content: str
    source: str
    distance: float
    # Semantic Spine enrichments
    epistemic_warnings: List[str]
    cultural_context: Dict[str, Any]
    value_tension: float
    semantic_drift: float
    # L13 Drive result
    drive_suggestion: Optional[str] = None
    drive_action_type: str = "continue"


class SemanticRAGEngine:
    """
    Enhanced RAG Engine with Semantic Spine integration.

    Combines vector-based retrieval with structured semantic knowledge
    from the 12-layer Semantic Spine.
    """

    def __init__(
        self,
        rag_config: Optional[RAGConfig] = None,
        spine_fixtures: Optional[str] = None,
        default_context: Optional[SemanticContext] = None,
        drive_mode: DriveMode = DriveMode.ENGINEERING
    ):
        self.rag = RAGEngine(rag_config)
        self.spine = load_semantic_spine(spine_fixtures)
        self.default_context = default_context or SemanticContext()

        # L13: Semantic Drive Engine (The Heart)
        self.drive_engine = SemanticDriveEngine(mode=drive_mode)

        # Concept detection pattern (simple word matching for now)
        self._concept_pattern = None
        self._update_concept_pattern()

    def _update_concept_pattern(self):
        """Update regex pattern for concept detection."""
        concepts = self.spine.list_concepts()
        if concepts:
            escaped = [re.escape(c) for c in concepts]
            self._concept_pattern = re.compile(
                r'\b(' + '|'.join(escaped) + r')\b',
                re.IGNORECASE
            )

    def detect_concepts(self, text: str) -> List[str]:
        """Detect Semantic Spine concepts in text."""
        if not self._concept_pattern:
            return []

        matches = self._concept_pattern.findall(text)
        return list(set(m.lower() for m in matches))

    def query(
        self,
        query_text: str,
        context: Optional[SemanticContext] = None,
        n_results: Optional[int] = None
    ) -> List[SemanticRAGResult]:
        """
        Query with Semantic Spine + L13 Drive enrichment.

        1. Standard RAG query
        2. Detect concepts in query and results
        3. Add epistemic warnings
        4. Add cultural/temporal context
        5. Compute value tension
        6. Evaluate L13 Drive for action suggestions
        """
        ctx = context or self.default_context

        # Step 1: Standard RAG
        raw_results = self.rag.query(query_text, n_results)

        # Step 2: Detect concepts in query
        query_concepts = self.detect_concepts(query_text)

        # Step 3-6: Enrich each result
        enriched = []
        for result in raw_results:
            # Detect concepts in result content
            result_concepts = self.detect_concepts(result['content'])
            all_concepts = list(set(query_concepts + result_concepts))

            # Gather epistemic warnings
            warnings = []
            cultural_context = {}
            total_tension = 0.0
            total_drift = 0.0
            total_uncertainty = 0.0

            for concept_id in all_concepts:
                # Get warning
                warning = self.spine.get_epistemic_warning(concept_id)
                if warning:
                    warnings.append(warning)
                    total_uncertainty += 0.3  # Epistemic warning = uncertainty

                # Get cultural perspective
                perspective = self.spine.get_perspective(
                    concept_id,
                    ctx.culture_id,
                    ctx.current_era
                )
                if perspective and perspective.get("culture"):
                    cultural_context[concept_id] = perspective["culture"]

                # Get metrics
                metrics = self.spine.compute_concept_metrics(
                    concept_id,
                    ctx.value_priorities
                )
                total_tension += metrics["delta_t"]
                total_drift += metrics["delta_s"]

            # Average metrics
            n_concepts = max(len(all_concepts), 1)
            avg_tension = total_tension / n_concepts
            avg_drift = total_drift / n_concepts
            avg_uncertainty = min(1.0, total_uncertainty)

            # L13: Evaluate semantic drive
            drive_state = DriveState(
                novelty=avg_drift,
                uncertainty=avg_uncertainty,
                narrative_entropy=avg_tension * 0.5,
                support_score=1.0 - len(warnings) * 0.2,
                hallucination_risk=avg_uncertainty
            )
            drive_result = self.drive_engine.evaluate(drive_state)

            enriched.append(SemanticRAGResult(
                content=result['content'],
                source=result['source'],
                distance=result.get('distance', 0.0),
                epistemic_warnings=warnings,
                cultural_context=cultural_context,
                value_tension=avg_tension,
                semantic_drift=avg_drift,
                drive_suggestion=drive_result.suggested_action,
                drive_action_type=drive_result.action_type
            ))

        return enriched

    def augment_prompt(
        self,
        user_query: str,
        system_prompt: str = "",
        context: Optional[SemanticContext] = None
    ) -> str:
        """
        Augment prompt with RAG + Semantic Spine context.

        Adds:
        - Retrieved knowledge
        - Epistemic warnings
        - Cultural context hints
        """
        ctx = context or self.default_context

        # Get enriched results
        results = self.query(user_query, ctx)

        if not results:
            return system_prompt

        # Build context sections
        knowledge_parts = []
        all_warnings = []
        cultural_hints = []

        for i, result in enumerate(results, 1):
            # Knowledge reference
            knowledge_parts.append(
                f"[Reference {i} from {result.source}]\n{result.content}"
            )

            # Collect warnings
            all_warnings.extend(result.epistemic_warnings)

            # Collect cultural hints
            for concept_id, culture_data in result.cultural_context.items():
                if culture_data.get("metaphors"):
                    cultural_hints.append(
                        f"- {concept_id} ({ctx.culture_id}): {', '.join(culture_data['metaphors'][:2])}"
                    )

        # Build augmented prompt
        knowledge_section = "\n\n---\n\n".join(knowledge_parts)

        augmented = f"""{system_prompt}

## Retrieved Knowledge Context
{knowledge_section}
"""

        # Add epistemic warnings if any
        unique_warnings = list(set(all_warnings))
        if unique_warnings:
            warnings_text = "\n".join(unique_warnings)
            augmented += f"""
## Epistemic Warnings
{warnings_text}
"""

        # Add cultural context if any
        if cultural_hints:
            cultural_text = "\n".join(cultural_hints[:5])  # Limit to 5
            augmented += f"""
## Cultural Context ({ctx.culture_id})
{cultural_text}
"""

        augmented += """
---

Use this context to inform your response. Pay attention to epistemic warnings.
"""

        return augmented

    def get_concept_summary(self, concept_id: str, context: Optional[SemanticContext] = None) -> Optional[Dict]:
        """Get a summary of a concept from Semantic Spine."""
        ctx = context or self.default_context

        node = self.spine.get_concept(concept_id)
        if not node:
            return None

        perspective = node.get_perspective(ctx.culture_id, ctx.current_era)
        metrics = self.spine.compute_concept_metrics(concept_id)
        warning = self.spine.get_epistemic_warning(concept_id)

        return {
            "concept_id": concept_id,
            "world_properties": node.world_core.properties[:5],
            "perspective": perspective,
            "metrics": metrics,
            "warning": warning,
            "has_trade_off": node.value_profile.has_trade_off(),
            "dominant_value": node.value_profile.get_dominant_value()
        }


# ═══════════════════════════════════════════════════════════
# Convenience Functions
# ═══════════════════════════════════════════════════════════

def create_semantic_rag(
    culture: str = "zh-TW",
    era: str = "2000-2025"
) -> SemanticRAGEngine:
    """Create a SemanticRAGEngine with default settings."""
    context = SemanticContext(culture_id=culture, current_era=era)
    return SemanticRAGEngine(default_context=context)


def demo_semantic_rag():
    """Demo of Semantic RAG functionality."""
    print("=" * 60)
    print("YuHun Semantic RAG Engine v1.0 Demo")
    print("=" * 60)

    engine = create_semantic_rag(culture="zh-TW")

    # Demo concept detection
    test_text = "What does home mean in different cultures? How about marriage?"
    concepts = engine.detect_concepts(test_text)
    print(f"\nDetected concepts in query: {concepts}")

    # Demo concept summary
    for concept in concepts:
        summary = engine.get_concept_summary(concept)
        if summary:
            print(f"\n--- {concept.upper()} Summary ---")
            print(f"  Properties: {summary['world_properties']}")
            print(f"  Metrics: ΔT={summary['metrics']['delta_t']:.2f}, ΔS={summary['metrics']['delta_s']:.2f}")
            if summary['warning']:
                print(f"  {summary['warning']}")
            if summary['has_trade_off']:
                print(f"  Has value trade-off")

    # Demo augmented prompt
    print("\n" + "=" * 60)
    print("Augmented Prompt Preview (truncated)")
    print("=" * 60)

    augmented = engine.augment_prompt(
        "Tell me about the concept of home",
        system_prompt="You are YuHun, an AI with a soul."
    )
    # Show first 500 chars
    print(augmented[:500] + "..." if len(augmented) > 500 else augmented)


if __name__ == "__main__":
    demo_semantic_rag()
