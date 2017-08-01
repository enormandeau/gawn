#!/usr/bin/env python
"""Annotate sequences with info from uniprot

Usage:
    ./01_scripts/03_annotate_genes.py sequence_file annotation_folder output_file
"""

# Modules
import sys
import os

# Classes
class Fasta(object):
    """Fasta object with name and sequence
    """
    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence
    def write_to_file(self, handle):
        handle.write(">" + self.name + "\n")
        handle.write(self.sequence + "\n")

class Info(object):
    """Uniprot informations about a sequence
    """
    def __init__(self, info_file, sequence):
        self.sequence_name = sequence.name.split(" ")[0]
        self.accession = ""
        self.fullname  = ""
        self.altnames  = ""
        self.pfam      = " "
        self.go        = " "
        self.goC       = " "
        self.goF       = " "
        self.goP       = " "

        def get_info(line):
            l = line.strip()[5:]
            if ":" in l:
                l = l.split(":")[1].strip()

            l = l.replace(";", "")
            return l

        try:
            with open(info_file) as ifile:
                for line in ifile:
                    if line.startswith("AC"):
                        self.accession = get_info(line)
                    elif line.startswith("DE   RecName: Full="):
                        l = line.replace("DE   RecName: Full=", "").strip()
                        l = l.replace(";", "")
                        self.fullname = l
                    elif line.startswith("DE   AltName: Full="):
                        l = line.replace("DE   AltName: Full=", "").strip()
                        self.altnames += l
                    elif line.startswith("DR   GO;"):
                        l = line.replace("DR   GO;", "").strip()
                        l1 = l.split(";")[0]
                        l2 = l.split(";")[1]
                        self.go += l1 + ";"
                        if "C:" in l2:
                            self.goC += l2 + ";"
                        if "F:" in l2:
                            self.goF += l2 + ";"
                        if "P:" in l2:
                            self.goP += l2 + ";"

                    elif line.startswith("DR   Pfam;"):
                        l = line.replace("DR   Pfam;", "").strip()
                        l = l.split(";")[0]
                        self.pfam += l + ";"
        except:
            pass

    def __repr__(self):
        return "\t".join([self.sequence_name,
            self.accession,
            self.fullname,
            self.altnames,
            self.pfam,
            self.go,
            self.goC,
            self.goF,
            self.goP])

# Functions
def fasta_iterator(input_file):
    """Takes a fasta file input_file and returns a fasta iterator
    """
    with open(input_file) as f:
        sequence = ""
        name = ""
        begun = False
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if begun:
                    yield Fasta(name, sequence)
                name = line.replace(">", "")
                sequence = ""
                begun = True
            else:
                sequence += line
        yield Fasta(name, sequence)

# Parse user input
try:
    sequence_file = sys.argv[1]
    annotation_folder = sys.argv[2]
    output_file = sys.argv[3]
except:
    print __doc__
    sys.exit(1)

# Read fasta file and get annotation
sequences = fasta_iterator(sequence_file)

with open(output_file, "w") as ofile:
    ofile.write("\t".join(["Name", "Accession", "Fullname", "Altnames", "Pfam", "GO", "CellularComponent", "Molecular Function", "Biological Process"]) + "\n")
    for s in sequences:
        name = s.name.split(" ")[0]
        info_file = os.path.join(annotation_folder, name + ".info")
        info = Info(info_file, s)
        ofile.write(str(info) + "\n")
