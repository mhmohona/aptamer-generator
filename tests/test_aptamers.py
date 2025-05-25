import pytest
from aptamer_generator.aptamers import AptamerGenerator
from aptamer_generator.utils import AptamerUtils


def test_aptamer_generation():
    """Test basic aptamer generation functionality."""
    generator = AptamerGenerator()
    candidates = generator.generate_candidate_sequences(num_candidates=5)

    assert len(candidates) == 5
    for sequence, score in candidates:
        assert isinstance(sequence, str)
        assert isinstance(score, float)
        assert 0 <= score <= 1
        assert AptamerUtils.validate_sequence(sequence)


def test_sequence_validation():
    """Test sequence validation utility."""
    utils = AptamerUtils()

    assert utils.validate_sequence("ATGC")
    assert not utils.validate_sequence("ATGCX")
    assert utils.validate_sequence("ATGCATGC")


def test_gc_content():
    """Test GC content calculation."""
    utils = AptamerUtils()

    assert utils.calculate_gc_content("ATGC") == 0.5
    assert utils.calculate_gc_content("AAAA") == 0.0
    assert utils.calculate_gc_content("GGGG") == 1.0
