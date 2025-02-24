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