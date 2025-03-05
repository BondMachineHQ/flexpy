#!/usr/bin/env python


"""Flexpy - FPGA Logic from EXpressions 
   Copyright 2025 - Mirko Mariotti - https://www.mirkomariotti.it

Usage:
  flexpy -e <expression> -o <outputfile> (--basm | --hls) [-r <registersize>] [-t <type>]
  flexpy -h | --help

Options:
  -h --help                                         Show this screen.
  -e <expression>                                   The expression to convert.
  -o <outputfile>                                   The output file.
  -r <registersize>                                 The size of the registers, only needed if the data type is variable size.
  -t <type>                                         The type of the numbers, if not specified it is set to float32.
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

	localParams = {'spExpr': None}
	globalParams = {'sp': sp}
	exec(expr, globalParams, localParams)
	spExpr = localParams['spExpr']

	if spExpr is None:
		print("Error: The expression is not valid")
		return

	# spExpr = sp.parse_expr(expr, evaluate=False)
	# print(srepr(spEXpr))

	eng=flexpyEngine(spExpr, regsize=arguments["-r"], type=arguments["-t"])

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