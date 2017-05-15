from viki.cerebro import Cerebro 
import datetime
import pandas_datareader.data as web

s = datetime.datetime(2015,1,26)
e = datetime.datetime(2016,12,31)


# crb = Cerebro()

# crb.setInstruments(["070960.KS", "000660.KS", "005930.KS"])

# ss = crb.makeBaseDataSet(["006220.KS"], s,e)
# print ss
df = web.DataReader("089590.KS", 'yahoo', s, e)[['Volume', 'Open','High','Low','Close']]
print df[df['Close']==0]