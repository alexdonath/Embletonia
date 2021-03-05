#!/usr/bin/env python3

### AUTHOR: D. Karmeinski

""" This script is meant for removing all reference sequences from multiple
    sequence alignments. The script has to be in the same directory as the
	files from which the reference sequences are to be removed. It will
	create a subdirectory named "no_refseqs" to which the modified files
	will be saved. Input files have to have the ending .fas!
"""

import os
from Bio import SeqIO
import shutil


indir = "./"
outdir = os.path.join(indir, "no_refseqs")

if os.path.exists(outdir):
	print("Using " + outdir + " as output directory.\n")
else:
	os.makedirs(outdir)
	print("Creating output directory " + outdir + " ...\n")


fas_files = []

for f in os.listdir(indir):
	if ".fas" in f:
		fas_files.append(f)
	else:
		print("Skipping \"" + f + "\" as it does not seem to be a fasta file.\n Fasta files have to have the ending *.fas!")

print("\n" + str(len(fas_files)) + " fasta files found in input directory.")
print("Writing modified files to output directory...")


for f in fas_files:
	seq_objects = []

	infile = os.path.join(indir, f)
	outfile = os.path.join (outdir, f)

	for seq in SeqIO.parse(infile, "fasta"):
		if len(seq.id.split("|")) == 4:
			seq_objects.append(seq)
		else:
			continue

	with open(outfile, "w") as file:
		for seq in seq_objects:
			file.write(">" + str(seq.id) + "\n")
			file.write(str(seq.seq) + "\n")

print("Done!")