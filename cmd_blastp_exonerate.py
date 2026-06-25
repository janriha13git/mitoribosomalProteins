import os

# Search in both nuclear assemblies and predicted proteomes with queries from closely related organisms

with open('groups.txt') as f:
    groups = [line.strip() for line in f.readlines()]

for group in groups:

    with open(f'./{group}/proteins.txt') as f:
        proteins = [line.strip() for line in f.readlines()]

    with open(f"./{group}/organisms.txt") as f:
        organisms = [line.strip() for line in f.readlines()]

    for organism in organisms:

        os.system(f"makeblastdb -in ./{group}/db/{organism}_proteins.faa -dbtype prot -parse_seqids")
        print(f"BLAST database build for organism: {organism} in group: {group}.")

        for protein in proteins:
            os.system(f"blastp -db ./{group}/db/{organism}_proteins.faa -query ./{group}/input/{protein}.fasta -out ./{group}/output/{organism}_{protein}_blastp.txt -outfmt 1 -evalue 1e-3 -num_threads 4")
            os.system(f"exonerate -q ./{group}/input/{protein}.fasta -t ./{group}/db/{organism}_genomic.fasta --model protein2genome --score 80 -Q protein -T dna -c 6 > ./{group}/output/{organism}_{protein}_exonerate.txt")
            print(f"BLAST and exonerate for organism: {organism} for protein: {protein} in group: {group} have finished.")