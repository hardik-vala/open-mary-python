"""
Translates text files using the Open Mary online API.

@author: Hardik
"""

import argparse
import logging
import os
import re
import time

from open_mary import OpenMaryClient, OpenMaryXMLParser


# Configure logging.
log_format = "%(levelname)s: [%(asctime)s] %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)


def main():
	parser_description = ("")
	parser = argparse.ArgumentParser(description=parser_description)

	parser.add_argument('in_path', help="path to input")
	parser.add_argument('out_path', help="path to output")
	
	arg_help = ("target locale ('en_US' - (US) English, 'fr' - French, 'de' - "
		"German, 'it' - Italian, 'ru' - Russian, 'sv' - Swedish, 'te' - "
		"Telugu, or 'tu' - Turkish)")
	parser.add_argument('locale', help=arg_help)

	parser.add_argument('-d', '--dir', action='store_true',
		help="input and output correspond to directories")

	arg_help = ("interval (seconds) between translation of files (only "
		"applicable to directories)")
	parser.add_argument('-i', '--interval', help=arg_help, type=int, default=2)

	parser.add_argument('-f', '--format',
		help="format of output ('txt' or 'xml')", default='txt')

	arg_help = ("file extension for output files (only applicable to "
		"directories)")
	parser.add_argument('-x', '--ext', help=arg_help)
	
	args = parser.parse_args()

	# Make sure a valid format is given and if no output extension is specified,
	# set the default according to the format (only matters for directories).
	if args.format == 'txt':
		if args.ext is None:
			args.ext = '.txt'
	elif args.format == 'xml':
		if args.ext is None:
			args.ext = '.txt'
	else:
		raise ValueError("Format must be one of 'txt' or 'xml'")

	omc = OpenMaryClient()
	omxp = OpenMaryXMLParser()

	# Make sure a valid locale is passed.
	supported_locales = set(omc.locales())
	if args.locale not in supported_locales:
		raise ValueError("Locale '%s' not supported (run with -h for more info)"
			% args.locale)

	# If run in directory mode, create the output directory if it doesn't
	# already exist.
	if args.dir and not os.path.exists(args.out_path):
		logging.info("Creating directory %s..." % args.out_path)
		os.makedirs(args.out_path)

	# Drops the extension in a filename.
	drop_ext = lambda fname : '.'.join(fname.split('.')[:-1])

	# Translates a single file.
	def translate_file(in_fpath, out_fpath):
		logging.info("Translating %s..." % in_fpath)

		# Retrieve the Open Mary XML translation, stripping any numbers
		# beforehand.
		with open(in_fpath) as fin:
			text = fin.read()
			translation_xml = omc.translate(text, args.locale).encode('utf-8')

		logging.info("Done! Saving translation to %s..." % out_fpath)

		# Output the translation to file according to the specified format.
		if args.format == 'xml':
			with open(out_fpath, 'w') as fout:
				fout.write(translation_xml)
		elif args.format == 'txt':
			pro_text = omxp.parse_string_to_text(translation_xml)
			with open(out_fpath, 'w') as fout:
				fout.write(pro_text)

	# Run in directory mode, where input and output paths given correspond to
	# directories.
	if args.dir:
		# Loop through input directory files.
		dir_listing = os.listdir(args.in_path)
		file_cnt = len(dir_listing)
		for i, fname in enumerate(dir_listing):
			# Ignore hidden files.
			if fname.startswith('.'):
				continue

			in_fpath = os.path.join(args.in_path, fname)

			out_fname = drop_ext(fname) + args.ext
			out_fpath = os.path.join(args.out_path, out_fname)

			translate_file(in_fpath, out_fpath)

			if i < file_cnt - 1:
				logging.info("Sleeping for %d s..." % args.interval)
				time.sleep(args.interval)
	else:
		translate_file(args.in_path, args.out_path)


if __name__ == '__main__':
	main()
