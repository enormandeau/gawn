#!/usr/bin/env python3
"""Rename genes in GFF using fullnames in transcript annotation table

Usage:
    <program> input_gff input_transcriptome output_gff
"""

# Modules
import sys

# Parse user input
try:
    input_gff = sys.argv[1]
    input_transcriptome = sys.argv[2]
    output_gff = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Read transcriptome
transcriptome = [x.strip().split("\t")[:3] for x in open(input_transcriptome).readlines()]
transcript_names = {}

for t in transcriptome:
    if len(t) > 2:
        _id, name = t[0], t[2]

        if _id in transcript_names:
            print("WARNING: transcript {_id} found more than once")

        transcript_names[_id] = name

# Read gff and rename
with open(output_gff, "wt") as outfile:
    with open(input_gff, "rt") as infile:
        for line in infile:

            if line.startswith("#"):
                outfile.write(line)
                continue

            l = line.strip().split("\t")
            info = l[8].split(";")
            _id = ".".join(info[0][3:].split(".")[:2])

            try:
                name = transcript_names[_id]
            except:
                continue

            info[1] = "Name=" + name
            l[8] = ";".join(info)
            outfile.write("\t".join(l) + "\n")
