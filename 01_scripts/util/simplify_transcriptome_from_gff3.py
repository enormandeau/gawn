#!/usr/bin/env python3
"""Use a gff3 file from GAWN and genome file to create simplified transcriptome

/!\ WARNING /!\ 
This script is experimental and does not seem to work properly

Usage:
    <program> input_fasta input_gff3 output_fasta
"""

# Modules
from collections import defaultdict
import itertools
import sys

# Classes
class Fasta(object):
    """Fasta object with name and sequence
    """

    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence.upper()

    def write_to_file(self, handle):
        handle.write(">" + self.name + "\n")
        handle.write(self.sequence + "\n")

    def __repr__(self):
        return self.name + " " + self.sequence[:31]

# Functions
def myopen(_file, mode="rt"):
    if _file.endswith(".gz"):
        return gzip.open(_file, mode=mode)

    else:
        return open(_file, mode=mode)

def fasta_iterator(input_file):
    """Takes a fasta file input_file and returns a fasta iterator
    """
    with myopen(input_file) as f:
        sequence = ""
        name = ""
        begun = False

        for line in f:
            line = line.strip()

            if line.startswith(">"):
                if begun:
                    yield Fasta(name, sequence)

                name = line[1:]
                sequence = ""
                begun = True

            else:
                sequence += line

        if name != "":
            yield Fasta(name, sequence)

def overlap(range1, range2):
    """Does the range (start1, end1) overlap with (start2, end2)?
    """
    start1, end1 = range1
    start2, end2 = range2

    decision = end1 >= start2 and end2 >= start1

    #print("Overlap" if decision else "different")
    #print(range1, end1 - start1)
    #print(range2, end2 - start2)
    #print()

    return decision

def get_gene_range(gene):
    unnested = [item for sublist in gene for item in sublist]
    return (min(unnested), max(unnested))

def to_ranges(iterable):
    iterable = sorted(set(iterable))
    for key, group in itertools.groupby(enumerate(iterable),
                                        lambda t: t[1] - t[0]):
        group = list(group)
        yield group[0][1], group[-1][1]

def combine_ranges(r1, r2):
    positions = set()

    for exon in r1 + r2:
        positions = positions.union(set(range(exon[0], exon[1] + 1)))

    return list(to_ranges(positions))

def extract_transcript_name(info):
    i = "_".join(info.split(";")[0].split(".")[0:2]).split("=")[1]
    return i

# Parse user input
try:
    input_fasta = sys.argv[1]
    input_gff3 = sys.argv[2]
    output_fasta = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Read gff3 file recreate isoforms
transcripts = defaultdict(lambda: defaultdict(list))
max_dist = 100000
counter = 0
max_counter = 1000000

with open(input_gff3) as infile:
    for line in infile:

        # Bypass header lines
        if line.startswith("#"):
            continue

        l = line.strip().split()

        # Keep only exons
        if not "exon" in l:
            continue

        scaffold, genome, tag, start, end, simil, orientation, \
                dot, transcript, _, _, _ = l 

        # Filters (minlen, similarity...)
        if int(simil) >= 90 and int(end) - int(start) >= 20:
            transcript_name = extract_transcript_name(transcript)
            transcripts[scaffold][transcript_name].append(
                    (int(start), int(end)))

        ### Counter to debug smaller parts of the input
        counter += 1
        #print(counter)
        if counter > max_counter:
            break

# Simplify genes
reduced = defaultdict(list)
tcount = 0
scount = 0
rcount = 0

for scaffold in transcripts:
    scount += 1
    #print("####### Scaffold:", scount)
    for transcript_name in transcripts[scaffold]:
        tcount += 1
        #print("transcript:", tcount)

        exons = transcripts[scaffold][transcript_name]
        r1 = get_gene_range(exons)

        if scaffold not in reduced:
            reduced[scaffold] = [exons]

        else:
            unique = False
            for i, gene in enumerate(reduced[scaffold]):
                r2 = get_gene_range(gene)

                # Exons are too far, treat as distinct genes
                if abs(exons[0][0] - gene[0][0]) > max_dist:
                    unique = True
                    break

                # If overlap, merge individual exons
                elif overlap(r1, r2):
                    if exons != gene:
                        #print(reduced[scaffold][i])
                        #print(exons)
                        reduced[scaffold][i] = combine_ranges(exons, gene)
                        rcount += 1
                        #print(reduced[scaffold][i])

                        # Stop looking for other hits once one is found
                        break
                
                else:
                    unique = True

            if unique:
                reduced[scaffold].append(exons)

num_genes = 0
num_exons = 0

for scaffold in reduced:
    num_genes += len(reduced[scaffold])

    for gene in reduced[scaffold]:
        num_exons += len(gene)

print(num_exons, "exons in", num_genes, "genes")
print("Reduced", rcount, "genes")
sys.exit()

# Extract transcriptome
sequences = fasta_iterator(input_fasta)
gene_counter = 0

with myopen(output_fasta, "wt") as outfile:
    for s in sequences:
        for gene in reduced[s.name]:
            gene_sequence = []

            for exon in sorted(gene):
                gene_sequence.append(
                        s.sequence[exon[0]: exon[1] + 1])

            gene_counter += 1
            gene_number = "000000" + str(gene_counter)
            gene_number = gene_number[-6:]
            gene_fasta = Fasta(
                    "transcript_" + gene_number,
                    "".join(gene_sequence)
                    )

            #print(gene_fasta)
            gene_fasta.write_to_file(outfile)
