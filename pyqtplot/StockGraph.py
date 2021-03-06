# -*- coding: utf-8 -*-
import _locale
_locale._getdefaultlocale = (lambda *args: ['zh_CN', 'utf8'])


import numpy as np
import pandas as pd
from StockCode import *
from PyQt5.QtCore import pyqtSignal, QThread, QObject
from PyQt5.QtWidgets import QSizePolicy

import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
# import mpl_finance as mpf


class GraphWork(QObject):
    signal_Update =pyqtSignal(int, int, str)
    signal_Show =pyqtSignal(str, str)
    signal_UnShow =pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(GraphWork, self).__init__(parent)
        self.LastCode = ''
        self.BeforeLine = 0
        self.LowLine = 0
        self.HighLine = 0
        self.OpenLine = 0
        self.CloseLine = 0

    def graphInitWorker(self, fig, codename='000001平安银行'):
        self.Axes = fig.add_subplot(111) # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
        self.graphShowParam(codename)
        self.graphShowCandle(1)
        # self.graphShowCandle(0)
        
    def graphShowParam(self, codename, periodday=90, periodspace=1):
        if self.LastCode != codename:
            self.StockData = stock_GetLocalData(codename)
            if self.StockData.empty:
                self.LastCode = ''
            else:
                self.LastCode = codename
                self.PeriodDay = periodday
                self.PeriodSpace = periodspace
                tdata = pd.DataFrame(np.arange(0,len(self.StockData)))
                pricearray = pd.concat([tdata, self.StockData[['开盘价', '最高价', '最低价', '收盘价']]],axis=1)
                self.DatepPiceList =np.array(pricearray).tolist()
                print(self.DatepPiceList)
    
    def graphShowCandle(self, show):
        if self.LastCode and self.PeriodDay <= len(self.StockData):
            if show:
                self.BeforeLine = self.Axes.plot(self.StockData.index[-self.PeriodDay: -self.PeriodSpace :], self.StockData['前收盘'][-self.PeriodDay: -self.PeriodSpace :], color='magenta')
            elif self.BeforeLine:
                self.BeforeLine.pop(0).remove()

