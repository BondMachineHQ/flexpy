#!/usr/bin/env python


"""Flexpy - FPGA Logic from EXpressions 
   Copyright 2025 - Mirko Mariotti - https://www.mirkomariotti.it

Usage:
  flexpy -e <expression> -o <outputfile> (--basm | --hls) [-r <registersize>] [-p <prefix>] [-t <type>]
  flexpy -h | --help

Options:
  -h --help                                         Show this screen.
  -e <expression>                                   The expression to convert.
  -o <outputfile>                                   The output file.
  -r <registersize>                                 The size of the registers.
  -p <prefix>                                       The prefix for the numbers.
  -t <type>                                         The type of the numbers.
  --basm                                            Convert the expression to BASM.
  --hls                                             Convert the expression to HLS.
"""

from docopt import docopt
import sympy as sp
from sympy import *
from flexpyengine import flexpyEngine

def main():
	arguments = docopt(__doc__, version='Flexpy 0.0')

	# Create the expression
	exprFile = arguments["-e"]

	# Read the content of the file and parse it
	f = open(exprFile, "r")
	expr = f.read()
	f.close()

	with sp.evaluate(False):
		spEXpr = sp.parsing.sympy_parser.parse_expr(expr)
	# print(srepr(spEXpr))

	eng=flexpyEngine(spEXpr, regsize=arguments["-r"], prefix=arguments["-p"], type=arguments["-t"])

	if arguments["--basm"]:
		outbasm=eng.to_basm()
		# Save to a file the basm code
		with open(arguments["-o"], "w") as text_file:
			text_file.write(eng.basm)

	elif arguments["--hls"]:
		outhls=eng.to_hls()
		# Save to a file the hls code
		with open(arguments["-o"], "w") as text_file:
			text_file.write(eng.hls)

if __name__ == '__main__':
	main()