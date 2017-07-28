#!/usr/bin/env python
"""Create final genome annotation table

Usage:
    ./01_scripts/07_create_genome_annotation_table.py genome_file genome_gff3 transcriptome_table genome_table
"""

# Module
from collections import defaultdict
import sys
import re
import os

# Classes
class Gene(object):
    def __init__(self):
        self.name = "Albert"

# Parsing user input
try:
    genome_file = sys.argv[1]
    genome_gff3 = sys.argv[2]
    transcriptome_table = sys.argv[3]
    genome_table = sys.argv[4]
except:
    print __doc__
    sys.exit(1)

# Read genome fasta file to keep track of scaffolds
all_scaffolds = set()
scaffolds_with_genes = set()

with open(genome_file) as infile:
    for line in infile:
        if line.startswith(">"):
            all_scaffolds.add(line.strip()[1:])

all_scaffolds = sorted(list(all_scaffolds))

# Read genome gff3 file
# Keep only info from 'gene' lines
# Create Gene instances with name set to transcript
# Update scaffolds_with_genes as needed
transcripts = defaultdict(dict)
with open(genome_gff3) as infile:
    for line in infile:
        l = line.strip().split("\t")
        if len(l) > 3 and l[2] == "gene":
            scaffold_name = l[0]
            from_position = int(l[3])
            to_position = int(l[4])
            sense = l[6]
            transcript_info = l[8].split("=")[1].split(";")[0]
            transcript_name = re.sub("\.path\d+$", "", transcript_info)
            transcript_path = re.findall("path\d+$", transcript_info)[0]
            transcripts[transcript_name][transcript_path] = [
                    scaffold_name,
                    from_position,
                    to_position,
                    sense,
                    transcript_name,
                    transcript_path
                    ]

# Read transcriptome annotation table
with open(transcriptome_table) as infile:
    for line in infile:
        if not line.startswith("Name"):
            l = line.strip().split("\t")
            transcript_name = l[0]

            try:
                gene_accession = l[1]
                gene_name = l[2]
                gene_altnames = l[3]
                gene_pfam = l[4]
                gene_go = l[5]
            except:
                gene_accession = "na"
                gene_name = "na"
                gene_altnames = "na"
                gene_pfam = "na"
                gene_go = "na"

            for path in transcripts[transcript_name]:
                transcripts[transcript_name][path] += [
                        gene_accession,
                        gene_name,
                        gene_altnames,
                        gene_pfam,
                        gene_go
                        ]

# TODO
# Re-arrange genes by scaffold and position

# Write genome annotation tables
# If scaffold has no gene, put a line for this
# if scaffold has multiple genes, output them sorted by start position
# For each gene, give transcript and its annotation if available


genes = []
for transcript in sorted(transcripts):
    for path in transcripts[transcript]:
        genes.append(transcripts[transcript][path])

genes = sorted(genes)

with open(genome_table, "w") as outfile:
    outfile.write("\t".join([
        "scaffold_name",
        "from_position",
        "to_position",
        "sense",
        "transcript_name",
        "transcript_path",
        "gene_accession",
        "gene_name",
        "gene_altnames",
        "gene_pfam",
        "gene_go"
        ]) + "\n")

    for g in genes:
        outfile.write("\t".join([str(x) for x in g]) + "\n")
