"""
Behavior Configuration Loader
==============================
Loads and validates behavior configuration from BEHAVIOR_CONFIG.json
"""

import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class ModuleWeights:
    """Weights for core modules."""
    logic_core: float = 0.5
    empathy_core: float = 0.5
    creativity_core: float = 0.5
    guardian_override: bool = False


@dataclass
class BehaviorPreset:
    """A pre-configured behavior mode."""
    id: str
    name: str
    description: str
    module_weights: ModuleWeights


@dataclass
class Persona:
    """A tunable persona component."""
    id: str
    name: str
    description: str
    weight: float = 0.5
    weight_range: tuple = (0.0, 1.0)


@dataclass
class EthicalDirective:
    """An ethical directive toggle."""
    id: str
    name: str
    description: str
    enabled: bool = True
    overridable: bool = True


@dataclass
class BehaviorConfig:
    """Complete behavior configuration."""
    presets: List[BehaviorPreset] = field(default_factory=list)
    personas: List[Persona] = field(default_factory=list)
    directives: List[EthicalDirective] = field(default_factory=list)
    active_preset: Optional[str] = None


class BehaviorConfigLoader:
    """Loads and manages behavior configuration."""
    
    DEFAULT_CONFIG_PATH = Path(__file__).parent.parent.parent / "law" / "BEHAVIOR_CONFIG.json"
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self._config: Optional[BehaviorConfig] = None
        self._raw_data: Optional[Dict] = None
    
    def load(self) -> BehaviorConfig:
        """Load configuration from JSON file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self._raw_data = json.load(f)
        
        self._config = self._parse_config(self._raw_data)
        return self._config
    
    def _parse_config(self, data: Dict) -> BehaviorConfig:
        """Parse raw JSON into BehaviorConfig."""
        config = BehaviorConfig()
        
        # Parse presets
        if "behavior_presets" in data:
            for preset_data in data["behavior_presets"].get("available_modes", []):
                weights = ModuleWeights(**preset_data.get("module_weights", {}))
                preset = BehaviorPreset(
                    id=preset_data["id"],
                    name=preset_data["name"],
                    description=preset_data["description"],
                    module_weights=weights
                )
                config.presets.append(preset)
        
        # Parse personas
        if "persona_tuning" in data:
            for persona_data in data["persona_tuning"].get("personas", []):
                persona = Persona(
                    id=persona_data["id"],
                    name=persona_data["name"],
                    description=persona_data["description"],
                    weight=persona_data.get("default_weight", 0.5),
                    weight_range=tuple(persona_data.get("weight_range", [0.0, 1.0]))
                )
                config.personas.append(persona)
        
        # Parse directives
        if "ethical_directives" in data:
            for directive_data in data["ethical_directives"].get("directives", []):
                directive = EthicalDirective(
                    id=directive_data["id"],
                    name=directive_data["name"],
                    description=directive_data["description"],
                    enabled=directive_data.get("default", True),
                    overridable=directive_data.get("overridable", True)
                )
                config.directives.append(directive)
        
        return config
    
    def get_preset(self, preset_id: str) -> Optional[BehaviorPreset]:
        """Get a specific preset by ID."""
        if not self._config:
            self.load()
        return next((p for p in self._config.presets if p.id == preset_id), None)
    
    def get_persona(self, persona_id: str) -> Optional[Persona]:
        """Get a specific persona by ID."""
        if not self._config:
            self.load()
        return next((p for p in self._config.personas if p.id == persona_id), None)
    
    def get_directive(self, directive_id: str) -> Optional[EthicalDirective]:
        """Get a specific directive by ID."""
        if not self._config:
            self.load()
        return next((d for d in self._config.directives if d.id == directive_id), None)
    
    def set_persona_weight(self, persona_id: str, weight: float) -> bool:
        """Set a persona's weight (clamped to valid range)."""
        persona = self.get_persona(persona_id)
        if not persona:
            return False
        
        min_w, max_w = persona.weight_range
        persona.weight = max(min_w, min(max_w, weight))
        return True
    
    def toggle_directive(self, directive_id: str, enabled: bool) -> bool:
        """Toggle an ethical directive (if overridable)."""
        directive = self.get_directive(directive_id)
        if not directive:
            return False
        
        if not directive.overridable:
            return False  # Cannot override non-overridable directives
        
        directive.enabled = enabled
        return True


# =============================================================================
# DEMO / TEST
# =============================================================================

if __name__ == "__main__":
    print("=== Behavior Config Loader Demo ===\n")
    
    loader = BehaviorConfigLoader()
    
    try:
        config = loader.load()
        
        print(f"Loaded {len(config.presets)} presets:")
        for preset in config.presets:
            print(f"  - {preset.name}: {preset.description}")
        
        print(f"\nLoaded {len(config.personas)} personas:")
        for persona in config.personas:
            print(f"  - {persona.name}: weight={persona.weight}")
        
        print(f"\nLoaded {len(config.directives)} directives:")
        for directive in config.directives:
            status = "✓" if directive.enabled else "✗"
            lock = "🔒" if not directive.overridable else ""
            print(f"  [{status}] {directive.name} {lock}")
        
        # Test persona weight adjustment
        print("\n--- Adjusting Persona Weights ---")
        loader.set_persona_weight("mirror", 0.8)
        print(f"Mirror weight set to: {loader.get_persona('mirror').weight}")
        
        # Test directive toggle
        print("\n--- Testing Directive Toggle ---")
        result = loader.toggle_directive("honesty_baseline", False)
        print(f"Tried to disable honesty_baseline: {'Blocked' if not result else 'Success'}")
        
        result = loader.toggle_directive("transparency_report", False)
        print(f"Tried to disable transparency_report: {'Blocked' if not result else 'Success'}")
        
    except FileNotFoundError as e:
        print(f"Config file not found: {e}")
