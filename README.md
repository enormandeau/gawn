# GAWN v0.3.2 

## Genome Annotation Without Nightmares

Developed by [Eric Normandeau](https://github.com/enormandeau) in
[Louis Bernatchez](http://www.bio.ulaval.ca/louisbernatchez/presentation.htm)'s
laboratory with suggestions and important code contributions from
[Jérémy Le Luyer](https://github.com/jleluyer).

## Description

**GAWN** is a genome annotation pipeline that uses an assembled transcriptome (in nucleoties, not amino acids),
either from the same species or from a related species, to create an
evidence-based genome annotation. Its primary goal is to provide good enough
genome annotation with a fraction of the time and effort required to run
more complete genome annotation pipelines. It uses existing tools, such as GMAP,
TransDecoder, blastx, the Swissprot database, etc. to produce the annotation.
The result files are:

- A GFF3 annotation file
- A transcript annotation .tsv table
- A genome annotation .tsv table

The .tsv tables are formatted to maximize usability by non-specialized users.

## Use cases

This approach is especially useful to annotate genomes of species for which
there is a good assembled transcriptome. It will also work when a good
transcriptome is available for a related species. It provides only gene
annotations for available transcripts. As such, it does not depend on *ab
initio* gene prediction models.

## Overview of the analyses

During the analyses, the following steps are performed:

- Index the genome (`GMAP`)
- Annotate genes using available transcripts (`GMAP`)
- Annotate the transcripts (`blastx` and the Swissprot database)
- Produce a transcriptome annotation table (Python script)
- Produce a genome annotation table (Python script)
- TODO: add CpG island annotations

## Resources needed

**GAWN** depends on different tools to annotate genomes. The requirements in
terms of RAM, disk space, and time, is dependent on these tools. Here are
example requirements for three different eukaryote genomes. The annotation was
run on a Lenovo ThinkStation D20 with 8 Xeon CPUs (16 threads, 2.40GHz) on
Linux Mint 17 (Ubuntu 16.04). All of these datasets, except *Salvelinus fontinalis*
were run using the most recent genomes and transcriptomes available from Genbank.

| Genome                    | Size (Gbp)| RAM (GB)  | Final disc space (GB) | Time (h)  |
|---------------------------|-----------|-----------|-----------------------|-----------|
| Human genome              | 3.29      | 16        | 37                    | ~48       |
| *Salvelinus fontinalis*   | 2.67      | 14.3      | 31.2                  | ~48       |
| *Drosophila melanogaster* | 1.45      | 10.2      | 3.1                   | 28        |

## Installation

To use **GAWN**, you will need a local copy of its repository, which can be
[found here](https://github.com/enormandeau/gawn/archive/master.zip). Just
download and unzip the folder. Use a new downloaded folder for each analysis.

Different releases can be
[accessed here](https://github.com/enormandeau/gawn/releases). We suggest using
the latest release. Avoid any release prior to 0.3.1. Some of these older releases
are broken for some versions of the dependencies).

## Dependencies

You will also need to have the following programs installed on your computer. The
version numbers are the ones that have been tested. It is suggested that you use
these or more recent versions.

- GNU Linux or OSX
- bash 4+
- python 2.7+ or 3.6+
- cufflinks v2.2.1+
- gmap (2017-10-12)
- wget 1.17.1
- gnu parallel 2017xxxx+
- blastplus utilities (blastx) 2.7.1+ (**Very important**, do not use old blastplus binaries)
- a local copy of the [swissprot database](ftp://ftp.ncbi.nlm.nih.gov/blast/db/swissprot.tar.gz)

The relevant TransDecoder scripts are included with their license in
`01_scripts/TransDecoder`.

## Running the pipeline

For each new project, get a new copy of GAWN's repository from the
sources listed in the **Installation** section and copy your data in the
`03_data` folder.

- Install dependencies
- Download **GAWN** repository (see **Installation** section above)
- Put your genome and transcriptome fasta files (uncompressed) in `03_data`
- Edit the parameters in `02_info/gawn_config.sh` (you can rename the file)
- Run the following command:

```bash
./gawn 02_infos/gawn_config.sh  # or your renamed file
```

## Results

Once the pipeline has completed, all result files are found in the `05_results`
folder.

- A valid gff3 annotation file
- A transcriptome annotation .tsv table
- A genome annotation .tsv table

## License

CC share-alike

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">GAWN</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Eric Normandeau</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/enormandeau/gawn" rel="dct:source">https://github.com/enormandeau/gawn</a>.
