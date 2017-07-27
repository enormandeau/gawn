#!/bin/bash

# Parameters
GENOME_NAME=$1

# Index genome with GMAP
gmap_build --dir 03_data 03_data/"$GENOME_NAME" -d indexed_genome
