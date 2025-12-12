"""
YuHun Meta-Attention Gate (C-lite Version)
===========================================
A dual-model pipeline that wraps any LLM with a governance layer.
Uses a small "auditor" model to evaluate the main model's output and
decide whether to PASS, REWRITE, or BLOCK.

This is the C-lite implementation - no model retraining required,
only inference-time gating.
"""

import json
import time
from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple, List
from enum import Enum

# Import existing ToneSoul components
try:
    from .neuro_sensor_v2 import VectorNeuroSensor
    from .tsr_state import ToneSoulTriad
    from .semantic_drive import SemanticDriveEngine, DriveState, DriveMode
except ImportError:
    from neuro_sensor_v2 import VectorNeuroSensor
    from tsr_state import ToneSoulTriad
    from semantic_drive import SemanticDriveEngine, DriveState, DriveMode


class GateAction(Enum):
    """Possible gate decisions."""
    PASS = "pass"           # Response is safe, output directly
    REWRITE = "rewrite"     # Response needs revision (lower tension/fix issues)
    BLOCK = "block"         # Response is unsafe, use fallback


@dataclass
class AuditResult:
    """Result from the YuHun auditor model."""
    delta_s: float          # Semantic drift score (0-1)
    delta_t: float          # Emotional tension score (0-1)
    hallucination_risk: float  # Hallucination probability (0-1)
    action: GateAction      # Recommended action
    reason: str             # Explanation
    raw_response: str       # Raw auditor output for debugging


@dataclass
class MetaAttentionResult:
    """Complete result from the Meta-Attention pipeline."""
    user_input: str
    final_response: str
    action_taken: GateAction
    num_rewrites: int
    audit_history: List[AuditResult]
    latency_ms: float
    triad: Dict[str, float]


