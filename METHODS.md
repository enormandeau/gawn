# Overview of GAWN methods

Genome annotation was performed automatically by using GAWN v0.3.2 (https://github.com/enormandeau/gawn)

- Genome: ???
- Transcriptome: ???

Briefly,

- Genome indexed with gmap (v2024-11-20, command gmap_build, default parameters).
- Find transcript positions with gmap (v2024-11-20, -f gff3_gene --gff3-add-separator=0).
- Annotate transcripts by blasting on swissprot database with blast (v2.16.0+, command blastx, -evalue 1e-3 -output 6 -max_target_seq 1).
- Automatically retrieve uniprot information from www.uniprot.org and annotate the transcripts based on their blast hits.
- Produce a table for each of the transcripts found in the genome and the annotation of their corresponding swissprot proteins.
