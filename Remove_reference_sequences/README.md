# remove_reference_sequences.py

The script removes all sequences belonging to reference species from the alignments. Reference sequences are identified using the 1KITE<sup>[1](#one)</sup> sequence header format. Thus, the script can be used on any alignment that follows this header format.

## System requirements

* Python 3.6.4 or newer
* Required Python modules: `Bio`, `os`, `shutil`

## Other requirements

The script has to be in the same directory as the files from which the reference sequences are to be removed.

Note that input files have to have the ending `.fas[ta]`.

## Output

It will automatically create a subdirectory named `no_refseqs/`, in which the modified files will be saved.

---

<a name="one">[1]</a> Misof, B., Liu, S., Meusemann, K. et al. Phylogenomics resolves the timing and pattern of insect evolution. Science 346, 6210 (2014). [https://doi.org/10.1126/science.1257570](https://doi.org/10.1126/science.1257570)
