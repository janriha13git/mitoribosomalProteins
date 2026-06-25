#!/bin/bash
#PBS -N iqtree_mito_-protein-_replicates_C60_v6
#PBS -l walltime=300:00:00
#PBS -l select=1:ncpus=10:mem=6gb:scratch_local=6gb
#PBS -j oe
#PBS -m abe

trap 'clean_scratch' TERM EXIT

# Setup
DATADIR="/storage/brno2/home/janriha/mitoribosomes/relocalizations/v6_0/-protein-"
OUTPUTDIR="/storage/brno2/home/janriha/mitoribosomes/relocalizations/v6_0/-protein-"
ALIGNMENT="-protein-_seq.linsi.trimmed.aln"
NUM_TREES=15

# Ensure scratch exists
if [ ! -d "$SCRATCHDIR" ]; then
  echo "Scratch not created!" >&2
  exit 1
fi

# Copy input data
cp "$DATADIR"/"$ALIGNMENT" "$SCRATCHDIR"
cd "$SCRATCHDIR" || exit 1

# Load IQ-TREE
module add iqtree/2.3.4-mpi

# Run IQ-TREE 20 times, each in a new directory
for i in $(seq 1 $NUM_TREES); do
  mkdir -p "run_$i"
  cd "run_$i" || exit 1
  iqtree -s "../$ALIGNMENT" -m LG+C60+G4 -mwopt -B 5000 -bnni -alrt 5000 -T 10 -nstop 150 -pre "tree_$i"
  cd ..
done

# Copy results back
mkdir -p "$OUTPUTDIR"
cp -r "$SCRATCHDIR"/* "$OUTPUTDIR" || export CLEAN_SCRATCH=false
