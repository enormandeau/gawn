#!/bin/bash

# Parameters
GENOME_NAME=$1

# Index genome with GMAP
gmap_build -D 03_data -d indexed_genome 03_data/"$GENOME_NAME"
