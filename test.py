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
import numpy
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

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

def getRiseRate(df, codes):
	rate_dict = {}
	for code in codes:
		prices_code = map(lambda x:x[0], df[[strCode(code)]].values.tolist())
		rate_dict[code] = float(prices_code[-1] - prices_code[0])/float(prices_code[0]) * 100
	return rate_dict

def getKospiRate(df):
	ind_list = df.index.tolist()
	df2 = web.DataReader("^KS11", 'yahoo', s_date, end_date)[['Close']]
	kospi = map(lambda x:x[0], df2.values.tolist())
	return float(kospi[-1] - kospi[0])/float(kospi[0]) * 100

rise_dict = getRiseRate(df_total, codes)
kosp_rate = getKospiRate(df_total)

sum_val = 0
for key, val in rise_dict.iteritems():
	sum_val += val



print "average rate : " + str(float(sum_val)/len(codes))
print "kospi rate : " + str(kosp_rate)
# df_total = df + result 
df_dict = {}
for idx, code in enumerate(codes):
	df_dict[code] = df_total[[strCode(code)]]
	df_dict[code].columns = ['Close']

feed = Feed(s_date, end_date)

for key, val in df_dict.iteritems():
	feed.addDailyFeed(val, key)

# # add all daily feed


alphaman = Alphaman(s_date, end_date)
alphaman.setFeed(feed)
alphaman.setStrategy(VikiStrategy(codes, labels))
alphaman.run()
alphaman.show()


