import sys
sys.path.insert(0, './Alphaman')
from alphaman.strategy import BaseStrategy
from alphaman.signal import BaseSignal

class VIKISignal(BaseSignal):

	def __init(self):
		

	def calculateSignal(self):
		self.__data

class VIKIStrategy(BaseStrategy):
	def __init__(self, instrument):
		self.__instruments = instrument
		self.addSignals("cross", CrossSignal(instrument))

	def handleData(self):
		crossSignal = self.getSignal("cross")
		if crossSignal == BuySignal.Long:
			self.orderTarget(self.__instrument, 0.7)
		elif crossSignal == BuySignal.Short:
			self.orderTarget(self.__instrument, 0.2)

