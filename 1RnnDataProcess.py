# -*-coding:utf8-*-

import os
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

TEST_DATA_NUM   = 50
INPUT_TENSOR_SHAPE_LEN   = 12
RNN_CELLSIZE = 10
BATCHSIZE = 13
TRAINING_EPOH   = 50

MODELDIR = os.path.dirname(os.path.abspath(__file__)) + "\\model"
if (os.path.exists(MODELDIR) == False):
    os.makedirs(MODELDIR)

def getCsvData(code):
    if(type(code) == type(1)):
        code = "%(code)06d"%{'code':code}
    csvfile = os.path.dirname(os.path.abspath(__file__)) + "\\csv\\%(code)s.csv"%{'code' : code}
    if(os.path.isfile(csvfile)):
        try:
            csvstockdata = pd.read_csv(csvfile, encoding='gbk')#, nrows=1)
            if (csvstockdata.empty == False):
                return csvstockdata
        except pd.errors.EmptyDataError as e: 
            print("EmptyDataError")
    return pd.DataFrame()
    
def preProcessCsvTaget(csvdata, type=0):
    csvdict = {'开盘价': 0, '收盘价': 1, '前收盘': 2, '最高价': 3, '最低价': 4, 
                '成交量': 5, '成交金额': 6, '涨跌额': 7, '涨跌幅': 8, '换手率': 9,
                '总市值':10, '流通市值': 11, '日期': 15}
    if(type < 5):
        csvdictkey = [k for k,v in csvdict.items() if v==type]
        csvdict[csvdictkey[0]] = 0
        csvdict['开盘价'] = type
    print(csvdict)
    csvdata.rename(columns=csvdict, inplace=True) 
    return csvdata

def preProcessCsvData(csvdata, type=0):
    predata = []
    if (csvdata.empty == False):
        csvdata = csvdata.drop(['名称', '股票代码'], axis = 1)
        csvdata = csvdata[ ~ csvdata['涨跌幅'].str.contains('None') ]    
        csvdata[ ['涨跌额', '涨跌幅'] ] = csvdata[ ['涨跌额', '涨跌幅'] ].astype('float32') 
        preProcessCsvTaget(csvdata, type)
        # csvdata = csvdata.sort_values(by=15, ascending=True).reset_index(drop=True, inplace=False)
        csvdata.sort_index(ascending=False, inplace=True)
        csvdata.reset_index(drop=True, inplace=True)
        # print(csvdata.head(20))
        csvdata.sort_index(axis=1, inplace=True)
        csvdata.drop(index=[0], inplace=True)      
        csvdata = csvdata.values
        csvdata = np.array(csvdata)
        # self.stockdorgata = csvdata.copy()
        predata = csvdata[:,0].copy()
        # print(predata)
        for i in range (0, 12):
            csvdata[:,i] = (csvdata[:,i] - csvdata[:,i].min()) / (csvdata[:,i].max() - csvdata[:,i].min())
    else:
        print('there is not stock data csv data')
        os._exit(-1)
    # print(predata)
    
    xdata = csvdata[ : , 0:INPUT_TENSOR_SHAPE_LEN].astype('float32')
    ydata = predata[ : ].astype('float32')
    # xdata = csvdata[ :predata.shape[0]-TEST_DATA_NUM, 0:INPUT_TENSOR_SHAPE_LEN].astype('float32')
    # ydata = predata[1 : predata.shape[0]-TEST_DATA_NUM+1].astype('float32')
    # xdata = xdata.reshape(predata.shape[0]-TEST_DATA_NUM, INPUT_TENSOR_SHAPE_LEN)
    # ydata = ydata.reshape(predata.shape[0]-TEST_DATA_NUM, 1)
    print('total:', predata.shape, 'x shape:', xdata.shape, 'y shape: ', ydata.shape)
    return xdata, ydata

def trainCsvData(xdata, ydata, code):
    if(type(code) == type(1)):
        code = "%(code)06d"%{'code':code}
    xdata = xdata[ :ydata.shape[0]-TEST_DATA_NUM, 0:INPUT_TENSOR_SHAPE_LEN]
    ydata = ydata[1 : ydata.shape[0]-TEST_DATA_NUM+1]

    print(xdata[0, 0:INPUT_TENSOR_SHAPE_LEN].shape)
    model_layers = [
        tf.keras.layers.Reshape((INPUT_TENSOR_SHAPE_LEN, 1),input_shape=(INPUT_TENSOR_SHAPE_LEN,)),
        tf.keras.layers.GRU(RNN_CELLSIZE, return_sequences=True),
        tf.keras.layers.GRU(RNN_CELLSIZE),
        tf.keras.layers.Dense(1) ]
    model = tf.keras.Sequential(model_layers)
    model.summary()
    model.compile(
       loss = 'mean_squared_error',
       optimizer = 'adam' )
    h = model.fit(xdata, ydata, batch_size=BATCHSIZE, epochs = TRAINING_EPOH)
    model.save(MODELDIR + '\\%(code)s.h5'%{'code': code})
    # plt.plot(h.history['loss'])
    # plt.show()
    
def verifyCsvData(xdata, ydata, code):
    if(type(code) == type(1)):
        code = "%(code)06d"%{'code':code}
    xdata = xdata[ydata.shape[0]-TEST_DATA_NUM : ydata.shape[0]-1, 0:INPUT_TENSOR_SHAPE_LEN]
    ydata = ydata[ydata.shape[0]-TEST_DATA_NUM+1 : ydata.shape[0]]
    # xdata = xdata.reshape(predata.shape[0]-TEST_DATA_NUM, INPUT_TENSOR_SHAPE_LEN)
    # ydata = ydata.reshape(predata.shape[0]-TEST_DATA_NUM, 1)
    model = tf.keras.models.load_model(MODELDIR + '\\%(code)s.h5'%{'code': code})
    predict = []
    for i in range(TEST_DATA_NUM - 1):
        x_train = xdata[i, 0:INPUT_TENSOR_SHAPE_LEN].reshape(1,12)
        one_predict = model.predict(x_train)[0][0]
        predict.append(one_predict) 
    print("pre is :", predict)
    print("real is :", ydata)
    
    x = range(1, TEST_DATA_NUM, 1)
    plt.plot(x, ydata, 'r', label='LowPrice')
    plt.plot(x, predict, 'g', label='Prelow')
    plt.legend()
    plt.show()

def oneCodeRnn(code):
    csvdata = getCsvData(code)
    xtrain, ypre = preProcessCsvData(csvdata, 1)
    trainCsvData(xtrain, ypre, code)
    verifyCsvData(xtrain, ypre, code)

if __name__ == '__main__': 
    # handleCsv = HandleStockData(688396)
    # handleCsv = HandleStockData(2402)
    oneCodeRnn(2402)
