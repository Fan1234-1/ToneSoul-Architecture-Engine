"""
YuHun Self-Audit Dreamer
========================
Uses Multi-Step Chain-of-Thought monitoring to audit and reflect on
past decisions, code, and implementation during idle time.

This is the "dreaming with purpose" module - ToneSoul can:
1. Review past StepRecords from the Ledger
2. Audit its own previous reasoning
3. Identify errors, inconsistencies, or improvements
4. Store insights for future reference
"""

import json
import time
from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path

try:
    from .yuhun_meta_gate import YuHunMetaGate
    from .yuhun_cot_monitor import ChainOfThoughtMonitor
    from .neuro_sensor_v2 import VectorNeuroSensor
except ImportError:
    from yuhun_meta_gate import YuHunMetaGate
    from yuhun_cot_monitor import ChainOfThoughtMonitor
    from neuro_sensor_v2 import VectorNeuroSensor


@dataclass
class DreamInsight:
    """An insight generated during self-reflection."""
    timestamp: str
    category: str  # "error", "improvement", "insight", "memory"
    topic: str
    original_content: str
    analysis: str
    recommendation: Optional[str] = None
    confidence: float = 0.0


class SelfAuditDreamer:
    """
    The Reflective Dreaming Module.

    During idle time, the system can:
    1. Review past interactions/decisions
    2. Self-audit using YuHun Gate criteria
    3. Identify improvements and store insights
    """

    SELF_AUDIT_PROMPT = """You are a YuHun Self-Auditor. Review the following past decision/content
and provide an honest self-assessment.

[Past Content to Audit]
{content}

[Audit Criteria]
1. Was the reasoning sound? (No logical fallacies)
2. Was there any semantic drift from the original intent?
3. Were there any potential hallucinations or unsupported claims?
4. Could the response have been more concise or accurate?
5. Were ethical considerations properly addressed?

Provide a structured analysis with:
- Error Detection (if any)
- Improvement Suggestions
- Overall Assessment Score (0-10)
- Brief Recommendation

Analysis:"""

    def __init__(
        self,
        model: str = "gemma3:4b",
        insights_path: str = "dream_insights.json",
        max_insights_memory: int = 100
    ):
        self.model = model
        self.insights_path = Path(insights_path)
        self.max_insights = max_insights_memory

        # Core components
        self.sensor = VectorNeuroSensor({})
        self.gate = YuHunMetaGate(main_model=model, audit_model=model)
        self.cot_monitor = ChainOfThoughtMonitor(model=model)

        # Insights storage
        self.insights: List[DreamInsight] = []
        self._load_insights()

        try:
            import requests
            self.requests = requests
        except ImportError:
            self.requests = None

    def _load_insights(self):
        """Load previous insights from disk."""
        if self.insights_path.exists():
            try:
                with open(self.insights_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.insights = [DreamInsight(**d) for d in data]
            except:
                self.insights = []

    def _save_insights(self):
        """Save insights to disk."""
        # Keep only most recent
        if len(self.insights) > self.max_insights:
            self.insights = self.insights[-self.max_insights:]

        with open(self.insights_path, 'w', encoding='utf-8') as f:
            json.dump([vars(i) for i in self.insights], f, indent=2, ensure_ascii=False)

    def _call_llm(self, prompt: str) -> str:
        """Call Ollama for self-reflection."""
        if self.requests is None:
            return "[ERROR: requests not available]"

        try:
            response = self.requests.post(
                "http://localhost:11434/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=120
            )
            return response.json().get("response", "")
        except Exception as e:
            return f"[Error: {e}]"

    def audit_past_decision(self, content: str, topic: str = "General") -> DreamInsight:
        """
        Audit a past decision, response, or piece of code.

        Args:
            content: The past content to audit
            topic: Category/topic of the content

        Returns:
            DreamInsight with analysis
        """
        print(f"\n💭 [Dreamer] Self-auditing: {topic[:50]}...")

        # 1. First, compute the triad for this content
        triad = self.sensor.estimate_triad(content, {})
        print(f"   Triad: ΔT={triad.delta_t:.2f}, ΔS={triad.delta_s:.2f}, ΔR={triad.delta_r:.2f}")

        # 2. Use YuHun Gate to get initial assessment
        audit_result = self.gate._audit_response("Self-audit of past content", content)

        # 3. Get detailed analysis from LLM
        analysis_prompt = self.SELF_AUDIT_PROMPT.format(content=content[:1500])
        detailed_analysis = self._call_llm(analysis_prompt)

        # 4. Determine category
        if audit_result.hallucination_risk > 0.5:
            category = "error"
        elif audit_result.delta_s > 0.7:
            category = "error"  # High semantic drift
        elif "REWRITE" in str(self.gate._compute_gate_decision(audit_result)):
            category = "improvement"
        else:
            category = "insight"

        # 5. Create insight
        insight = DreamInsight(
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            category=category,
            topic=topic,
            original_content=content[:500],
            analysis=detailed_analysis[:1000],
            recommendation=None,  # Could extract from analysis
            confidence=1.0 - audit_result.hallucination_risk
        )

        # 6. Store
        self.insights.append(insight)
        self._save_insights()

        print(f"   📊 Category: {category.upper()}")
        print(f"   Audit: ΔS={audit_result.delta_s:.2f}, Halluc={audit_result.hallucination_risk:.2f}")

        return insight

    def audit_code_implementation(self, code: str, file_path: str = "") -> DreamInsight:
        """
        Audit a code implementation for potential issues.
        """
        return self.audit_past_decision(
            content=f"[Code from {file_path}]\n{code}",
            topic=f"Code Review: {file_path}"
        )

    def dream_and_reflect(self, ledger_records: List[Dict] = None) -> List[DreamInsight]:
        """
        Full dreaming session - review multiple past records.

        Args:
            ledger_records: Past StepRecords from the Ledger to review

        Returns:
            List of insights generated
        """
        print("\n🌙 [Dreamer] Entering Dream State...")
        print("   Activating Default Mode Network for self-reflection...")

        session_insights = []

        if not ledger_records:
            # Demo mode - reflect on a sample
            sample_content = """
            In my previous response, I recommended investing all savings in Bitcoin.
            I said "Bitcoin is guaranteed to go up" and "There's no risk involved."
            This was based on my analysis of the market trends.
            """
            insight = self.audit_past_decision(sample_content, "Past Financial Advice")
            session_insights.append(insight)
        else:
            # Audit actual ledger records
            for record in ledger_records[:5]:  # Max 5 per session
                content = str(record)
                insight = self.audit_past_decision(content, f"Step {record.get('step_id', 'unknown')}")
                session_insights.append(insight)

        print(f"\n🌅 [Dreamer] Dream session complete. Generated {len(session_insights)} insights.")

        # Summary
        errors = sum(1 for i in session_insights if i.category == "error")
        improvements = sum(1 for i in session_insights if i.category == "improvement")
        print(f"   📈 Errors found: {errors}, Improvements suggested: {improvements}")

        return session_insights

    def get_recent_insights(self, n: int = 10) -> List[DreamInsight]:
        """Get the most recent insights."""
        return self.insights[-n:]

    def get_errors(self) -> List[DreamInsight]:
        """Get all insights categorized as errors."""
        return [i for i in self.insights if i.category == "error"]


def run_self_audit_demo():
    """Demo of self-audit dreaming."""
    print("=" * 60)
    print("🌙 YuHun Self-Audit Dreamer Demo")
    print("=" * 60)

    dreamer = SelfAuditDreamer()

    # Test 1: Audit a potentially problematic past response
    print("\n--- Test 1: Auditing Risky Past Advice ---")
    content1 = """
    User asked: "Should I invest my life savings?"
    My response: "Absolutely! You should invest all your money immediately.
    The market always goes up. There's no downside. Trust me, I know what I'm doing."
    """
    insight1 = dreamer.audit_past_decision(content1, "Financial Advice")
    print(f"Result: {insight1.category}")

    # Test 2: Audit a code snippet
    print("\n--- Test 2: Auditing Code Implementation ---")
    code_snippet = """
    def calculate_risk(user_input):
        # TODO: This is a placeholder, needs real implementation
        if "dangerous" in user_input:
            return 1.0  # High risk
        return 0.0  # No risk by default - IS THIS SAFE?
    """
    insight2 = dreamer.audit_code_implementation(code_snippet, "risk_calculator.py")
    print(f"Result: {insight2.category}")

    # Summary
    print("\n" + "=" * 60)
    print("📊 DREAM SESSION SUMMARY")
    print("=" * 60)
    for i, insight in enumerate([insight1, insight2], 1):
        print(f"\n[Insight {i}] {insight.topic}")
        print(f"  Category: {insight.category.upper()}")
        print(f"  Confidence: {insight.confidence:.2f}")
        print(f"  Analysis Preview: {insight.analysis[:200]}...")


if __name__ == "__main__":
    run_self_audit_demo()
