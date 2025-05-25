from typing import List, Tuple, Optional
import numpy as np
from .config import Config
from .utils import AptamerUtils


class AptamerGenerator:
    """
    Generates candidate aptamers.

    Based on concepts from AptaDesign and sequence analysis from AptamerRunner.
    """

    def __init__(self, config: Optional[Config] = None):
        """Initialize the aptamer generator with configuration."""
        self.config = config or Config()
        self.utils = AptamerUtils()
        self.min_length = self.config.core.min_length
        self.max_length = self.config.core.max_length
        self.default_candidates = self.config.core.default_candidates

        if self.config.core.random_seed is not None:
            np.random.seed(self.config.core.random_seed)

    def generate_candidate_sequences(
        self, num_candidates: Optional[int] = None
    ) -> List[Tuple[str, float]]:
        """
        Generate candidate aptamer sequences.

        Args:
            num_candidates: Number of candidates to generate

        Returns:
            List of tuples containing (sequence, score)
        """
        if num_candidates is None:
            num_candidates = self.default_candidates

        candidates = []
        nucleotides = ["A", "T", "G", "C"]

        for _ in range(num_candidates):
            length = np.random.randint(self.min_length, self.max_length + 1)
            sequence = "".join(np.random.choice(nucleotides, size=length))
            gc_content = self.utils.calculate_gc_content(sequence)
            score = self._calculate_sequence_score(sequence, gc_content)

            candidates.append((sequence, score))

        return sorted(candidates, key=lambda x: x[1], reverse=True)

    def _calculate_sequence_score(self, sequence: str, gc_content: float) -> float:
        """
        Calculate score for a sequence based on aptamer properties.

        Implements scoring methodology similar to RaptGen.
        """
        gc_score = 1 - abs(0.5 - gc_content)
        rep_score = self._calculate_repetitive_score(sequence)

        return gc_score * rep_score

    def _calculate_repetitive_score(self, sequence: str) -> float:
        """
        Calculate penalty for repetitive regions.

        Based on sequence analysis principles from AptamerRunner.
        """
        n = len(sequence)
        repeats = sum(
            sequence.count(seq) > 1
            for seq in [sequence[i : i + 4] for i in range(n - 3)]
        )
        return max(0.1, 1 - (repeats / (n - 3)))


class AptamerUtils:
    """
    Utility functions for aptamer generation and analysis.

    Provides helper functions for sequence manipulation and validation.
    """

    @staticmethod
    def load_fasta_file(filename: str) -> List[Tuple[str, str]]:
        """
        Load sequences from a FASTA file.

        Args:
            filename: Path to FASTA file

        Returns:
            List of (header, sequence) tuples
        """
        sequences = []
        with open(filename, "r") as f:
            for header, seq in SimpleFastaParser(f):
                sequences.append((header, seq))
        return sequences

    @staticmethod
    def validate_sequence(sequence: str) -> bool:
        """
        Validate that a sequence contains only valid nucleotides.

        Args:
            sequence: DNA/RNA sequence to validate

        Returns:
            bool: True if sequence is valid
        """
        valid_nucleotides = set("ATGC")
        return all(nucleotide in valid_nucleotides for nucleotide in sequence.upper())

    @staticmethod
    def calculate_gc_content(sequence: str) -> float:
        """
        Calculate GC content of a sequence.

        Args:
            sequence: DNA/RNA sequence

        Returns:
            float: GC content ratio (0-1)
        """
        sequence = sequence.upper()
        gc_count = sequence.count("G") + sequence.count("C")
        return gc_count / len(sequence) if sequence else 0.0
