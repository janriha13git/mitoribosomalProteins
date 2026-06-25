import os
import shutil

# Relocalization HMMER workflow No. 3
# Updated by ChatGPT

# Load protein list
with open('proteins.txt') as f:
    proteins = [line.strip() for line in f.readlines()]

# Load organism list
with open('./proteins/S15/organisms.txt') as f:
    organisms = [line.strip() for line in f.readlines()]

for protein in proteins:

    print(f"\n🔍 Collecting all sequences for protein: {protein}")

    # Folder where all per-organism FASTA files should be copied
    seq_dir = f"./proteins/{protein}/seq"
    os.makedirs(seq_dir, exist_ok=True)

    # -------------------------------------------------------------
    # Copy all available FASTA files for this protein
    # Example files:
    #   L10_Arabidopsis_mito.fasta
    #   L10_Arabidopsis_plastid.fasta
    #   L10_Chlamy_cyto.fasta
    # -------------------------------------------------------------
    copied_files = []

    for organism in organisms:
        org_seq_dir = f"./organisms/{organism}/seq"

        # Files like: protein_organism_*.fasta
        pattern = f"{protein}_{organism}_"

        if not os.path.isdir(org_seq_dir):
            continue

        for fname in os.listdir(org_seq_dir):
            if fname.startswith(pattern) and fname.endswith(".fasta"):
                src = os.path.join(org_seq_dir, fname)
                dst = os.path.join(seq_dir, fname)
                shutil.copy(src, dst)
                copied_files.append(dst)

                print(f"  ✓ Copied: {fname}")

    if not copied_files:
        print(f"⚠ No sequences found for protein {protein}")
        continue

    # -------------------------------------------------------------
    # Concatenate into one final file
    # -------------------------------------------------------------
    output_file = f"./proteins/{protein}/{protein}.fasta"

    with open(output_file, "w") as outfile:
        for fname in copied_files:
            with open(fname) as infile:
                outfile.write(infile.read())

    print(f"✔ Final merged FASTA: {output_file}")
