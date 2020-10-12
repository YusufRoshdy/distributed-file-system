# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'another_try.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.



from PyQt5.QtGui import QImage
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import *
from client import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(420, 150, 151, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(360, 250, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.get_input)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(360, 280, 131, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(420, 190, 361, 31))
        self.textEdit.setObjectName("textEdit")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(210, 350, 391, 192))
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 200, 371, 16))
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(380, 330, 55, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 160, 271, 16))
        self.label_4.setObjectName("label_4")
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(420, 80, 221, 31))
        self.textEdit_3.setObjectName("textEdit_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(40, 80, 181, 16))
        self.label_5.setObjectName("label_5")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(680, 80, 93, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.start)
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(170, 10, 461, 41))
        self.textBrowser_2.setObjectName("textBrowser_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Initialize"))
        self.comboBox.setItemText(1, _translate("MainWindow", "get_pool"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Read Directory"))
        self.comboBox.setItemText(3, _translate("MainWindow", "Change Directory"))
        self.comboBox.setItemText(4, _translate("MainWindow", "Make Directory"))
        self.comboBox.setItemText(5, _translate("MainWindow", "Remove Directory"))
        self.comboBox.setItemText(6, _translate("MainWindow", "Create File"))
        self.comboBox.setItemText(7, _translate("MainWindow", "Delete File"))
        self.comboBox.setItemText(8, _translate("MainWindow", "Copy FIle"))
        self.comboBox.setItemText(9, _translate("MainWindow", "Move FIle"))
        self.comboBox.setItemText(10, _translate("MainWindow", "Write File"))
        self.comboBox.setItemText(11, _translate("MainWindow", "Read File"))
        self.comboBox.setItemText(12, _translate("MainWindow", "Info"))
        self.pushButton.setText(_translate("MainWindow", "Submit"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label.setText(_translate("MainWindow", "Enter the File or Directory to accompany your selection above"))
        self.label_3.setText(_translate("MainWindow", "Output:"))
        self.label_4.setText(_translate("MainWindow", "Select the command you want to execute"))
        self.label_5.setText(_translate("MainWindow", "NameNode\'s ip and port"))
        self.pushButton_2.setText(_translate("MainWindow", "Start"))
        self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:20pt; font-weight:600; font-style:italic; text-decoration: underline; color:#aaff7f;\">INNOPOLIS FILE SYSTEM</span></p></body></html>"))



    def get_input(self):

        command=''

        if(str(self.comboBox.currentText())=='Initialize'):
            command = 'initialize'
        if (str(self.comboBox.currentText()) == 'Make directory'):
            command = 'mkdir'
        if (str(self.comboBox.currentText()) == 'Change Directory'):
            command = 'cd'
        if (str(self.comboBox.currentText()) == 'Remove Directory'):
            command = 'rmdir'
        if (str(self.comboBox.currentText()) == 'Read Directory'):
            command = 'ls'
        if (str(self.comboBox.currentText()) == 'Create File'):
            command = 'touch'
        if (str(self.comboBox.currentText()) == 'Read File'):
            command = 'get'
        if (str(self.comboBox.currentText()) == 'Remove File'):
            command = 'rm'
        if (str(self.comboBox.currentText()) == 'File Info'):
            command = 'info'
        if (str(self.comboBox.currentText()) == 'File Copy'):
            command = 'cp'
        if (str(self.comboBox.currentText()) == 'File Move'):
            command = 'mv'
        if (str(self.comboBox.currentText()) == 'Write File'):
            command = 'put'
        if (str(self.comboBox.currentText()) == 'get_pool'):
            command = 'get_pool'    

        addition_to_cmd = self.textEdit.toPlainText()
        func = getattr(self.client, command)
        final_cmd = command + " " + addition_to_cmd
        #print(final_cmd)
        Command = final_cmd
        func(final_cmd.split())


    def start(self):
        address = self.textEdit_3.toPlainText()
        #print(address)
        self.client = Client(address)

def print(*args, **kwargs):
    from builtins import print as native_print
    native_print(*args, **kwargs)

    ui.textBrowser.setText(*args)



if __name__ == "__main__":

    # cmd = input().split(' ')
    # func = getattr(client, cmd[0])
    # func(cmd)
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()

    sys.exit(app.exec_())