from viki.cerebro import Cerebro
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.optimizers import SGD , Adam
from keras.layers.core import Dense, Dropout, Activation, Flatten
from viki.utils import getRandCompany, getCloseStartDate, strCode, ReMakeError

import pandas_datareader.data as web
import h5py

LEARNING_RATE = 1e-4

class DQNCerebro(Cerebro):

	def __init__(self, inst_num, input_days):
		self._input_days = input_days
		self._inst_num = inst_num
		Cerebro.__init__(self)

	def buildModel(self):
		num_of_instruments = self._inst_num
		num_of_input_factor = len(self._input_factor)
		model = Sequential()
		model.add(Conv2D(32, 8, 8, subsample=(4, 4), border_mode='same',input_shape=(self._inst_num, self._input_days, num_of_input_factor)))  #20 * 20 * 5
		model.add(Activation('relu'))
		model.add(Conv2D(64, 4, 4, subsample=(2, 2), border_mode='same'))
		model.add(Activation('relu'))
		model.add(Conv2D(64, 3, 3, subsample=(1, 1), border_mode='same'))
		model.add(Activation('relu'))
		model.add(Flatten())
		model.add(Dense(512))
		model.add(Activation('relu'))
		model.add(Dense(num_of_instruments + 1))
		adam = Adam(lr=LEARNING_RATE)
		model.compile(loss='mse',optimizer=adam, metrics=['accuracy'])
		return model

	def train(self, train_num):
		self.__model = self.buildModel()
		try:
			self.__model.model.load_weights('DQNCerebro.h5')
		except:
			pass
		cnt = 0
		while cnt < train_num:
			images, labels, _ = self.makeData(self._input_days, self._inst_num, self._learning_start_date, self._learning_end_date)
			self.__model.fit(images, labels, epochs=10, batch_size=1, verbose=2)
			self.__model.save_weights("DQNCerebro.h5", overwrite=True)
			cnt += 1

	def getTestingResult(self):
		images, labels, codes = self.makeData(self._input_days, self._inst_num, self._learning_start_date, self._learning_end_date)
		return self.__model.predict(images), codes

	def setInstNum(self, num):
		self._inst_num = num

	def makeData(self, day, inst_num, start_date, end_date):

		codes = self.getRandInstruments(inst_num)
		try: 
			# codes = [u'11790', u'34310', u'152330', u'10050', u'2200', u'5620', u'16800', u'3470', u'6200', u'93230', u'3490', u'11160', u'12630', u'32830', u'4440', u'143210', u'4690', u'660', u'10120', u'21960']
		# ["000660", "005190"]
			images, prices = self.generateImages(day, codes, start_date, end_date)
			labels = self.generateLabelWithPrices(prices)
			return images[1::], labels, codes
		except :
			return self.makeTrainData(day, inst_num, start_date, end_date)

	def getRandInstruments(self, inst_num):
		return getRandCompany(inst_num)

	def getCloseStartInstruments(self, codes):
		return getCloseStartDate(codes)

	def getRandPriceDatas(self, codes, start_date, end_date):
		print codes
		close_start_date = self.getCloseStartInstruments(codes)
		s_date = (close_start_date, start_date)[start_date > close_start_date]
		print s_date
		print end_date
		baseDataset, prices = self.makeBaseDataSet(map(lambda x:strCode(x)+".KS", codes), s_date, end_date)
		return baseDataset, prices

	def generateImages(self, days, codes, start_date, end_date):
		images = []
		randDatas, prices = self.getRandPriceDatas(codes, start_date, end_date)
		for i in range(len(randDatas) - days):
			images.append(randDatas[i: i + days])
		return images, prices[:-days]

	# def generateLabelWithImage(self, images):
	# 	label = []
	# 	prevPrices = map(lambda x:x[-1], images[0][-1])
	# 	for image in images[1::]:
	# 		priceLabel = [0] * (len(image[0]) + 1)
	# 		curPrices = map(lambda x:x[-1], image[-1])
	# 		diffPrices = [(curPrices[i] - prevPrices[i])/prevPrices[i] for i in range(len(curPrices))]
	# 		max_val = max(diffPrices)
	# 		if max_val == float('Inf'):
	# 			max_idx = diffPrices.index(max_val)
	# 			print prevPrices[max_idx], curPrices[max_idx]

	# 		if max_val > 0 :
	# 			max_idx = diffPrices.index(max_val)
	# 			priceLabel[max_idx] = 1
	# 		else:
	# 			priceLabel[-1] = 1
	# 		prevPrices = curPrices
	# 		label.append(priceLabel)
	# 	return label

	def generateLabelWithPrices(self, prices):
		label = []
		# try:
		# 	# for item in prices :
		# 	# 	print item
		# 	# 	print item.index(0)
		# 	# 	print "hi"
		# except:
		# 	pass
		if len(prices) == 0:
			raise ReMakeError("len == 0")
		# prevIdx = prices[0]
		for idx, price in enumerate(prices[1::]):
			priceLabel = [0] * (len(prices[0]) + 1)
			# if prevPrice[i] == 
			prevPrice =  prices[idx]
			try :
				idx2 = prevPrice.index(0)
				print idx
				print idx2
				print prevPrice[idx2]
				print price[idx2]
			except:
				pass
			diffPrices = [(price[i] - prevPrice[i])/prevPrice[i] for i in range(len(price))]
			max_val = max(diffPrices)
			if max_val > 0 :
				max_idx = diffPrices.index(max_val)
				priceLabel[max_idx] = 1
			else:
				priceLabel[-1] = 1
			label.append(priceLabel)
		return label

