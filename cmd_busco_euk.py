import os
import subprocess

# BUSCO 6.0 for all predicted protemes used in this study

with open('organisms.txt') as f:
    organisms = [line.strip() for line in f.readlines()]



for organism in organisms:

    lineage = "eukaryota_odb12"

    protein_file = f"./eukdb_individually/{organism}.faa"

    output_dir = f"{organism}_{lineage}_BUSCO"

    try:
        if os.path.isfile(protein_file):
            print(f"Running BUSCO (protein mode) for {organism}")
            subprocess.run([
                "busco",
                "-i", protein_file,
                "-m", "proteins",
                "-l", lineage,
                "-c", "6",
                "-o", output_dir
            ], check=True)

        else:
            print(f"{organism}: No valid input files found")
            with open("error_log.txt", "a") as error_log:
                error_log.write(f"{organism} - No input file found\n")

    except subprocess.CalledProcessError as e:
        print(f"BUSCO failed for {organism}")
        with open("error_log.txt", "a") as error_log:
            error_log.write(f"{organism} - BUSCO run failed: {e}\n")
