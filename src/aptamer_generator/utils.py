from typing import List, Tuple
from Bio.SeqIO.FastaIO import SimpleFastaParser
import numpy as np

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
        with open(filename, 'r') as f:
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
        valid_nucleotides = set('ATGC')
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
        gc_count = sequence.count('G') + sequence.count('C')
        return gc_count / len(sequence) if sequence else 0.0