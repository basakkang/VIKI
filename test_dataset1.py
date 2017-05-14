from viki.cerebro import Cerebro 
import datetime

s = datetime.datetime(2017,5,3)
e = datetime.datetime(2017,5,10)


crb = Cerebro()

# crb.setInstruments(["070960.KS", "000660.KS", "005930.KS"])

ss = crb.makeBaseDataSet(["070960.KS", "000660.KS", "005930.KS"], s,e)
print ss