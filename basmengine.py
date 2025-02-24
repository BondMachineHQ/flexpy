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
