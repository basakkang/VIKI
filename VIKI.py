class VIKI:

	def setCerebro(self, cerebro):
		self.__cerebro = cerebro

	def runCerebro(self):
		self.__cerebro.run()

	def getTestResultCerebro(self):
		return self.__cerebro.testing()

	def analyzeCerebro(self):
