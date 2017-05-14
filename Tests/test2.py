import numpy
from keras.datasets import imdb
from keras.preprocessing import sequence
from func import getTrainData
import datetime
import pandas_datareader.data as web
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
import pickle
from sklearn.preprocessing import MinMaxScaler
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

numpy.random.seed(7)

start_l = datetime.datetime(2004, 1, 1)
end_l = datetime.datetime(2014, 12, 31)

start_t = datetime.datetime(2015, 1, 1)
end_t = datetime.datetime(2017, 4, 1)

timeStep = 60
ma = 20

scaler_x = MinMaxScaler(feature_range=(0, 1))
scaler_y = MinMaxScaler(feature_range=(0, 1))

x_train, y_train, z_train 	= getTrainData("000660.KS", start_l, end_l, timeStep, ma)
x_test, y_test, z_test 		= getTrainData("000660.KS", start_t, end_t, timeStep, ma)
x_len = len(x_train)
scaled_x = scaler_x.fit_transform(x_train+x_test)
x_train = scaled_x[:x_len]
x_test 	= scaled_x[x_len:]
x_train = map(lambda x: [x], x_train)
x_test = map(lambda x: [x], x_test)

# create and fit the LSTM network
model = Sequential()
model.add(LSTM(32, input_shape=(1, 5)))
model.add(Dense(100))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=10, batch_size=1, verbose=2)

testPredict = model.predict(x_test)
dff = web.DataReader("000660.KS", 'yahoo', start_t, end_t)
cc = dff['Adj Close'].values.tolist()[:-timeStep]

f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot(cc)
axarr[0].plot(z_test)
axarr[1].plot(map(lambda x:x, testPredict))
plt.savefig('./result')
