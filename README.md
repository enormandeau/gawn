# GAWN v0.1

## GAWN (Genome Annotation Without Nightmares)

Developed by [Eric Normandeau](https://github.com/enormandeau) in
[Louis Bernatchez](http://www.bio.ulaval.ca/louisbernatchez/presentation.htm)'s
laboratory.

See license information at the end of this file.

## Documentation

This documentation file can be
[found here](https://github.com/enormandeau/gawn/blob/master/README.md).

## Description

**GAWN** is a genome annotation pipeline that uses an assembled transcriptome,
either from the same or a related species, to create evidence-based annotation.
Its primary goal is to provide good enough genome annotation rapidly.

**GAWN** annotates the transcriptome using Swissprot, maps it on the genome
with GMAP, and adds UTR-3 and UTR-5 annotations with TransDecoder and
Cufflinks. The result files are:

- A GFF3 annotation file
- A transcript annotation CSV table
- A genome annotation CSV table.

The CSV tables are formatted to maximize usability by non-specialized users.

## Use cases

The approach implemented in **GAWN** is especially useful to annotate genomes
of species for which there is a good assembled transcriptome. **GAWN** will
also work when a good transcriptome is available for a related species. It
provides only gene annotations for available transcripts then adds UTR regions.
As such, it does not depend on *ab initio* gene prediction models.

## Overview of the analyses

During the analyses, the following steps are performed:

- Index the genome (`GMAP`)
- Annotate genes using available transcripts (`GMAP`)
- Add 3' and 5' UTR regions (`cufflinks` and `TransDecoder`)
- TODO: Produce transcriptome annotation table (Python script)
- TODO: Produce genome annotation table (Python script)

## Installation

To use **GAWN**, you will need a local copy of its repository, which can be
[found here](https://github.com/enormandeau/gawn/archive/master.zip).

Different releases can be
[accessed here](https://github.com/enormandeau/gawn/releases). It is
recommended to use the latest version or at least version 1.3.

## Dependencies

You will also need to have the following programs installed on your computer.

- OSX or GNU Linux
- bash 4+
- python 2.7+ (TODO or 3.5+)
- cufflinks v2.2.1+

The relevant TransDecoder scripts are included with their license in
`01_scripts/TransDecoder`.

## Running the pipeline

For each new project, get a new copy of the **GAWN** repository from the
sources listed in the **Installation** section and copy your data in the
`03_data` folder.

- Install dependencies if needed
- Download **GAWN** (see **Installation** section above)
- Put your genome and transcriptome fasta files (uncompressed) in `03_data`
- Make a copy of `02_info/gawn_config.sh` and edit the parameters
- Run the following command:

```bash
./gawn 02_info/MY_CONFIG_FILE.sh
```

## Results

Once the pipeline has completed, all result files are found in the `05_results`
folder.

### GFF3
TODO: Description...

- `asdf.gff3`

### Transcriptome table
TODO: Description...

- `asdf.csv`

### Genome table
TODO: Description...

- `asdf.csv`

## Test dataset
# TODO

### WARNING: Not yet available
A test dataset is available as a
[sister repository on GitHub](https://github.com/enormandeau/gawn_test_dataset).

Download the repository and then move the data in **GAWN**'s `03_data` folder.
Follow the normal pipeline procedure to analyse this small dataset. It should
run in one to ten minutes depending on your computer.

## License

CC share-alike

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">GAWN</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Eric Normandeau</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/enormandeau/gawn" rel="dct:source">https://github.com/enormandeau/gawn</a>.
