from viki.cerebro import Cerebro 
import datetime

s = datetime.datetime(2000,5,20)
e = datetime.datetime(2016,5,30)


crb = Cerebro()

# crb.setInstruments(["070960.KS", "000660.KS", "005930.KS"])

print crb.makeBaseDataSet(["070960.KS", "000660.KS", "005930.KS"], s,e)