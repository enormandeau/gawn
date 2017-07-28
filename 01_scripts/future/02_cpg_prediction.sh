#!/bin/bash


# Requirement
#[EMBOSS](http://emboss.sourceforge.net/)


# Variables
GENOME="genome.fasta"
HARDMASK="hardmasked_genome.fasta"
GENOME_FOLDER="04_reference"
OUTPOUT_FOLDER="05_results"
OUTPUTGG="GG.CpGi"
OUTPUTGGM="GGM.CpGi"
OUTPUTTJ="TJ.CpGi"

# Takai and Jones (Takai and Jones., 2002)
cpgplot -sequence "$GENOME" -window 100 -minlen 500 -minoe 0.65 -minpc 55.0 -outfile "$OUTPOUT_FOLDER"/"$OUTPUTTJ".cpgplot -graph none -outfeat "$OUTPOUT_FOLDER"/"$OUTPUTTJ".gff

# Gardiner-Garden approach (Gardiner-Garden et al., 1987)
cpgplot -sequence "$GENOME" -window 100 -minlen 200 -minoe 0.6 -minpc 50.0 -outfile "$OUTPOUT_FOLDER"/"$OUTPUTGG".cpgplot -graph none -outfeat "$OUTPOUT_FOLDER"/"$OUTPUTGG".gff

#Gardiner-Garden masked approach (Bock et al., 2007)
cpgplot -sequence "$HARDMASK" -window 100 -minlen 200 -minoe 0.6 -minpc 50.0 -outfile "$OUTPOUT_FOLDER"/"$OUTPUTGGM".cpgplot -graph none -outfeat "$OUTPOUT_FOLDER"/"$OUTPUTGGM".gff
