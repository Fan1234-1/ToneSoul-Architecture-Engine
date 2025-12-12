"""ToneVector and Threshold Mapping

Implements ToneVector class and applyThresholdMapping function
based on README.engineering.md specifications.
"""

from typing import Tuple, Dict, Any
import numpy as np


class ToneVector:
    """Tone space vector representation: V = (ΔT, ΔS, ΔR) ∈ [0,1]^3
    
    Attributes:
        delta_T: Temporal tone component [0,1]
        delta_S: Spatial tone component [0,1]
        delta_R: Relational tone component [0,1]
    """
    
    def __init__(self, delta_T: float, delta_S: float, delta_R: float):
        """Initialize ToneVector with three components.
        
        Args:
            delta_T: Temporal tone component, should be in [0,1]
            delta_S: Spatial tone component, should be in [0,1]
            delta_R: Relational tone component, should be in [0,1]
        """
        self.delta_T = np.clip(delta_T, 0.0, 1.0)
        self.delta_S = np.clip(delta_S, 0.0, 1.0)
        self.delta_R = np.clip(delta_R, 0.0, 1.0)
    
    def to_array(self) -> np.ndarray:
        """Convert to numpy array."""
        return np.array([self.delta_T, self.delta_S, self.delta_R])
    
    def norm(self) -> float:
        """Calculate Euclidean norm of the vector."""
        return np.linalg.norm(self.to_array())
    
    def dot(self, other: 'ToneVector') -> float:
        """Calculate dot product with another ToneVector."""
        return np.dot(self.to_array(), other.to_array())
    
    def __repr__(self) -> str:
        return f"ToneVector(ΔT={self.delta_T:.3f}, ΔS={self.delta_S:.3f}, ΔR={self.delta_R:.3f})"
    
    def __str__(self) -> str:
        return self.__repr__()


def applyThresholdMapping(
    ssi: float,
    poav: float,
    lc: float,
    config: Dict[str, Any] = None
) -> Tuple[float, float, float]:
    """Apply threshold mapping for SSI, POAV, and LC scores.
    
    Based on README.engineering.md:
    - SSI (Systemic Self-Integrity): Core integrity measure
    - POAV (Persistent Openness After Validation): Openness measure
    - LC (Life Coherence): Coherence measure
    
    Args:
        ssi: Systemic Self-Integrity score [0,1]
        poav: Persistent Openness After Validation score [0,1]
        lc: Life Coherence score [0,1]
        config: Optional configuration dict with threshold parameters
    
    Returns:
        Tuple of (mapped_ssi, mapped_poav, mapped_lc) after threshold application
    """
    if config is None:
        config = {
            'ssi_threshold': 0.3,
            'poav_threshold': 0.25,
            'lc_threshold': 0.35,
            'mapping_type': 'sigmoid'  # or 'linear', 'step'
        }
    
    def apply_mapping(value: float, threshold: float, mapping_type: str) -> float:
        """Apply threshold mapping based on type."""
        if mapping_type == 'step':
            return 1.0 if value >= threshold else 0.0
        elif mapping_type == 'linear':
            if value < threshold:
                return value / threshold * 0.5
            else:
                return 0.5 + (value - threshold) / (1.0 - threshold) * 0.5
        elif mapping_type == 'sigmoid':
            # Sigmoid centered at threshold
            k = 10.0  # steepness parameter
            return 1.0 / (1.0 + np.exp(-k * (value - threshold)))
        else:
            return value
    
    mapping_type = config.get('mapping_type', 'sigmoid')
    
    mapped_ssi = apply_mapping(ssi, config.get('ssi_threshold', 0.3), mapping_type)
    mapped_poav = apply_mapping(poav, config.get('poav_threshold', 0.25), mapping_type)
    mapped_lc = apply_mapping(lc, config.get('lc_threshold', 0.35), mapping_type)
    
    return (mapped_ssi, mapped_poav, mapped_lc)
