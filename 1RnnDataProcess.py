# -*-coding:utf8-*-

import os
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

TEST_DATA_NUM   = 50
INPUT_TENSOR_SHAPE_LEN   = 13
RNN_CELLSIZE = 15
BATCHSIZE = 13
TRAINING_EPOH   = 50
DAYTIME = 5
DAYOFF = 1

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
                '总市值':10, '流通市值': 11}
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
        csvdata['日期']=pd.to_datetime(csvdata['日期'])
        csvdata=csvdata.set_index('日期')
        csvdata.sort_index(ascending=True, inplace=True)
        csvdata.sort_index(axis=1, inplace=True)
        csvdata.insert(csvdata.shape[1], 12, 0)
        csvdata.loc[:, csvdata.shape[1]] = csvdata.index
        csvdata = csvdata.values
        csvdata = np.array(csvdata)
        # print(csvdata)
        predata = csvdata[:,[0, csvdata.shape[1]-1]].copy()
        # print(predata)
        for i in range (DAYTIME, csvdata.shape[0]):
            csvdata[i, csvdata.shape[1]-2] = csvdata[i,0]
            for j in range (0, DAYTIME):
                csvdata[i, csvdata.shape[1]-2] = csvdata[i, csvdata.shape[1]-2] + csvdata[i - j - 1, 0]
            csvdata[i, csvdata.shape[1]-2] = csvdata[i, csvdata.shape[1]-2] / DAYTIME
        # print(csvdata[:20, :])
        for i in range (0, INPUT_TENSOR_SHAPE_LEN):
            csvdata[:,i] = (csvdata[:,i] - csvdata[:,i].min()) / (csvdata[:,i].max() - csvdata[:,i].min())
        # print(csvdata[:20, :])
    else:
        print('there is not stock data csv data')
        os._exit(-1)
    # print(predata)
    # xdata = csvdata[ : , :].astype('float32')
    # ydata = predata[ : , :].astype('float32')
    print('x shape:', csvdata.shape, 'y shape: ', predata.shape)
    return csvdata, predata

def trainCsvData(xdata, ydata, code):
    if(type(code) == type(1)):
        code = "%(code)06d"%{'code':code}
    trainlen = ydata.shape[0]-TEST_DATA_NUM
    xtrain = xdata[ : trainlen, 0:INPUT_TENSOR_SHAPE_LEN].astype('float32')
    ytrain = ydata[DAYOFF : trainlen+DAYOFF, 0].astype('float32')

    # print(xdata[ : trainlen, :])
    # print(ydata[DAYOFF : trainlen+DAYOFF, :])

    # print(xdata[0, 0:INPUT_TENSOR_SHAPE_LEN].shape, xdata[0, 0:INPUT_TENSOR_SHAPE_LEN])
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
    h = model.fit(xtrain, ytrain, batch_size=BATCHSIZE, epochs = TRAINING_EPOH)
    model.save(MODELDIR + '\\%(code)s.h5'%{'code': code})
    # plt.plot(h.history['loss'])
    # plt.show()
    
def verifyCsvData(xdata, ydata, code):
    if(type(code) == type(1)):
        code = "%(code)06d"%{'code':code}
    verifylen = ydata.shape[0]-TEST_DATA_NUM
    xverify = xdata[verifylen : ydata.shape[0]-DAYOFF, 0:INPUT_TENSOR_SHAPE_LEN].astype('float32')
    yverify = ydata[verifylen+DAYOFF : ydata.shape[0], :]#.astype('float32')
    
    print(xdata[verifylen +30 : verifylen+40, :])
    print(ydata[verifylen+DAYOFF +30 : verifylen+DAYOFF+40, :])

    model = tf.keras.models.load_model(MODELDIR + '\\%(code)s.h5'%{'code': code})
    predict = []
    for i in range(TEST_DATA_NUM - DAYOFF):
        # print(xverify[i, 0:INPUT_TENSOR_SHAPE_LEN])
        x_train = xverify[i, 0:INPUT_TENSOR_SHAPE_LEN].reshape(1,INPUT_TENSOR_SHAPE_LEN)
        one_predict = model.predict(x_train)[0][0]
        predict.append(one_predict) 
    print("pre is :", predict)
    print("real is :", yverify[:, 0])
    
    x = range(1, TEST_DATA_NUM + 1 - DAYOFF, 1)
    plt.figure(1)
    plt.subplot(121)
    plt.plot(x, yverify[:,0], 'r', label='ydtat')
    plt.plot(x, predict, 'g', label='predata')
    plt.ylim(yverify[:,0].min() - 1, yverify[:,0].max() + 1)
    plt.legend()
    plt.subplot(122)
    offset = (yverify[:,0].min() + yverify[:,0].max())/2
    predict[:] = predict[:] - yverify[:,0]
    plt.plot(x, predict, 'b', label='offset=pre-ydata')
    zeoroff = np.zeros_like(predict)
    plt.plot(x, zeoroff, 'r', label='zerooffset')
    zeoroff = np.array(zeoroff)
    zeoroff[:] = zeoroff[:] + max(predict)
    plt.plot(x, zeoroff, 'g', label='maxoffset')
    zeoroff[:] = zeoroff[:] - max(predict) + min(predict)
    plt.plot(x, zeoroff, 'g', label='minoffset')
    plt.ylim(yverify[:,0].min() - 1 - offset, yverify[:,0].max() + 1 -offset )
    plt.legend()
    plt.show()

def oneCodeRnn(code):
    csvdata = getCsvData(code)
    xtrain, ypre = preProcessCsvData(csvdata, 1)
    # trainCsvData(xtrain, ypre, code)
    verifyCsvData(xtrain, ypre, code)

if __name__ == '__main__': 
    # handleCsv = HandleStockData(688396)
    # handleCsv = HandleStockData(2402)
    oneCodeRnn(600410)
