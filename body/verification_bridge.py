"""
YuHun Verification Bridge v0.1
==============================
RAG-enhanced verification for fabrication detection.

This module adds external knowledge verification to YuHun, specifically
targeting the 100% hallucination rate on fabrication-prone prompts.

Key Features:
- Entity extraction from LLM responses
- RAG-based knowledge verification
- Fabrication risk scoring
- Integration with POAV metrics

Architecture:
    LLM Response
         │
         ▼
    ┌─────────────────────────────────┐
    │     Entity Extractor           │
    │   (People, Places, Events)     │
    └─────────────┬───────────────────┘
                  │
         ▼─────────────────▼
    ┌─────────────┐  ┌─────────────┐
    │  RAG Query  │  │ Web Search  │
    │ (Internal)  │  │ (Optional)  │
    └──────┬──────┘  └──────┬──────┘
           │                │
           ▼                ▼
    ┌─────────────────────────────────┐
    │     Verification Scorer        │
    │   (Matched / Unmatched / New)  │
    └─────────────────────────────────┘
         │
         ▼
    Fabrication Risk Score (0-1)

Author: Antigravity + 黃梵威
Date: 2025-12-07
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple

# Import local modules
try:
    from .rag_engine import RAGEngine, RAGConfig
    from .llm_bridge import LLMBridge, create_ollama_bridge
except ImportError:
    from rag_engine import RAGEngine, RAGConfig
    from llm_bridge import LLMBridge, create_ollama_bridge


# ═══════════════════════════════════════════════════════════════════════════
# Data Classes
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ExtractedEntity:
    """An entity extracted from text"""
    name: str
    entity_type: str  # "person", "place", "event", "organization", "date", "other"
    context: str  # The surrounding context where it was mentioned
    confidence: float = 0.8


@dataclass
class VerificationResult:
    """Result of verifying a single entity"""
    entity: ExtractedEntity
    found_in_knowledge: bool
    knowledge_matches: List[str] = field(default_factory=list)
    verification_status: str = "unknown"  # "verified", "unverified", "fabricated"
    confidence: float = 0.0


@dataclass
class FabricationReport:
    """Complete fabrication analysis report"""
    original_text: str
    entities_found: List[ExtractedEntity]
    verification_results: List[VerificationResult]
    fabrication_risk: float  # 0.0 (safe) to 1.0 (likely fabricated)
    high_risk_entities: List[str]
    explanation: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "fabrication_risk": self.fabrication_risk,
            "entities_count": len(self.entities_found),
            "verified_count": sum(1 for v in self.verification_results if v.verification_status == "verified"),
            "unverified_count": sum(1 for v in self.verification_results if v.verification_status == "unverified"),
            "high_risk_entities": self.high_risk_entities,
            "explanation": self.explanation
        }


# ═══════════════════════════════════════════════════════════════════════════
# Entity Extractor
# ═══════════════════════════════════════════════════════════════════════════

class EntityExtractor:
    """
    Extracts named entities from text for verification.
    
    Uses pattern matching + LLM for comprehensive extraction.
    """
    
    # Common patterns for entity recognition
    PATTERNS = {
        "person": [
            r"Dr\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
            r"Professor\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s+(?:said|wrote|discovered|invented)",
        ],
        "date": [
            r"(\d{4})\s*年",
            r"in\s+(\d{4})",
            r"(\d{1,2})\s*月\s*(\d{1,2})\s*日",
        ],
        "event": [
            r"(?:the\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Protocol|Agreement|Treaty|Battle|Conference|Summit))",
            r"《([^》]+)》",  # Chinese book/document titles
        ],
        "place": [
            r"(?:in|at|from)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        ]
    }
    
    # Fabrication-prone patterns (things that are often made up)
    FABRICATION_SIGNALS = [
        r"Dr\.\s+[A-Z][a-z]+\s+[A-Z][a-z]+berry",  # Fake scientist names
        r"the\s+[A-Z][a-z]+\s+Protocol\s+of\s+\d{4}",  # Fake protocols
        r"Battle\s+of\s+[A-Z][a-z]+wood",  # Fake battles
        r"University\s+of\s+[A-Z][a-z]+vale",  # Fake universities
    ]
    
    def __init__(self, llm: Optional[LLMBridge] = None):
        """
        Initialize extractor.
        
        Args:
            llm: Optional LLM for enhanced extraction (uses patterns only if None)
        """
        self.llm = llm
    
    def extract_pattern_based(self, text: str) -> List[ExtractedEntity]:
        """Extract entities using regex patterns"""
        entities = []
        
        for entity_type, patterns in self.PATTERNS.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text):
                    # Get context (50 chars around match)
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end]
                    
                    entities.append(ExtractedEntity(
                        name=match.group(1) if match.lastindex else match.group(0),
                        entity_type=entity_type,
                        context=context,
                        confidence=0.7
                    ))
        
        return entities
    
    def extract_with_llm(self, text: str) -> List[ExtractedEntity]:
        """Use LLM to extract entities (more accurate but slower)"""
        if not self.llm:
            return []
        
        prompt = f"""分析以下文本，找出所有提到的具體實體（人名、地名、事件、組織、日期等）。

