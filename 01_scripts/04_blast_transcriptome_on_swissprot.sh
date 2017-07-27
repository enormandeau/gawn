#!/bin/bash

# Parameters
TRANSCRIPTOME_NAME=$1
SWISSPROT_DB=$2
NCPUS=$3

# Global variables
DATA_FOLDER=03_data
ANNOTATION_FOLDER=04_annotation
BASENAME="$ANNOTATION_FOLDER"/"${TRANSCRIPTOME_NAME%.fasta}"
SWISSPROT_RESULTS="$BASENAME".swissprot
SWISSPROT_HITS="$BASENAME".hits

# Blast all sequences against local swissprot database
cat "$DATA_FOLDER"/"$TRANSCRIPTOME_NAME" |
    parallel -j "$NCPUS" -k --block 1k --recstart '>' --pipe 'blastx -db '$SWISSPROT_DB' \
        -query - -evalue 1e-3 -outfmt 6 -max_target_seqs 1' > "$SWISSPROT_RESULTS"

# Extract analyzed_genes.hits
awk '{print $1,$2}' "$SWISSPROT_RESULTS" | uniq > "$SWISSPROT_HITS"
