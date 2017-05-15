from viki.cerebro.DQNCerebro import DQNCerebro
import datetime
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

cerebro = DQNCerebro(20,20)

cerebro.setInstruments(["000660.KS", "070960.KS"])

start_l = datetime.datetime(2006, 12, 1)
end_l = datetime.datetime(2016, 6, 30)
cerebro.setLearningDate(start_l, end_l)
start_t = datetime.datetime(2016, 7, 1)
end_t = datetime.datetime(2017, 5, 14)
cerebro.setTestingDate(start_t, end_t)
cerebro.buildModel()
cerebro.train(10)
print cerebro.getTestingResult()
