import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime
from sklearn.preprocessing import MinMaxScaler

def getNewDF(name, start, end, future_date, smaTime):
	df = web.DataReader(name, 'yahoo', start, end)
	diffSeries = pd.Series()

	adjClose = df['Adj Close']
	sum = 0
	smaArr = np.zeros(len(adjClose))		
	for idx, value in enumerate(adjClose):
		sum += value
		if idx < smaTime:
			smaArr[idx] = sum/(idx+1)
		else:
			sum -= adjClose[idx - smaTime]
			smaArr[idx] = sum/smaTime

	df["SMA"] = pd.Series(smaArr, index=df.index)
	smaArr = df["SMA"]
	diffArr = np.zeros(len(smaArr))
	diffPercentArr = np.zeros(len(smaArr))
	for idx, value in enumerate(smaArr):
		if idx > len(adjClose) - (future_date+1) :
			break
		diff = value - smaArr[idx + future_date]
		diffArr[idx] = diff
		diffPercentArr[idx] = diff / adjClose[idx] * 100

	df["Diff"] = pd.Series(diffArr, index=df.index)
	df["Diff Percent"] = pd.Series(diffPercentArr, index=df.index)
	return df[:-future_date]


def getTrainData(name, start, end, future_date, smaTime, ):
	df = getNewDF(name, start, end, future_date, smaTime)
	x_train = df[['Adj Close', 'Open', 'High', 'Low', 'Volume']].values.tolist()
	y_train = df[['Diff Percent']].values.tolist()
	z_train = df[['SMA']].values.tolist()
	return x_train, y_train, z_train
