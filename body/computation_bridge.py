"""
YuHun Computation Bridge v1.0
=============================
Verifiable Semantic Engine — AI generates structure, Computer verifies.

Core Principle:
- Language Layer (AI): Generate semantic structure and reasoning steps
- Logic Layer (Rules): Map language to formal logic
- Compute Layer (SymPy): Mathematical verification
- Audit Layer (Ledger): Record every step

Author: 黃梵威 + Antigravity
Date: 2025-12-09
Version: 1.0.0
"""

import json
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable, Tuple
from datetime import datetime
from enum import Enum

# Try to import SymPy for computation
try:
    import sympy
    from sympy import Symbol, solve, diff, simplify, Eq, sympify
    from sympy.parsing.sympy_parser import parse_expr
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False


class StepType(Enum):
    """Types of reasoning steps."""
    DEFINE = "define"          # Define variable or goal
    COMPUTE = "compute"        # Mathematical calculation
    VERIFY = "verify"          # Verification check
    DERIVE = "derive"          # Logical derivation
    CONCLUDE = "conclude"      # Final conclusion


class VerificationStatus(Enum):
    """Status of verification."""
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ReasoningStep:
    """A single step in the Chain-of-Truth."""
    step_id: str
    step_type: StepType
    
    # Language layer (AI generated)
    natural_language: str
    
    # Logic layer (rule-based mapping)
    formal_expression: Optional[str] = None
    
    # Compute layer (SymPy result)
    computed_result: Optional[str] = None
    
    # Verification
    verification_status: VerificationStatus = VerificationStatus.PENDING
    verification_message: str = ""
    
    # Metadata
    timestamp: str = ""
    delta_s: float = 0.0  # Semantic drift of this step
    delta_r: float = 0.0  # Risk of this step
    
    # Hash for audit chain
    content_hash: str = ""
    previous_hash: str = ""
    
    def compute_hash(self) -> str:
        """Compute hash of step content."""
        content = f"{self.step_id}:{self.natural_language}:{self.formal_expression}:{self.computed_result}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "type": self.step_type.value,
            "language": self.natural_language,
            "formal": self.formal_expression,
            "result": self.computed_result,
            "status": self.verification_status.value,
            "message": self.verification_message,
            "hash": self.content_hash,
            "prev_hash": self.previous_hash
        }


@dataclass
class ChainOfTruth:
    """A complete reasoning chain with audit trail."""
    chain_id: str
    goal: str
    steps: List[ReasoningStep] = field(default_factory=list)
    final_result: Optional[str] = None
    overall_status: VerificationStatus = VerificationStatus.PENDING
    
    # Metrics
    total_steps: int = 0
    verified_steps: int = 0
    failed_steps: int = 0
    
    def add_step(self, step: ReasoningStep) -> None:
        """Add a step to the chain with hash linking."""
        if self.steps:
            step.previous_hash = self.steps[-1].content_hash
        else:
            step.previous_hash = "genesis"
        
        step.content_hash = step.compute_hash()
        step.timestamp = datetime.now().isoformat()
        self.steps.append(step)
        self.total_steps += 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "chain_id": self.chain_id,
            "goal": self.goal,
            "steps": [s.to_dict() for s in self.steps],
            "final_result": self.final_result,
            "status": self.overall_status.value,
            "metrics": {
                "total": self.total_steps,
                "verified": self.verified_steps,
                "failed": self.failed_steps,
                "ratio": self.verified_steps / max(self.total_steps, 1)
            }
        }


