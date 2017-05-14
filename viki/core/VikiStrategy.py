import sys
sys.path.insert(0, './Alphaman')
from alphaman.strategy import BaseStrategy


class VikiSignal(BaseSignal):

	def __init__(self, instruments):
		self.__instruments = instruments

	def getSignal(self, instrument):
		return self.calculateSignal(instrument)

	def calculateSignal(self, instrument):
		#짜야함ㅋㅋ


class VikiStrategy(BaseStrategy):
	def __init__(self, instruments):
		self.__instruments = instruments
		self.addSignals("Viki", VikiSignal(instruments))

	def handleData(self):
		for instrument in self.__instruments:
			probability = self.getSignal("viki", instrument)
			self.orderTarget(instrument, probability)
