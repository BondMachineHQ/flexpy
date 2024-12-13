#!/usr/bin/env python

from sympy import *
# from qiskit import QuantumCircuit
# from qiskit.circuit import Parameter, ParameterVector
# from qiskit_symb.quantum_info import Operator
# from IPython import display

# y = Parameter('y')
# p = ParameterVector('p', length=2)

# pqc = QuantumCircuit(2)
# pqc.ry(y, 0)
# pqc.cx(0, 1)
# pqc.u(0, *p, 1)

# pqc.draw('mpl')

# op = Operator(pqc)
# sm = op.to_sympy()

# test = sm[3,0]
x = Symbol('x')
l = Symbol('l')
test = (1+x)+l

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
	def hlsEngine(self, expr):
		self.index+=1
		myIndex = int(self.index)
		out = "node_"+str(myIndex)
		if not myIndex == 1:
			if len(expr.args) == 0:
				# This is an input node, create a link using the index among all the inputs, even if inputs grow the index will be unique
				if not str(expr) in self.inputs:
					self.inputs.append(str(expr))
				inIdx = self.inputs.index(str(expr))
				self.hls += "TERMINAL\n"
			else:
				# Create my side of the link, my caller will create the other side
				for i in range(len(expr.args)):
					arg=expr.args[i]
					inp,idx=self.hlsEngine(arg)
					self.hls += "\n"
					# Create link to the called nodeindex
				self.hls += "\n"
		else:
			self.hls += "void func(unsigned int N, ARGS){\n"
			self.hls += "#pragma hls interface mode=m_axi port=x offset=slave bundle=gmem\n"
			self.hls += "#pragma hls interface mode=m_axi port=y offset=slave bundle=gmem\n"
			self.hls += "#pragma hls interface mode=m_axi port=z offset=slave bundle=gmem\n"
			self.hls += "for(int i = 0; i < N; i++){\n"
			self.hls += "  #pragma hls pipeline\n"
			self.hls += "  out[i] = OP;\n"
			self.hls += " }\n"
			self.hls += "\n"
		return out,myIndex
	def basmEngine(self, expr):
		self.index+=1
		myIndex = int(self.index)
		out = "node_"+str(myIndex)+"_link"
		if myIndex == 1:
			self.basm += "%meta ioatt "+out+" cp:bm, type: output, index: 0\n"
		# self.basm += "#######" + str(expr) +" ## "+ str(myIndex)+"\n"	
		if len(expr.args) == 0:
			# This is an input node, create a link using the index among all the inputs, even if inputs grow the index will be unique
			if not str(expr) in self.inputs:
				self.inputs.append(str(expr))
			inIdx = self.inputs.index(str(expr))
			# self.basm += "%meta iodef "+out+"\n"
			self.basm += "%meta ioatt "+out+" cp:bm, index: "+str(inIdx)+", type: input\n"
			return out,myIndex
		else:
			# Create the processor
			if len(expr.args) == 1:
				self.basm += "%meta cpdef node_"+str(myIndex)+" romcode: unary, execmode: ha\n"
			else:
				self.basm += "%meta cpdef node_"+str(myIndex)+" romcode: binary, execmode: ha\n"
			# Create my side of the link, my caller will create the other side
			for i in range(len(expr.args)):
				arg=expr.args[i]
				inp,idx=self.basmEngine(arg)
				self.basm += "%meta ioatt "+inp+" cp: node_"+str(myIndex)+", type: input, index: "+str(i)+"\n"
				# Create link to the called nodeindex
			# self.basm += "%meta iodef "+out+"\n"
			self.basm += "%meta ioatt "+out+" cp: node_"+str(myIndex)+", type: output, index: 0\n"
			return out,myIndex
		
eng=flexpyEngine(test)
outbasm=eng.to_basm()
outhls=eng.to_hls()

# Save to a file the basm code
with open("test.basm", "w") as text_file:
    text_file.write(eng.basm)

# Save to a file the HLS code
with open("test.hls", "w") as text_file:
    text_file.write(eng.hls)