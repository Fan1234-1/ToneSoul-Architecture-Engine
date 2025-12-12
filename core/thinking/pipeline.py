from typing import Dict, Any, List
from .base import OperatorContext, OperationResult
from .operators import (
    OpAbstraction, OpReverseEngineering, OpCrossDomainTranslation,
    OpForking, OpStructuralRebuild, OpCrossScenarioMapping, OpGroundingCompiler
)

class ThinkingPipeline:
    """
    Orchestrator for Thinking Operators.
    Manages the flow of cognition through different 'Monster Pipelines'.
    """
    
    def __init__(self):
        self.operators = {
            "ABSTRACTION": OpAbstraction(),
            "REVERSE_ENGINEERING": OpReverseEngineering(),
            "CROSS_DOMAIN_TRANSLATION": OpCrossDomainTranslation(),
            "FORKING": OpForking(),
            "STRUCTURAL_REBUILD": OpStructuralRebuild(),
            "CROSS_SCENARIO_MAPPING": OpCrossScenarioMapping(),
            "GROUNDING_COMPILER": OpGroundingCompiler()
        }

    def execute_pipeline(self, context: OperatorContext, p_level: str = "P1") -> Dict[str, Any]:
        """
        Executes a sequence of operators based on the pipeline level.
        
        Args:
            context: The initial context.
            p_level: The pipeline definition (e.g., 'P1', 'FULL_MONSTER').
            
        Returns:
            A dictionary containing results from all executed operators.
        """
        print(f"🧠 ThinkingPipeline: Activating {p_level}...")
        results = {}
        
        pipeline_steps = []
        
        if p_level == "P1": # Ethical Friction / Refusal Analysis
            pipeline_steps = ["ABSTRACTION", "REVERSE_ENGINEERING", "GROUNDING_COMPILER"]
            
        elif p_level == "FULL_MONSTER": # The "7+1" Strategy
            pipeline_steps = [
                "ABSTRACTION", 
                "REVERSE_ENGINEERING", 
                "CROSS_DOMAIN_TRANSLATION", 
                "FORKING", 
                "CROSS_SCENARIO_MAPPING", 
                "STRUCTURAL_REBUILD", 
                "GROUNDING_COMPILER"
            ]

        elif p_level == "COUNCIL_DEBATE": # The AGI Pioneer Council
            print("  🏛️ Convening the Council of Giants...")
            
            # 1. Define the Problem
            res_abs = self.operators["ABSTRACTION"].execute(context)
            results["abstraction"] = res_abs.output
            
            # 2. Hear from the Giants (Parallel Execution Concept)
            council_members = ["Schmidhuber", "Sutskever", "LeCun", "Hassabis"]
            debate_minutes = {}
            
            for member in council_members:
                # Create a temporary context with the persona
                member_ctx = OperatorContext(
                    input_text=context.input_text,
                    system_metrics={**context.system_metrics, "persona": member},
                    history=context.history
                )
                op = self.operators["CROSS_SCENARIO_MAPPING"]
                print(f"  -> 🗣️ {member} takes the floor...")
                res = op.execute(member_ctx)
                debate_minutes[member] = res.output
                
            results["council_debate"] = debate_minutes
            
            # 3. Synthesize
            res_ground = self.operators["GROUNDING_COMPILER"].execute(context)
            results["synthesis"] = res_ground.output
            
            return {
                "pipeline": p_level,
                "results": results,
                "status": "Council Adjourned"
            }
            
        else: # Default single step
            pipeline_steps = ["ABSTRACTION"]

        # Execute steps sequentially (for standard pipelines)
        current_context = context
        for step_id in pipeline_steps:
            operator = self.operators.get(step_id)
            if operator:
                print(f"  -> Running Operator: {step_id}")
                res = operator.execute(current_context)
                results[step_id.lower()] = res.output
                # Update context for next step (conceptually)
                # In a real system, we'd merge the output into the context
                
        return {
            "pipeline": p_level,
            "results": results,
            "status": "Complete"
        }
