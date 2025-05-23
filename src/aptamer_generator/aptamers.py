import random
import subprocess
import os
from Bio import SeqIO

def run(self):
    def predict_mfe(sequence):
        cmd = f"echo {sequence} | RNAfold --noPS"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.splitlines()
        mfe = float(lines[1].split()[1][1:-1])  # Extract MFE from output
        return mfe

    def mutate_sequence(sequence, mutation_rate=0.01):
        seq_list = list(sequence)
        for i in range(len(seq_list)):
            if random.random() < mutation_rate:
                seq_list[i] = random.choice('ACGT')
        return ''.join(seq_list)

    # Initialize pool with n_pool sequences from self.sequences
    sequences = [str(seq.seq) for seq in self.sequences]
    if len(sequences) < self.n_pool:
        pool = sequences * (self.n_pool // len(sequences) + 1)
        pool = pool[:self.n_pool]
    else:
        pool = random.sample(sequences, self.n_pool)

    for gen in range(self.n_gen):
        # Evaluate pool: calculate MFE for each sequence
        mfe_scores = [(seq, predict_mfe(seq)) for seq in pool]
        # Sort by MFE ascending (lower is better)
        mfe_scores.sort(key=lambda x: x[1])
        # Select top n_candidates
        candidates = [seq for seq, mfe in mfe_scores[:self.n_candidates]]

        # Generate new pool by mutating candidates
        new_pool = []
        for candidate in candidates:
            for _ in range(self.n_pool // self.n_candidates):
                mutated = mutate_sequence(candidate)
                new_pool.append(mutated)
        # Adjust if n_pool not divisible by n_candidates
        while len(new_pool) < self.n_pool:
            mutated = mutate_sequence(random.choice(candidates))
            new_pool.append(mutated)
        pool = new_pool

    # After generations, select top n_candidates from final pool
    final_mfe_scores = [(seq, predict_mfe(seq)) for seq in pool]
    final_mfe_scores.sort(key=lambda x: x[1])
    final_candidates = [seq for seq, mfe in final_mfe_scores[:self.n_candidates]]

    # Write to output file
    output_file = os.path.join(self.output_path, f"{self.output_name}.txt")
    with open(output_file, 'w') as f:
        f.write("Generated aptamer candidates:\n")
        for i, seq in enumerate(final_candidates, 1):
            f.write(f"Candidate {i}: {seq}\n")

    print(f"Generating aptamers using {self.fasta_file} for {self.n_gen} generations...")
    return {"status": "Aptamer generation completed", "output_file": output_file}
