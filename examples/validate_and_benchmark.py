"""
This script validates and benchmarks the aptamer-generator package by:
1. Loading reference thrombin-binding aptamer sequences from thrombin_aptamers.fasta.
2. Generating candidate aptamer sequences with lengths similar to the reference (14-15 nt).
3. Comparing properties like length and GC content between reference and generated sequences.
4. Performing sequence alignment to assess similarity between generated and reference sequences.
"""

from aptamer_generator.aptamers import AptamerGenerator
from aptamer_generator.config import Config
from aptamer_generator.utils import AptamerUtils

from Bio.Align import PairwiseAligner
import numpy as np
import sys


def validate_and_benchmark():
    """Validate and benchmark the aptamer-generator package."""
    try:
        # Load reference dataset
        reference_sequences = AptamerUtils.load_fasta_file("thrombin_aptamers.fasta")
        if not reference_sequences:
            raise ValueError("No sequences found in reference file")

        print("Reference Sequences:")
        for header, seq in reference_sequences:
            gc_content = AptamerUtils.calculate_gc_content(seq)
            length = len(seq)
            print(f"Header: {header}, Length: {length}, GC Content: {gc_content:.2f}")

        # Compute statistics for reference sequences
        ref_lengths = [len(seq) for _, seq in reference_sequences]
        ref_gc_contents = [
            AptamerUtils.calculate_gc_content(seq) for _, seq in reference_sequences
        ]
        mean_ref_length = np.mean(ref_lengths)
        std_ref_length = np.std(ref_lengths)
        mean_ref_gc = np.mean(ref_gc_contents)
        std_ref_gc = np.std(ref_gc_contents)

        print(f"\nReference Statistics:")
        print(f"  Mean Length: {mean_ref_length:.2f}, Std Dev: {std_ref_length:.2f}")
        print(f"  Mean GC Content: {mean_ref_gc:.2f}, Std Dev: {std_ref_gc:.2f}")

        # Create a custom configuration to match reference lengths
        config = Config()
        # Update core configuration directly
        config.core.min_length = 14
        config.core.max_length = 15
        generator = AptamerGenerator(config)

        # Generate candidate sequences
        generated_sequences = generator.generate_candidate_sequences(num_candidates=5)
        if not generated_sequences:
            raise ValueError("No sequences generated")

        print("\nGenerated Sequences:")
        for i, (seq, score) in enumerate(generated_sequences, 1):
            gc_content = AptamerUtils.calculate_gc_content(seq)
            length = len(seq)
            print(
                f"Candidate {i}: Length: {length}, GC Content: {gc_content:.2f}, Score: {score:.3f}"
            )

        # Compute statistics for generated sequences
        gen_lengths = [len(seq) for seq, _ in generated_sequences]
        gen_gc_contents = [
            AptamerUtils.calculate_gc_content(seq) for seq, _ in generated_sequences
        ]
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
        aligner.mode = "global"
        aligner.match_score = 2
        aligner.mismatch_score = -1
        aligner.open_gap_score = -0.5
        aligner.extend_gap_score = -0.1

        for i, (gen_seq, _) in enumerate(generated_sequences, 1):
            best_score = -float("inf")
            best_header = None
            for ref_header, ref_seq in reference_sequences:
                try:
                    alignments = aligner.align(gen_seq, ref_seq)
                    if alignments:
                        score = alignments[0].score
                        if score > best_score:
                            best_score = score
                            best_header = ref_header
                except Exception as e:
                    print(f"Warning: Alignment error for candidate {i}: {str(e)}")
                    continue
            if best_header:
                print(
                    f"Candidate {i} best aligns with {best_header}: Score {best_score:.2f}"
                )
            else:
                print(f"Candidate {i} has no significant alignment")

    except KeyboardInterrupt:
        print("\nValidation interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    validate_and_benchmark()
