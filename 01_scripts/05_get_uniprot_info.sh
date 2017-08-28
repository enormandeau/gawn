#!/bin/bash

# Parameters
TRANSCRIPTOME_NAME=$1

# Global variables
DATA_FOLDER=03_data
ANNOTATION_FOLDER=04_annotation
BASENAME="$ANNOTATION_FOLDER"/"${TRANSCRIPTOME_NAME%.fasta}"
SWISSPROT_HITS="$BASENAME".hits
INFO_FOLDER="$ANNOTATION_FOLDER"/genbank_info
FISHER_FOLDER=06_fisher_tests

# Get info from uniprot for each hit in parallel
## Create commands
cat "$SWISSPROT_HITS" |
    while read i
    do
        echo $i
        feature=$(echo $i | cut -d " " -f 1)
        hit=$(echo $i | cut -d "|" -f 4 | cut -d "." -f 1)
        echo "wget -q -O - http://www.uniprot.org/uniprot/${hit}.txt > $INFO_FOLDER/${feature}.info"
    done > wget_genbank_commands.txt

## Create info folder
rm -r "$INFO_FOLDER" 2>/dev/null
mkdir "$INFO_FOLDER"

## Run commands
cat wget_genbank_commands.txt | parallel "eval {}"

## Cleanup commands
rm wget_genbank_commands.txt
