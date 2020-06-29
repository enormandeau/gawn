#!/usr/bin/env python3
"""Remove consecutive "identical" annotations from genome annotation table

Usage:
    <program> input_file output_file
"""

# Modules
import sys

# Functions
def enough_overlap(r1, r2, threshold):
    """Return whether the combined ranges are at MOST <treshold> times larger
    than the largest transcript.

    threshold is a float equals to or greater than 1. eg: 1.1
    """

    # No overlap at all
    if not (r1[1] > r2[0] and r1[0] < r2[1]):
        return False

    r1 = set(range(int(r1[0]), int(r1[1]) + 1))
    r2 = set(range(int(r2[0]), int(r2[1]) + 1))
    rtot = len(r1.union(r2))
    rmax = max(len(r1), len(r2))

    return (rtot / rmax) <= threshold

# Parse user input
try:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
except:
    print(__doc__)
    sys.exit(1)

# Read gff3 file and filter annotations
previous_info = ("-1000", "0", "asdf")

with open(input_file, "rt") as infile:
    with open(output_file, "wt") as outfile:
        for line in infile:
            
            # Header
            if line.startswith("#") or line.startswith("ScaffoldName"):
                outfile.write(line)
                continue

            else:
                l = line.strip().split("\t")
                if l[8] in ["-", ""]:
                    continue

                info = (l[1], l[2], l[8])

                if info[:2] == previous_info[:2]:
                    continue

                elif info[2] == previous_info[2] and enough_overlap(info[:2], previous_info[:2], 1.1):
                    continue

                else:
                    outfile.write(line)
                    previous_info = info
