# -*-coding:utf8-*-

import os
import numpy as np
import pandas as pd
import tensorflow as tf

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor, as_completed, wait, ALL_COMPLETED,FIRST_COMPLETED

TEST_DATA_NUM   = 100
TRAINING_EPOH   = 20
STEPRATE        = 0.01

class HandleStockData(object):
    csvdir              = os.path.dirname(os.path.abspath(__file__)) + '\\csv'

    def __init__(self, code):
        if(type(code) == type(1)):
            self.code = "%(code)06d"%{'code':code}
        else:
            self.code = code
        
        # pool = ThreadPoolExecutor(max_workers=4)
        # task_list = []
        # for index in range (1, 6, 1):
        #     self.train_data_func(index)
        # #     task_list.append(pool.submit(self.train_data_func, index))
        self.train_data_func(2)

    def train_data_func(self, type):
        if (type == 1 or type == 2 or type == 3 or type == 4 or type == 5):
            self.type    = type
            self.predata = self.read_stock_data()
            pre, w, b = self.train_data_model()
            self.sess.close()
        else:
            print('type error')

    
    def read_stock_data(self):
        csvdir = self.csvdir + "\\%(code)s.csv"%{'code': self.code}
        stockdata = pd.DataFrame()
        if(os.path.isfile(csvdir)):
            # datatype = {'日期':np.str, '名称':np.str, '股票代码':np.str, '开盘价':np.float, '收盘价':np.float, '最高价':np.float, '最低价':np.float, 
            #             '前收盘':np.float, '换手率':np.float, '涨跌额':np.float, '涨跌幅':np.float, '成交量':np.float, '成交金额':np.float, '总市值':np.float, '流通市值':np.float}
            stockdata = pd.read_csv(csvdir, encoding='gbk')#, dtype=datatype)#, nrows=1)
            if (stockdata.empty == False):
                # print(self.stockdorgata)
                self.stockname = stockdata.loc[0]['名称']
                stockdata = stockdata.drop(['名称', '股票代码'], axis = 1)
                # print(self.stockdorgata)
                stockdata = stockdata[ ~ stockdata['涨跌幅'].str.contains('None') ]      
                stockdata.insert(13, '收幅', 0)
                stockdata[ ['涨跌额', '涨跌幅', '收幅'] ] = stockdata[ ['涨跌额', '涨跌幅', '收幅'] ].astype('float32') 
                # print(stockdata)
                # stockdata.rename(columns={  '日期':'DATE', '换手率':'TURNOVERRATE', 
                #                             '开盘价':'OPENPRICE', '收盘价':'CLOSEPRICE', '前收盘':'PREPRICE',
                #                             '最高价':'HIGHPRICE', '最低价':'LOWPRICE', 
                #                             '涨跌额':'UPDOWNPRICE', '涨跌幅':'UPDOWNRANGE',
                #                             '成交量':'VOLUME', '成交金额':'AMOUNT', 
                #                             '总市值':'MARKETVALUE', '流通市值':'FLOW'},inplace=True) 
                if (self.type == 1):
                    stockdata.rename(columns={  '日期': 15, '换手率': 11, 
                                                '开盘价': 0, '收幅' : 16,
                                                '收盘价': 1, '前收盘': 2,
                                                '最高价': 3, '最低价': 4, 
                                                '成交量': 5, '成交金额': 6, 
                                                '涨跌额': 7, '涨跌幅': 8,
                                                '总市值':9, '流通市值': 10},inplace=True) 
                elif (self.type == 2):
                    stockdata.rename(columns={  '日期': 15, '换手率': 11, 
                                                '开盘价': 1, '收幅' : 16,
                                                '收盘价': 0, '前收盘': 2,
                                                '最高价': 3, '最低价': 4, 
                                                '成交量': 5, '成交金额': 6, 
                                                '涨跌额': 7, '涨跌幅': 8,
                                                '总市值':9, '流通市值': 10},inplace=True) 
                elif (self.type == 3):
                    stockdata.rename(columns={  '日期': 15, '换手率': 11, 
                                                '开盘价': 3, '收幅' : 16,
                                                '收盘价': 1, '前收盘': 2,
                                                '最高价': 0, '最低价': 4, 
                                                '成交量': 5, '成交金额': 6, 
                                                '涨跌额': 7, '涨跌幅': 8,
                                                '总市值':9, '流通市值': 10},inplace=True) 
                elif (self.type == 4):
                    stockdata.rename(columns={  '日期': 15, '换手率': 11, 
                                                '开盘价': 4, '收幅' : 16,
                                                '收盘价': 1, '前收盘': 2,
                                                '最高价': 3, '最低价': 0, 
                                                '成交量': 5, '成交金额': 6, 
                                                '涨跌额': 7, '涨跌幅': 8,
                                                '总市值':9, '流通市值': 10},inplace=True) 
                elif (self.type == 5):
                    stockdata.rename(columns={  '日期': 15, '换手率': 11, 
                                                '开盘价': 8, '收幅' : 16,
                                                '收盘价': 1, '前收盘': 2,
                                                '最高价': 3, '最低价': 4, 
                                                '成交量': 5, '成交金额': 6, 
                                                '涨跌额': 7, '涨跌幅': 0,
                                                '总市值':9, '流通市值': 10},inplace=True) 

                stockdata = stockdata.sort_values(by=15, ascending=True).reset_index(drop=True, inplace=False)
                stockdata.sort_index(axis=1, inplace=True)
                stockdata.drop(index=[0], inplace=True)      
                stockdata = stockdata.values
                stockdata = np.array(stockdata)
                # if (self.type == 2):
                #     stockdata[1:,13] = (stockdata[1:,0] - stockdata[:-1,0]) / stockdata[:-1,0]
                # else:
                #     stockdata[1:,13] = (stockdata[1:,1] - stockdata[:-1,1]) / stockdata[:-1,1]
                # print(stockdata)
                self.stockdorgata = stockdata.copy()
                for i in range (0, 12):
                    stockdata[:,i] = (stockdata[:,i] - stockdata[:,i].min()) / (stockdata[:,i].max() - stockdata[:,i].min())
                # print(stockdata)
                # print(stockdata[:, ])
                # print(stockdata[:, 3])
                # print(self.stockdorgata[:, 3])
        return stockdata
        
    def pre_data_model(self, x):
        with tf.name_scope('Model'):
            w = tf.Variable(tf.random.normal([12, 1], stddev=0.01), name='W')
            b = tf.Variable(1.0, name='B')
            def base_model(x, w, b):
                return tf.matmul(x, w) + b
            pred = base_model(x, w, b)
            return pred, w, b
            
    def train_data_model(self):
        xdata = self.predata[ :self.predata.shape[0]-TEST_DATA_NUM, 0:12].astype('float32')
        ydata = self.stockdorgata[1 : self.predata.shape[0]-TEST_DATA_NUM+1, 0].astype('float32')
        # print(xdata , "\nshape:" , xdata.shape)
        # print(ydata , "\nshape:" , ydata.shape)
        tf.compat.v1.disable_eager_execution()
        x = tf.compat.v1.placeholder(tf.float32, [None, 12], name='X')
        y = tf.compat.v1.placeholder(tf.float32, [None, 1], name='Y')

        pred, w, b= self.pre_data_model(x)
        with tf.name_scope('LossFunction'):
            lossfunc = tf.reduce_mean(tf.pow(y - pred, 2))
        optimizer = tf.compat.v1.train.GradientDescentOptimizer(STEPRATE).minimize(lossfunc)
        self.sess = tf.compat.v1.Session()
        init = tf.compat.v1.global_variables_initializer()
        self.sess.run(init)
        # print(xdata)
        # print(ydata)
        for epoch in range(0, TRAINING_EPOH):
            loss_sum = 0.0
            for xs, ys in zip(xdata, ydata):
                xs = xs.reshape(1, 12)
                ys = np.array(ys).reshape(1, 1)
                _, loss = self.sess.run([optimizer, lossfunc], feed_dict={x: xs, y: ys})
                loss_sum = loss_sum + loss

            # indices = tf.range(start=0, limit=tf.shape(xdata)[0], dtype=tf.int32)
            # idx = tf.random.shuffle(indices)
            # xdata = tf.gather(xdata, idx)
            # ydata = tf.gather(ydata, idx)
            # print(xdata, 'sahrp:', xdata.shape)
            # perm = tf.random.shuffle(tf.range(tf.shape(ydata)[0]))
            # xdata = tf.gather(xdata, perm, axis=0)
            # ydata = tf.gather(ydata, perm, axis=0)
            # xdatas, ydatas = tf.random.shuffle(xdata, ydata)
            btemp = b.eval(session = self.sess)
            wtemp = w.eval(session = self.sess)
            # print(ydata.shape[0])
            loss_avg = loss_sum / ydata.shape[0]
            if (epoch > TRAINING_EPOH - 5):
                print('epcoh=', epoch+1, 'loss=', loss_avg, 'b=', btemp)#, 'w=', wtemp)
            else:
                print('=', end='')

        
        n = np.random.randint(TEST_DATA_NUM)
        xdata = self.predata[self.predata.shape[0]-n : self.predata.shape[0]-1, 0:12].astype('float32')
        ydata = self.stockdorgata[self.predata.shape[0]-n+1 : self.predata.shape[0], 0].astype('float32')
        hdata = self.stockdorgata[self.predata.shape[0]-n+1 : self.predata.shape[0], 3].astype('float32')
        # print(ydata)
        # print(hdata)
        count = self.predata.shape[0]-n
        prearry=[]
        for xs, ys in zip(xdata, ydata):
            count = count + 1
            xs = xs.reshape(1, 12)
            # ys = np.array(ys).reshape(1, 1)
            pre = self.sess.run(pred, feed_dict={x: xs})
            prearry.append(pre[0, 0])
            # print("stocknum: %(date)s\tydata: %(y)f\tpre: %(pre)f"%{'date': self.predata[count, 12], 'y': ys, 'pre': pre})

        xs = self.predata[self.predata.shape[0]-1, 0:12].astype('float32')
        # print(xs)
        xs = xs.reshape(1, 12)
        # ys = np.array(ys).reshape(1, 1)
        pre = self.sess.run(pred, feed_dict={x: xs})
        # print(pred)
        if (self.type == 1):
            print("code: %(code)s 开盘价 pre: %(pre)f loss: %(loss)f"%{'code': self.code, 'pre': pre, 'loss': loss_avg})
        elif (self.type == 2):
            print("code: %(code)s 收盘价 pre: %(pre)f loss: %(loss)f"%{'code': self.code, 'pre': pre, 'loss': loss_avg})
            
            print(prearry)
            self.plot_data(ydata, prearry, hdata)
            prearry.append(pre)
            prearry = np.array(prearry)
            prearry[1:] = 100 * (prearry[1:] - prearry[:-1]) / prearry[:-1]
            print(prearry)
        elif (self.type == 3):
            print("code: %(code)s 最高价 pre: %(pre)f loss: %(loss)f"%{'code': self.code, 'pre': pre, 'loss': loss_avg})
        elif (self.type == 4):
            print("code: %(code)s 最低价 pre: %(pre)f loss: %(loss)f"%{'code': self.code, 'pre': pre, 'loss': loss_avg})
        elif (self.type == 5):
            print("code: %(code)s 涨跌幅 pre: %(pre)f loss: %(loss)f"%{'code': self.code, 'pre': pre, 'loss': loss_avg})

        return pred, wtemp, btemp

    def plot_data(self, y, pre, high):
        import matplotlib.pyplot as plt
        x = range(1, len(pre)+1, 1)
        # print(x)
        # print(pre, len(pre))
        # print(y, len(y))
        # print(high, len(high))
        plt.plot(x, y, 'r', label='LowPrice')
        plt.plot(x, pre, 'g', label='Prelow')
        plt.plot(x, high, 'b', label='HighPrice')
        plt.legend()
        plt.show()


    def verify_data_model(self, pred):
        n = np.random.randint(TEST_DATA_NUM)
        xdata = self.predata[self.predata.shape[0]-n : self.predata.shape[0]-2, 1:12].astype('float32')
        ydata = self.predata[self.predata.shape[0]-n+1 : self.predata.shape[0] - 1, 0].astype('float32')
        count = self.predata.shape[0]-n
        for xs, ys in zip(xdata, ydata):
            count = count + 1
            xs = xs.reshape(1, 11)
            # ys = np.array(ys).reshape(1, 1)
            self.sess.run(pred, feed_dict={x: xs})
            print("stocknum: %(num)d\tydata: %(y)f\tpre: %(pre)f"%{'num': count, 'y': ys, 'pre': pred})
        
        xs = self.predata[self.predata.shape[0]-1, 1:12].astype('float32')
        print(xs)
        xs = xs.reshape(1, 11)
        # ys = np.array(ys).reshape(1, 1)
        self.sess.run(pred, feed_dict={x: xs})
        print("pre: %(pre)f"%{ 'pre': pred})

if __name__ == '__main__': 
    # handleCsv = HandleStockData(688396)
    handleCsv = HandleStockData(2402)
