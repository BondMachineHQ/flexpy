#!/usr/bin/env python


"""Flexpy - FPGA Logic from EXpressions 
   Copyright 2025 - Mirko Mariotti - https://www.mirkomariotti.it

Usage:
  flexpy -e <expression> -o <outputfile> (--basm | --hls) [-d] [--config-file <config>] [-r <registersize>] [-t <type>] [--build-app] [--app-file <appfile>] [--emit-bmapi-maps] [--bmapi-maps-file <bmapi-maps-file>] [--io-mode <iomode>] [--neuron-statistics <neuron-statistics>] 
  flexpy -e <expression> --iomap-only --basm [-d] [--config-file <config>]
  flexpy -h | --help

Options:
  -d                                                  Debug mode.
  -h --help                                           Show this screen.
  -e <expression>                                     The expression to convert.
  -o <outputfile>                                     The output file.
  -r <registersize>, --register-size <registersize>   The size of the registers, only needed if the data type is variable size.
  -t <type>, --data-type <type>                       The type of the numbers, if not specified it is set to float32.
  --basm                                              Convert the expression to BASM.
  --hls                                               Convert the expression to HLS.
  --config-file <config>                              The JSON configuration file to use.
  --build-app                                         Build the application
  --app-file <appfile>                                The application file to generate.
  --emit-bmapi-maps                                   Emit the bmapi maps.
  --bmapi-maps-file <bmapi-maps-file>                 The file where to save the bmapi maps.
  --io-mode <iomode>                                  The iomode to use [default: sync].
  --iomap-only                                        Generate only the iomap file.
  --neuron-statistics <neuron-statistics>             Save the neuron statistics to a file.
"""
from docopt import docopt
import sympy as sp
import numpy as np
import json
from flexpyengine import flexpyEngine
from jinja2 import Environment, DictLoader

from files_cpynqapi import cpynqapi

def main():
	arguments = docopt(__doc__, version='Flexpy 0.0')
	
	# Create the expression
	exprFile = arguments["-e"]

	# Read the content of the file and read it
	f = open(exprFile, "r")
	expr = f.read()
	f.close()

	# Load the configuration file by executing the code
	localParams = {'spExpr': None, 'testRanges': None}
	globalParams = {'sp': sp, 'np': np}
	exec(expr, globalParams, localParams)
	spExpr = localParams['spExpr']
	testRanges = localParams['testRanges']

	if spExpr is None:
		print("Error: The expression is not valid")
		return

	config = None
	# Eventually load the JSON configuration file
	if arguments["--config-file"]:
		configFile = arguments["--config-file"]
		with open(configFile) as json_file:
			config = json.load(json_file)

	debugMode = False
	if arguments["-d"]:
		debugMode = True


	neuronStatistics = None
	if arguments["--neuron-statistics"]:
		neuronStatistics = arguments["--neuron-statistics"]
	eng=flexpyEngine(config, spExpr, regsize=arguments["--register-size"], type=arguments["--data-type"], debug=debugMode, neuronStatistics=neuronStatistics)

	if arguments["--io-mode"] == "async":
		eng.basm += "%meta bmdef global iomode: async\n"
	else:
		eng.basm += "%meta bmdef global iomode: sync\n"


	if arguments["--basm"]:
		outbasm=eng.to_basm()
		if not arguments["--iomap-only"]:
			# Save to a file the basm code
			with open(arguments["-o"], "w") as text_file:
				text_file.write(eng.basm)
		else:
			print(eng.inputs)
			print(eng.outputs)

		if arguments["--neuron-statistics"]:
			# Save the neuron statistics to a JSON file
			with open(arguments["--neuron-statistics"], "w") as json_file:
				json.dump(eng.neurons, json_file, indent=4)

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