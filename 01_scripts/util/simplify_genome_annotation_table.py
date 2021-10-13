#!/usr/bin/env python3
"""Remove consecutive "identical" annotations from genome annotation table

Usage:
    <program> input_file max_region_increase output_file

Where:
    max_region_increase is the maximum increase in gene region size accepted.
    Should be between 1.0 and 2.0. Transcripts must overlap by at least 1bp
    to be considered.
"""

# Modules
import sys

# Functions
def enough_overlap(r1, r2, threshold):
    """Return whether the combined ranges are at MOST <treshold> times larger
    than the largest transcript.

    threshold is a float equals to or greater than 1.0 and smaller than 2.0.
    Eg: 1.1. Values above 2.0 will be equivalent to 2.0.
    """

    r1 = [int(x) for x in r1]
    r2 = [int(x) for x in r2]

    # No overlap at all
    if not (r1[1] > r2[0] and r1[0] < r2[1]):
        return False

    leftmost = min([r1[0], r1[1], r2[0], r2[1]])
    rightmost = max([r1[0], r1[1], r2[0], r2[1]])

    new_size = rightmost - leftmost
    max_size = max([r1[1] - r1[0], r2[1] - r2[0]])

    return (new_size / max_size) <= threshold

# Parse user input
try:
    input_file = sys.argv[1]
    max_region_increase = float(sys.argv[2])
    output_file = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Read gff3 file and filter annotations
prev = ("-1000", "0", "asdf")

with open(input_file, "rt") as infile:
    with open(output_file, "wt") as outfile:
        for line in infile:
            
            # Header
            if line.startswith("#") or line.startswith("ScaffoldName"):
                outfile.write(line)
                continue

            else:
                l = line.strip().split("\t")
                if l[6] in ["-", ""]:
                    continue

                info = (l[1], l[2], l[6])

                if info[2] == prev[2] and enough_overlap(info[:2], prev[:2], max_region_increase):
                    continue

                else:
                    outfile.write(line)
                    prev = info

    # Flush last read
    if info[2] != prev[2]:
        print("Flushed last entry")
        outfile.write(line)
