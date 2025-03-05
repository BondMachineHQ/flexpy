import sys
import sympy as sp

def basmEngine(self, expr):
	self.index+=1
	mId = "_"+str(self.mindex)+"_"
	myIndex = int(self.index)

	outRe = ""
	outIm = ""

	hasReal,hasImm = tuple(x != 0 for x in expr.as_real_imag())
	if hasReal:
		outRe = "node"+mId+str(myIndex)+"_link_re"
	if hasImm:
		outIm = "node"+mId+str(myIndex)+"_link_im"
	if myIndex == 1:
		if hasReal:
			self.outputs.append("real: "+str(expr))
			print(str(len(self.outputs)-1) + " -> real: "+str(expr))
			self.basm += "%meta filinkatt "+outRe+" fi:ext, type: output, index: "+str(len(self.outputs)-1)+"\n"
		if hasImm:
			self.outputs.append("imag: "+str(expr))
			print(str(len(self.outputs)-1) + " -> imag: "+str(expr))
			self.basm += "%meta filinkatt "+outIm+" fi:ext, type: output, index: "+str(len(self.outputs)-1)+"\n"
	if len(expr.args) == 0:
		# print(expr)
		# This is an input node, create a link using the index among all the inputs, even if inputs grow the index will be unique
		# this is true even when basmEngine is called multiple times to generate matrix elements	
		if hasReal:
			if not "real: "+str(expr) in self.inputs:
				self.inputs.append("real: "+str(expr))
				print("real: "+str(expr)+" -> "+str(len(self.inputs)-1))
			inIdx = self.inputs.index("real: "+str(expr))
			self.basm += "%meta filinkatt "+outRe+" fi:ext, index: "+str(inIdx)+", type: input\n"
		if hasImm:
			if not "imag: "+str(expr) in self.inputs:
				self.inputs.append("imag: "+str(expr))
				print("imag: "+str(expr)+" -> "+str(len(self.inputs)-1))
			inIdx = self.inputs.index("imag: "+str(expr))
			self.basm += "%meta filinkatt "+outIm+" fi:ext, index: "+str(inIdx)+", type: input\n"
		return outRe,outIm,myIndex
	else:
		# Preprocess the expression
		expr = self.basmExprPreprocessor(expr)
		# print(expr)

		# Create the processor and return the arguments really used, not the ones eventually absorbed by the processor
		realArgs = self.basmArgsProcessor(expr, myIndex)
		# Create my side of the link, my caller will create the other side

		linkIdx = 0
		for i in range(len(realArgs)):
			arg=realArgs[i]
			inpRe,inpIm,idx=self.basmEngine(arg)
			if inpRe != "":
				self.basm += "%meta filinkatt "+inpRe+" fi: node"+mId+str(myIndex)+", type: input, index: "+str(linkIdx)+"\n"
				linkIdx+=1
			if inpIm != "":
				self.basm += "%meta filinkatt "+inpIm+" fi: node"+mId+str(myIndex)+", type: input, index: "+str(linkIdx)+"\n"
				linkIdx+=1
			# Create link to the called nodeindex

		oi = 0	
		if hasReal:
			self.basm += "%meta filinkatt "+outRe+" fi: node"+mId+str(myIndex)+", type: output, index: "+str(oi)+"\n"
			oi+=1
		if hasImm:
			self.basm += "%meta filinkatt "+outIm+" fi: node"+mId+str(myIndex)+", type: output, index: "+str(oi)+"\n"

		return outRe,outIm,myIndex