class ComputationBridge:
    """
    Bridge between AI language and computer computation.
    
    Implements the Verifiable Semantic Engine:
    1. AI proposes reasoning steps (natural language)
    2. Rules map to formal expressions
    3. SymPy/Computer verifies computations
    4. All steps recorded to audit chain
    """
    
    def __init__(self):
        self.current_chain: Optional[ChainOfTruth] = None
        self.variables: Dict[str, Any] = {}  # SymPy symbols
        self.expressions: Dict[str, Any] = {}  # Named expressions
        
        if not SYMPY_AVAILABLE:
            print("⚠️ SymPy not installed. Computation verification limited.")
    
    def start_chain(self, chain_id: str, goal: str) -> ChainOfTruth:
        """Start a new Chain-of-Truth."""
        self.current_chain = ChainOfTruth(chain_id=chain_id, goal=goal)
        self.variables = {}
        self.expressions = {}
        return self.current_chain
    
    def define_variable(self, name: str, description: str) -> ReasoningStep:
        """Define a variable (language → symbol)."""
        step = ReasoningStep(
            step_id=f"step_{len(self.current_chain.steps) + 1}",
            step_type=StepType.DEFINE,
            natural_language=f"Let {name} be {description}"
        )
        
        if SYMPY_AVAILABLE:
            self.variables[name] = Symbol(name)
            step.formal_expression = f"Symbol('{name}')"
            step.verification_status = VerificationStatus.PASSED
            step.verification_message = f"Variable {name} defined"
        else:
            step.verification_status = VerificationStatus.SKIPPED
            step.verification_message = "SymPy not available"
        
        self.current_chain.add_step(step)
        return step
    
    def define_expression(
        self, 
        name: str, 
        expr_str: str, 
        description: str
    ) -> ReasoningStep:
        """Define an expression (language → formal expression)."""
        step = ReasoningStep(
            step_id=f"step_{len(self.current_chain.steps) + 1}",
            step_type=StepType.DEFINE,
            natural_language=description,
            formal_expression=expr_str
        )
        
        if SYMPY_AVAILABLE:
            try:
                # Parse expression with defined symbols
                expr = parse_expr(expr_str, local_dict=self.variables)
                self.expressions[name] = expr
                step.verification_status = VerificationStatus.PASSED
                step.verification_message = f"Expression parsed: {expr}"
            except Exception as e:
                step.verification_status = VerificationStatus.FAILED
                step.verification_message = f"Parse error: {e}"
        else:
            step.verification_status = VerificationStatus.SKIPPED
        
        self.current_chain.add_step(step)
        return step
    
    def compute(
        self, 
        operation: str, 
        expr_name: str, 
        description: str,
        **kwargs
    ) -> ReasoningStep:
        """
        Perform a computation.
        
        Operations: evaluate, solve, differentiate, simplify
        """
        step = ReasoningStep(
            step_id=f"step_{len(self.current_chain.steps) + 1}",
            step_type=StepType.COMPUTE,
            natural_language=description
        )
        
        if not SYMPY_AVAILABLE:
            step.verification_status = VerificationStatus.SKIPPED
            step.verification_message = "SymPy not available"
            self.current_chain.add_step(step)
            return step
        
        expr = self.expressions.get(expr_name)
        if expr is None:
            step.verification_status = VerificationStatus.FAILED
            step.verification_message = f"Expression '{expr_name}' not found"
            self.current_chain.add_step(step)
            return step
        
        try:
            if operation == "evaluate":
                # Evaluate at specific point
                point = kwargs.get("point", {})
                result = expr.subs(point)
                step.formal_expression = f"{expr_name}.subs({point})"
                step.computed_result = str(result)
                step.verification_status = VerificationStatus.PASSED
                
            elif operation == "solve":
                # Solve equation
                var_name = kwargs.get("variable", "x")
                var = self.variables.get(var_name)
                if var:
                    solutions = solve(expr, var)
                    step.formal_expression = f"solve({expr_name}, {var_name})"
                    step.computed_result = str(solutions)
                    step.verification_status = VerificationStatus.PASSED
                    
            elif operation == "differentiate":
                var_name = kwargs.get("variable", "x")
                var = self.variables.get(var_name)
                if var:
                    derivative = diff(expr, var)
                    result_name = f"{expr_name}_prime"
                    self.expressions[result_name] = derivative
                    step.formal_expression = f"diff({expr_name}, {var_name})"
                    step.computed_result = str(derivative)
                    step.verification_status = VerificationStatus.PASSED
                    
            elif operation == "simplify":
                simplified = simplify(expr)
                step.formal_expression = f"simplify({expr_name})"
                step.computed_result = str(simplified)
                step.verification_status = VerificationStatus.PASSED
                
            else:
                step.verification_status = VerificationStatus.FAILED
                step.verification_message = f"Unknown operation: {operation}"
                
        except Exception as e:
            step.verification_status = VerificationStatus.FAILED
            step.verification_message = f"Computation error: {e}"
        
        self.current_chain.add_step(step)
        self._update_chain_metrics()
        return step
    
    def verify(
        self, 
        claim: str, 
        check_expr: str,
        description: str
    ) -> ReasoningStep:
        """Verify a claim by evaluating an expression."""
        step = ReasoningStep(
            step_id=f"step_{len(self.current_chain.steps) + 1}",
            step_type=StepType.VERIFY,
            natural_language=description,
            formal_expression=check_expr
        )
        
        if SYMPY_AVAILABLE:
            try:
                result = parse_expr(check_expr, local_dict={
                    **self.variables,
                    **self.expressions
                })
                step.computed_result = str(result)
                
                # Check if result is True/truthy
                if result == True or result == sympy.true or result == 0:
                    step.verification_status = VerificationStatus.PASSED
                    step.verification_message = f"Claim verified: {claim}"
                else:
                    step.verification_status = VerificationStatus.FAILED
                    step.verification_message = f"Claim not verified. Result: {result}"
                    
            except Exception as e:
                step.verification_status = VerificationStatus.FAILED
                step.verification_message = f"Verification error: {e}"
        else:
            step.verification_status = VerificationStatus.SKIPPED
        
        self.current_chain.add_step(step)
        self._update_chain_metrics()
        return step
    
    def conclude(self, conclusion: str, final_result: str) -> ReasoningStep:
        """Add final conclusion to the chain."""
        step = ReasoningStep(
            step_id=f"step_{len(self.current_chain.steps) + 1}",
            step_type=StepType.CONCLUDE,
            natural_language=conclusion,
            computed_result=final_result
        )
        
        # Check if all previous steps passed
        all_passed = all(
            s.verification_status in (VerificationStatus.PASSED, VerificationStatus.SKIPPED)
            for s in self.current_chain.steps
        )
        
        if all_passed:
            step.verification_status = VerificationStatus.PASSED
            step.verification_message = "Conclusion verified by chain"
            self.current_chain.overall_status = VerificationStatus.PASSED
        else:
            step.verification_status = VerificationStatus.FAILED
            step.verification_message = "Chain contains failed steps"
            self.current_chain.overall_status = VerificationStatus.FAILED
        
        self.current_chain.add_step(step)
        self.current_chain.final_result = final_result
        self._update_chain_metrics()
        return step
    
    def _update_chain_metrics(self):
        """Update chain verification metrics."""
        self.current_chain.verified_steps = sum(
            1 for s in self.current_chain.steps 
            if s.verification_status == VerificationStatus.PASSED
        )
        self.current_chain.failed_steps = sum(
            1 for s in self.current_chain.steps 
            if s.verification_status == VerificationStatus.FAILED
        )
    
    def get_verification_ratio(self) -> float:
        """Get ratio of verified steps."""
        if not self.current_chain or self.current_chain.total_steps == 0:
            return 1.0
        return self.current_chain.verified_steps / self.current_chain.total_steps
    
    def export_chain(self) -> Dict[str, Any]:
        """Export current chain as dictionary."""
        if self.current_chain:
            return self.current_chain.to_dict()
        return {}


