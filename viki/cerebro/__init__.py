
import pandas_datareader.data as web
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class Cerebro:

	_input_factor = ['Open','High','Low','Close','Volume']

	_input_days = 5

	def __init__(self):
		pass

	def setInstruments(self, instruments):
		self._instruments = instruments

	def setLearningDate(self, start_date, end_date):
		self._learning_start_date = start_date
		self._learning_end_date = end_date

	def setTestingDate(self, start_date, end_date):
		self._testing_start_date = start_date
		self._testing_end_date = end_date

	def getModel(self):
		return __model

	def makeModel(self):
		raise NotImplementedError

	def makeBaseDataSet(self, instruments, start_date, end_date):

		# Scaler
		scaler_x = MinMaxScaler(feature_range=(0, 1))

		df_total = None

		# df_prices = None
				
		for idx, item in enumerate(instruments):

			df = web.DataReader(item, 'yahoo', start_date, end_date)[['Volume', 'Open','High','Low','Close']]
			# df = df[df.Volume != 0]
			# df.columns = ['V'+str(idx), 'O'+str(idx), 'H'+str(idx), 'L'+str(idx), 'C'+str(idx)]
			# make data serialized
			df_total = (df, pd.concat([df_total, df], axis=1))[df_total is not None]

		# make NaN 0
		df_total = df_total.fillna(0)
		df_volume = df_total['Volume']
		idx_list = []
		for idx, item in enumerate(df_volume.values.tolist()):
			v_total = reduce(lambda x, y: x+y, item)
			if v_total == 0:
				idx_list.append(idx)
 		df_total = df_total.drop(df_total.index[idx_list])

		# normalize
		scaled_x = scaler_x.fit_transform(df_total.values.tolist())
		len_instruments = len(instruments)
		# new_scaled_x = map(lambda x: [x[],[],[],[],[]], scaled_x)
		new_scaled_x = []
		for item in scaled_x:
			newItem = []
			lenOfItem = len(item)
			for idx, val in enumerate(item):
				if idx % (lenOfItem/len_instruments) == 0:
					newItem.append([])
				newItem[-1].append(val)
			new_scaled_x.append(newItem)
		return new_scaled_x, df_total['Close'].values.tolist()

	def train(self):
		self.__model = self.makeModel()
		if self.__model != None:
			self.__model.fit(x_train, y_train, epochs=10, batch_size=1, verbose=2)

	def getTestingResult(self):
		return self.__model.predict(x_test)
	