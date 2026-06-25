import os

# Relocalization HMMER workflow No. 1
# script used for HMMER search in nuclear genomes with different profiles hmm for analysis of of relocalizations
# original script reviewed by ChatGPT to search with more types of hmm profiles at once

# Three hmm profile types available
TYPES = ["mito", "plastid", "cyto"]

# Load the protein list
with open("proteins.txt") as f:
    proteins = [line.strip() for line in f.readlines()]

# Loop over proteins
for protein in proteins:

    protein_dir = f"./proteins/{protein}"

    # List of organisms to search for this protein:type
    organism_list_file = f"{protein_dir}/organisms.txt"
    if not os.path.isfile(organism_list_file):
        print(f"Warning: missing {organism_list_file}")
        continue

    with open(organism_list_file) as f:
        organisms = [line.strip() for line in f.readlines()]

    for hmm_type in TYPES:

        # HMM profile path (only process if it exists)
        hmm_profile = f"{protein_dir}/{protein}_{hmm_type}.hmm"
        if not os.path.isfile(hmm_profile):
            continue  # skip if this protein does not use this type        

        # Run hmmsearch for all organisms in the list
        for organism in organisms:

            print(f"{protein} [{hmm_type}] → {organism}")

            out_dir = f"./organisms/{organism}/hmmer"
            os.makedirs(out_dir, exist_ok=True)

            protein_faa = f"./organisms/{organism}/{organism}_protein.faa"
            output_file = f"{out_dir}/{protein}_{hmm_type}_{organism}.out"

            cmd = (
                f"hmmsearch {hmm_profile} {protein_faa} "
                f"> {output_file}"
            )

            os.system(cmd)
