from Bio import SearchIO, SeqIO
import os
import re

# Relocalization HMMER workflow No. 2
# Updated from original script by ChatGPT

# -------------------------------------------------------------
# Load FASTA into dictionary
# -------------------------------------------------------------
def load_fasta_sequences(fasta_file):
    sequences = {}
    for record in SeqIO.parse(fasta_file, 'fasta'):
        sequences[record.id] = record
    return sequences

# -------------------------------------------------------------
# Parse HMMER output files for a specific TYPE of search
# -------------------------------------------------------------
def hit_parser(files, sequence_db, protein, organism, hmm_type):

    unique_ids = set()
    sequences = {}

    for fname in files:
        path = f"./organisms/{organism}/hmmer/{fname}"
        records = SearchIO.parse(path, "hmmer3-text")

        for record in records:
            for hit in record.hits:
                if hit.is_included:
                    unique_ids.add(hit.id)
                    print(f"[{organism}] {protein} ({hmm_type}) → ID: {hit.id}")

                    if hit.id in sequence_db:
                        sequences[hit.id] = sequence_db[hit.id]
                    else:
                        print(f"WARNING: ID {hit.id} not found in sequence DB")

    # ---------------------------------------------------------
    # Write output for this type
    # ---------------------------------------------------------
    out_dir = f'./organisms/{organism}/seq'
    os.makedirs(out_dir, exist_ok=True)
    out_file = f"{out_dir}/{protein}_{organism}_{hmm_type}.fasta"

    with open(out_file, 'w') as fasta_file:
        for seq_id, record in sequences.items():
            fasta_file.write(f">{record.description}\n{record.seq}\n")

    print(f"✔ Output written: {out_file}")


# -------------------------------------------------------------
# MAIN WORKFLOW
# -------------------------------------------------------------
with open('proteins.txt') as f:
    proteins = [line.strip() for line in f.readlines()]

with open('all_organisms.txt') as f:
    organisms = [line.strip() for line in f.readlines()]

# Detect types automatically from filenames (mito/plastid/cyto/etc.)
TYPE_PATTERN = re.compile(r".+?_(\w+)_\w+\.out")

for organism in organisms:

    fasta_file_path = f"./organisms/{organism}/{organism}_protein.faa"
    print(f"\nLoading FASTA for organism: {organism}")

    try:
        sequence_db = load_fasta_sequences(fasta_file_path)
    except:
        print(f"ERROR: Could not load FASTA: {fasta_file_path}")
        continue

    hmmer_dir = f"./organisms/{organism}/hmmer"
    hmmer_files = os.listdir(hmmer_dir)

    for protein in proteins:

        # -----------------------------------------------------
        # Match files like: protein_type_organism.out
        # Example: L10_mito_Chlamydomonas.out
        # -----------------------------------------------------
        protein_files = [
            f for f in hmmer_files
            if f.startswith(protein + "_") and f.endswith(".out")
        ]

        # Group files by HMM type
        type_dict = {}

        for f in protein_files:
            match = TYPE_PATTERN.match(f)
            if match:
                hmm_type = match.group(1)
                type_dict.setdefault(hmm_type, []).append(f)

        if not type_dict:
            print(f"No HMMER files found for protein {protein} in {organism}")
            continue

        # -----------------------------------------------------
        # Process each type separately
        # -----------------------------------------------------
        for hmm_type, files in type_dict.items():
            print(f"\nProcessing: {protein} ({hmm_type}) for {organism}")
            try:
                hit_parser(files, sequence_db, protein, organism, hmm_type)
            except Exception as e:
                print(f"ERROR while parsing {protein}/{hmm_type}/{organism}")
                print(e)
                continue
