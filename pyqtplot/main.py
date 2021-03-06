# -*- coding: utf-8 -*-
import sys
import time
from Ui_mainwindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QAction, QTreeWidgetItem, QCompleter#, QBrush, QColor
from PyQt5.QtCore import pyqtSignal, QDate, QStringListModel, QThread, QObject

import numpy as np
import pandas as pd
from StockCode import *
from StockGraph import *

import _locale
_locale._getdefaultlocale = (lambda *args: ['zh_CN', 'utf8'])

# http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQA%3BEXCHANGE%3ACNSESH&fields=SYMBOL&count=5000&type=query
class WorkObject(QObject):
    signal_Add =pyqtSignal(int, int, str)

    def __init__(self,parent=None):
        super(WorkObject, self).__init__(parent)
        self.startType = 0
   
    def addTreeData(self, chunk):      
        codename = "%(code)06d"%{'code':chunk.loc['SYMBOL']}
        tlist=[stock_CodeIdentify(codename), codename, chunk.loc['NAME']]
        codename = tlist[1] + tlist[2]
        if tlist[0] == '':
            print(tlist)
        elif tlist[0] == MARKER_TYPE_SZ_ZXB:
            self.signal_Add.emit(2, -1, codename)
        elif tlist[0] == MARKER_TYPE_SH_KCB:
            self.signal_Add.emit(3, -1, codename)
        elif tlist[0] == MARKER_TYPE_SZ_CYB:
            self.signal_Add.emit(4, -1, codename)
        elif MARKER_TYPE_B in tlist[0]:
            if tlist[0] == MARKER_TYPE_SZ_B:
                self.signal_Add.emit(1, 0, codename)
            elif tlist[0] == MARKER_TYPE_SH_B:
                self.signal_Add.emit(1, 1, codename)
        elif MARKER_TYPE_A in tlist[0]:
            if tlist[0] == MARKER_TYPE_SZ_A:
                self.signal_Add.emit(0, 0, codename)
            elif tlist[0] == MARKER_TYPE_SH_A:
                self.signal_Add.emit(0, 1, codename)

    def treeInitWorker(self):
        # print("this is listdata"  )

        # ItData = stock_IdentifyType(0)
        # while True:
        #     try:
        #         chunk = ItData.get_chunk(100)
        #         self.addTreeData(chunk.loc[chunk.index.values[0]], tree)
        #     except StopIteration:
        #         print ("market Iteration is stopped.")
        #         break

        AllStockData = stock_IdentifyType(1)
        for i in range(0, len(AllStockData)):
            chunk = AllStockData.loc[i]
            self.addTreeData(chunk)
        self.signal_Add.emit(-1, -1, 'add over')	

