from aptamer_generator.aptamers import AptamerGenerator
from aptamer_generator.config import Config
import argparse


def main():
    parser = argparse.ArgumentParser(description="Generate candidate aptamers")
    parser.add_argument("--num-candidates", type=int, default=5)
    parser.add_argument("--output-dir", type=str, default="output")
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    generator = AptamerGenerator()
    candidates = generator.generate_candidate_sequences(args.num_candidates)

    if args.verbose:
        print("Generated Aptamer Candidates:")
        print("-" * 50)
        for idx, (seq, score) in enumerate(candidates, 1):
            print(f"Candidate {idx}:")
            print(f"Sequence: {seq}")
            print(f"Length: {len(seq)}")
            print(f"Score: {score:.3f}")
            print("-" * 50)

    with open(f"{args.output_dir}/aptamers.txt", "w") as f:
        for idx, (seq, score) in enumerate(candidates, 1):
            f.write(f"Candidate {idx}:\n")
            f.write(f"Sequence: {seq}\n")
            f.write(f"Length: {len(seq)}\n")
            f.write(f"Score: {score:.3f}\n")
            f.write("-" * 50 + "\n")

        print(f"Results saved to {args.output_dir}/aptamers.txt")
        print("Aptamer generation completed.")


if __name__ == "__main__":
    main()
