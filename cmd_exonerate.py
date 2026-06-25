# Nuclear assemblies search workflow No. 1

# This script will be used for exonerate automatization

import os

with open('proteins.txt') as f:
    proteins = [line.strip() for line in f.readlines()]

with open("organisms.txt") as f:
    organisms = [line.strip() for line in f.readlines()]

proteins_length = eval(open("proteins_length_dict.txt").read())

score = 100

for organism in organisms:

    os.makedirs(f"./organisms/{organism}/exonerate", exist_ok=True)

    for protein in proteins:
        if proteins_length[protein] < 95:
            score = 95
        elif proteins_length[protein] < 80:
            score = 75
        elif proteins_length[protein] < 60:
            score = 70
        elif proteins_length[protein] > 200:
            score = 125
        else:
            score = 100

        cmd = (
            f"exonerate "
            f"-q ./input/{protein}.fasta "
            f"-t ./organisms/{organism}/{organism}_genomic.fasta "
            f"-Q protein -T dna -c 10 "
            f"--model protein2genome "
            f"--score {score} "
            f"--bestn 3 "
            f"--ryo \">%ti_%tab_%tae_ribosomal_protein_{protein}_{organism}_exonerate_nuclear\\n%tcs\\n\" "
            f"--showvulgar no --showalignment yes "
            f"> ./organisms/{organism}/exonerate/{protein}_{organism}_exonerate.txt"
        )
        os.system(cmd)
        print(f"Exonerate for organism: {organism} protein: {protein} has finished")


#Exonerate is a generic tool for pairwise sequence comparison
# -q query
# -t target
# -Q query type
# -T target type
# -c 4 number of CPU
# --model model used = protein2genome (aligning protein sequence to genome (with introns))
# --score 100 - if protein is smaller than 80 aa, score is 75 (smaller protein = lower score), if protein is more than 200 aa - score = 125 (to limit false positives), otherwise score = 100 (basic value)
# --bestn 6 -> first 6 best hits (if there are more hits with same score, prints even more hits)
# --ryo \">%ti_%tab_%tae_ribosomal_protein_{protein}_{organism}_TARGET\\n%tcs\\n\" --ryo = roll you own format -> output header will be compatible with other headers (id as scaffold id with start and end coordinates)
# --showvulgar yes -> vulgar format printer before ryo, --showalignment no -> human readable algiment not printed
# save using > output_file


# exonerate -q ./conseq/{protein}_hmmerbuild_conseq.fasta -t ./organisms/{organism}/{organism}_genomic.fna -Q protein -T dna -c 4 --model protein2genome --score 100 --bestn 6 --ryo \">%ti_%tab_%tae_ribosomal_protein_{protein}_{organism}_exonerate_r%r_s%s_TARGET\\n%tcs\\n\" --showvulgar yes --showalignment no > ./organisms/{organism}/exonerate/{protein}_{organism}_exonerate.txt