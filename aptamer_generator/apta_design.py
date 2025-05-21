# Adapted from https://github.com/JuanCRueda/AptaDesign by Juan Carlos Rueda Silva

import os
import shutil
from Bio import SeqIO

class AptaDesign:
    def __init__(self, fasta_file, n_gen, output_path, output_name, Hybridation_target=None, **kwargs):
        """Initialize the AptaDesign class for aptamer generation."""
        # Validate input parameters
        if not os.path.exists(fasta_file):
            raise FileNotFoundError(f"FASTA file {fasta_file} does not exist")
        if not isinstance(n_gen, int) or n_gen <= 0:
            raise ValueError("n_gen must be a positive integer")
        if not os.path.isdir(output_path):
            raise NotADirectoryError(f"Output path {output_path} is not a valid directory")
        
        # Assign parameters
        self.fasta_file = fasta_file
        self.n_gen = n_gen
        self.output_path = output_path
        self.output_name = output_name
        self.Hybridation_target = Hybridation_target
        
        # Set default parameters from kwargs
        self.n_conserved_seqs = kwargs.get('n_conserved_seqs', 8)
        self.n_pool = kwargs.get('n_pool', 100)
        self.n_candidates = kwargs.get('n_candidates', 10)
        self.min_length = kwargs.get('min_length', 10)
        self.hyperdiverse_generations = kwargs.get('hyperdiverse_generations', 3)
        self.max_consecutive_hyperdiverse = kwargs.get('max_consecutive_hyperdiverse', 10)
        self.max_consecutive_score = kwargs.get('max_consecutive_score', 10)
        self.visualize = kwargs.get('visualize', True)
        self.break_score = kwargs.get('break_score', 0.99)
        
        # Check for required external tools (RNAfold, RNAhybrid)
        if not shutil.which('RNAfold'):
            raise EnvironmentError("RNAfold is not installed or not in PATH")
        if not shutil.which('RNAhybrid'):
            raise EnvironmentError("RNAhybrid is not installed or not in PATH")
        
        # Load FASTA file sequences
        try:
            self.sequences = list(SeqIO.parse(fasta_file, 'fasta'))
            if not self.sequences:
                raise ValueError("FASTA file is empty")
        except Exception as e:
            raise ValueError(f"Error reading FASTA file: {str(e)}")

    def run(self):
        """Run the aptamer generation process."""
        # Placeholder for aptamer generation logic (adapt from original AptaDesign)
        # Steps include:
        # 1. Extract motifs from sequences
        # 2. Generate evaluation equation
        # 3. Initialize sequence pool
        # 4. Evolve pool over n_gen generations
        # 5. Select top candidates, apply mutations
        # 6. Check stop conditions
        # 7. Generate output files (.xlsx, .log, .png)
        output_file = os.path.join(self.output_path, f"{self.output_name}.txt")
        with open(output_file, 'w') as f:
            f.write("Generated aptamers placeholder\n")
        print(f"Generating aptamers using {self.fasta_file} for {self.n_gen} generations...")
        return {"status": "Aptamer generation completed", "output_file": output_file}