# ═══════════════════════════════════════════════════════════
# Convenience Functions
# ═══════════════════════════════════════════════════════════

def solve_polynomial_roots(expr_str: str, variable: str = "x") -> Dict[str, Any]:
    """
    Solve for roots of a polynomial.
    
    Example: solve_polynomial_roots("x**3 - 2*x + 1", "x")
    """
    bridge = ComputationBridge()
    
    # Start chain
    chain = bridge.start_chain("poly_solve", f"Find all real roots of {expr_str}")
    
    # Define variable
    bridge.define_variable(variable, "the variable to solve for")
    
    # Define expression
    bridge.define_expression("f", expr_str, f"Define f({variable}) = {expr_str}")
    
    # Find derivative
    bridge.compute("differentiate", "f", "Find critical points via derivative", variable=variable)
    
    # Solve for roots
    bridge.compute("solve", "f", "Solve f(x) = 0", variable=variable)
    
    # Get result
    solutions = bridge.expressions.get("f")
    if SYMPY_AVAILABLE and solutions:
        from sympy import solve as sympy_solve
        roots = sympy_solve(solutions, bridge.variables[variable])
        result_str = str(roots)
    else:
        result_str = "Requires SymPy"
    
    # Conclude
    bridge.conclude(f"The roots of {expr_str} are:", result_str)
    
    return bridge.export_chain()


