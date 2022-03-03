class VocabDict:
	def __init__(self):
		self.d = {}
		self.w = []
		
	def getIdOrAdd(self, word):
		if word in self.d : 
			return self.d[word]
		self.d[word] = len(self.d)
		self.w.append(word)
		return len(self.d) -1
		
	def getId(self, word):
		if word in self.d:
			return self.d[word]
		return -1
		
	def getWord(self, id):
		return self.w[id]
		
	def len(self):
		return len(self.w)
		
	def printWords(self):
		for w in self.w:
			print(w)
		return