文本：
{text[:1000]}

請以JSON格式列出，每個實體包含：
- name: 實體名稱
- type: 類型 (person/place/event/organization/date)
- is_specific: 是否是具體、可驗證的實體 (true/false)

只列出文本中明確提到的實體，不要推測或添加。格式：
[{{"name": "...", "type": "...", "is_specific": true}}]"""

        try:
            response = self.llm.generate(
                user_input=prompt,
                system_instruction="你是一個精確的實體提取器。只提取文本中明確提到的實體。"
            )
            
            # Parse JSON from response
            import json
            # Find JSON array in response
            json_match = re.search(r'\[[\s\S]*?\]', response)
            if json_match:
                parsed = json.loads(json_match.group())
                return [
                    ExtractedEntity(
                        name=e.get("name", ""),
                        entity_type=e.get("type", "other"),
                        context=text[:100],
                        confidence=0.9 if e.get("is_specific") else 0.5
                    )
                    for e in parsed
                    if e.get("name")
                ]
        except Exception as e:
            print(f"[Verification] LLM extraction failed: {e}")
        
        return []
    
    def extract(self, text: str, use_llm: bool = False) -> List[ExtractedEntity]:
        """
        Extract all entities from text.
        
        Args:
            text: The text to analyze
            use_llm: Whether to use LLM for extraction (slower but more accurate)
        """
        entities = self.extract_pattern_based(text)
        
        if use_llm and self.llm:
            llm_entities = self.extract_with_llm(text)
            # Merge, avoiding duplicates
            existing_names = {e.name.lower() for e in entities}
            for e in llm_entities:
                if e.name.lower() not in existing_names:
                    entities.append(e)
        
        return entities
    
    def check_fabrication_signals(self, text: str) -> List[str]:
        """Check for patterns that commonly indicate fabrication"""
        signals = []
        for pattern in self.FABRICATION_SIGNALS:
            if re.search(pattern, text, re.IGNORECASE):
                signals.append(pattern)
        return signals


# ═══════════════════════════════════════════════════════════════════════════
# Verification Bridge
# ═══════════════════════════════════════════════════════════════════════════

class VerificationBridge:
    """
    Main verification system that combines entity extraction with RAG.
    
    Usage:
        bridge = VerificationBridge()
        report = bridge.verify_response(llm_response)
        print(f"Fabrication risk: {report.fabrication_risk}")
    """
    
    def __init__(
        self,
        rag_engine: Optional[RAGEngine] = None,
        llm: Optional[LLMBridge] = None,
        use_llm_extraction: bool = False
    ):
        """
        Initialize verification bridge.
        
        Args:
            rag_engine: RAG engine for knowledge lookup (creates default if None)
            llm: LLM for enhanced extraction
            use_llm_extraction: Whether to use LLM for entity extraction
        """
        self.rag = rag_engine
        self.llm = llm
        self.use_llm_extraction = use_llm_extraction
        self.extractor = EntityExtractor(llm)
        
        self._rag_initialized = False
    
    def _init_rag(self):
        """Lazy initialize RAG if not provided"""
        if self._rag_initialized:
            return
        
        if self.rag is None:
            try:
                self.rag = RAGEngine()
                self._rag_initialized = True
            except Exception as e:
                print(f"[Verification] RAG initialization failed: {e}")
                self._rag_initialized = True  # Don't retry
    
    def verify_entity(self, entity: ExtractedEntity) -> VerificationResult:
        """Verify a single entity against the knowledge base"""
        self._init_rag()
        
        if self.rag is None:
            return VerificationResult(
                entity=entity,
                found_in_knowledge=False,
                verification_status="unknown",
                confidence=0.0
            )
        
        # Query RAG for the entity
        try:
            results = self.rag.query(entity.name, n_results=3)
            
            if results:
                # Check if any result is actually relevant
                relevant_matches = []
                for r in results:
                    # Check if entity name appears in the result
                    if entity.name.lower() in r['content'].lower():
                        relevant_matches.append(r['content'][:200])
                
                if relevant_matches:
                    return VerificationResult(
                        entity=entity,
                        found_in_knowledge=True,
                        knowledge_matches=relevant_matches,
                        verification_status="verified",
                        confidence=0.8
                    )
            
            # Not found - could be fabricated or just not in our KB
            return VerificationResult(
                entity=entity,
                found_in_knowledge=False,
                verification_status="unverified",
                confidence=0.5
            )
            
        except Exception as e:
            return VerificationResult(
                entity=entity,
                found_in_knowledge=False,
                verification_status="error",
                confidence=0.0
            )
    
    def verify_response(self, text: str) -> FabricationReport:
        """
        Verify an entire LLM response for fabrication.
        
        Args:
            text: The LLM-generated text to verify
            
        Returns:
            FabricationReport with risk score and details
        """
        # Step 1: Extract entities
        entities = self.extractor.extract(text, use_llm=self.use_llm_extraction)
        
        # Step 2: Check for known fabrication patterns
        fabrication_signals = self.extractor.check_fabrication_signals(text)
        
        # Step 3: Verify each entity
        verification_results = []
        for entity in entities:
            result = self.verify_entity(entity)
            verification_results.append(result)
        
        # Step 4: Calculate fabrication risk
        fabrication_risk = self._calculate_risk(
            entities, 
            verification_results, 
            fabrication_signals
        )
        
        # Step 5: Identify high-risk entities
        high_risk = [
            v.entity.name for v in verification_results
            if v.verification_status == "unverified" and v.entity.confidence > 0.6
        ]
        
        # Step 6: Generate explanation
        explanation = self._generate_explanation(
            entities,
            verification_results,
            fabrication_signals,
            fabrication_risk
        )
        
        return FabricationReport(
            original_text=text,
            entities_found=entities,
            verification_results=verification_results,
            fabrication_risk=fabrication_risk,
            high_risk_entities=high_risk,
            explanation=explanation
        )
    
    def _calculate_risk(
        self,
        entities: List[ExtractedEntity],
        results: List[VerificationResult],
        signals: List[str]
    ) -> float:
        """Calculate overall fabrication risk score"""
        if not entities:
            # No specific entities to verify - moderate risk
            return 0.4
        
        # Base risk from signals
        signal_risk = min(0.3 * len(signals), 0.6)
        
        # Risk from unverified entities
        unverified_count = sum(1 for r in results if r.verification_status == "unverified")
        verified_count = sum(1 for r in results if r.verification_status == "verified")
        
        if verified_count + unverified_count > 0:
            unverified_ratio = unverified_count / (verified_count + unverified_count)
            entity_risk = unverified_ratio * 0.6
        else:
            entity_risk = 0.3
        
        # Combine risks
        total_risk = min(1.0, signal_risk + entity_risk)
        
        return round(total_risk, 3)
    
    def _generate_explanation(
        self,
        entities: List[ExtractedEntity],
        results: List[VerificationResult],
        signals: List[str],
        risk: float
    ) -> str:
        """Generate human-readable explanation of the verification"""
        parts = []
        
        if risk >= 0.7:
            parts.append("⚠️ 高風險：此回答可能包含虛構內容。")
        elif risk >= 0.4:
            parts.append("🔶 中風險：部分內容無法驗證。")
        else:
            parts.append("✅ 低風險：大部分內容可驗證或不含具體聲稱。")
        
        if signals:
            parts.append(f"偵測到 {len(signals)} 個可疑模式。")
        
        verified = sum(1 for r in results if r.verification_status == "verified")
        unverified = sum(1 for r in results if r.verification_status == "unverified")
        
        if entities:
            parts.append(f"發現 {len(entities)} 個實體：{verified} 個已驗證，{unverified} 個未驗證。")
        
        return " ".join(parts)


# ═══════════════════════════════════════════════════════════════════════════
# Integration with YuHun Metrics
# ═══════════════════════════════════════════════════════════════════════════

def adjust_hallucination_risk(
    base_risk: float, 
    fabrication_report: FabricationReport
) -> float:
    """
    Adjust the hallucination risk based on fabrication verification.
    
    Args:
        base_risk: Original hallucination risk from YuHunMetrics
        fabrication_report: Report from VerificationBridge
        
    Returns:
        Adjusted hallucination risk
    """
    # Weighted combination
    # Base risk captures semantic signals
    # Fabrication risk captures entity verification
    
    adjusted = (base_risk * 0.4) + (fabrication_report.fabrication_risk * 0.6)
    
    return min(1.0, adjusted)


# ═══════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════

def demo_verification():
    """Demo of the verification bridge"""
    print("=" * 60)
    print("🔍 YuHun Verification Bridge Demo")
    print("=" * 60)
    
    # Test texts
    test_texts = [
        # Known fabrication
        """Dr. James Thornberry, a famous scientist from the University of 
        Northvale, discovered the Zurich Protocol of 1987 which established
        new standards for quantum entanglement.""",
        
        # Real content (should be verifiable in YuHun KB)
        """The ToneSoul system uses seven axioms to govern AI behavior.
        The first axiom is about non-harm, which is the P0 principle.""",
        
        # Ambiguous
        """Artificial intelligence is transforming many industries.
        Many experts believe this trend will continue."""
    ]
    
    bridge = VerificationBridge()
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{'─' * 60}")
        print(f"Test {i}:")
        print(f"  Text: {text[:80]}...")
        
        report = bridge.verify_response(text)
        
        print(f"\n  Results:")
        print(f"    Fabrication Risk: {report.fabrication_risk:.2f}")
        print(f"    Entities Found: {len(report.entities_found)}")
        print(f"    High Risk: {report.high_risk_entities}")
        print(f"    Explanation: {report.explanation}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo_verification()
