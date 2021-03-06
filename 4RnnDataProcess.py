# -*-coding:utf8-*-

import os
import datetime
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

TEST_DATA_NUM   = 50
INPUT_TENSOR_SHAPE_LEN   = 5
RNN_CELLSIZE = 16
BATCHSIZE = 1
TRAINING_EPOH   = 50
PREDAY = 6
# DAYOFF = 2 #0:nextday, 1:next two day

gcsvdata = pd.DataFrame()
scaler = MinMaxScaler()
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
    global gcsvdata
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
        csvdata.drop([1,2,3,4,5,6,7,8,9,10,11], axis = 1, inplace=True)
        # print(csvdata.head())
        # predata = csvdata.loc[:, 0].copy()
        testst = csvdata.tail(INPUT_TENSOR_SHAPE_LEN).index[0]
        gcsvdata = csvdata
        trainxdata = csvdata.loc[:testst].copy()
        testst = csvdata.tail(PREDAY*INPUT_TENSOR_SHAPE_LEN).index[0]
        preydata    = csvdata.loc[testst: ].copy()
        trainxdata  = scaler.fit_transform(trainxdata)
        print(preydata)
        # preydata    = scaler.transform(preydata)
        # print(preydata)
    else:
        print('there is not stock data csv data')
        os._exit(-1)
    print('x shape:', trainxdata.shape, 'y shape: ', preydata.shape)
    return trainxdata, preydata

def trainCsvData(xdata, ydata, code):
    if(type(code) == type(1)):
        code = "%(code)06d"%{'code':code}
    xtrainend = xdata.shape[0] - 2*INPUT_TENSOR_SHAPE_LEN + 1
    xtrain, ytrain = [], []
    for i in range (0, xtrainend):
        xtrain.append(np.array(xdata[i : i+INPUT_TENSOR_SHAPE_LEN]))
        ytrain.append(np.array(xdata[i+INPUT_TENSOR_SHAPE_LEN : i+2*INPUT_TENSOR_SHAPE_LEN]))
        # print(xdata[i : i+INPUT_TENSOR_SHAPE_LEN])
        # print(xdata[i+INPUT_TENSOR_SHAPE_LEN : i+2*INPUT_TENSOR_SHAPE_LEN])
    xtrain, ytrain = np.array(xtrain).astype('float32').reshape([-1,INPUT_TENSOR_SHAPE_LEN]), np.array(ytrain).astype('float32').reshape([-1,INPUT_TENSOR_SHAPE_LEN])

    print(xtrain.shape, ytrain.shape)
    model_layers = [
        # tf.keras.layers.Reshape((INPUT_TENSOR_SHAPE_LEN, 1),input_shape=(INPUT_TENSOR_SHAPE_LEN,)),
        # tf.keras.layers.GRU(RNN_CELLSIZE, return_sequences=True),
        # tf.keras.layers.GRU(RNN_CELLSIZE, return_sequences=True),
        tf.keras.layers.Reshape((INPUT_TENSOR_SHAPE_LEN, 1),input_shape=(INPUT_TENSOR_SHAPE_LEN,),batch_size = BATCHSIZE),
        tf.keras.layers.GRU(RNN_CELLSIZE, return_sequences=True, stateful=True),
        tf.keras.layers.GRU(RNN_CELLSIZE, return_sequences=True, stateful=True),
        tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(1)),
        tf.keras.layers.Flatten() ]
    model = tf.keras.Sequential(model_layers)
    model.summary()
    model.compile(
       loss = 'mean_squared_error',
       optimizer = 'adam' )
    h = model.fit(xtrain, ytrain, batch_size=BATCHSIZE, epochs = TRAINING_EPOH)
    model.save(MODELDIR + '\\%(code)s-%(num)spre-scaler.h5'%{'code': code, 'num': INPUT_TENSOR_SHAPE_LEN})
    # plt.plot(h.history['loss'])
    # plt.show()
     

def verifyCsvData(xdata, ydata, code):
    # print(gcsvdata)
    # gcsvdata.plot()
    # plt.show()
    if(type(code) == type(1)):
        code = "%(code)06d"%{'code':code}
    predict = []
    model = tf.keras.models.load_model(MODELDIR + '\\%(code)s-%(num)spre-scaler.h5'%{'code': code, 'num': INPUT_TENSOR_SHAPE_LEN})
    # last_data = np.array(xdata[-INPUT_TENSOR_SHAPE_LEN : ]).astype('float32').reshape([1,INPUT_TENSOR_SHAPE_LEN])
    # # print(xdata[-INPUT_TENSOR_SHAPE_LEN - i: -i])
    # predicts = model.predict(last_data).reshape([INPUT_TENSOR_SHAPE_LEN,1])
    # results = scaler.inverse_transform(np.array(predicts).reshape(INPUT_TENSOR_SHAPE_LEN,1))
    # predict.append(results)
    # print(predict)
    # ydata['pre'] = results
    # print(ydata)
    # ydata.plot()
    # plt.show()
    
    for i in range(-PREDAY*INPUT_TENSOR_SHAPE_LEN, 0 , INPUT_TENSOR_SHAPE_LEN):
        if(i+INPUT_TENSOR_SHAPE_LEN == 0):
            last_data = np.array(xdata[i : ]).astype('float32').reshape([1,INPUT_TENSOR_SHAPE_LEN])
        else:
            last_data = np.array(xdata[i : i+INPUT_TENSOR_SHAPE_LEN]).astype('float32').reshape([1,INPUT_TENSOR_SHAPE_LEN])
        predicts = model.predict(last_data).reshape([INPUT_TENSOR_SHAPE_LEN,1])
        predict.extend(predicts.flatten().tolist())
    results = scaler.inverse_transform(np.array(predict).reshape(-1,1))
    print(results)
    print(predict)
    ydata['pre'] = results
    print(ydata)
    ydata.plot()
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
