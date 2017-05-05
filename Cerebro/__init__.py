
import pandas_datareader.data as web
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class Cerebro:

	def __init__(self):
		pass

	#__model = Sequential()

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

	def makeDataSet(self, start_date, end_date):

		df_total = {}

		# Scaler
		scaler_x = MinMaxScaler(feature_range=(0, 1))
				
		for item in self.__instruments:

			df = web.DataReader(item, 'yahoo', start_date, end_date)[['Open','High','Low','Close','Volume']]

			# make data serialized
			if len(df_total) == 0:
				df_total = df
			else:
				df_total = pd.concat([df_total, df], axis=1)

		# test
		print df_total

		# make NaN 0
		df_total = df_total.fillna(0)

		# normalize
		scaled_x = scaler_x.fit_transform(df_total.values.tolist())

		return scaled_x

	def run(self):
		self.makeModel()
		self.__model.fit(x_train, y_train, epochs=10, batch_size=1, verbose=2)

	def getTestingResult(self):
		return self.__model.predict(x_test)
	