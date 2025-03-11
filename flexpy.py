#!/usr/bin/env python


"""Flexpy - FPGA Logic from EXpressions 
   Copyright 2025 - Mirko Mariotti - https://www.mirkomariotti.it

Usage:
  flexpy -e <expression> -o <outputfile> (--basm | --hls) [-r <registersize>] [-t <type>] [--build-app] [--app-file <appfile>] [--emit-bmapi-maps] [--bmapi-maps-file <bmapi-maps-file>] [--iomode <iomode>]
  flexpy -h | --help

Options:
  -h --help                                         Show this screen.
  -e <expression>                                   The expression to convert.
  -o <outputfile>                                   The output file.
  -r <registersize>                                 The size of the registers, only needed if the data type is variable size.
  -t <type>                                         The type of the numbers, if not specified it is set to float32.
  --basm                                            Convert the expression to BASM.
  --hls                                             Convert the expression to HLS.
  --build-app                                       Build the application
  --app-file <appfile>                              The application file to generate.
  --emit-bmapi-maps                                 Emit the bmapi maps.
  --bmapi-maps-file <bmapi-maps-file>               The file where to save the bmapi maps.
  --iomode <iomode>                                 The iomode to use [default: sync].
"""
from docopt import docopt
import sympy as sp
import json
from flexpyengine import flexpyEngine
from jinja2 import Environment, DictLoader

from files_cpynqapi import cpynqapi

def main():
	arguments = docopt(__doc__, version='Flexpy 0.0')

	# Create the expression
	exprFile = arguments["-e"]

	# Read the content of the file and parse it
	f = open(exprFile, "r")
	expr = f.read()
	f.close()

	localParams = {'spExpr': None, 'testRanges': None}
	globalParams = {'sp': sp}
	exec(expr, globalParams, localParams)
	spExpr = localParams['spExpr']
	testRanges = localParams['testRanges']

	if spExpr is None:
		print("Error: The expression is not valid")
		return

	# spExpr = sp.parse_expr(expr, evaluate=False)
	# print(srepr(spEXpr))

	eng=flexpyEngine(spExpr, regsize=arguments["-r"], type=arguments["-t"])

	if arguments["--iomode"] == "async":
		eng.basm += "%meta bmdef global iomode: async\n"
	else:
		eng.basm += "%meta bmdef global iomode: sync\n"


	if arguments["--basm"]:
		outbasm=eng.to_basm()
		# Save to a file the basm code
		with open(arguments["-o"], "w") as text_file:
			text_file.write(eng.basm)

		if arguments["--build-app"]:
			if arguments["--app-file"]:

				items = [{"bminputs": str(len(eng.inputs)), "bmoutputs": str(len(eng.outputs))}]
				# Save to a file the app code
				with open(arguments["--app-file"], "w") as appFile:
					env = Environment(loader=DictLoader({'cpynqapi': cpynqapi}))
					template = env.get_template('cpynqapi')
					appFile.write(template.render(items=items))
			else:
				print("Error: The app file is not specified")
				return
		
		if arguments["--emit-bmapi-maps"]:
			if arguments["--bmapi-maps-file"]:
				# Save to a file the bmapi maps
				with open(arguments["--bmapi-maps-file"], "w") as bmapiFile:
					assoc={}
					for i in range(len(eng.inputs)):
						assoc["i"+str(i)]=str(i)
					for i in range(len(eng.outputs)):
						assoc["o"+str(i)]=str(i)
					mapFile= {"Assoc": assoc}
					json.dump(mapFile, bmapiFile)
			else:
				print("Error: The bmapi maps file is not specified")
				return

	elif arguments["--hls"]:
		outhls=eng.to_hls()
		# Save to a file the hls code
		with open(arguments["-o"], "w") as text_file:
			text_file.write(eng.hls)

if __name__ == '__main__':
	main()