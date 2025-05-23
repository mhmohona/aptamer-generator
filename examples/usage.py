import argparse
from aptamer_generator.aptamers import AptamerGenerator
from aptamer_generator.utils import AptamerUtils

def main():
    """Main function to demonstrate aptamer generation."""
    parser = argparse.ArgumentParser(description='Generate candidate aptamers')
    parser.add_argument('--num-candidates', type=int, default=5,
                        help='Number of candidate aptamers to generate')
    parser.add_argument('--min-length', type=int, default=20,
                        help='Minimum length of generated aptamers')
    parser.add_argument('--max-length', type=int, default=80,
                        help='Maximum length of generated aptamers')
    args = parser.parse_args()

    # Initialize generator with custom parameters
    generator = AptamerGenerator()
    generator.min_length = args.min_length
    generator.max_length = args.max_length

    # Generate candidates
    candidates = generator.generate_candidate_sequences(args.num_candidates)

    # Print results
    print("Generated Aptamer Candidates:")
    print("-" * 50)
    for idx, (seq, score) in enumerate(candidates, 1):
        gc_content = AptamerUtils.calculate_gc_content(seq)
        print(f"Candidate {idx}:")
        print(f"Sequence: {seq}")
        print(f"Length: {len(seq)}")
        print(f"GC Content: {gc_content:.2%}")
        print(f"Score: {score:.3f}")
        print("-" * 50)

if __name__ == "__main__":
    main()