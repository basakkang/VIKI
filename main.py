from viki.cerebro.DQNCerebro import DQNCerebro
import datetime

cerebro = DQNCerebro(20,20)

cerebro.setInstruments(["000660.KS", "070960.KS"])

start_l = datetime.datetime(2006, 12, 1)
end_l = datetime.datetime(2016, 12, 31)
# cerebro.makeTrainData(20, 20, start_l, end_l)
cerebro.setLearningDate(start_l, end_l)
cerebro.train()