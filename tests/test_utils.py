import pytest
import os
from aptamer_generator.aptamers import AptamerGenerator
from aptamer_generator.utils import AptamerUtils


def test_aptadesign_init():
    """Test aptamer generation initialization."""
    generator = AptamerGenerator()
    assert generator.min_length == 20
    assert generator.max_length == 80


def test_aptadesign_run():
    """Test aptamer generation execution."""
    generator = AptamerGenerator()
    candidates = generator.generate_candidate_sequences(num_candidates=5)
    assert len(candidates) == 5
    for sequence, score in candidates:
        assert isinstance(sequence, str)
        assert isinstance(score, float)
