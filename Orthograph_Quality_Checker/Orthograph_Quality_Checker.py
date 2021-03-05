#!/usr/bin/env python3

### AUTHOR: D. Karmeinski

import argparse
import os
import sys
import re
import shutil
from Bio import SeqIO
from operator import attrgetter


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', help='path to your config file', required=True)
parser.add_argument('-t', '--tmpdir', help='path to directory for temporary summary files', required=True)
parser.add_argument('--reuse_tmp', help='re-use the summary files from a previous run without creating new ones', action='store_true')
args = parser.parse_args()



class ArgsFromFile():

	def read_args(self, config):
		with open(config) as file:
			for line in file:
				if 'ALNDIR=' in line:
					self.alndir = line.rstrip().split('=')[1]
				if 'ORTHOGRAPH=' in line:
					self.orthopath = line.rstrip().split('=')[1]
				if 'ASSEMBLERS=' in line:
					self.assemblers = re.sub(r'\s+', '', line.rstrip().split('=')[1]).split(',')
				if 'TAXA=' in line:
					self.taxa = re.sub(r'\s+', '', line.rstrip().split('=')[1]).split(',')


class AlnLengths():

	def get_length(self, alndir):
		self.lengths = {}
		self.total_length = 0

		for dirname, dirnames, filenames in os.walk(alndir):
			for filename in filenames:
				if '.aln.fa' in filename:
					for entry in SeqIO.parse(os.path.join(dirname, filename), "fasta"):

						self.lengths[filename.split('.')[0]] = len(entry.seq)
						break

		for key in self.lengths:
			self.total_length += self.lengths[key]


class AnalyzeAA():

	def analyze_aa(self, orthopath, assemblers, taxa):

		for taxon in taxa:
			for ass in assemblers:
				indir = '/'.join([orthopath, ass, taxon, 'aa'])
				lengths = {}

				if os.path.exists(indir) == False:
					sys.exit('Warning: ' + indir + ' does not exist!\nCheck if the parameters ORTHOGRAPH, ASSEMBLERS and TAXA in your config file ' + args.config + ' are correct!')

				print('Reading files in ' + indir)

				for dirname, dirnames, filenames in os.walk(indir):
					for filename in filenames:
						if '.aa.fa' in filename:
							for entry in SeqIO.parse(os.path.join(dirname, filename), "fasta"):

								if taxon in entry.id:
									lengths[filename.split('.')[0]] = len(re.sub(r'X', '', str(entry.seq)))

				outfile = os.path.join(args.tmpdir, '_'.join([taxon, ass]))
				print ('Writing summary to ' + outfile)

				with open(outfile, 'w') as file:
					file.write("OG_Id\tTranscript Length\tAlignment Length\n")

					for key in sorted(lengths):
						file.write(key + "\t" + str(lengths[key]) + "\t" + str(aln.lengths[key]) +"\n")


class Assemblies():

	def __init__(self, tmpdir, taxon, assembler):
		self.tmpdir = tmpdir
		self.taxon = taxon
		self.assembler = assembler


	def read_lengths(self):
		infile = os.path.join(self.tmpdir, '_'.join([self.taxon, self.assembler]))
		self.total_seqs = 0
		self.total_length = 0
		self.summed_aln_length = 0

		with open(infile) as file:
			for line in file:
				if 'OG_Id' in line:
					pass
				else:
					self.total_seqs += 1
					self.total_length += int(line.rstrip().split("\t")[1])
					self.summed_aln_length += int(line.rstrip().split("\t")[2])
					self.normalized_length = self.total_length / self.summed_aln_length



arguments = ArgsFromFile()
arguments.read_args(args.config)

print('Starting Orthograph_Quality_Checker.py with the following parameters:\n' + ' '.join(sys.argv) + "\n")
print('Alignment directory is: ' + arguments.alndir)
print('Orthograph output directory is: ' + arguments.orthopath)
print('Assemblers are: ' + ', '.join(arguments.assemblers))
print('Taxa are: ' + ', '.join(arguments.taxa) + "\n")


if os.path.exists(args.tmpdir) == True and args.reuse_tmp == False:
	print('Removing output directory ' + args.tmpdir + ' from previous run')
	shutil.rmtree(args.tmpdir)

if os.path.exists(args.tmpdir) == False and args.reuse_tmp == True:
	sys.exit('Warning: ' + args.tmpdir + ' does not exist!\nCheck if the argument -o/--tmpdir is correct!')

if os.path.exists(args.tmpdir) == False:
	print('Creating output directory ' + args.tmpdir)
	os.makedirs(args.tmpdir)


aln = AlnLengths()
aln.get_length(arguments.alndir)
print('Importing alignment lengths from ' + arguments.alndir)

if args.reuse_tmp == False:
	print('')
	aa_files = AnalyzeAA()
	aa_files.analyze_aa(arguments.orthopath, arguments.assemblers, arguments.taxa)
	print('')
else:
	print('Using summary files in ' + args.tmpdir + ' from a previous run')


with open('./Summarized_Orthograph_results.tsv', 'w') as file:
	print('Writing summary table to ./Summarized_Orthograph_results.tsv')
	taxa = []

	for taxon in arguments.taxa:
		assemblies = []

		for assembler in arguments.assemblers:
			assembly = Assemblies(args.tmpdir, taxon, assembler)
			assembly.read_lengths()
			assemblies.append(assembly)

		taxa.append(assemblies)

	for taxon in taxa:
		file.write(taxon[0].taxon + "\t")
		line = []

		for ass_obj in sorted(taxon, key = attrgetter('total_length'), reverse = True):
			line.append(ass_obj.assembler + ' ')
			line.append(str(ass_obj.total_seqs) + ' ')
			line.append(str(ass_obj.total_length) + ' ')
			line.append("%.2f" % (ass_obj.normalized_length * 100) + "\t")

		file.write(''.join(line).strip("\t") + "\n")

print('Done!')