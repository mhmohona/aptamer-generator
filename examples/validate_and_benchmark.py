"""
validate_and_benchmark.py

This script validates and benchmarks the aptamer-generator package by:
1. Loading reference thrombin-binding aptamer sequences from thrombin_aptamers.fasta.
2. Generating candidate aptamer sequences with lengths similar to the reference (14-15 nt).
3. Comparing properties like length and GC content between reference and generated sequences.
4. Performing sequence alignment to assess similarity between generated and reference sequences.

Usage:
    python validate_and_benchmark.py
"""

from aptamer_generator import Config, AptamerGenerator, AptamerUtils
from Bio.Align import PairwiseAligner
import numpy as np

def validate_and_benchmark():
    """Validate and benchmark the aptamer-generator package."""
    # Load reference dataset
    reference_sequences = AptamerUtils.load_fasta_file('examples/thrombin_aptamers.fasta')
    print("Reference Sequences:")
    for header, seq in reference_sequences:
        gc_content = AptamerUtils.calculate_gc_content(seq)
        length = len(seq)
        print(f"Header: {header}, Length: {length}, GC Content: {gc_content:.2f}")

    # Compute statistics for reference sequences
    ref_lengths = [len(seq) for _, seq in reference_sequences]
    ref_gc_contents = [AptamerUtils.calculate_gc_content(seq) for _, seq in reference_sequences]
    mean_ref_length = np.mean(ref_lengths)
    std_ref_length = np.std(ref_lengths)
    mean_ref_gc = np.mean(ref_gc_contents)
    std_ref_gc = np.std(ref_gc_contents)
    print(f"\nReference Statistics:")
    print(f"  Mean Length: {mean_ref_length:.2f}, Std Dev: {std_ref_length:.2f}")
    print(f"  Mean GC Content: {mean_ref_gc:.2f}, Std Dev: {std_ref_gc:.2f}")

    # Create a custom configuration to match reference lengths
    config = Config()
    config.update(min_length=14, max_length=15)
    generator = AptamerGenerator(config)

    # Generate candidate sequences
    generated_sequences = generator.generate_candidate_sequences(num_candidates=5)
    print("\nGenerated Sequences:")
    for i, (seq, score) in enumerate(generated_sequences, 1):
        gc_content = AptamerUtils.calculate_gc_content(seq)
        length = len(seq)
        print(f"Candidate {i}: Length: {length}, GC Content: {gc_content:.2f}, Score: {score:.3f}")

    # Compute statistics for generated sequences
    gen_lengths = [len(seq) for seq, _ in generated_sequences]
    gen_gc_contents = [AptamerUtils.calculate_gc_content(seq) for seq, _ in generated_sequences]
    mean_gen_length = np.mean(gen_lengths)
    std_gen_length = np.std(gen_lengths)
    mean_gen_gc = np.mean(gen_gc_contents)
    std_gen_gc = np.std(gen_gc_contents)
    print(f"\nGenerated Statistics:")
    print(f"  Mean Length: {mean_gen_length:.2f}, Std Dev: {std_gen_length:.2f}")
    print(f"  Mean GC Content: {mean_gen_gc:.2f}, Std Dev: {std_gen_gc:.2f}")

    # Perform sequence alignment
    print("\nSequence Alignment Analysis:")
    aligner = PairwiseAligner()
    aligner.mode = 'global'
    aligner.match_score = 2
    aligner.mismatch_score = -1
    aligner.open_gap_score = -0.5
    aligner.extend_gap_score = -0.1

    for i, (gen_seq, _) in enumerate(generated_sequences, 1):
        best_score = -float('inf')
        best_header = None
        for ref_header, ref_seq in reference_sequences:
            alignments = aligner.align(gen_seq, ref_seq)
            if alignments:
                score = alignments[0].score
                if score > best_score:
                    best_score = score
                    best_header = ref_header
        if best_header:
            print(f"Candidate {i} best aligns with {best_header}: Score {best_score:.2f}")
        else:
            print(f"Candidate {i} has no significant alignment")

if __name__ == "__main__":
    validate_and_benchmark()