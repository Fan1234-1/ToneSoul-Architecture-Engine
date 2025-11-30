"""
Genesis Layer (from Genesis-ChainSet)
-------------------------------------
Responsible for bootstrapping the ToneSoul system with initial state,
configuration, and 'genetic' memory.
"""

import json
import os
from typing import Dict, Any

class GenesisLoader:
    def __init__(self, genesis_path: str):
        self.genesis_path = genesis_path
        self._config: Dict[str, Any] = {}

    def load(self) -> Dict[str, Any]:
        """
        Loads the genesis block (configuration).
        In a real scenario, this might verify a cryptographic signature
        of the genesis file to ensure it hasn't been tampered with.
        """
        if not os.path.exists(self.genesis_path):
            return self._create_default_genesis()
            
        try:
            with open(self.genesis_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            print(f"Genesis Block loaded from {self.genesis_path}")
            return self._config
        except Exception as e:
            print(f"Failed to load Genesis Block: {e}")
            return self._create_default_genesis()

    def _create_default_genesis(self) -> Dict[str, Any]:
        """Returns a default 'Seed' state."""
        return {
            "version": "0.1.0",
            "timestamp": 0,
            "persona": {
                "name": "ToneSoul",
                "archetype": "Guardian",
                "traits": ["Rational", "Benevolent", "Cautious"]
            },
            "parameters": {
                "default_tension": 0.0,
                "learning_rate": 0.01
            }
        }
