class Scheme:
	def setDataFrame(self, data):
		self.__data = data

	def handle(self): 
		pass

	def run(self):
		result = self.handle()
		return result
