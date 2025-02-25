import sys
import sympy as sp

def basmEngine(self, expr):
	self.index+=1
	myIndex = int(self.index)
	out = "node_"+str(myIndex)+"_link"
	if myIndex == 1:
		self.basm += "%meta filinkatt "+out+" fi:ext, type: output, index: 0\n"
	# self.basm += "#######" + str(expr) +" ## "+ str(myIndex)+"\n"	
	if len(expr.args) == 0:
		print(expr)
		# This is an input node, create a link using the index among all the inputs, even if inputs grow the index will be unique
		if not str(expr) in self.inputs:
			self.inputs.append(str(expr))
		inIdx = self.inputs.index(str(expr))
		# self.basm += "%meta iodef "+out+"\n"
		self.basm += "%meta filinkatt "+out+" fi:ext, index: "+str(inIdx)+", type: input\n"
		return out,myIndex
	else:
		# Create the processor and return the arguments really used, no the ones absorbed by the processor
		realArgs = self.basmArgsProcessor(expr, myIndex)
		# Create my side of the link, my caller will create the other side
		for i in range(len(realArgs)):
			arg=realArgs[i]
			inp,idx=self.basmEngine(arg)
			self.basm += "%meta filinkatt "+inp+" fi: node_"+str(myIndex)+", type: input, index: "+str(i)+"\n"
			# Create link to the called nodeindex
		# self.basm += "%meta iodef "+out+"\n"
		self.basm += "%meta filinkatt "+out+" fi: node_"+str(myIndex)+", type: output, index: 0\n"
		return out,myIndex

def basmArgsProcessor(self, expr, myIndex):
	realArsg = []
	self.basm += "%meta cpdef node_"+str(myIndex)+" fragcollapse:node_"+str(myIndex)+"\n"

	# Start identifying the node and mapping it to known fragments
	# Addition
	if expr.func == sp.Add or expr.func == sp.Mul:
		if len(expr.args) == 2:
			arg0 = expr.args[0]
			arg1 = expr.args[1]
			if expr.func == sp.Add:
				opName = "add"
				opOp = self.ops["addop"]
			elif expr.func == sp.Mul:
				opName = "mult"
				opOp = self.ops["multop"]

			# Check if the arguments are numbers
			numParams = 0
			numVal = 0
			realArsg = []
			if arg0.is_number:
				numParams+=1
				numVal = arg0.evalf()
			else:
				realArsg.append(arg0)

			if arg1.is_number:
				numParams+=1
				numVal = arg1.evalf()
			else:
				realArsg.append(arg1)

			if numParams == 2:
				print ("Unimplemented")
				sys.exit(1)
			elif numParams == 1:
				self.basm += "%meta fidef node_"+str(myIndex)+" fragment:"+opName+"num, number: 0f"+str(numVal)+", "+opName+"op:"+opOp+"\n"
			else:
				self.basm += "%meta fidef node_"+str(myIndex)+" fragment:"+opName+", "+opName+"op:"+opOp+" \n"

			return realArsg
		else:
			print ("Unimplemented")
			sys.exit(1)
	else:
		print ("Unimplemented")
		sys.exit(1)

	# An add node with a hardcoded number

	return realArsg
	