#!/bin/bash

# Parameters
GENOME_NAME=$1
TRANSCRIPTOME_NAME=$2

# Global variables
DATA_FOLDER=03_data
ANNOTATION_FOLDER=04_annotation
TRANSDECODER_FOLDER="./01_scripts/TransDecoder"

# Create GTF file from GFF3
echo GAWN: Create GTF file from GFF3
gffread "$ANNOTATION_FOLDER"/"${GENOME_NAME%.fasta}".gff3 -T -o "$ANNOTATION_FOLDER"/"${GENOME_NAME%.fasta}".gtf

# Create genome based transcriptome
echo GAWN: Create genome based transcriptome
#"$UTIL_FOLDER"/cufflinks_gtf_genome_to_cdna_fasta.pl \
"$TRANSDECODER_FOLDER"/util/cufflinks_gtf_genome_to_cdna_fasta.pl \
    "$ANNOTATION_FOLDER"/"${GENOME_NAME%.fasta}".gtf \
    "$DATA_FOLDER"/"$GENOME_NAME" \
    > "$ANNOTATION_FOLDER"/"${GENOME_NAME%.fasta}".cdna

# GTF to predicted GFF3
echo GAWN: GTF to predicted GFF3
"$TRANSDECODER_FOLDER"/util/cufflinks_gtf_to_alignment_gff3.pl \
    "$ANNOTATION_FOLDER"/"${GENOME_NAME%.fasta}".gtf \
    > "$ANNOTATION_FOLDER"/"${GENOME_NAME%.fasta}".predicted.gff3

# Best ORF candidate
echo GAWN: Best ORF candidate
"$TRANSDECODER_FOLDER"/TransDecoder.LongOrfs -t \
    "$ANNOTATION_FOLDER"/"${GENOME_NAME%.fasta}".cdna

# Move transdecoder_dir
echo GAWN: Move transdecoder_dir
mv "${GENOME_NAME%.fasta}".cdna.transdecoder_dir "$ANNOTATION_FOLDER"/"${GENOME_NAME%.fasta}".transdecoder_dir
#rm -r "$ANNOTATION_FOLDER"/"$TRANSCRIPTOME_NAME".transdecoder_dir


# Genome based coding region annotation file
echo GAWN: Genome based coding region annotation file
"$TRANSDECODER_FOLDER"/util/cdna_alignment_orf_to_genome_orf.pl \
    "$ANNOTATION_FOLDER"/"${GENOME_NAME%.fasta}".transdecoder_dir/longest_orfs.gff3 \
    "$ANNOTATION_FOLDER"/"${GENOME_NAME%.fasta}".predicted.gff3 \
    "$ANNOTATION_FOLDER"/"${GENOME_NAME%.fasta}".cdna > "$ANNOTATION_FOLDER"/transcripts.transdecoder.genome.gff3
