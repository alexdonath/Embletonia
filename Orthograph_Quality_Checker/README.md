# Orthograph_Quality_Checker.py

**Orthograph_Quality_Checker** performs a quality assessment of transcriptome assemblies based on orthology predictions with [Orthograph](https://github.com/mptrsen/Orthograph)[^1].

## System requirements

---

* Python 3.6.4 or newer
* Required Python modules: `argparse`, `Bio`, `operator`, `os`, `re`, `shutil`, `sys`

## Parameters

---

The program has three parameters:

`-c/--config` (mandatory)

The config file (for an example, see below).

`-t/--tmpdir` (mandatory)

The path to the directory where the (temporary) summary files for individual assemblies are to be stored. **Note:** If not present, the directory will be automatically created.

`--reuse_tmp` (optional)

Setting `--reuse_tmp` allows you to re-use the summary files from a previous run that are stored in your temporary directory (see `-t/--tmpdir`) to skip the time-consuming step of analyzing all assemblies. This comes in handy if you only want to repeat the step leading to the final summary file.

## The config file

---

The config file has to be in text format; any file suffix will do.

An example config file could look like this:

    ALNDIR=./aln
    ORTHOGRAPH=./Orthograph
    ASSEMBLERS=BinPacker, Shannon
    TAXA=HW01_Armina_tigrina, HW02_Berghia_verrucicornis

`ALNDIR=` specifies the path to the directory where the alignments of the reference sequences reside that were used for orthology prediction. This usually is `Orthograph/sets/[setname]/aln`. Character strings following the tag may contain spaces.

`ORTHOGRAPH=` specifies the path to the directory where the Orthograph output directories are located.

`ASSEMBLERS=` specifies the names of the assemblers that were used to create the assemblies that are to be analyzed. The assembler names may contain spaces, but individual names have to be separated by commas.

`TAXA=` specified the names of the taxa that are to be analyzed. Taxon names may contain spaces, but individual names have to be separated by commas.

All paths have to be either absolute or relative to the location of `Orthograph_Quality_Checker.py`.

## Data preparation

---

In order for the program to work properly, the structure of the directory tree in the directory specified using the tag `ORTHOGRAPH=` has to look like this:
`ORTHOGRAPH/ASSEMBLER/TAXON/aa`

## The output

---

The final output is a tab-separated spreadsheet file (`Summarized_Orthograph_results.tsv`) that can be opened in a text editor or a spreadsheet editor like Excel.
The first column in the file contains the taxon names. The following fields in the same row each correspond to one assembly of this taxon.

There are four values in each of those fields:

1. The name of the assembler that was used to create the assembly
2. The number of orthologous groups predicted by Orthograph for this assembly
3. The total sequence length of all Orthograph hits for this assembly
4. The percentage of reference sequence length covered by the total sequence length of all Orthograph hits for this assembly [%]

---

[^1] Petersen, M., Meusemann, K., Donath, A. et al. Orthograph: a versatile tool for mapping coding nucleotide sequences to clusters of orthologous genes. BMC Bioinformatics 18, 111 (2017). [https://doi.org/10.1186/s12859-017-1529-8](https://doi.org/10.1186/s12859-017-1529-8)
