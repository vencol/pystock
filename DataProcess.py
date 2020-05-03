# -*-coding:utf8-*-

import os
import numpy as np
import pandas as pd
import tensorflow as tf

TRAINING_EPOH   = 50
STEPRATE        = 0.01

class HandleStockData(object):
    csvdir              = os.path.dirname(os.path.abspath(__file__)) + '\\csv'

    def __init__(self, code):
        if(type(code) == type(1)):
            self.code = "%(code)06d"%{'code':code}
        else:
            self.code = code
        self.predata = self.read_stock_data()
        self.train_stock_data()
    
    def read_stock_data(self):
        csvdir = self.csvdir + "\\%(code)s.csv"%{'code': self.code}
        stockdata = pd.DataFrame()
        if(os.path.isfile(csvdir)):
            stockdata = pd.read_csv(csvdir, encoding='gbk')#, nrows=1)
            if (stockdata.empty == False):
                self.stockname = stockdata.loc[0]['名称']
                stockdata = stockdata.drop(['名称', '股票代码'], axis = 1)
                # stockdata.rename(columns={  '日期':'DATE', '换手率':'TURNOVERRATE', 
                #                             '开盘价':'OPENPRICE', '收盘价':'CLOSEPRICE', '前收盘':'PREPRICE',
                #                             '最高价':'HIGHPRICE', '最低价':'LOWPRICE', 
                #                             '涨跌额':'UPDOWNPRICE', '涨跌幅':'UPDOWNRANGE',
                #                             '成交量':'VOLUME', '成交金额':'AMOUNT', 
                #                             '总市值':'MARKETVALUE', '流通市值':'FLOW'},inplace=True) 
                stockdata.rename(columns={  '日期': 15, '换手率': 11, 
                                            '开盘价': 8, 
                                            '收盘价': 1, '前收盘': 2,
                                            '最高价': 3, '最低价': 4, 
                                            '成交量': 5, '成交金额': 6, 
                                            '涨跌额': 7, '涨跌幅': 0,
                                            '总市值':9, '流通市值': 10},inplace=True) 
                stockdata = stockdata.sort_values(by=15, ascending=True).reset_index(drop=True, inplace=False)
                stockdata.sort_index(axis=1, inplace=True)
                # print(stockdata)
                for i in range (1, 12):
                    stockdata.loc[:,i] = (stockdata.loc[:,i] - stockdata.loc[:,i].min()) / (stockdata.loc[:,i].max() - stockdata.loc[:,i].min())
                # print(stockdata)
                stockdata = stockdata.values
                stockdata = np.array(stockdata)
                # print(stockdata[:, 2])
        return stockdata
        
    def train_stock_data(self):
        xdata = self.predata[:self.predata.shape[0]-1, 1:12].astype('float32')
        ydata = self.predata[1:, 0].astype('float32')
        # print(xdata , "\nshape:" , xdata.shape)
        # print(ydata , "\nshape:" , ydata.shape)
        tf.compat.v1.disable_eager_execution()
        x = tf.compat.v1.placeholder(tf.float32, [None, 11], name='X')
        y = tf.compat.v1.placeholder(tf.float32, [None, 1], name='Y')
        with tf.name_scope('Model'):
            w = tf.Variable(tf.random.normal([11, 1], stddev=0.01), name='W')
            b = tf.Variable(1.0, name='B')
            def base_model(x, w, b):
                return tf.matmul(x, w) + b
            pred = base_model(x, w, b)
    
        with tf.name_scope('LossFunction'):
            lossfunc = tf.reduce_mean(tf.pow(y - pred, 2))
        optimizer = tf.compat.v1.train.GradientDescentOptimizer(STEPRATE).minimize(lossfunc)
        sess = tf.compat.v1.Session()
        init = tf.compat.v1.global_variables_initializer()
        sess.run(init)
        # print(xdata)
        # print(ydata)
        for epoch in range(0, TRAINING_EPOH):
            loss_sum = 0.0
            for xs, ys in zip(xdata, ydata):
                xs = xs.reshape(1, 11)
                ys = np.array(ys).reshape(1, 1)
                _, loss = sess.run([optimizer, lossfunc], feed_dict={x: xs, y: ys})
                loss_sum = loss_sum + loss

            # print(xdata, 'sahrp:', xdata.shape)
            # perm = tf.random.shuffle(tf.range(tf.shape(ydata)[0]))
            # xdata = tf.gather(xdata, perm, axis=0)
            # ydata = tf.gather(ydata, perm, axis=0)
            # xdatas, ydatas = tf.random.shuffle(xdata, ydata)
            b0temp = b.eval(session = sess)
            w0temp = w.eval(session = sess)
            loss_avg = loss_sum / len(ydata)
            print('epcoh=', epoch+1, 'loss=', loss_avg, 'b=', b0temp, 'w=', w0temp)



if __name__ == '__main__': 
    handleCsv = HandleStockData(688396)
