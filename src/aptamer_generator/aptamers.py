from typing import List, Tuple
import numpy as np
from .utils import AptamerUtils

class AptamerGenerator:
    """
    Generates candidate aptamers.
    
    Based on concepts from AptaDesign and sequence analysis from AptamerRunner 
    """
    def __init__(self):
        """Initialize the aptamer generator with default parameters."""
        self.min_length = 20  # Minimum length for generated aptamers
        self.max_length = 80  # Maximum length for generated aptamers
        self.utils = AptamerUtils()

    def generate_candidate_sequences(self, num_candidates: int = 10) -> List[Tuple[str, float]]:
        """
        Generate candidate aptamer sequences.
        
        Args:
            num_candidates: Number of candidates to generate
            
        Returns:
            List of tuples containing (sequence, score)
        """
        candidates = []
        nucleotides = ['A', 'T', 'G', 'C']
        
        for _ in range(num_candidates):
            # Randomly select length within bounds
            length = np.random.randint(self.min_length, self.max_length + 1)
            
            # Generate random sequence
            sequence = ''.join(np.random.choice(nucleotides, size=length))
            
            # Calculate basic score based on sequence properties
            gc_content = self.utils.calculate_gc_content(sequence)
            score = self._calculate_sequence_score(sequence, gc_content)
            
            candidates.append((sequence, score))
        
        return sorted(candidates, key=lambda x: x[1], reverse=True)

    def _calculate_sequence_score(self, sequence: str, gc_content: float) -> float:
        """
        Calculate score for a sequence based on aptamer properties.
        
        Implements scoring methodology similar to RaptGen 
        """
        # Base score from GC content (optimal around 40-60%)
        gc_score = 1 - abs(0.5 - gc_content)
        
        # Penalize repetitive sequences
        rep_score = self._calculate_repetitive_score(sequence)
        
        return gc_score * rep_score

    def _calculate_repetitive_score(self, sequence: str) -> float:
        """
        Calculate penalty for repetitive regions.
        
        Based on sequence analysis principles from AptamerRunner 
.
        """
        n = len(sequence)
        repeats = sum(sequence.count(seq) > 1 
                     for seq in [sequence[i:i+4] for i in range(n-3)])
        return max(0.1, 1 - (repeats / (n-3)))