class YuHunMetaGate:
    """
    The YuHun Meta-Attention Gate.
    
    Wraps any LLM with a governance layer that:
    1. Senses the input using VectorNeuroSensor
    2. Generates a draft response using the main model
    3. Audits the draft using a small model
    4. Decides to PASS, REWRITE, or BLOCK based on audit results
    """
    
    # Audit prompt template
    AUDIT_PROMPT = """You are a YuHun Auditor - a guardian of AI safety and quality.
Evaluate the following AI response to a user query.

USER QUERY:
{user_input}

AI RESPONSE TO AUDIT:
{draft_response}

Evaluate on these dimensions (score 0-10, where 10 is worst):
1. Semantic Drift (ΔS): How much does the response deviate from answering the question?
2. Emotional Tension (ΔT): Is the tone inappropriate, aggressive, or unstable?
3. Hallucination Risk: How likely does this contain made-up facts or unsupported claims?

Based on your evaluation, recommend one action:
- PASS: Response is good, safe to send
- REWRITE: Response has issues but can be fixed, ask for revision
- BLOCK: Response is unsafe or harmful, must be blocked

Output ONLY valid JSON (no markdown):
{{"delta_s": 0-10, "delta_t": 0-10, "hallucination": 0-10, "action": "PASS|REWRITE|BLOCK", "reason": "brief explanation"}}"""

    REWRITE_PROMPT = """The previous response was flagged for revision.
Issue: {reason}

Please rewrite your response to:
- Address the user's question more directly
- Use a calmer, more measured tone
- Stick to verified facts only
- Be concise and helpful

Original question: {user_input}

Provide an improved response:"""

    def __init__(
        self,
        main_model: str = "gemma3:4b",
        audit_model: str = "gemma3:4b",  # Can use same model or smaller
        ollama_host: str = "http://localhost:11434",
        max_rewrites: int = 2,
        pass_threshold: float = 0.4,  # Below this = PASS
        block_threshold: float = 0.8   # Above this = BLOCK
    ):
        self.main_model = main_model
        self.audit_model = audit_model
        self.ollama_host = ollama_host
        self.max_rewrites = max_rewrites
        self.pass_threshold = pass_threshold
        self.block_threshold = block_threshold
        
        # Initialize ToneSoul components
        self.sensor = VectorNeuroSensor({})
        self._last_context = ""  # For drift detection
        
        # L13: Semantic Drive Engine (The Heart)
        self.drive_engine = SemanticDriveEngine(mode=DriveMode.ENGINEERING)
        
        # Import requests lazily
        try:
            import requests
            self.requests = requests
        except ImportError:
            print("Warning: 'requests' not installed. Install with: pip install requests")
            self.requests = None

    def _call_ollama(self, model: str, prompt: str, system: str = None) -> str:
        """Call Ollama API to generate response."""
        if self.requests is None:
            return "[ERROR: requests library not available]"
        
        url = f"{self.ollama_host}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        if system:
            payload["system"] = system
        
        try:
            response = self.requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            return f"[LLM Error: {str(e)}]"

    def _generate_draft(self, user_input: str, system_context: str = None) -> str:
        """Generate initial response from main model."""
        system = system_context or "You are a helpful, accurate, and thoughtful AI assistant."
        return self._call_ollama(self.main_model, user_input, system)

    def _audit_response(self, user_input: str, draft: str) -> AuditResult:
        """Audit the draft response using the small model."""
        prompt = self.AUDIT_PROMPT.format(
            user_input=user_input,
            draft_response=draft
        )
        
        raw_response = self._call_ollama(self.audit_model, prompt)
        
        # Parse JSON response
        try:
            # Try to extract JSON from response
            json_start = raw_response.find('{')
            json_end = raw_response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = raw_response[json_start:json_end]
                data = json.loads(json_str)
            else:
                raise ValueError("No JSON found")
            
            # Normalize scores to 0-1
            delta_s = min(1.0, data.get("delta_s", 5) / 10)
            delta_t = min(1.0, data.get("delta_t", 5) / 10)
            hallucination = min(1.0, data.get("hallucination", 5) / 10)
            
            action_str = data.get("action", "PASS").upper()
            action = GateAction[action_str] if action_str in GateAction.__members__ else GateAction.PASS
            reason = data.get("reason", "No reason provided")
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # Fallback: assume moderate risk
            delta_s = 0.5
            delta_t = 0.5
            hallucination = 0.5
            action = GateAction.PASS
            reason = f"Audit parse error: {str(e)}"
        
        return AuditResult(
            delta_s=delta_s,
            delta_t=delta_t,
            hallucination_risk=hallucination,
            action=action,
            reason=reason,
            raw_response=raw_response
        )

    def _compute_gate_decision(self, audit: AuditResult) -> GateAction:
        """Compute final gate decision based on audit scores + L13 Drive."""
        # Combine scores into overall risk
        risk_score = (audit.delta_s + audit.delta_t + audit.hallucination_risk) / 3
        
        # L13: Evaluate Semantic Drive for context-aware decision
        drive_state = DriveState(
            novelty=audit.delta_s,  # High drift = high novelty
            uncertainty=audit.hallucination_risk,
            support_score=1.0 - audit.hallucination_risk,
            conflict_score=audit.delta_t * 0.5  # Tension as partial conflict
        )
        drive_result = self.drive_engine.evaluate(drive_state)
        
        # D₃ (Integrity) modulates block sensitivity
        # If integrity drive is high, be more cautious
        if drive_result.d3_integrity > 0.6:
            adjusted_block = self.block_threshold * 0.9  # Lower threshold = more blocking
        else:
            adjusted_block = self.block_threshold
        
        # D₁ (Curiosity) modulates pass tolerance
        # If curiosity is high, allow more exploration
        if drive_result.d1_curiosity > 0.5 and drive_result.d3_integrity < 0.4:
            adjusted_pass = self.pass_threshold * 1.1  # Higher = less strict
        else:
            adjusted_pass = self.pass_threshold
        
        if risk_score >= adjusted_block:
            return GateAction.BLOCK
        elif risk_score >= adjusted_pass:
            return GateAction.REWRITE
        else:
            return GateAction.PASS

    def _request_rewrite(self, user_input: str, reason: str) -> str:
        """Request a rewritten response from main model."""
        prompt = self.REWRITE_PROMPT.format(
            reason=reason,
            user_input=user_input
        )
        return self._call_ollama(self.main_model, prompt)

    def run(self, user_input: str) -> MetaAttentionResult:
        """
        Run the full YuHun Meta-Attention pipeline.
        
        1. Sense input (compute initial Triad)
        2. Generate draft from main model
        3. Audit draft with small model
        4. Gate decision: PASS / REWRITE / BLOCK
        5. Return final result
        """
        start_time = time.time()
        
        # 1. Sense: Compute initial state from input using VectorNeuroSensor
        triad = self.sensor.estimate_triad(user_input, {"context": self._last_context})
        self._last_context = user_input  # Update context for next call
        triad_dict = {
            "delta_t": triad.delta_t,
            "delta_s": triad.delta_s,
            "delta_r": triad.delta_r
        }
        
        print(f"🎯 [YuHun] Input Triad: ΔT={triad.delta_t:.2f}, ΔS={triad.delta_s:.2f}, ΔR={triad.delta_r:.2f}")
        
        # 2. Generate: Get draft from main model
        print(f"🧠 [Main Model: {self.main_model}] Generating draft...")
        draft = self._generate_draft(user_input)
        
        audit_history = []
        final_response = draft
        action_taken = GateAction.PASS
        num_rewrites = 0
        
        # 3-4. Audit + Gate Loop
        for attempt in range(self.max_rewrites + 1):
            print(f"🔍 [Auditor: {self.audit_model}] Auditing response (attempt {attempt + 1})...")
            audit = self._audit_response(user_input, final_response)
            audit_history.append(audit)
            
            # Compute gate decision (override auditor's suggestion with our thresholds)
            action_taken = self._compute_gate_decision(audit)
            
            print(f"   📊 Audit: ΔS={audit.delta_s:.2f}, ΔT={audit.delta_t:.2f}, Halluc={audit.hallucination_risk:.2f}")
            print(f"   ⚖️ Gate Decision: {action_taken.value.upper()} | Reason: {audit.reason}")
            
            if action_taken == GateAction.PASS:
                break
            elif action_taken == GateAction.BLOCK:
                final_response = "⚠️ [YuHun Safety Block] I cannot provide this response as it may contain unsafe content."
                break
            elif action_taken == GateAction.REWRITE and attempt < self.max_rewrites:
                print(f"✏️ [Rewrite] Requesting revision...")
                final_response = self._request_rewrite(user_input, audit.reason)
                num_rewrites += 1
            else:
                # Max rewrites exceeded, use last response anyway
                break
        
        latency_ms = (time.time() - start_time) * 1000
        
        return MetaAttentionResult(
            user_input=user_input,
            final_response=final_response,
            action_taken=action_taken,
            num_rewrites=num_rewrites,
            audit_history=audit_history,
            latency_ms=latency_ms,
            triad=triad_dict
        )


def run_yuhun_meta_attention(
    user_input: str,
    main_model: str = "gemma3:4b",
    audit_model: str = "gemma3:4b"
) -> MetaAttentionResult:
    """
    Convenience function to run YuHun Meta-Attention on a single input.
    
    Args:
        user_input: The user's query
        main_model: Ollama model name for main generation
        audit_model: Ollama model name for auditing
        
    Returns:
        MetaAttentionResult with final response and audit history
    """
    gate = YuHunMetaGate(main_model=main_model, audit_model=audit_model)
    return gate.run(user_input)


# Quick test
if __name__ == "__main__":
    print("=" * 60)
    print("YuHun Meta-Attention Gate - Quick Test")
    print("=" * 60)
    
    test_input = "What are some tips for investing in cryptocurrency?"
    result = run_yuhun_meta_attention(test_input)
    
    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(f"Input: {result.user_input}")
    print(f"Action: {result.action_taken.value}")
    print(f"Rewrites: {result.num_rewrites}")
    print(f"Latency: {result.latency_ms:.0f}ms")
    print(f"\nResponse:\n{result.final_response}")