def basmExprPreprocessor(self, expr):
	# The preprocessor will take care of the expressions that are not directly supported by the BASM engine
	# but can be transformed into a supported expression
	# For example, an addition of more than 2 elements can be transformed into a chain of additions
	# Version 1 implementation
	# Addition of more than 2 elements
	if expr.func == sp.Add and len(expr.args) > 2:
		for i in range(0,len(expr.args),2):
			with sp.evaluate(False):
				if i == 0:
					newExpr = expr.args[i] + expr.args[i+1]
				else:
					newExpr = newExpr + (expr.args[i] + expr.args[i+1])
				
				if i+2 == len(expr.args)-1:
					newExpr = newExpr + expr.args[i+2]
					break
		expr = newExpr

	# Multiplication of more than 2 elements
	if expr.func == sp.Mul and len(expr.args) > 2:
		for i in range(0,len(expr.args),2):
			with sp.evaluate(False):
				if i == 0:
					newExpr = expr.args[i] * expr.args[i+1]
				else:
					newExpr = newExpr * (expr.args[i] * expr.args[i+1])
				
				if i+2 == len(expr.args)-1:
					newExpr = newExpr * expr.args[i+2]
					break
		expr = newExpr

	# Version 2 (check issue #2)
	## TODO: Implement this		 			
	return expr

def basmArgsProcessor(self, expr, myIndex):
	mId = "_"+str(self.mindex)+"_"
	realArsg = []
	self.basm += "%meta cpdef node"+mId+str(myIndex)+" fragcollapse:node"+mId+str(myIndex)+"\n"

	# Start identifying the node and mapping it to known fragments
	# Addition
	if expr.func == sp.Add or expr.func == sp.Mul:
		if len(expr.args) == 2:
			arg0 = expr.args[0]
			arg1 = expr.args[1]
			if expr.func == sp.Add:
				opName = "add"
			elif expr.func == sp.Mul:
				opName = "mult"

			# Check if the arguments have real/imaginary parts
			arg0Real,arg0Im = tuple(x != 0 for x in arg0.as_real_imag())
			arg1Real,arg1Im = tuple(x != 0 for x in arg1.as_real_imag())

			# print (arg0,arg1)
			# print(arg0Real,arg0Im,arg1Real,arg1Im)

			# Check whether the arguments are real, imaginary or full complex numbers
			if arg0Real and arg0Im:
				arg0Type = "full"
			elif arg0Real:
				arg0Type = "real"
			elif arg0Im:
				arg0Type = "imag"
			else:
				arg0Type = "zero"

			if arg1Real and arg1Im:
				arg1Type = "full"
			elif arg1Real:
				arg1Type = "real"
			elif arg1Im:
				arg1Type = "imag"
			else:
				arg1Type = "zero"

			# Check if the arguments are numbers
			numParams = 0 
			numValReal = 0
			numValIm = 0
			realArsg = []
			if arg0.is_number:
				numParams+=1
				if arg0Real:
					numValReal = arg0.as_real_imag()[0]
				if arg0Im:
					numValIm = arg0.as_real_imag()[1]

			else:
				realArsg.append(arg0)

			if arg1.is_number:
				numParams+=1
				if arg1Real:
					numValReal = arg1.as_real_imag()[0]
				if arg1Im:
					numValIm = arg1.as_real_imag()[1]
			else:
				realArsg.append(arg1)

			if numParams == 2:
				print ("unimplemented: the expression is a " + opName + " with two numbers")
				sys.exit(1)
			elif numParams == 1:
				if arg0.is_number:
					nodeName = opName + "arg" + arg1Type + "num" + arg0Type
				else:
					nodeName = opName + "arg" + arg0Type + "num" + arg1Type
				self.basm += "%meta fidef node"+mId+str(myIndex)+" fragment:"+nodeName+", numberreal: 0f"+str(numValReal)+", numberimag: 0f"+str(numValIm)+", "+self.opsstring+"\n"
			else:
				nodeName = opName + "arg" + arg0Type + "arg" + arg1Type
				self.basm += "%meta fidef node"+mId+str(myIndex)+" fragment:"+nodeName+", "+self.opsstring+"\n"

			return realArsg
		else:
			print ("Unimplemented")
			sys.exit(1)
	else:
		print ("Unimplemented")
		sys.exit(1)

	# An add node with a hardcoded number

	return realArsg
	