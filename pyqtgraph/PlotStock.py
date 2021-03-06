#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:dell
from PyQt5 import QtWidgets
import pyqtgraph as pg
import os
import numpy as np
import pandas as pd



class MyGraphWindow(object):
    csvdir = os.path.dirname(os.path.abspath(__file__)) + '\\..\\csv'
    allxdata = 2000
    disxdata = 200
    movexdata = 20
    def __init__(self, graphic):
        super(MyGraphWindow, self).__init__()
        pg.setConfigOptions(antialias=True)  # pg全局变量设置函数，antialias=True开启曲线抗锯齿
        self.win = pg.GraphicsLayoutWidget()  # 创建pg layout，可实现数据界面布局自动管理
        self.p1 = self.win.addPlot(row=1, col= 0, rowspan=3, colspan=1)  # 添加第一个绘图窗口
        self.p1.setLabel('left', text='价格', color='#ffffff')  # y轴设置函数
        self.p1.showGrid(x=True, y=True)  # 栅格设置函数
        self.p1.setLogMode(x=False, y=False)  # False代表线性坐标轴，True代表对数坐标轴
        # self.p1.setLabel('bottom', text='time', units='s')  # x轴设置函数
        # p1.addLegend()  # 可选择是否添加legend
        self.p1.showAxis('left', show=True)
        
        # self.labelp1 = pg.LabelItem(justify='right')
        # self.win.addItem(self.labelp1)
        # self.p1.showAxis('right', show=True)
        # raxes = self.p1.getAxis('right')
        # raxes.setRange(-4, 4)

        # self.win.nextRow()  # layout换行，采用垂直排列，不添加此行则默认水平排列
        # self.win.nextRow()  # layout换行，采用垂直排列，不添加此行则默认水平排列
        self.p2 = self.win.addPlot(row=4, col= 0, rowspan=1, colspan=1, title="cos 函数")
        self.p2.setLabel('left', text='量能', color='#ffffff')
        self.p2.showGrid(x=True, y=True)
        self.p2.setLogMode(x=False, y=False)
        # self.p2.setLabel('bottom', text='time', units='s')
        # p2.addLegend()

        # Plotted = self.p1 
        self.xxLine = pg.InfiniteLine(angle=90, pen='g') 
        self.xLine = pg.InfiniteLine(angle=90, pen='g') 
        self.yLine = pg.InfiniteLine(angle=0, pen='g') 
        self.win.scene().sigMouseMoved.connect(self.mouse1Moved) 
        # self.p2.scene().sigMouseMoved.connect(self.mouse2Moved) 
        
        # pg绘图窗口可以作为一个widget添加到GUI中的graph_layout，当然也可以添加到Qt其他所有的容器中
        graphic.addWidget(self.win)

    def mouse1Moved(self,evt): 
        mousePoint = evt 
        print("win x:", mousePoint)
        if self.p1.sceneBoundingRect().contains(mousePoint): 
            if self.xLine not in self.p1.listDataItems():
                self.p2.removeItem(self.xLine)
                self.p1.addItem(self.xLine, ignoreBounds=False)
            if self.yLine not in self.p1.listDataItems():
                self.p2.removeItem(self.yLine)
                self.p1.addItem(self.yLine, ignoreBounds=False)
            if self.xxLine not in self.p2.listDataItems():
                self.p1.removeItem(self.xxLine)
                self.p2.addItem(self.xxLine, ignoreBounds=False)
            mousePoint = self.p1.vb.mapSceneToView(mousePoint) 
            print("p1 x:", mousePoint.x(), "y:", mousePoint.y())
            # if mousePoint.x() < self.stockdata.index.stop and mousePoint.x() + 1 > self.xhigh:
            #     offset = mousePoint.x() + MyGraphWindow.movexdata
            #     if offset > self.stockdata.index.stop:
            #         offset = self.stockdata.index.stop
            #     mousePoint = pg.Point(mousePoint.x() + offset - self.xhigh, mousePoint.y())
            #     self.xhigh = int(offset) + 1
            #     self.xlow = self.xhigh - MyGraphWindow.disxdata
            # elif mousePoint.x() > self.stockdata.index.stop - MyGraphWindow.allxdata and mousePoint.x() - 1 < self.xlow:
            #     offset = mousePoint.x() - MyGraphWindow.movexdata
            #     if offset < self.stockdata.index.stop - MyGraphWindow.allxdata:
            #         offset = self.stockdata.index.stop - MyGraphWindow.allxdata
            #     mousePoint = pg.Point(mousePoint.x() - offset + self.xhigh, mousePoint.y())
            #     self.xlow = int(offset)
            #     self.xhigh = self.xlow + MyGraphWindow.disxdata
            self.setDisplaylimt(self.xlow, self.xhigh)

        elif self.p2.sceneBoundingRect().contains(mousePoint): 
            if self.xLine not in self.p2.listDataItems():
                self.p1.removeItem(self.xLine)
                self.p2.addItem(self.xLine, ignoreBounds=False)
            if self.yLine not in self.p2.listDataItems():
                self.p1.removeItem(self.yLine)
                self.p2.addItem(self.yLine, ignoreBounds=False)
            if self.xxLine not in self.p1.listDataItems():
                self.p2.removeItem(self.xxLine)
                self.p1.addItem(self.xxLine, ignoreBounds=False)
                
            mousePoint = self.p2.vb.mapSceneToView(mousePoint) 
            print("p2 x:", mousePoint.x(), "y:", mousePoint.y())
        else:
            return
        print("out xlow:", self.xlow, "xhigh:", self.xhigh)
        print("out x:", mousePoint.x(), "y:", mousePoint.y())
        self.xxLine.setPos(round(mousePoint.x())) 
        self.xLine.setPos(round(mousePoint.x())) 
        self.yLine.setPos(mousePoint.y())
        self.setDisplayValue(round(mousePoint.x()), mousePoint.y())

    def setDisplayValue(self, x, y):
        setstr = "<span style='color: blue'>open:%0.2f " % (self.stockdata['开盘价'].values[x])
        setstr += "<span style='color: yellow'>close:%0.2f " % (self.stockdata['收盘价'].values[x])
        setstr += "<span style='color: red'>high:%0.2f " % (self.stockdata['最高价'].values[x])
        setstr += "<span style='color: green'>low:%0.2f " % (self.stockdata['最低价'].values[x])
        
        print(self.stockdata['日期'].values[x])
        setstrp1 = "%s %s " % (self.stockname, self.stockdata['日期'].values[x]) 
        x = x + MyGraphWindow.allxdata - self.stockdata.index.values[-1] - 1
        # print(x)
        print(self.average[x])
        print(self.minvalue[x+4])
        # print(self.min5dvalue[x])
        setstr += "<span style='color: cyan'>1min能:%d " % (self.minvalue[x+4])
        setstr += "<span style='color: magenta'>1m/5d能:%d " % (self.min5dvalue[x])
        self.p2.setTitle(setstr)
        
        setstrp1 += "量均价:%0.2f " % (self.average[x])
        setstrp1 += " x=%d y=%0.1f " % (x, y)
        self.p1.setTitle(setstrp1)

                
    def setDisplaylimt(self, xlow, xhigh):
        self.xlow = xlow
        self.xhigh = xhigh
        print("low: ", self.xlow, "high: ", self.xhigh)
        self.p2.setXRange(self.xlow, self.xhigh, padding=0) 
        self.p1.setXRange(self.xlow, self.xhigh, padding=0) 
        dates = self.stockdata['日期'].values[self.xlow : self.xhigh : 30]
        # print(dates)
        print(range(self.xlow ,self.xhigh ,20))
        datedict =  dict( zip(range(self.xlow ,self.xhigh ,30), dates) )
        bottomaxis = self.p1.getAxis('bottom')
        bottomaxis.setTicks([datedict.items()])
        
        self.ylow = 0
        print(np.array(self.stockdata['最高价'].values[self.xlow : self.xhigh]).max())
        self.yhigh = int(np.array(self.stockdata['最高价'].values[self.xlow : self.xhigh]).max() +3)
        self.p1.setYRange(self.ylow, self.yhigh, padding=0)   
        
    def getStock(self, code):
        stockdata = pd.DataFrame()
        if(type(code) == type(1)):
            stockdir = MyGraphWindow.csvdir + "\\%(code)06d.csv"%{'code': code}
        else:
            stockdir = MyGraphWindow.csvdir + "\\%(code)s.csv"%{'code': code}
        if( False == os.path.isfile(stockdir)):
            print("not get stock path", stockdir)
            return ("", stockdata)
        # datatype = {'日期':np.str, '名称':np.str, '股票代码':np.str, '开盘价':np.float, '收盘价':np.float, '最高价':np.float, '最低价':np.float, 
        #             '前收盘':np.float, '换手率':np.float, '涨跌额':np.float, '涨跌幅':np.float, '成交量':np.float, '成交金额':np.float, '总市值':np.float, '流通市值':np.float}
        stockdata = pd.read_csv(stockdir, encoding='gbk')#, dtype=datatype)#, nrows=1)
        if (stockdata.empty ):
            print(stockdir, "get empty data")
            return ("", stockdata)

        stockname = stockdata.loc[0,'名称'] + '(' + stockdata.loc[0,'股票代码'][1:] + ')'
        stockdata = stockdata.drop(['名称', '股票代码'], axis = 1)
        stockdata = stockdata.sort_values(by='日期', ascending=True).reset_index(drop=True, inplace=False)
        return (stockname, stockdata)


    def plotStock(self, code):
        self.stockname, self.stockdata = self.getStock(code)
        print(self.stockname)
        self.p1.setTitle(self.stockname)
        self.setDisplaylimt(self.stockdata.index.values[-MyGraphWindow.disxdata], self.stockdata.index.values[-1])
        self.p1.plot(self.stockdata.index[-MyGraphWindow.allxdata:], self.stockdata['开盘价'].values[-MyGraphWindow.allxdata:], pen='b', name='open', clear=True)
        self.p1.plot(self.stockdata.index[-MyGraphWindow.allxdata:], self.stockdata['收盘价'].values[-MyGraphWindow.allxdata:], pen='y', name='close', clear=False)
        self.p1.plot(self.stockdata.index[-MyGraphWindow.allxdata:], self.stockdata['最高价'].values[-MyGraphWindow.allxdata:], pen='r', name='high', clear=False)
        self.p1.plot(self.stockdata.index[-MyGraphWindow.allxdata:], self.stockdata['最低价'].values[-MyGraphWindow.allxdata:], pen='g', name='low', clear=False)
        self.average = self.stockdata['成交金额'].values[-MyGraphWindow.allxdata:] / self.stockdata['成交量'].values[-MyGraphWindow.allxdata:]
        self.p1.plot(self.stockdata.index[-MyGraphWindow.allxdata:], self.average, pen='w', name='low', clear=False)
        
        
        values = self.stockdata['成交量'].values[-MyGraphWindow.allxdata-4:]
        self.minvalue = values / (4 * 60)
        self.min5dvalue = ( values[:-4] + values[1:-3] + values[2:-2] + values[3:-1] + values[4:] ) / (5* 4 * 60)
        self.p2.plot(self.stockdata.index[-MyGraphWindow.allxdata:], self.minvalue[4:], pen='c', name='1min', clear=True)
        self.p2.plot(self.stockdata.index[-MyGraphWindow.allxdata:], self.min5dvalue, pen='m', name='1m/5d', clear=False)
        
        labelp1 = pg.LabelItem(justify='right')
        self.p1.addItem(labelp1)
        labelp1.setText("<span style='font-size: 12pt'> 'asdgas'</span>") # <span style='color: red'>
        self.p1.setXRange(self.xlow, self.xhigh, padding=0) 
        self.p1.setYRange(self.ylow, self.yhigh, padding=0)    




