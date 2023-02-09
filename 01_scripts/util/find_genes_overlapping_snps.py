#!/usr/bin/env python3
"""Get genes that overlap regions of interest, for example DMRs

Usage:
    <program> genome_annotation bedfile flanking_size output_genes

Parallel:
    parallel 01_scripts/util/find_genes_overlapping_regions.py \
            05_results/genome_annotation_table_simplified.tsv {} 0 {}.overlap ::: *.bed
"""

# Modules
from collections import defaultdict
import sys

def overlaps(gene_range, region_range, flanking_size):
    """Determine if gene_range overlaps region_range
    """
    gene_range[0] -= flanking_size
    gene_range[1] += flanking_size
    result = (gene_range[0] <= region_range[1]) and (gene_range[1] >= region_range[0])
    return result

# Parsing user input
try:
    genome_annotation = sys.argv[1]
    bedfile = sys.argv[2]
    flanking_size = int(sys.argv[3])
    output_genes = sys.argv[4]
except:
    print(__doc__)
    sys.exit(1)

# Get regions of interest
regions = defaultdict(list)

with open(bedfile) as infile:
    for line in infile:
        l = line.strip().split("\t")
        regions[l[0]].append([int(l[1]), int(l[1])])

# Find which genes overlap with the regions
# Report each gene only once
first_line_found = False
found_genes = set()

with open(output_genes, "wt") as outfile:
    with open(genome_annotation) as infile:

        for line in infile:
            if not first_line_found:
                first_line_found = True
                continue

            l = line.strip().split("\t")
            scaf = l[0]
            gene_range = [int(x) for x in l[1: 3]]

            for region_range in regions[scaf]:
                if overlaps(gene_range[:], region_range[:], flanking_size):
                    gene = l[4]
                    
                    if gene not in found_genes:
                        found_genes.add(gene)
                        outfile.write("\t".join([gene, scaf, str(region_range[0]), str(region_range[1])] + l) + "\n")
