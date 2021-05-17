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

from ui_application import *
#from client import getDAQReadings
from sqliteDB import *
from TSS_Basic_Widgets import *


class E_toll_application(QMainWindow, Ui_Application):
    Reg_Details = pyqtSignal(str, str, str, str)
    def __init__(self, *args, **kwargs):
        super(E_toll_application, self).__init__(*args, **kwargs)
        
        self.setupUi(self)
        #print("Start_Test")
        self.Reg_Details.connect(self.display_data)
        self.addStyleSheet()
        self.buttons = [self.radioButton_Gpay,self.radioButton_paytm,self.radioButton_phonepay]
        #self.setBasicvalidations()
        #self.connectSignalsToSlots()
        self.center()
        
        
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
        

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        
        
        
    def connectSignalsToSlots(self, Start, Destination, vehicle_number,mobile_number,tolls):
         
         self.pushButton_Submit.clicked.connect(lambda:self.on_click_start_button(Start, Destination, vehicle_number,mobile_number,tolls))
         self.pushButton_Cancel.clicked.connect(self.on_click_cancel_button)
             
        
    
    def display_data(self, Start, Destination, vehicle_number,mobile_number):
        
        self.lineEdit_StartFrom.setText(Start)
        self.lineEdit_Dest.setText(Destination)
        
        Toll_Details = get_tolldetails(Start, Destination) 
        value = str(Toll_Details).strip('[]')
        translation = {39: None} 
        data =  str(value).translate(translation)
        tolls = list(data.split(","))       
        Toll_way = []  
        for num in range(len(tolls)):
            Toll_way.append('oneway')
            Toll_way.append('twoway')
        displayCheck_box(self, 2*len(tolls), Toll_way)
        sRecord = ""
        Toll_Data = get_tollprice(tolls)
        columnnames =['oneway', 'twoway']
        self.tableWidget.setRowCount(len(tolls))
        if len(Toll_Data) > 0 :
            self.tableWidget.setColumnCount(2)
        else :
            self.tableWidget.setColumnCount(0)
        self.tableWidget.setVerticalHeaderLabels(tolls)    
        self.tableWidget.setHorizontalHeaderLabels(columnnames)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)       
        irow = icol = 0
        #rowposition = self.tableWidget.RowCount()
        #self.tableWidget.insertRow(rowposition)
        for row  in Toll_Data:
            #icol = 0
            #for record in row:
            sRecord = row
            #print(sRecord)
            self.tableWidget.setItem(irow,icol, QTableWidgetItem(sRecord))
            icol = icol+1
        irow = irow+1
        #print("toll_price:", Toll_Data)
        self.connectSignalsToSlots(Start, Destination, vehicle_number,mobile_number,tolls)
        
        
    def on_click_start_button(self, Start, Destination, vehicle_number,mobile_number,tolls):
        vehicle_number = vehicle_number+","
        mobile_number = mobile_number+","
        Start = Start+","
        Destination= Destination+","
        data =""
        HOST ='127.0.0.1'
        PORT =1993
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, PORT))
                s.sendall(bytes((vehicle_number).encode('utf8')))
                s.sendall(bytes((mobile_number).encode('utf8')))
                s.sendall(bytes((Start).encode('utf8')))
                s.sendall(bytes((Destination).encode('utf8')))
                for i, v in enumerate(self.Checkbox):
                    if v.checkState() == 2:
                        name = []
                        name = tolls[i]
                        print("name:", name)
                        value = v.text()
                        data = name+value+","
                        print("toll-name:", data)
                        s.sendall(bytes((data).encode('utf8')))
                        #print(v.text())
                #s.settimeout(5.0)
                for i, v in enumerate(self.buttons):
                    if v.isChecked() == True:
                        s.sendall(bytes((v.text()).encode('utf8')))
                data = s.recv(1024)
                s.settimeout(None)
            except socket_error as serr:
                print ("socket error: {}".format(serr))
                data = "Error"
            print('Received', repr(data))
        s.close()
        
        
    def on_click_cancel_button(self):
        self.close()    
        
        
        
if __name__ == "__main__":
    import sys
    app = QApplication([])
    window = E_toll_application()
    window.show()
    app.exec_()
        

