from aptamer_generator import AptaDesign

ad = AptaDesign(fasta_file='examples/thrombin_aptamers.fasta', n_gen=2, output_path='.', output_name='test')
result = ad.run()
print(result)