# 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键
class StockGraph(FigureCanvas):
    
    def __init__(self, parent=None, width=11, height=5, dpi=100):
        # super(StockGraph, self).__init__(parent)
        self.fig = Figure(figsize=(width, height), dpi=dpi)  # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure
        FigureCanvas.__init__(self, self.fig) # 初始化父类
        self.fig.subplots_adjust(bottom=0.2)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding,  QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.PeriodSpace=0
        self.PeriodDay=0
        self.LastCode = ''
        self.Axes = self.fig.add_subplot(111) # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
        self.OpenLine   = self.Axes.plot([], [], color='red')
        self.CloseLine  = self.Axes.plot([], [], color='green')
        self.BeforeLine = self.Axes.plot([], [], color='magenta')
        self.HighLine   = self.Axes.plot([], [], color='blue')
        self.LowLine    = self.Axes.plot([1,2,3], [1,2,3], color='yellow')
        

        # self.GraphThread=QThread()
        # self.GraphWorker=GraphWork()
        # self.GraphWorker.moveToThread(self.GraphThread)
        # # self.GraphThread.started.connect(self.GraphWorker.graphInitWorker)
        # # self.GraphWorker.signal_Add.connect(self.treeItemAdd)
        # self.GraphThread.start()
        # self.GraphWorker.graphInitWorker(fig)
        
    def paintStockPrice(self, codename):
        pass

    def graphInitPriceWorker(self, codename='000001平安银行', periodday=90, periodspace=1):
        self.graphShowUpdateCode(codename)
        self.graphShowUpdateTime(periodday, periodspace)
        self.graphShowBeforeLine(1)
        self.graphShowOpenLine(1)
        self.graphShowCloseLine(1)
        self.graphShowHighLine(1)
        self.graphShowLowLine(1)
        
    def graphShowUpdateCode(self, codename):
        if self.LastCode != codename:
            self.StockData = stock_GetLocalData(codename)
            if self.StockData.empty:
                self.LastCode = ''
            else:
                self.LastCode = codename
                self.StockData['日期'] = pd.to_datetime(self.StockData['日期'])
                self.StockData = self.StockData.sort_index(ascending=False)
                print(self.StockData.tail(20))
                print(self.StockData['日期'][-1::-1])
                # tdata = pd.DataFrame(np.arange(0,len(self.StockData)))
                # pricearray = pd.concat([tdata, self.StockData[['开盘价', '最高价', '最低价', '收盘价']]],axis=1)
                # self.DatepPiceList =np.array(pricearray).tolist()
                # print(self.DatepPiceList)

    def graphUpdateLineData(self, line):
        if line == 'open':
            LineData = self.StockData['开盘价']
        elif line == 'close':
            LineData = self.StockData['收盘价']
        elif line == 'before':
            LineData = self.StockData['前收盘']
        elif line == 'high':
            LineData = self.StockData['最高价']
        elif line == 'low':
            LineData = self.StockData['最低价']
        else:
            return []

        MaxDay = self.PeriodDay * self.PeriodSpace
        if MaxDay == 0 or MaxDay > len(self.StockData):
            return []
        CellData = LineData[-MaxDay : : self.PeriodSpace]
        CellData.index = range(0, self.PeriodDay)
        DrawData = CellData
        for i in range(1 , self.PeriodSpace):
            CellData = LineData[-MaxDay + i : : self.PeriodSpace]
            CellData.index = range(0, self.PeriodDay)
            DrawData = DrawData + CellData
        DrawData = DrawData / self.PeriodSpace
        print(self.StockData['日期'][-1:30:1])
        print(DrawData)
        return DrawData

    def graphShowUpdateTime(self, periodday, periodspace):
        NeedUpdateData = 0
        if periodday != self.PeriodDay:
            self.PeriodDay = periodday
            NeedUpdateData = 1
        if periodspace != self.PeriodSpace:
            self.PeriodSpace = periodspace
            NeedUpdateData = 1

        if NeedUpdateData and self.StockData.empty == False:
            self.OpenData   = self.graphUpdateLineData('open')
            self.CloseData  = self.graphUpdateLineData('close')
            self.BeforeData = self.graphUpdateLineData('before')
            self.HighData   = self.graphUpdateLineData('high')
            self.LowData    = self.graphUpdateLineData('low')
            # print(self.DateData)
            # print(self.OpenData)
        
    def graphUpdateShowData(self, showline, show=1):
        if showline == self.OpenLine:
            DrawData = self.OpenData
        elif showline == self.CloseLine:
            DrawData = self.CloseData
        elif showline == self.BeforeLine:
            DrawData = self.BeforeData
        elif showline == self.HighLine:
            DrawData = self.HighData
        elif showline == self.LowLine:
            DrawData = self.LowData
        else:
            return []

        MaxDay = self.PeriodDay * self.PeriodSpace
        if MaxDay == 0 or MaxDay > len(self.StockData):
            return []

        if showline :
            # print(self.Axes.get_lines())
            showline.pop(0).remove()
            # DrawLine.remove()
            # print(self.Axes.get_lines())
        self.Axes.set_autoscale_on(True)
        if show and DrawData.any() :                
            if showline == self.OpenLine:
                self.OpenLine = self.Axes.plot(range(0,self.PeriodDay), DrawData, color='red')
            elif showline == self.CloseLine:
                self.CloseLine = self.Axes.plot(range(0,self.PeriodDay), DrawData, color='green')
            elif showline == self.BeforeLine:
                self.BeforeLine = self.Axes.plot(range(0,self.PeriodDay), DrawData, color='magenta')
            elif showline == self.HighLine:
                self.HighLine = self.Axes.plot(range(0,self.PeriodDay), DrawData, color='blue')
            elif showline == self.LowLine:
                self.LowLine = self.Axes.plot(range(0,self.PeriodDay), DrawData, color='yellow')
            # print(self.Axes.get_lines())
        min, max = self.Axes.set_ylim()
        min = DrawData.min() * 0.95
        if max < DrawData.max() * 1.05:
            max = DrawData.max() * 1.05
        # print("min is %(min)d max is %(max)d" %{'min' : min, 'max':max})
        self.Axes.set_ylim(min, max)
        print(self.Axes.get_xticklabels()[:])
        print(self.Axes.get_xticks()[:])
        self.Axes.set_xlim(0, self.PeriodDay)
        # self.Axes.set_xticklabels(self.DateData[::10], rotation=60)
        # print(self.DateData[:-1:10])
        # print(self.StockData.loc[(-MaxDay + self.PeriodSpace - 1 : : self.PeriodSpace),'日期'] )
        # print(self.StockData.index[-MaxDay + self.PeriodSpace - 1 : : self.PeriodSpace].tolist())
        # print(DrawData.tolist())
        self.draw()

    
    def graphShowBeforeLine(self, show):
        self.graphUpdateShowData(self.BeforeLine, show)
    
    def graphShowOpenLine(self, show):
        self.graphUpdateShowData(self.OpenLine, show)
    
    def graphShowCloseLine(self, show):
        self.graphUpdateShowData(self.CloseLine, show)
    
    def graphShowHighLine(self, show):
        self.graphUpdateShowData(self.HighLine, show)
    
    def graphShowLowLine(self, show):
        self.graphUpdateShowData(self.LowLine, show)

