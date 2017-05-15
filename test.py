from viki.cerebro.DQNCerebro import DQNCerebro
import datetime
import requests.packages.urllib3
import pandas_datareader.data as web
import pandas as pd
import sys
sys.path.append('./viki/Alphaman')
import alphaman
from alphaman import Alphaman
from alphaman.feed import DailyInstrumentData, DailyFeed, Feed
from viki.utils import strCode
from viki.core.VikiStrategy import VikiStrategy
import pickle

requests.packages.urllib3.disable_warnings()

cerebro = DQNCerebro(20,20)

start_l = datetime.datetime(2006, 12, 1)
end_l = datetime.datetime(2016, 6, 30)
cerebro.setLearningDate(start_l, end_l)
start_t = datetime.datetime(2016, 7, 1)
end_t = datetime.datetime(2017, 5, 14)
cerebro.setTestingDate(start_t, end_t)
cerebro.buildModel()
# cerebro.train(10)
labels, codes, s_date, end_date, date_list = cerebro.getTestingResult()
print labels

feed = Feed(s_date, end_date)

df_total = None

df_list = []

for item in codes:
	df = web.DataReader(strCode(item)+".KS", 'yahoo', s_date, end_date)[['Close','Volume']]
	df.columns = [strCode(item),'Volume']
	# make data serialized
	df_list.append(df)
	df_total = (df, pd.concat([df_total, df], axis=1))[df_total is not None]

df_total = df_total.fillna(0)

idx_list = []
for idx, item in enumerate(df_total['Volume'].values.tolist()):
	v_total = reduce(lambda x, y: x*y, item)
	if v_total == 0:
		idx_list.append(idx)
df_total = df_total.drop(df_total.index[idx_list]).ix[21::]

# df_total = df + result 
df_dict = {}
for idx, code in enumerate(codes):
	df_dict[code] = df_total[[strCode(code)]]
	df_dict[code].columns = ['Close']

for key, val in df_dict.iteritems():
	feed.addDailyFeed(val, key)

# # add all daily feed
alphaman = Alphaman(s_date, end_date)
alphaman.setFeed(feed)
alphaman.setStrategy(VikiStrategy(codes, labels))
alphaman.run()
alphaman.show()


