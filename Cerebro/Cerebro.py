class Cerebro:

	__model = Sequential()

	def setInstruments(self, instruments):
		self.__instruments = instruments

	def setLearningDate(self, start_date, end_date):
		self.__learning_start_date = start_date
		self.__learning_end_date = end_date

	def setTestingDate(self, start_date, end_date):
		self.__testing_start_date = start_date
		self.__testing_end_date = end_date

	def getModel(self):
		return __model

	def makeModel(self):
		pass

	def makeDataSet(self):
		pass

	def run(self):
		self.makeModel()
		self.__model.fit(x_train, y_train, epochs=10, batch_size=1, verbose=2)

	def getTestingResult(self):
		return self.__model.predict(x_test)
	