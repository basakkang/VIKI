class VIKI:

	def setCerebro(self, cerebro):
		self.__cerebro = cerebro

	def runCerebro(self):
		self.__cerebro.run()

	def getTestResultCerebro(self):
		return self.__cerebro.getTestingResult()

	def analyzeCerebro(self):
		result = self.getTestResultCerebro()
		feed = Feed(start_date, end_date)
		# feed.addDailyFeed(df, instrument)
		# add all daily feed
		alphaman = Alphaman(start_date, end_date)
		alphaman.setFeed(feed)
		alphaman.setStrategy(VikiStrategy(self.__cerebro.instruments))
		alphaman.run()
		alphaman.show()

