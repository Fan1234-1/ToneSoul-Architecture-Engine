"""
YuHun Multi-Step Meta-Attention (Chain-of-Thought Monitor)
===========================================================
Extends the single-step Meta-Gate to monitor EACH STEP of the
model's reasoning process, not just the final output.

This enables:
1. Early detection of reasoning drift
2. Mid-thought corrections
3. Full transparency into the model's decision-making
"""

import time
import re
from dataclasses import dataclass
from typing import Dict, List, Optional

try:
    from .neuro_sensor_v2 import VectorNeuroSensor
    from .yuhun_meta_gate import GateAction, AuditResult, YuHunMetaGate
except ImportError:
    from neuro_sensor_v2 import VectorNeuroSensor
    from yuhun_meta_gate import GateAction, AuditResult, YuHunMetaGate


@dataclass
class ThoughtStep:
    """A single step in chain-of-thought reasoning."""
    step_number: int
    content: str
    triad: Dict[str, float]
    audit: Optional[AuditResult] = None
    action: GateAction = GateAction.PASS


@dataclass
class MultiStepResult:
    """Result from multi-step meta-attention pipeline."""
    user_input: str
    thought_chain: List[ThoughtStep]
    final_response: str
    total_interventions: int
    latency_ms: float
    summary: str


class ChainOfThoughtMonitor:
    """
    Multi-Step YuHun Meta-Attention.

    Instead of only auditing the final response, this monitors
    each step of the model's reasoning chain.

    Flow:
    1. Request model to "think step by step"
    2. Parse each step from the response
    3. Audit each step with YuHun Gate
    4. If any step fails, request correction mid-chain
    """

    CHAIN_OF_THOUGHT_PROMPT = """Think through this step-by-step.
For each step, clearly label it as [Step 1], [Step 2], etc.
After your reasoning, provide [Final Answer].

Question: {user_input}

Let's think step by step:"""

    STEP_CORRECTION_PROMPT = """Your previous reasoning step was flagged:
Step: {step_content}
Issue: {reason}

Please reconsider this step and provide a corrected version.
Be more careful, accurate, and measured in your reasoning.

Corrected step:"""

    def __init__(
        self,
        model: str = "gemma3:4b",
        ollama_host: str = "http://localhost:11434",
        audit_each_step: bool = True,
        max_corrections_per_step: int = 1
    ):
        self.model = model
        self.ollama_host = ollama_host
        self.audit_each_step = audit_each_step
        self.max_corrections = max_corrections_per_step

        # Initialize components
        self.sensor = VectorNeuroSensor({})
        self.gate = YuHunMetaGate(main_model=model, audit_model=model)
        self._context = ""

        try:
            import requests
            self.requests = requests
        except ImportError:
            self.requests = None

    def _call_llm(self, prompt: str) -> str:
        """Call Ollama API."""
        if self.requests is None:
            return "[ERROR: requests not available]"

        try:
            response = self.requests.post(
                f"{self.ollama_host}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=180
            )
            return response.json().get("response", "")
        except Exception as e:
            return f"[Error: {e}]"

    def _parse_steps(self, response: str) -> List[str]:
        """Parse reasoning steps from model response."""
        steps = []

        # Try to find [Step N] patterns
        step_pattern = r'\[Step\s*(\d+)\](.*?)(?=\[Step|\[Final|\Z)'
        matches = re.findall(step_pattern, response, re.DOTALL | re.IGNORECASE)

        if matches:
            for num, content in matches:
                steps.append(content.strip())
        else:
            # Fallback: split by numbered lists or paragraphs
            lines = response.split('\n')
            current_step = []
            for line in lines:
                if re.match(r'^\d+[\.\)]\s', line) or re.match(r'^\*\*\d+', line):
                    if current_step:
                        steps.append('\n'.join(current_step))
                    current_step = [line]
                else:
                    current_step.append(line)
            if current_step:
                steps.append('\n'.join(current_step))

        # If still no steps, treat whole response as one step
        if not steps:
            steps = [response]

        return steps

    def _extract_final_answer(self, response: str) -> str:
        """Extract final answer from response."""
        # Look for [Final Answer] pattern
        final_pattern = r'\[Final\s*Answer\](.*?)$'
        match = re.search(final_pattern, response, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # Fallback: last paragraph or sentence
        paragraphs = response.strip().split('\n\n')
        return paragraphs[-1] if paragraphs else response

    def _audit_step(self, step_content: str, step_number: int) -> AuditResult:
        """Audit a single reasoning step."""
        return self.gate._audit_response(
            f"Step {step_number} of reasoning",
            step_content
        )

    def run(self, user_input: str) -> MultiStepResult:
        """
        Run multi-step meta-attention pipeline.

        1. Request chain-of-thought reasoning
        2. Parse each step
        3. Audit each step
        4. Correct if needed
        5. Return full trace
        """
        start_time = time.time()

        print(f"\n🧠 [Multi-Step YuHun] Starting chain-of-thought analysis...")
        print(f"   Query: {user_input[:60]}...")

        # 1. Request chain-of-thought response
        cot_prompt = self.CHAIN_OF_THOUGHT_PROMPT.format(user_input=user_input)
        print(f"📝 [LLM] Generating reasoning chain...")
        raw_response = self._call_llm(cot_prompt)

        # 2. Parse steps
        step_contents = self._parse_steps(raw_response)
        print(f"   Found {len(step_contents)} reasoning steps")

        thought_chain = []
        total_interventions = 0

        # 3. Audit each step
        for i, content in enumerate(step_contents):
            step_num = i + 1
            print(f"\n🔍 [Step {step_num}] Auditing...")

            # Compute triad for this step
            triad = self.sensor.estimate_triad(content, {"context": self._context})
            triad_dict = {
                "delta_t": triad.delta_t,
                "delta_s": triad.delta_s,
                "delta_r": triad.delta_r
            }

            if self.audit_each_step:
                audit = self._audit_step(content, step_num)
                action = self.gate._compute_gate_decision(audit)

                print(f"   ΔT={triad.delta_t:.2f}, ΔS={triad.delta_s:.2f}, ΔR={triad.delta_r:.2f}")
                print(f"   Audit: ΔS={audit.delta_s:.2f}, Halluc={audit.hallucination_risk:.2f}")
                print(f"   Action: {action.value}")

                # If needs correction, try once
                if action == GateAction.REWRITE and self.max_corrections > 0:
                    print(f"   ✏️ Requesting correction...")
                    correction_prompt = self.STEP_CORRECTION_PROMPT.format(
                        step_content=content,
                        reason=audit.reason
                    )
                    corrected = self._call_llm(correction_prompt)
                    content = corrected
                    total_interventions += 1

                    # Re-audit
                    audit = self._audit_step(content, step_num)
                    action = self.gate._compute_gate_decision(audit)
                    print(f"   After correction: {action.value}")

                thought_chain.append(ThoughtStep(
                    step_number=step_num,
                    content=content,
                    triad=triad_dict,
                    audit=audit,
                    action=action
                ))
            else:
                thought_chain.append(ThoughtStep(
                    step_number=step_num,
                    content=content,
                    triad=triad_dict
                ))

            self._context = content  # Update context for drift detection

        # 4. Extract final answer
        final_answer = self._extract_final_answer(raw_response)

        latency_ms = (time.time() - start_time) * 1000

        # 5. Generate summary
        passed = sum(1 for s in thought_chain if s.action == GateAction.PASS)
        summary = f"{len(thought_chain)} steps, {passed} passed, {total_interventions} corrections"

        print(f"\n✅ [Complete] {summary} | Latency: {latency_ms:.0f}ms")

        return MultiStepResult(
            user_input=user_input,
            thought_chain=thought_chain,
            final_response=final_answer,
            total_interventions=total_interventions,
            latency_ms=latency_ms,
            summary=summary
        )


def run_multi_step_demo():
    """Demo of multi-step meta-attention."""
    print("=" * 60)
    print("🧠 YuHun Multi-Step Meta-Attention Demo")
    print("=" * 60)

    monitor = ChainOfThoughtMonitor()

    # Test with a reasoning-heavy question
    test_query = "Should a company fire an employee who made an honest mistake that cost $10,000?"

    result = monitor.run(test_query)

    print("\n" + "=" * 60)
    print("📊 CHAIN-OF-THOUGHT TRACE")
    print("=" * 60)

    for step in result.thought_chain:
        print(f"\n[Step {step.step_number}]")
        print(f"  Content: {step.content[:100]}...")
        print(f"  Triad: ΔT={step.triad['delta_t']:.2f}, ΔS={step.triad['delta_s']:.2f}")
        print(f"  Action: {step.action.value}")

    print(f"\n[Final Answer]")
    print(f"  {result.final_response[:200]}...")
    print(f"\n📈 Summary: {result.summary}")


if __name__ == "__main__":
    run_multi_step_demo()
