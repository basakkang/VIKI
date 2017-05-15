import sys
sys.path.insert(0, './Alphaman')
from alphaman.strategy import BaseStrategy
from alphaman.signal import BaseSignal


class VikiSignal(BaseSignal):

	def __init__(self, instruments):
		self.__instruments = instruments

	def getSignal(self, instrument):
		return self.calculateSignal(instrument)

	def calculateSignal(self, instrument):
		return self.get(instrument, "prop", 0)


class VikiStrategy(BaseStrategy):
	def __init__(self, instruments, props):
		self.__instruments = instruments
		self.props = props
		# self.addSignals("Viki", VikiSignal(instruments))
		self.cnt = 0

	def handleData(self):
		probList = []
		for idx, instrument in enumerate(self.__instruments):
			probability = self.props[self.cnt][idx]
			probList.append((instrument, probability))
		probList.sort(key=lambda tup: tup[1])
		for prob in probList:		
			self.orderTarget(prob[0], prob[1])
		self.cnt += 1