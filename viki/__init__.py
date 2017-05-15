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

		for item in instr:

			df = web.DataReader(item, 'yahoo', sDate, eDate)[['Close']]
			df.columns = [item]
			# make data serialized
			df_total = (df, pd.concat([df_total, df], axis=1))[df_total is not None]

		# make NaN 0
		df_total = df_total.fillna(0)

		# df_total = df + result 
		df_total = df_total.join(result, how='outer')
		alphaman.run()
		alphaman.show()

