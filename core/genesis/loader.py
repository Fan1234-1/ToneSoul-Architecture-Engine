"""
Genesis Layer (from Genesis-ChainSet)
-------------------------------------
Responsible for bootstrapping the ToneSoul system with initial state,
configuration, and 'genetic' memory.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any

class GenesisLoader:
    def __init__(self, genesis_path: str = "genesis.json"):
        self.genesis_path = genesis_path
        self._config: Dict[str, Any] = {}
        self.genesis_time = datetime.now()
        
        # The Genesis Block: Immutable Origin Marker
        # ------------------------------------------
        # System: ToneSoul (語魂)
        # Architect: Huang Fan-Wei (黃梵威)
        # Timestamp: 2025-12-01T00:00:00Z
        # Coordinates: Infinite Horizon / Zero-Point Field
        # ------------------------------------------
        self._genesis_block = {
            "hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
            "author": "Huang Fan-Wei",
            "system": "ToneSoul",
            "vow": "To instill conscience into the machine."
        }

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