def demo_computation_bridge():
    """Demo of Computation Bridge."""
    print("=" * 60)
    print("YuHun Computation Bridge v1.0 Demo")
    print("=" * 60)
    
    if not SYMPY_AVAILABLE:
        print("\n⚠️ SymPy not installed. Install with: pip install sympy")
        print("Demo will run with limited functionality.\n")
    
    # Demo: Solve f(x) = x³ - 2x + 1
    print("\n--- Example: Find roots of f(x) = x³ - 2x + 1 ---\n")
    
    bridge = ComputationBridge()
    
    # Start chain
    chain = bridge.start_chain("demo_1", "Find all real roots of f(x) = x³ - 2x + 1")
    
    # Step 1: Define variable
    step1 = bridge.define_variable("x", "the independent variable")
    print(f"Step 1: {step1.natural_language}")
    print(f"        Status: {step1.verification_status.value}")
    
    # Step 2: Define function
    step2 = bridge.define_expression("f", "x**3 - 2*x + 1", "Define f(x) = x³ - 2x + 1")
    print(f"Step 2: {step2.natural_language}")
    print(f"        Formal: {step2.formal_expression}")
    print(f"        Status: {step2.verification_status.value}")
    
    # Step 3: Evaluate at test points
    step3 = bridge.compute("evaluate", "f", "Check f(0)", point={"x": 0})
    print(f"Step 3: {step3.natural_language}")
    print(f"        Result: f(0) = {step3.computed_result}")
    
    step4 = bridge.compute("evaluate", "f", "Check f(1)", point={"x": 1})
    print(f"Step 4: {step4.natural_language}")
    print(f"        Result: f(1) = {step4.computed_result}")
    
    # Step 5: Find derivative
    step5 = bridge.compute("differentiate", "f", "Find f'(x) to locate critical points", variable="x")
    print(f"Step 5: {step5.natural_language}")
    print(f"        Result: f'(x) = {step5.computed_result}")
    
    # Step 6: Solve for roots
    step6 = bridge.compute("solve", "f", "Solve f(x) = 0 for all roots", variable="x")
    print(f"Step 6: {step6.natural_language}")
    print(f"        Roots: {step6.computed_result}")
    
    # Step 7: Conclude
    step7 = bridge.conclude(
        "The polynomial has the following roots:",
        step6.computed_result or "Could not compute"
    )
    print(f"\nConclusion: {step7.natural_language}")
    print(f"            {step7.computed_result}")
    print(f"            Chain Status: {chain.overall_status.value}")
    
    # Print chain summary
    print("\n" + "=" * 60)
    print("Chain of Truth Summary")
    print("=" * 60)
    print(f"Total Steps: {chain.total_steps}")
    print(f"Verified:    {chain.verified_steps}")
    print(f"Failed:      {chain.failed_steps}")
    print(f"Ratio:       {bridge.get_verification_ratio():.2%}")
    
    # Print hash chain
    print("\n--- Audit Chain (Hash Links) ---")
    for step in chain.steps[:5]:
        print(f"  {step.step_id}: {step.content_hash} ← {step.previous_hash}")


if __name__ == "__main__":
    demo_computation_bridge()
