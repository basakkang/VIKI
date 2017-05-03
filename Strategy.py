import sys
sys.path.insert(0, './Alphaman')
from alphaman.strategy import BaseStrategy


class MyStrategy(BaseStrategy):
	def __init__(self, instrument):
		self.__instrument = instrument
		self.addSignals("cross", CrossSignal(instrument))

	def handleData(self):
		crossSignal = self.getSignal("cross")
		if crossSignal == BuySignal.Long:
			self.orderTarget(self.__instrument, 0.7)
		elif crossSignal == BuySignal.Short:
			self.orderTarget(self.__instrument, 0.2)