class LogicWindow(QMainWindow, Ui_MainWindow):
    signal_Show = pyqtSignal(str)
    signal_Close = pyqtSignal(int, str)

    
    g_datapath = os.path.dirname(os.path.abspath(__file__))
    logpath = g_datapath + '\\uidebug.txt'
    logfp = open(logpath, "w")
    logfp.write("start the A market get data program at s\n")

    def __init__(self, parent=None):
        super(LogicWindow, self).__init__(parent)
        self.setupUi(self)
        self.setMenuData()
        self.setInitData()
        self.setInitData()
        self.setInitTabData()
        self.setTreeData()
        self.setInitTabGraph()


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
        self.dateEdit_Start.setDate(QDate.currentDate())
        self.dateEdit_End.setDate(QDate.currentDate())
        self.setCodeName()        

    def setCodeName(self):#use more time
        # self.lineEdit_StockCode.editingFinished.connect(self.editCodeFinished)
        self.lineEdit_StockCode.textChanged['QString'].connect(self.searchCodeChange)
        self.completerCodeEdit = QCompleter()
        # # 设置匹配模式  有三种： Qt.MatchStartsWith 开头匹配（默认）  Qt.MatchContains 内容匹配  Qt.MatchEndsWith 结尾匹配
        self.completerCodeEdit.setFilterMode(QtCore.Qt.MatchContains)
        # # 设置补全模式  有三种： QCompleter.PopupCompletion（默认）  QCompleter.InlineCompletion   QCompleter.UnfilteredPopupCompletion
        # self.completerCodeEdit.setCompletionMode(QCompleter.PopupCompletion)
        self.completerCodeListModel = QStringListModel()
        self.lineEdit_StockCode.setCompleter(self.completerCodeEdit)
        self.completerCodeEdit.setModel(self.completerCodeListModel)
        self.completerCodeEdit.activated['QString'].connect(self.completerCodeFunction)

    def completerCodeFunction(self, text):
        if len(text) >= 6:
            items = self.treeWidget.findItems(text, QtCore.Qt.MatchStartsWith  | QtCore.Qt.MatchRecursive)
            # self.treeWidget.collapseItem(self.treeWidget.topLevelItem(0))
            # self.treeWidget.expandItem(self.treeWidget.topLevelItem(0))
            self.treeWidget.collapseAll()
            self.treeWidget.setCurrentItem(items[0])

    def searchCodeChange(self, text):
        if text == '' or len(text) >= 6:
            pass
        else:
            if text.isdigit():
                items = self.treeWidget.findItems(text, QtCore.Qt.MatchStartsWith  | QtCore.Qt.MatchRecursive)
                itlen = len(items)
                if itlen == 0:
                    items = self.treeWidget.findItems(text, QtCore.Qt.MatchContains  | QtCore.Qt.MatchRecursive)
            else:
                items = self.treeWidget.findItems(text, QtCore.Qt.MatchContains  | QtCore.Qt.MatchRecursive)
            itlen = len(items)
            if itlen:
                setlist = []
                if itlen > 7:
                    itlen = 7
                for i in range(0, itlen):
                    setlist.append(items[i].text(0))
                # print(setlist)
                self.completerCodeListModel.setStringList(setlist)


    def setTreeData(self):#use more source
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
        # self.treeWidget.itemClicked['QTreeWidgetItem*','int'].connect(self.treeItemClick)
        self.treeWidget.currentItemChanged.connect(self.treeItemChange)

        self.WorkThread=QThread()
        self.Worker=WorkObject()
        self.Worker.moveToThread(self.WorkThread)
        self.WorkThread.started.connect(self.Worker.treeInitWorker)
        self.Worker.signal_Add.connect(self.treeItemAdd)
        self.WorkThread.start()

    def treeItemAdd(self, parenttype, childtype, name):
        if parenttype < 0:
            self.treeWidget.collapseAll()
            self.WorkThread.quit()
        else:
            if childtype < 0:
                UpParent = self.treeWidget.topLevelItem(parenttype)
                child = QTreeWidgetItem(UpParent)
                child.setText(0, name)
            else:
                UpParent = self.treeWidget.topLevelItem(parenttype).child(childtype)
                child = QTreeWidgetItem(UpParent)
                child.setText(0, name)

    def treeItemClick(self,item,n):
        print("this is item : " + item.text(n) + "num is : " + str(n))
        self.lineEdit_StockCode.setText(item.text(n))
    def treeItemChange(self,currentitem,preitem):
        # if preitem:
        #     print("pre item is : " + preitem.text(0) )
        # else:
        #     print("pre item is : none " )
        # print("current item is : " + currentitem.text(0) )
        self.lineEdit_StockCode.setText(currentitem.text(0))
        print(stock_GetLocalData(currentitem.text(0)))


    def setInitTabData(self):
        # prise data init
        self.pushButtonEralyClose.clicked.connect(self.ButtonEralyCloseCliked)
        self.pushButtonEralyClose.setStyleSheet(
                                "QPushButton{background-color:magenta}"  #按键背景色
                                "QPushButton{border-radius:6px}"  #圆角半径
                                )                                
        self.pushButtonOpen.clicked.connect(self.ButtonOpenCliked)
        self.pushButtonOpen.setStyleSheet("QPushButton{background-color:red}" "QPushButton{border-radius:6px}")
        self.pushButtonClose.clicked.connect(self.ButtonCloseCliked)
        self.pushButtonClose.setStyleSheet("QPushButton{background-color:green}" "QPushButton{border-radius:6px}")
        self.pushButtonHigh.clicked.connect(self.ButtonHighCliked)
        self.pushButtonHigh.setStyleSheet("QPushButton{background-color:blue}" "QPushButton{border-radius:6px}")
        self.pushButtonLow.clicked.connect(self.ButtonLowCliked)
        self.pushButtonLow.setStyleSheet("QPushButton{background-color:yellow}" "QPushButton{border-radius:6px}")

    def ButtonEralyCloseCliked(self):
        if self.pushButtonEralyClose.isChecked():
            self.pushButtonEralyClose.setStyleSheet("QPushButton{background-color:magenta}" "QPushButton{border-radius:6px}")
        else:
            self.pushButtonEralyClose.setStyleSheet("QPushButton{background-color:rgb(255,255,255)}" "QPushButton{border-radius:6px}")
        self.GraphWorker.graphShowBeforeLine(self.pushButtonEralyClose.isChecked())

    def ButtonOpenCliked(self):
        if self.pushButtonOpen.isChecked():
            self.pushButtonOpen.setStyleSheet("QPushButton{background-color:red}" "QPushButton{border-radius:6px}")
        else:
            self.pushButtonOpen.setStyleSheet("QPushButton{background-color:rgb(255,255,255)}" "QPushButton{border-radius:6px}")
        self.GraphWorker.graphShowOpenLine(self.pushButtonOpen.isChecked())

    def ButtonCloseCliked(self):
        if self.pushButtonClose.isChecked():
            self.pushButtonClose.setStyleSheet("QPushButton{background-color:green}" "QPushButton{border-radius:6px}")
        else:
            self.pushButtonClose.setStyleSheet("QPushButton{background-color:rgb(255,255,255)}" "QPushButton{border-radius:6px}")
        self.GraphWorker.graphShowCloseLine(self.pushButtonClose.isChecked())

    def ButtonHighCliked(self):
        if self.pushButtonHigh.isChecked():
            self.pushButtonHigh.setStyleSheet("QPushButton{background-color:blue}" "QPushButton{border-radius:6px}")
        else:
            self.pushButtonHigh.setStyleSheet("QPushButton{background-color:rgb(255,255,255)}" "QPushButton{border-radius:6px}")
        self.GraphWorker.graphShowHighLine(self.pushButtonHigh.isChecked())

    def ButtonLowCliked(self):
        if self.pushButtonLow.isChecked():
            self.pushButtonLow.setStyleSheet("QPushButton{background-color:yellow}" "QPushButton{border-radius:6px}")
        else:
            self.pushButtonLow.setStyleSheet("QPushButton{background-color:rgb(255,255,255)}" "QPushButton{border-radius:6px}")
        self.GraphWorker.graphShowLowLine(self.pushButtonLow.isChecked())
    
    
    def setInitTabGraph(self):
        self.lineEditDay.editingFinished.connect(self.editDayFinished)
        self.lineEditSpace.editingFinished.connect(self.editSpaceFinished)

        dpi = 100
        self.GraphThread=QThread()
        self.GraphWorker=StockGraph(width=self.tabStockData.width()/dpi+1, height=self.tabStockData.height()/dpi, dpi=dpi)
        self.GraphWorker.moveToThread(self.GraphThread)
        # self.GraphThread.started.connect(self.GraphWorker.graphInitWorker)
        # self.GraphWorker.signal_Add.connect(self.treeItemAdd)
        self.GraphThread.start()
        self.GraphWorker.graphInitPriceWorker()
        self.graphicScenePrice = QtWidgets.QGraphicsScene()
        self.graphicScenePrice.addWidget(self.GraphWorker)
        self.graphicsViewPrise.setScene(self.graphicScenePrice)
        self.graphicsViewPrise.show()

    def editDayFinished(self):
        pass
    def editSpaceFinished(self):
        pass

    def resizeEvent(self, QResizeEvent):
        # dpi = 100
        # StockGraphPrice = StockGraph(width=self.tabStockData.width()/dpi+1, height=self.tabStockData.height()/dpi, dpi=dpi)
        # # StockGraphPrice.test()
        # self.graphicScenePrice.addWidget(StockGraphPrice)
        # self.graphicsViewPrise.setScene(self.graphicScenePrice)
        # self.graphicsViewPrise.show()
        pass

if __name__ == "__main__": 
    app = QtWidgets.QApplication(sys.argv)
    logicWindow = LogicWindow()
    logicWindow.show()
    sys.exit(app.exec_())
