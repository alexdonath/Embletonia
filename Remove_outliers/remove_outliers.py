#!/usr/bin/env python3

### AUTHOR: D. Karmeinski

""" This script is meant for removing all outliers listed in outlier_2.txt.
    It will only work on aa alignments. The script has to be in the same
	directory as the outlier_2.txt file and the aa/ subdirectory.
"""

import os
from Bio import SeqIO
import shutil
import sys

### Check file system ###

print("Checking file system...")
print("Info: The aa directory should ONLY contain fasta files!")

aa_dir = './aa'

if os.path.exists(aa_dir):
	print("OK: aa directory is " + aa_dir)
else:
	sys.exit("No aa directory found!")

print("\nChecking files...")

aa_files = os.listdir(aa_dir)
print(aa_dir + " contains " + str(len(aa_files)) + " files")


### Get outlier info from outlier_2.txt ###

outliers = {}

print("\nStarting outlier removal...")

if os.path.exists('./outlier_2.txt'):
	print("Parsing outlier info from ./outlier_2.txt")
else:
	sys.exit("File ./outlier_2.txt not found!")

with open('outlier_2.txt') as file:
	for line in file:
		if "|" in line:
			line = line.strip()
			splitted = line.split("|")

			if splitted[0] not in outliers:
				outliers[splitted[0]] = []
				outliers[splitted[0]].append(splitted[2])
			else:
				outliers[splitted[0]].append(splitted[2])

files_w_outliers = len(outliers)
num_outliers = 0

for outlier in outliers:
	num_outliers += len(outliers[outlier])

print("File ./outlier_2.txt lists a total of " + str(num_outliers) + " outliers from " + str(files_w_outliers) + " files")


### Create directory for processed files ###

if os.path.exists('./aa_outliers_removed'):
	print("\nUsing directory ./aa_outliers_removed as output directory. Previous files will be overwritten!")
else:
	print("\nNo output directory found. Creating directory ./aa_outliers_removed...")
	os.makedirs('./aa_outliers_removed')


### Remove outliers from aa MSAs ###

print("\nRemoving outliers...")

for aa_file in aa_files:
	seq_objects = []

	splitted = aa_file.split(".")
	infile = os.path.join("./aa", aa_file)

	aa_out = ".".join([splitted[0], "aa", "fas"])
	outfile = os.path.join("./aa_outliers_removed", aa_out)

	if splitted[0] in outliers:
		seqs_to_remove = outliers[splitted[0]]

		for seq in SeqIO.parse(infile, "fasta"):
			taxon_id = seq.id.split("|")[2]

			if taxon_id in seqs_to_remove:
				continue
			else:
				seq_objects.append(seq)

		with open(outfile, "w") as file:
			for seq in seq_objects:
				file.write(">" + str(seq.id) + "\n")
				file.write(str(seq.seq) + "\n")

	else:
		shutil.copy(infile, outfile)

print("Done!")