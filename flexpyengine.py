from ast import expr
import sys
import subprocess
import json
import sympy as sp
from hlsengine import hlsEngine
from basmengine import basmEngine, basmArgsProcessor, basmExprPreprocessor

class flexpyEngine:
	def __init__(self, config=None, symexpr=None, type=None, regsize=None, debug=False, neuronStatistics=None, deviceExpr=None):
		self.debug = debug
		self.config = config
		if type == None:
			type = 'float32'
			
		findSize, findPrefix, findOps = self.callBmNumbers(type)
		self.neuronStatistics = neuronStatistics
		self.neurons={}
		self.type = type
		self.prefix = findPrefix
		self.ops = findOps
		self.deviceExpr = deviceExpr
		self.currentDevice = None
		self.currentDeviceIdx = 0
		self.opsstring = ''
		for k,v in findOps.items():
			self.opsstring += k+":"+v+","
		self.opsstring = self.opsstring[:-1]
		# If the configuration has parameters, use them to populate the params string
		if self.config != None and 'params' in self.config:
			self.params = ''
			for k,v in self.config['params'].items():
				self.params += k+":"+v+","
			self.params = self.params[:-1]
		else:
			self.params = ''

		if regsize is None:
			if findSize == -1:
				print ("Error: for the specified type, a register size must be provided")
				sys.exit(1)
			else:
				self.regsize = findSize
		else:
			if findSize != -1 and findSize != regsize:
				print ("Error: the specified register size does not match the type")
				sys.exit(1)
			else:
				self.regsize = regsize

		self.expr = symexpr
		self.hls = ''
		self.basm = '''%meta bmdef global registersize: '''+self.regsize+'''
'''
		self.inputs = []
		self.outputs = []
		self.index = 0
		self.mindex = 0

	def addToStatistics(self, neuron):
		if neuron not in self.neurons:
			self.neurons[neuron] = 1
		else:
			self.neurons[neuron] += 1

	def to_basm(self):
		self.index = 0
		self.inputs = []
		self.outputs = []
		for e in self.serializeExpr(self.expr):
			self.newout = True
			self.basmEngine(e)
		return self.basm
	def to_hls(self):
		self.index = 0
		self.inputs = []
		self.outputs = []
		for e in self.serializeExpr(self.expr):
			self.newout = True
			self.hlsEngine(e)
		return self.hls
	def serializeExpr(self, expr):
		if expr.is_Matrix:
			for i in range(expr.shape[0]):
				for j in range(expr.shape[1]):
					yield expr[i,j]
		elif type(expr) == sp.tensor.array.dense_ndim_array.ImmutableDenseNDimArray:
			fl = sp.flatten(expr)
			for i in fl:
				yield i
		else:
			yield expr

	def asFloat(self, realPart, expr):
		try:
			expr.is_number
		except:
			print ("Error: the expression is not a number")
			sys.exit(1)

		if expr == sp.I:
			if realPart:
				return 0.0
			else:
				return 1.0

		if expr == sp.pi:
			if realPart:
				return 3.141592653589793
			else:
				return 0.0
			
		if expr == sp.GoldenRatio:
			if realPart:
				return 1.618033988749895
			else:
				return 0.0
			
		if expr == sp.E:
			if realPart:
				return 2.718281828459045
			else:
				return 0.0

		if expr == sp.EulerGamma:
			if realPart:
				return 0.577215664901532
			else:
				return 0.0
			
		if expr == sp.Catalan:
			if realPart:
				return 0.915965594177219
			else:
				return 0.0
			
		if expr == sp.S.Half:
			if realPart:
				return 0.5
			else:
				return 0.0

		if realPart:
			return expr.evalf().as_real_imag()[0]
		else:
			return expr.evalf().as_real_imag()[1]

	def callBmNumbers(self, type):
		# Check if the bmnumbers executable is available
		try:
			bmNumbers = subprocess.Popen(['bmnumbers'], stdout=subprocess.PIPE)
			bmNumbers.wait()
		except:
			print ("Error: bmnumbers executable not found")
			sys.exit(1)

		# Call the bmnumbers executable to get the size of the type
		try:
			bmNumbers = subprocess.Popen(['bmnumbers',"-get-size", type], stdout=subprocess.PIPE)
			bmNumbers.wait()
			if bmNumbers.returncode == 1:
				print ("Error: the type is not supported")
				sys.exit(1)
			findSize = bmNumbers.stdout.read().decode('utf-8').strip()
		except:
			print ("Error: bmnumbers failed to get the size of the type")
			sys.exit(1)

		# Call the bmnumbers executable to get the prefix of the type
		try:
			bmNumbers = subprocess.Popen(['bmnumbers',"-get-prefix", type], stdout=subprocess.PIPE)
			bmNumbers.wait()
			if bmNumbers.returncode == 1:
				print ("Error: the type is not supported")
				sys.exit(1)
			findPrefix = bmNumbers.stdout.read().decode('utf-8').strip()
		except:
			print ("Error: bmnumbers failed to get the prefix of the type")
			sys.exit(1)

		# Call the bmnumbers executable to get the operations of the type
		try:
			bmNumbers = subprocess.Popen(['bmnumbers',"-get-instructions", type], stdout=subprocess.PIPE)
			bmNumbers.wait()
			if bmNumbers.returncode == 1:
				print ("Error: the type is not supported")
				sys.exit(1)
			findOps = bmNumbers.stdout.read().decode('utf-8').strip()
			# unmarshal operations from JSON to a map
			findOps = json.loads(findOps)
		except:
			print ("Error: bmnumbers failed to get the operations of the type")
			sys.exit(1)

		return findSize, findPrefix, findOps

flexpyEngine.hlsEngine = hlsEngine
flexpyEngine.basmEngine = basmEngine
flexpyEngine.basmArgsProcessor = basmArgsProcessor
flexpyEngine.basmExprPreprocessor = basmExprPreprocessor
