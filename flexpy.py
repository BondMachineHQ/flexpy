#!/usr/bin/env python


"""Flexpy - FPGA Logic from EXpressions 
   Copyright 2025 - Mirko Mariotti - https://www.mirkomariotti.it

Usage:
  flexpy -e <expression> -o <outputfile> (--basm | --hls)
  flexpy -h | --help

Options:
  -h --help                                         Show this screen.
  -e <expression>                                   The expression to convert.
  -o <outputfile>                                   The output file.
  --basm                                            Convert the expression to BASM.
  --hls                                             Convert the expression to HLS.
"""

from docopt import docopt
import sympy as sp

from flexpyengine import flexpyEngine

def main():
	arguments = docopt(__doc__, version='Flexpy 0.0')

	# Create the expression
	exprFile = arguments["-e"]

	# Read the content of the file and parse it
	f = open(exprFile, "r")
	expr = f.read()
	f.close()

	spEXpr = sp.parsing.sympy_parser.parse_expr(expr)
	print(spEXpr)

	eng=flexpyEngine(spEXpr)

	if arguments["--basm"]:
		outbasm=eng.to_basm()
		# Save to a file the basm code
		with open(arguments["-o"], "w") as text_file:
			text_file.write(eng.basm)

	if arguments["--hls"]:
		outhls=eng.to_hls()
		# Save to a file the hls code
		with open(arguments["-o"], "w") as text_file:
			text_file.write(eng.hls)

if __name__ == '__main__':
	main()