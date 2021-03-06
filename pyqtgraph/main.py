# -*- coding: utf-8 -*-
import sys
from Ui_mainwindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QAction, QTreeWidgetItem, QCompleter, QLayout#, QBrush, QColor
from PyQt5.QtCore import pyqtSignal, QDate, QStringListModel

import numpy as np
import pandas as pd
from StockCode import *
from PlotStock import MyGraphWindow
from GetStockByCsv import getStockCsv

import _locale
_locale._getdefaultlocale = (lambda *args: ['zh_CN', 'utf8'])

# http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQA%3BEXCHANGE%3ACNSESH&fields=SYMBOL&count=5000&type=query

class LogicWindow(QMainWindow, Ui_MainWindow):
    signal_Show = pyqtSignal(str)
    signal_Close = pyqtSignal(int, str)

    
    g_datapath = os.path.dirname(os.path.abspath(__file__))
    logpath = g_datapath + '\\000001amarket_log.txt'
    logfp = open(logpath, "w")
    logfp.write("start the A market get data program at s\n")

    def __init__(self, parent=None):
        super(LogicWindow, self).__init__(parent)
        self.setupUi(self)
        # self.formLayout.setSizeConstraint(QLayout.SetFixedSize)
        # self.formLayout.setSizeConstraint(QLayout::SetFixedSize)
        # self.groupBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.graphicswin = MyGraphWindow(self.graphicbox)
        # self.graphicswin.plotStock(2402)

        self.setMenuData()
        self.setInitData()
        self.setTreeData()
        self.setStatuBarData()


    def showEvent(self, evt):
        print("this is show"  )
        
    def closeEvent(self, evt):
        print("this is close"  )

     
    def setMenuData(self):   
        # test menu signandslot connect 
        self.menu_Test.triggered[QAction].connect(self.menuTestFunction)
        self.signal_Show.connect(self.testShowFunction)
        self.signal_Close.connect(self.testCloseFunction)        
        # file menu signandslot connect 
        self.action_New.triggered.connect(self.actionNewFunction)
        self.action_Open.triggered['bool'].connect(self.actionOpenFunction)
        self.action_Save.triggered['bool'].connect(self.actionSaveFunction)
        self.action_Quit.triggered['bool'].connect(self.actionQuitFunction)

    # menu slot function
    def actionNewFunction(self):
        print("this is new" )

    def actionOpenFunction(self):
        print("this is open" )

    def actionSaveFunction(self):
        print("this is save" )

    def actionQuitFunction(self):
        print("this is quit" )
        self.close()

    # test slot function
    def menuTestFunction(self, ob):
        self.statusBar().showMessage("this is menu" + ob.text() )
        # print("this is menu" + ob.text() )
        if ob == self.action_Show_test:
            self.signal_Show.emit("show here")
        elif ob == self.action_Close_test:
            self.signal_Close.emit(4, "close here")
        else:
            print("show o=n again")

    def testShowFunction(self, message):
        print("emit a message for " + message)

    def testCloseFunction(self, intstr, test):
        print("emit a message 1 for " + test)
        print("emit a message 2 for " + str(intstr) + test)


    def setInitData(self):
        # self.AllStockData = pd.DataFrame()
        self.dateEdit_Start.setDate(QDate.currentDate())
        self.dateEdit_End.setDate(QDate.currentDate())
        # self.lineEdit_StockCode.editingFinished.connect(self.editCodeFinished)
        self.lineEdit_StockCode.textChanged['QString'].connect(self.searchCodeChange)
        # self.lineEdit_StockName.editingFinished.connect(self.editCodeFinished)
        # self.lineEdit_StockName.textChanged['QString'].connect(self.searchNameChange)
        self.setCompleter()

    def setCompleter(self):#use more time
        # # 设置匹配模式  有三种： Qt.MatchStartsWith 开头匹配（默认）  Qt.MatchContains 内容匹配  Qt.MatchEndsWith 结尾匹配
        # self.completer.setFilterMode(Qt.MatchContains)
        # # 设置补全模式  有三种： QCompleter.PopupCompletion（默认）  QCompleter.InlineCompletion   QCompleter.UnfilteredPopupCompletion
        # self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completerCodeEdit = QCompleter()
        self.completerCodeListModel = QStringListModel()
        self.lineEdit_StockCode.setCompleter(self.completerCodeEdit)
        self.completerCodeEdit.setModel(self.completerCodeListModel)
        self.completerCodeEdit.activated['QString'].connect(self.completerCodeFunction)

    def completerCodeFunction(self, text):
        if len(text) >= 6:
            items = self.treeWidget.findItems(text, QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive)
            self.treeWidget.setCurrentItem(items[0])
            self.graphicswin.plotStock(int(text[:6]))

    def searchCodeChange(self, text):
        if text == '' or len(text) >= 6:
            pass
        else:
            items = self.treeWidget.findItems(text, QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive)
            itlen = len(items)
            if itlen:
                setlist = []
                if itlen > 10:
                    itlen = 10
                for i in range(0, itlen):
                    setlist.append(items[i].text(0))
                self.completerCodeListModel.setStringList(setlist)

      
    def setTreeHeader(self):  
        self.treeWidget.headerItem().setText(0, "股市")
        UpParent = QTreeWidgetItem(self.treeWidget)
        UpParent.setText(0, "A股")
        child = QTreeWidgetItem(UpParent)
        child.setText(0, "深市A股")
        child = QTreeWidgetItem(UpParent)
        child.setText(0, "沪市A股")
        UpParent = QTreeWidgetItem(self.treeWidget)
        UpParent.setText(0, "B股")
        child = QTreeWidgetItem(UpParent)
        child.setText(0, "深市B股")
        child = QTreeWidgetItem(UpParent)
        child.setText(0, "沪市B股")
        UpParent = QTreeWidgetItem(self.treeWidget)
        UpParent.setText(0, "中小板")
        UpParent = QTreeWidgetItem(self.treeWidget)
        UpParent.setText(0, "科创板")
        UpParent = QTreeWidgetItem(self.treeWidget)
        UpParent.setText(0, "创业板")

    def addTreeData(self, chunk):      
        codename = "%(code)06d"%{'code':chunk.loc['SYMBOL']}
        tlist=[stock_CodeIdentify(codename), codename, chunk.loc['NAME']]
        codename = tlist[1] + tlist[2]
        if tlist[0] == '':
            print(tlist)
        elif tlist[0] == MARKER_TYPE_SZ_ZXB:
            UpParent = self.treeWidget.topLevelItem(2)
            child = QTreeWidgetItem(UpParent)
            child.setText(0, codename)
            self.logfp.write(str(tlist[1]))
        elif tlist[0] == MARKER_TYPE_SH_KCB:
            UpParent = self.treeWidget.topLevelItem(3)
            child = QTreeWidgetItem(UpParent)
            child.setText(0, codename)
        elif tlist[0] == MARKER_TYPE_SZ_CYB:
            UpParent = self.treeWidget.topLevelItem(4)
            child = QTreeWidgetItem(UpParent)
            child.setText(0, codename)
        elif MARKER_TYPE_B in tlist[0]:
            if tlist[0] == MARKER_TYPE_SZ_B:
                UpParent = self.treeWidget.topLevelItem(1).child(0)
                child = QTreeWidgetItem(UpParent)
                child.setText(0, codename)
            elif tlist[0] == MARKER_TYPE_SH_B:
                UpParent = self.treeWidget.topLevelItem(1).child(1)
                child = QTreeWidgetItem(UpParent)
                child.setText(0, codename)
        elif MARKER_TYPE_A in tlist[0]:
            if tlist[0] == MARKER_TYPE_SZ_A:
                UpParent = self.treeWidget.topLevelItem(0).child(0)
                child = QTreeWidgetItem(UpParent)
                child.setText(0, codename)
            elif tlist[0] == MARKER_TYPE_SH_A:
                UpParent = self.treeWidget.topLevelItem(0).child(1)
                child = QTreeWidgetItem(UpParent)
                child.setText(0, codename)
        self.logfp.flush()

    def setTreeData(self):#use more source
        self.setTreeHeader()
        self.AllStockData = stock_IdentifyType(1)
        print(type(self.AllStockData['SYMBOL']))
        for i in range(0, len(self.AllStockData)):
            chunk = self.AllStockData.loc[i]
            self.addTreeData(chunk)
        self.treeWidget.itemClicked['QTreeWidgetItem*','int'].connect(self.treeItemClick)

    def setTreeDataByItor(self):#use more time
        self.setTreeHeader()
        ItData = stock_IdentifyType(0)
        while True:
            try:
                chunk = ItData.get_chunk(1)
                self.addTreeData(chunk.loc[chunk.index.start])  
            except StopIteration:
                print ("market Iteration is stopped.")
                break

    def treeItemClick(self,item,n):
        print("this is item : " + item.text(n) + "num is : " + str(n))
        self.lineEdit_StockCode.setText(item.text(n))
        if(item.text(n)[:6].isdigit()):
            print(int(item.text(n)[:6]))
            self.graphicswin.plotStock(int(item.text(n)[:6]))

    def setStatuBarData(self):   
        self.upadteBtn = QtWidgets.QPushButton()
        self.upadteBtn.setText("更新股票")
        self.updateProcessBar = QtWidgets.QProgressBar()
        self.updateProcessBar.setValue(0)
        self.statusbar.addPermanentWidget(self.upadteBtn,stretch=0)
        self.statusbar.addPermanentWidget(self.updateProcessBar,stretch=1)
        self.upadteBtn.clicked.connect(self.updateStockFile)
        self.updateProcessBar.setTextVisible(False)
        
    def updateStockFile(self): 
        text = self.upadteBtn.text()
        # self.updateProcessBar.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        # self.updateProcessBar.setFormat('当前值%v 百分比%p 已加载{},总共 %m'.format(self.updateProcessBar.value()-self.updateProcessBar.minimum()))
        if text == "更新股票":
            self.updateProcessBar.setMinimum(0)
            self.updateProcessBar.setMaximum(0)
            self.upadteBtn.setDisabled(True)
            self.upadteBtn.setText("进度：0.00%") 
            self.getcsv = getStockCsv()
            self.getcsv.updateProcess.connect(self.updateStockProcess)
            self.getcsv.start()
            
    def updateStockProcess(self, per, time): 
        if(per >= 100):
            self.upadteBtn.setText("进度：{:0.2f}% 耗时: {:0.2f}".format(per, time))
            self.updateProcessBar.setMaximum(100)
            self.updateProcessBar.setValue(100)
        else:
            self.upadteBtn.setText("进度：{:0.2f}% 耗时: {:0.2f}".format(per, time))

        

if __name__ == "__main__": 
    app = QtWidgets.QApplication(sys.argv)
    logicWindow = LogicWindow()
    logicWindow.show()
    sys.exit(app.exec_())
