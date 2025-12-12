"""TemporalIslandsMemory Module

Implements TemporalIslandsMemory class with consult_islands() API
based on README.engineering.md specifications.
"""

from typing import Dict, Any, List, Optional, Tuple
from .tonevector import ToneVector
import time


class Island:
    """Represents a temporal pattern island.
    
    Attributes:
        pattern_id: Unique identifier for the pattern
        tone_signature: ToneVector signature of the pattern
        timestamp: Creation timestamp
        frequency: Frequency of pattern occurrence
        context: Associated context data
    """
    
    def __init__(
        self,
        pattern_id: str,
        tone_signature: ToneVector,
        context: Dict[str, Any] = None
    ):
        self.pattern_id = pattern_id
        self.tone_signature = tone_signature
        self.timestamp = time.time()
        self.frequency = 1
        self.context = context or {}
        self.last_accessed = self.timestamp
    
    def update_access(self):
        """Update last access timestamp and increment frequency."""
        self.last_accessed = time.time()
        self.frequency += 1
    
    def similarity(
        self,
        other_tone: ToneVector,
        weight: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    ) -> float:
        """Calculate weighted similarity with another tone vector."""
        delta_T = abs(self.tone_signature.delta_T - other_tone.delta_T) * weight[0]
        delta_S = abs(self.tone_signature.delta_S - other_tone.delta_S) * weight[1]
        delta_R = abs(self.tone_signature.delta_R - other_tone.delta_R) * weight[2]
        
        # Inverse distance as similarity (normalized)
        distance = (delta_T + delta_S + delta_R) / sum(weight)
        return 1.0 - min(distance, 1.0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert island to dictionary representation."""
        return {
            'pattern_id': self.pattern_id,
            'tone_signature': str(self.tone_signature),
            'timestamp': self.timestamp,
            'frequency': self.frequency,
            'last_accessed': self.last_accessed,
            'context': self.context
        }


class TemporalIslandsMemory:
    """Temporal pattern memory system using islands metaphor.
    
    This class maintains a collection of temporal pattern "islands"
    that can be consulted for pattern matching and insight retrieval.
    
    Attributes:
        islands: Dictionary of pattern islands keyed by pattern_id
        max_islands: Maximum number of islands to maintain
        similarity_threshold: Minimum similarity for pattern matching
    """
    
    def __init__(
        self,
        max_islands: int = 1000,
        similarity_threshold: float = 0.6
    ):
        """Initialize TemporalIslandsMemory.
        
        Args:
            max_islands: Maximum number of islands to maintain
            similarity_threshold: Minimum similarity threshold for matching
        """
        self.islands: Dict[str, Island] = {}
        self.max_islands = max_islands
        self.similarity_threshold = similarity_threshold
        self.query_count = 0
    
    def consult_islands(
        self,
        query: str,
        tone_vector: ToneVector,
        context: Optional[Dict[str, Any]] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """Consult temporal islands for pattern insights.
        
        This is the primary API for querying the temporal islands memory.
        It finds similar patterns and returns relevant insights.
        
        Args:
            query: Query string for context
            tone_vector: ToneVector to match against
            context: Optional additional context
            top_k: Number of top matching patterns to return
        
        Returns:
            Dictionary containing:
            - 'patterns': List of matching pattern islands
            - 'similarities': Similarity scores for each pattern
            - 'insights': Derived insights from patterns
            - 'query_count': Total queries made to this memory
        """
        self.query_count += 1
        
        # Find similar patterns
        matches = self._find_similar_patterns(tone_vector, top_k)
        
        # Generate insights from matches
        insights = self._generate_insights(matches, query, context)
        
        # Update access for matched islands
        for island, similarity in matches:
            island.update_access()
        
        return {
            'patterns': [island.to_dict() for island, _ in matches],
            'similarities': [similarity for _, similarity in matches],
            'insights': insights,
            'query': query,
            'query_count': self.query_count,
            'timestamp': time.time()
        }
    
    def add_pattern(
        self,
        pattern_id: str,
        tone_vector: ToneVector,
        context: Dict[str, Any] = None
    ) -> bool:
        """Add a new pattern island to memory.
        
        Args:
            pattern_id: Unique identifier for the pattern
            tone_vector: ToneVector signature of the pattern
            context: Optional context data
        
        Returns:
            True if pattern was added, False if it already exists
        """
        if pattern_id in self.islands:
            # Update existing island
            self.islands[pattern_id].update_access()
            return False
        
        # Check if we need to prune before adding
        if len(self.islands) >= self.max_islands:
            self._prune_islands()
        
        # Add new island
        self.islands[pattern_id] = Island(pattern_id, tone_vector, context)
        return True
    
    def _find_similar_patterns(
        self,
        tone_vector: ToneVector,
        top_k: int
    ) -> List[Tuple[Island, float]]:
        """Find top-k similar patterns to the given tone vector."""
        if not self.islands:
            return []
        
        # Calculate similarities for all islands
        similarities = []
        for island in self.islands.values():
            similarity = island.similarity(tone_vector)
            if similarity >= self.similarity_threshold:
                similarities.append((island, similarity))
        
        # Sort by similarity (descending) and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def _generate_insights(
        self,
        matches: List[Tuple[Island, float]],
        query: str,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate insights from matched patterns."""
        if not matches:
            return {
                'summary': 'No matching patterns found',
                'confidence': 0.0,
                'recommendations': []
            }
        
        # Calculate average similarity
        avg_similarity = sum(sim for _, sim in matches) / len(matches)
        
        # Extract common patterns
        pattern_contexts = [island.context for island, _ in matches]
        
        return {
            'summary': f'Found {len(matches)} similar patterns',
            'confidence': avg_similarity,
            'average_frequency': sum(island.frequency for island, _ in matches) / len(matches),
            'pattern_contexts': pattern_contexts,
            'recommendations': [
                f"Pattern {island.pattern_id} (similarity: {sim:.2f})"
                for island, sim in matches[:3]
            ]
        }
    
    def _prune_islands(self, keep_ratio: float = 0.8):
        """Prune least recently used islands to free space."""
        if not self.islands:
            return
        
        # Sort islands by last accessed time (ascending)
        sorted_islands = sorted(
            self.islands.items(),
            key=lambda x: x[1].last_accessed
        )
        
        # Keep only top keep_ratio of islands
        keep_count = int(len(self.islands) * keep_ratio)
        islands_to_keep = dict(sorted_islands[-keep_count:])
        
        self.islands = islands_to_keep
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics."""
        if not self.islands:
            return {
                'total_islands': 0,
                'query_count': self.query_count,
                'average_frequency': 0.0,
                'oldest_island': None,
                'newest_island': None
            }
        
        islands_list = list(self.islands.values())
        return {
            'total_islands': len(self.islands),
            'query_count': self.query_count,
            'average_frequency': sum(i.frequency for i in islands_list) / len(islands_list),
            'oldest_island': min(islands_list, key=lambda x: x.timestamp).pattern_id,
            'newest_island': max(islands_list, key=lambda x: x.timestamp).pattern_id
        }
    
    def clear(self):
        """Clear all islands from memory."""
        self.islands = {}
        self.query_count = 0
