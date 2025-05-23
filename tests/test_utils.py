import pytest
import os
from aptamer_generator.apta_design import AptaDesign

def test_aptadesign_init():
    ad = AptaDesign(fasta_file='examples/thrombin_aptamers.fasta', n_gen=1, output_path='.', output_name='test')
    assert ad.fasta_file == 'examples/thrombin_aptamers.fasta'
    assert ad.n_gen == 1
    assert ad.output_path == '.'
    assert ad.output_name == 'test'
    assert len(ad.sequences) > 0  # Ensure sequences are loaded

def test_aptadesign_init_invalid_fasta():
    with pytest.raises(FileNotFoundError):
        AptaDesign(fasta_file='nonexistent.fasta', n_gen=1, output_path='.', output_name='test')

def test_aptadesign_run():
    ad = AptaDesign(fasta_file='examples/thrombin_aptamers.fasta', n_gen=1, output_path='.', output_name='test')
    result = ad.run()
    assert result["status"] == "Aptamer generation completed"
    assert os.path.exists(result["output_file"])
