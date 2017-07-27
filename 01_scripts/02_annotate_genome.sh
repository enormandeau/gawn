#!/bin/bash

# Parameters
GENOME_NAME=$1
TRANSCRIPTOME_NAME=$2
NCPUS=$3

# Global variables
DATA_FOLDER=03_data
INDEXED_GENOME_FOLDER=indexed_genome
ANNOTATION_FOLDER=04_annotation

# Align reads
cat "$DATA_FOLDER"/"$TRANSCRIPTOME_NAME" |
    gmap -t "$NCPUS" \
        --dir "$DATA_FOLDER" \
        -d "$INDEXED_GENOME_FOLDER" \
        -f gff3_gene \
        --gff3-add-separators=0 \
        > "$ANNOTATION_FOLDER"/"${GENOME_NAME%.fasta}".gff3
