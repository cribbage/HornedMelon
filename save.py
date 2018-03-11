import math, sys, random, time, copy

class Save:
	def __init__(self, data, saveFile):
		self.data = data
		self.saveFile = saveFile
		
	def save(self):		
		f = open(self.saveFile, "w")
		for datum in self.data:
			f.write(str(datum).strip('()')+"\n")
		f.close()
	
	def load(self, returnType):
		f = open(self.saveFile, "r")
		lines = (line.rstrip() for line in f)
		lines = (line for line in lines if line)
		for line in lines:
			self.data.append(returnType(line.strip('\n')))
		f.close()
		return self.data
		
