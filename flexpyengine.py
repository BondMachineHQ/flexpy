from hlsengine import hlsEngine
from basmengine import basmEngine, basmArgsProcessor

class flexpyEngine:
	def __init__(self, symexpr=None, type=None, prefix=None, regsize=None):
		if type is None: type = 'float'
		if prefix is None: prefix = '0f'
		if regsize is None: regsize = '32'
		self.expr = symexpr
		self.hls = ''
		self.basm = '''
%meta bmdef global registersize: '''+regsize+'''
'''
		self.type = type
		self.prefix = prefix
		self.ops = {"addop": "add", "multop": "mult"}
		self.regsize = regsize
		self.inputs = []
		self.index = 0

	def to_basm(self):
		self.index = 0
		self.inputs = []
		self.basmEngine(self.expr)
		return self.basm
	def to_hls(self):
		self.index = 0
		self.inputs = []
		self.hlsEngine(self.expr)
		return self.hls


flexpyEngine.hlsEngine = hlsEngine
flexpyEngine.basmEngine = basmEngine
flexpyEngine.basmArgsProcessor = basmArgsProcessor
