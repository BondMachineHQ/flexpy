from hlsengine import hlsEngine
from basmengine import basmEngine

class flexpyEngine:
	def __init__(self, symexpr=None):
		self.expr = symexpr
		self.hls = ''
		self.basm = '''
%meta bmdef global registersize:32

%section terminal .romtext iomode:sync
	entry _start
_start:
	mov o0, r0
	j _start
%endsection

%section unary .romtext iomode:sync
	entry _start
_start:
	mov r0, i0
	mov o0, r0
	j _start
%endsection

%section binary .romtext iomode:sync
	entry _start
_start:
	mov r0, i0
	mov r1, i1
	mov o0, r0
	j _start
%endsection

'''
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
