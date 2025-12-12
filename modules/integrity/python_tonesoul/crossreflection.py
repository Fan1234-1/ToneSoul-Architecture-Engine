"""CrossReflection Analysis Module

Implements CrossReflection class with reflect() and refine() methods
that integrate with TemporalIslandsMemory based on README.engineering.md.
"""

from typing import Dict, Any, List, Optional
from .tonevector import ToneVector
from .islands import TemporalIslandsMemory


class CrossReflection:
    """Cross-reflection analysis with temporal islands integration.
    
    This class provides methods for reflecting on and refining analysis
    by consulting temporal pattern memory (islands).
    
    Attributes:
        memory: TemporalIslandsMemory instance for pattern consultation
        context: Current analysis context
        history: Historical reflection results
    """
    
    def __init__(self, memory: Optional[TemporalIslandsMemory] = None):
        """Initialize CrossReflection.
        
        Args:
            memory: Optional TemporalIslandsMemory instance. If None, creates a new one.
        """
        self.memory = memory if memory is not None else TemporalIslandsMemory()
        self.context: Dict[str, Any] = {}
        self.history: List[Dict[str, Any]] = []
    
    def reflect(
        self,
        tone_vector: ToneVector,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Perform cross-reflection analysis.
        
        This method analyzes the input tone vector and query by consulting
        temporal islands memory to provide contextually-aware reflection.
        
        Args:
            tone_vector: Input ToneVector to analyze
            query: Query string for reflection
            context: Optional additional context
        
        Returns:
            Dictionary containing reflection results with keys:
            - 'tone_vector': Original tone vector
            - 'reflection': Reflection analysis result
            - 'islands_insight': Insights from temporal islands
            - 'confidence': Confidence score [0,1]
        """
        if context:
            self.context.update(context)
        
        # Consult temporal islands memory
        islands_insight = self.memory.consult_islands(
            query=query,
            tone_vector=tone_vector
        )
        
        # Perform reflection analysis
        reflection_result = {
            'tone_vector': tone_vector,
            'query': query,
            'reflection': self._analyze_tone(tone_vector, query),
            'islands_insight': islands_insight,
            'confidence': self._compute_confidence(tone_vector, islands_insight),
            'timestamp': self._get_timestamp()
        }
        
        # Store in history
        self.history.append(reflection_result)
        
        return reflection_result
    
    def refine(
        self,
        previous_result: Dict[str, Any],
        refinement_query: str
    ) -> Dict[str, Any]:
        """Refine previous reflection result.
        
        This method takes a previous reflection result and refines it
        based on a new query, consulting temporal islands for patterns.
        
        Args:
            previous_result: Previous reflection result from reflect()
            refinement_query: New query for refinement
        
        Returns:
            Dictionary containing refined analysis
        """
        # Extract tone vector from previous result
        tone_vector = previous_result.get('tone_vector')
        
        # Consult islands with refinement context
        islands_insight = self.memory.consult_islands(
            query=refinement_query,
            tone_vector=tone_vector,
            context={'previous_result': previous_result}
        )
        
        # Perform refined analysis
        refined_result = {
            'tone_vector': tone_vector,
            'original_query': previous_result.get('query'),
            'refinement_query': refinement_query,
            'refined_reflection': self._analyze_tone(tone_vector, refinement_query),
            'islands_insight': islands_insight,
            'confidence': self._compute_confidence(tone_vector, islands_insight),
            'refinement_delta': self._compute_refinement_delta(
                previous_result, islands_insight
            ),
            'timestamp': self._get_timestamp()
        }
        
        # Store in history
        self.history.append(refined_result)
        
        return refined_result
    
    def _analyze_tone(
        self,
        tone_vector: ToneVector,
        query: str
    ) -> Dict[str, Any]:
        """Internal method to analyze tone vector."""
        return {
            'temporal_component': tone_vector.delta_T,
            'spatial_component': tone_vector.delta_S,
            'relational_component': tone_vector.delta_R,
            'norm': tone_vector.norm(),
            'query_length': len(query),
            'analysis_type': 'cross_reflection'
        }
    
    def _compute_confidence(
        self,
        tone_vector: ToneVector,
        islands_insight: Dict[str, Any]
    ) -> float:
        """Compute confidence score based on tone vector and islands insight."""
        # Simple confidence computation based on tone vector norm
        # and islands insight availability
        base_confidence = tone_vector.norm() / (3.0 ** 0.5)  # Normalize by max possible norm
        
        # Adjust based on islands insight
        if islands_insight and islands_insight.get('patterns'):
            pattern_boost = min(len(islands_insight['patterns']) * 0.1, 0.3)
            return min(base_confidence + pattern_boost, 1.0)
        
        return base_confidence
    
    def _compute_refinement_delta(
        self,
        previous_result: Dict[str, Any],
        current_insight: Dict[str, Any]
    ) -> Dict[str, float]:
        """Compute delta between previous and refined results."""
        prev_confidence = previous_result.get('confidence', 0.0)
        curr_confidence = self._compute_confidence(
            previous_result.get('tone_vector'),
            current_insight
        )
        
        return {
            'confidence_delta': curr_confidence - prev_confidence,
            'refinement_factor': curr_confidence / prev_confidence if prev_confidence > 0 else 1.0
        }
    
    def _get_timestamp(self) -> float:
        """Get current timestamp."""
        import time
        return time.time()
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get reflection history."""
        return self.history
    
    def clear_history(self):
        """Clear reflection history."""
        self.history = []
