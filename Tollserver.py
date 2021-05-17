import socket
import errno
import ast
import datetime 
from socket import error as socket_error
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp, QDate, QTime, QDateTime, QTimer
from PyQt5.QtGui import QRegExpValidator, QIcon, QPixmap
from PyQt5.QtWidgets import QLineEdit,QMessageBox,QInputDialog, QFileDialog, QPushButton
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *
from PyQt5.QtWidgets import QMessageBox,QInputDialog, QFileDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QLabel, QPushButton, QDesktopWidget

from ui_Tollserver import *
#from client import getDAQReadings
from sqliteDB import *
from TcpServer20V import *


class E_toll_server(QMainWindow, Ui_MainWindow):
    
    def __init__(self, *args, **kwargs):
        super(E_toll_server, self).__init__(*args, **kwargs)
        self.setupUi(self)
        print("Toll-Data")
        self.addStyleSheet()
        #self.setBasicvalidations()
        self.connectSignalsToSlots()
        self.timerDaq = QTimer()
        self.timerDaq.setSingleShot(False)
        self.timerDaq.start(2*1000)
        self.readFromServer() 
        
    def addStyleSheet(self):
        sName = "Default"
        sHederColor = "#0080ff"
        sBodyColor = "#cdd6d9"
        sBackgroundColor = "#e9eaea"
        sBackImagePath = ""
        sTextColor = "black"
        sFont = "10"
        sTextStyle = "Arial"
        sTextBGColor = "#e9eaea"
        '''settingsList = getAppColorSettings()
        if len(settingsList) >=9:
            sName = settingsList[1]
            sHederColor = settingsList[2]
            sBodyColor = settingsList[3]
            sBackgroundColor = settingsList[4]
            sBackImagePath = settingsList[5]
            sTextColor = settingsList[6]
            sFont = settingsList[7]
            sTextStyle = settingsList[8]
            sTextBGColor = settingsList[9]'''
        
        styleSheet = '''QMenuBar,QToolBar{background: qlineargradient(x1:0,x2:0,y1:0,y2:1,stop:0 #cccccc, stop:0.4  #C0C0C0 );color:white;} 
QStatusBar{background: qlineargradient(x1:0,x2:0,y1:0,y2:1,stop:0 #cccccc, stop:0.4  #C0C0C0 );color:white;} 
QLineEdit{ background-color: '''+sTextBGColor+'''; padding: 1px; border-width: 5px;  border-color: beige;min-width: 120px; max-width: 190px;}
QComboBox{ background-color: '''+sTextBGColor+'''; padding: 1px; border-width: 1px;  border-color: beige;min-width: 120px;}
QMainWindow{background-color: '''+sBackgroundColor+''';} #widget_main{background-color:'''+sBodyColor+''';  border-radius: 5px;background-image:url('''+sBackImagePath+''')}
QPushButton{font: 10pt;background-color:;}
#widget_top{background-color:'''+sHederColor+''';  border-radius: 5px; border-style: outset;padding: 0px;}
QLabel{font:'''+sFont+'''pt '''+sTextStyle+''';color:'''+sTextColor+''';} QPushButton{font:'''+sFont+'''pt '''+sTextStyle+''';color:'''+sTextColor+''';} QLineEdit{font:'''+sFont+'''pt '''+sTextStyle+''';color:'''+sTextColor+''';} QCheckBox{font:'''+sFont+'''pt '''+sTextStyle+''';color:'''+sTextColor+''';} QComboBox{font:'''+sFont+'''pt '''+sTextStyle+''';color:'''+sTextColor+''';}'''
        self.setStyleSheet(styleSheet)
        
     
        
    def readFromServer(self):
        readings = str(getDAQReadings())
        tolldata = []    
        print("toll-info:", readings)
        self.displaydata(readings)
   
   
    def displaydata(self, tolls):
        print("toll-data:", tolls)
        Toll_Data = tolls
        
        #columnnames =['Vehiclenumber','Mobilenumber','Source','Destination',']
        self.tableWidget.setRowCount(len(tolls))
        if len(Toll_Data) > 0 :
            self.tableWidget.setColumnCount(2)
        else :
            self.tableWidget.setColumnCount(0)
        #self.tableWidget.setVerticalHeaderLabels(tolls)    
        #self.tableWidget.setHorizontalHeaderLabels(columnnames)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)       
        irow = icol = 0
        #rowposition = self.tableWidget.RowCount()
        #self.tableWidget.insertRow(rowposition)
        for row  in Toll_Data:
            icol = 0
            for record in row:
                sRecord = record
                print(sRecord)
                self.tableWidget.setItem(irow,icol, QTableWidgetItem(sRecord))
                icol = icol+1
            irow = irow+1  
   
    
    def connectSignalsToSlots(self):
        self.pushButton_submit.clicked.connect(self.on_click_start_button)
        self.pushButton_cancel.clicked.connect(self.on_click_cancel_button)
    
    
    
    def on_click_start_button(self):
        if self.tableWidget.rowCount != 0:
                    QMessageBox.information(None, 'Toll_Data', "Successful!")
                    
                    
    def on_click_cancel_button(self):
        self.close()
    
        
if __name__ == "__main__":
    import sys
    app = QApplication([])
    window = E_toll_server()
    window.show()
    app.exec_()
