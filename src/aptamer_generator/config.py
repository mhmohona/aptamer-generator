from dataclasses import dataclass
from typing import Optional, List, Dict
import os
from pathlib import Path


@dataclass
class CoreConfig:
    """Core configuration for aptamer generation."""

    min_length: int = 20  # Minimum sequence length
    max_length: int = 80  # Maximum sequence length
    default_candidates: int = 5  # Default number of candidates to generate
    random_seed: Optional[int] = None  # Random seed for reproducibility


@dataclass
class SequenceConfig:
    """Configuration for sequence generation and validation."""

    gc_min: float = 0.3  # Minimum GC content percentage
    gc_max: float = 0.7  # Maximum GC content percentage
    min_repeats: int = 4  # Minimum length of repeats to check
    allowed_nucleotides: List[str] = None  # Allowed nucleotides (None for all)

    def __post_init__(self):
        if self.allowed_nucleotides is None:
            self.allowed_nucleotides = ["A", "T", "G", "C"]


@dataclass
class OutputConfig:
    """Configuration for output handling."""

    output_dir: str = "output"  # Default output directory
    file_format: str = "fasta"  # Output file format
    verbose: bool = False  # Enable verbose output
    overwrite: bool = False  # Allow overwriting existing files

    def __post_init__(self):
        self.output_dir = os.path.abspath(self.output_dir)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)


class Config:
    """Main configuration class for aptamer generator."""

    def __init__(self):
        self.core = CoreConfig()
        self.sequence = SequenceConfig()
        self.output = OutputConfig()

    def update(self, **kwargs):
        """Update configuration from keyword arguments."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Unknown configuration key: {key}")

    def validate(self):
        """Validate configuration values."""
        if self.sequence.gc_min < 0 or self.sequence.gc_max > 1:
            raise ValueError("GC content must be between 0 and 1")
        if self.core.min_length < 1:
            raise ValueError("Minimum length must be positive")
        if self.core.max_length < self.core.min_length:
            raise ValueError("Maximum length must be greater than minimum length")
