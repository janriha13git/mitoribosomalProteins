import os

# Nuclear assemblies search workflow No. 3

with open('proteins.txt') as f:
    proteins = [line.strip() for line in f.readlines()]

with open("organisms.txt") as f:
    organisms = [line.strip() for line in f.readlines()]

proteins_length = eval(open("proteins_length_dict.txt").read())

for organism in organisms:
    try:
        print(f"Creating BLAST databse for organism: {organism}")
        os.system(f"makeblastdb -in ./organisms/{organism}/{organism}_genomic.fasta -dbtype nucl -parse_seqids")
    except Exception as e:
        print(f"Unable to create BLAST databse for organism: {organism}\n Error: {e}")


evalue = 1e-8

for organism in organisms:

    os.makedirs(f"./organisms/{organism}/tblastn", exist_ok=True)

    for protein in proteins:
        if proteins_length[protein] < 95:
            evalue = 1e-7
        elif proteins_length[protein] < 80:
            evalue = 1e-6
        elif proteins_length[protein] < 60:
            evalue = 1e-5
        elif proteins_length[protein] > 200:
            evalue = 1e-11
        else:
            evalue = 1e-8

        cmd = (
            f"tblastn "
            f"-query ./input/{protein}.fasta "
            f"-db ./organisms/{organism}/{organism}_genomic.fasta "
            f"-max_target_seqs 5 "
            f"-outfmt 6 "
            f"-num_threads 10 "
            f"-evalue {evalue} "
            f"-out ./organisms/{organism}/tblastn/{protein}_{organism}_tblastn.txt"
        )
        try:
            os.system(cmd)
            print(f"tBLASTn for organism: {organism} protein: {protein} has finished")
        except Exception as e:
            print(f"Could not run tBLASTn for organism: {organism}\n Error: {e}")

        