#!/bin/bash

# Parameters
GENOME_NAME=$1
TRANSCRIPTOME_NAME=$2

# Global variables
DATA_FOLDER=03_data
ANNOTATION_FOLDER=04_annotation
TRANSDECODER_FOLDER="./01_scripts/TransDecoder"
BASENAME="$ANNOTATION_FOLDER"/"${GENOME_NAME%.fasta}"

# Create GTF file from GFF3
echo GAWN: Create GTF file from GFF3
gffread "$BASENAME".gff3 -T -o "$BASENAME".gtf

# Create genome based transcriptome
echo GAWN: Create genome-based transcriptome
#"$UTIL_FOLDER"/cufflinks_gtf_genome_to_cdna_fasta.pl \
"$TRANSDECODER_FOLDER"/util/cufflinks_gtf_genome_to_cdna_fasta.pl \
    "$BASENAME".gtf \
    "$DATA_FOLDER"/"$GENOME_NAME" \
    > "$BASENAME".cdna

# GTF to predicted GFF3
echo GAWN: Creage predicted GFF3 from GTF file
"$TRANSDECODER_FOLDER"/util/cufflinks_gtf_to_alignment_gff3.pl \
    "$BASENAME".gtf \
    > "$BASENAME".predicted.gff3

# Best ORF candidate
echo GAWN: Find best ORF candidates
"$TRANSDECODER_FOLDER"/TransDecoder.LongOrfs -t \
    "$BASENAME".cdna

# Move transdecoder_dir
echo GAWN: Move transdecoder_dir
rm -r "$BASENAME".cdna.transdecoder_dir 2>/dev/null
mv "${GENOME_NAME%.fasta}".cdna.transdecoder_dir "$BASENAME".cdna.transdecoder_dir

# Create final genome annotation file
echo GAWN: Create final genome annotation file
"$TRANSDECODER_FOLDER"/util/cdna_alignment_orf_to_genome_orf.pl \
    "$BASENAME".cdna.transdecoder_dir/longest_orfs.gff3 \
    "$BASENAME".predicted.gff3 \
    "$BASENAME".cdna > "$BASENAME".gawn_annotated.gff3

# Copy result to 05_results
echo GAWN: Copy genome annotation to 05_results
cp "$BASENAME".gawn_annotated.gff3 05_results
