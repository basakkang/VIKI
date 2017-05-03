# Create first network with Keras
from keras.models import Sequential
from keras.layers import Dense
import numpy
import datetime
from func import getNewDF

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2016, 12, 31)

print getNewDF("000060.KS", start, end, 6)

# seed = 7
# numpy.random.seed(seed)
# # load pima indians dataset
# dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
# # split into input (X) and output (Y) variables
# X = dataset[:,0:8]
# Y = dataset[:,8]
# # create model

