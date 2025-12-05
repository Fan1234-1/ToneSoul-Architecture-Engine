import json
import os
import random
from dataclasses import dataclass, asdict, field
from typing import Dict, Any

@dataclass
class Genes:
    # Cognitive Weights
    w_tension: float = 0.33
    w_satisfaction: float = 0.33
    w_reality: float = 0.33
    
    # Thresholds
    max_tension: float = 0.8
    dream_latency: float = 10.0
    consolidation_interval: float = 30.0
    
    # Metabolic Rates
    base_burn_rate: float = 0.1
    deep_thought_cost: float = 2.0
    
    # Personality
    curiosity: float = 0.5 # Probability of hunting/exploring
    caution: float = 0.5   # Probability of Guardian blocking

@dataclass
class ToneSoulDNA:
    """
    ES (Evolutionary Strategy) - DNA Module.
    Manages the genetic parameters of ToneSoul and handles mutation/evolution.
    """
    generation: int = 0
    genes: Genes = field(default_factory=Genes)
    parent_id: str = "Genesis"
    mutation_rate: float = 0.05
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        genes_data = data.pop("genes", {})
        dna = cls(**data)
        dna.genes = Genes(**genes_data)
        return dna
        
    def save(self, filepath: str):
        with open(filepath, "w") as f:
            f.write(self.to_json())
            
    @classmethod
    def load(cls, filepath: str):
        if not os.path.exists(filepath):
            return cls()
        with open(filepath, "r") as f:
            return cls.from_json(f.read())

    def mutate(self):
        """
        Applies random mutations to genes based on mutation_rate.
        """
        print(f"🧬 [Evolution] Mutating DNA (Gen {self.generation} -> {self.generation + 1})...")
        self.generation += 1
        
        # Helper to mutate a value within bounds
        def mutate_val(val, rate, min_v, max_v):
            change = val * random.uniform(-rate, rate)
            return max(min_v, min(max_v, val + change))
            
        g = self.genes
        
        # Mutate Weights (Normalize later if needed, but for now let them drift)
        g.w_tension = mutate_val(g.w_tension, self.mutation_rate, 0.1, 0.9)
        g.w_satisfaction = mutate_val(g.w_satisfaction, self.mutation_rate, 0.1, 0.9)
        g.w_reality = mutate_val(g.w_reality, self.mutation_rate, 0.1, 0.9)
        
        # Mutate Thresholds
        g.max_tension = mutate_val(g.max_tension, self.mutation_rate, 0.5, 0.95)
        g.dream_latency = mutate_val(g.dream_latency, self.mutation_rate, 5.0, 60.0)
        g.consolidation_interval = mutate_val(g.consolidation_interval, self.mutation_rate, 10.0, 300.0)
        
        # Mutate Personality
        g.curiosity = mutate_val(g.curiosity, self.mutation_rate, 0.1, 1.0)
        g.caution = mutate_val(g.caution, self.mutation_rate, 0.1, 1.0)
        
        print(f"🧬 [Evolution] Mutation Complete. New Curiosity: {g.curiosity:.2f}, Caution: {g.caution:.2f}")

