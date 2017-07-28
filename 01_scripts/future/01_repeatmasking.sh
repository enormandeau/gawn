#!/bin/bash
#SBATCH -D ./
#SBATCH --job-name="windowsmasker"
#SBATCH -o log-windowsmasker
#SBATCH -c 1
#SBATCH -p ibismax
#SBATCH -A ibismax
#SBATCH --mail-type=ALL
#SBATCH --mail-user=type_your_mail@ulaval.ca
#SBATCH --time=1-00:00
#SBATCH --mem=50000

cd $SLURM_SUBMIT_DIR

#Requirments
#[windowmasker](https://www.ncbi.nlm.nih.gov/pubmed/16287941)


#variables
GENOME="genome.fasta"
STATFILE="stat.file.wm.txt"
SOFTWMASK="softmasked_genome.fasta"
HARDMASK="hardmasked_genome.fasta"


#stage 1
windowmasker -in $GENOME -mk_counts -out $STATFILE

#stage 2
windowmasker -in $GENOME -ustat $STATFILE -out $SOFTMASK -outfmt 'fasta'

# soft to hard clipping
perl -pe '/^[^>]/ and $_=~ s/[a-z]/N/g' $SOFTMASK >$HARDMASK

#Clean up
#rm $SOFTMASK
rm $STATFILE
