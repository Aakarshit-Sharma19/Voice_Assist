# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(732, 632)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.Status = QtWidgets.QLabel(self.centralwidget)
        self.Status.setObjectName("Status")
        self.gridLayout.addWidget(self.Status, 0, 0, 1, 1)
        self.layoutHistory = QtWidgets.QGridLayout()
        self.layoutHistory.setObjectName("layoutHistory")
        self.labelAssistant = QtWidgets.QLabel(self.centralwidget)
        self.labelAssistant.setObjectName("labelAssistant")
        self.layoutHistory.addWidget(self.labelAssistant, 0, 1, 1, 1)
        self.historyYou = QtWidgets.QTextBrowser(self.centralwidget)
        self.historyYou.setObjectName("historyYou")
        self.layoutHistory.addWidget(self.historyYou, 1, 2, 1, 1)
        self.labelYou = QtWidgets.QLabel(self.centralwidget)
        self.labelYou.setObjectName("labelYou")
        self.layoutHistory.addWidget(self.labelYou, 0, 2, 1, 1)
        self.historyAssistant = QtWidgets.QTextBrowser(self.centralwidget)
        self.historyAssistant.setObjectName("historyAssistant")
        self.layoutHistory.addWidget(self.historyAssistant, 1, 1, 1, 1)
        self.gridLayout.addLayout(self.layoutHistory, 1, 0, 1, 1)
        self.textInput = QtWidgets.QLineEdit(self.centralwidget)
        self.textInput.setObjectName("textInput")
        self.gridLayout.addWidget(self.textInput, 2, 0, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        spacerItem = QtWidgets.QSpacerItem(390, 27, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 0, 0, 1, 1)
        self.pushSpeak = QtWidgets.QPushButton(self.centralwidget)
        self.pushSpeak.setObjectName("pushSpeak")
        self.gridLayout_5.addWidget(self.pushSpeak, 0, 1, 1, 1)
        self.pushExit = QtWidgets.QPushButton(self.centralwidget)
        self.pushExit.setObjectName("pushExit")
        self.gridLayout_5.addWidget(self.pushExit, 0, 4, 1, 1)
        self.pushSwitch = QtWidgets.QPushButton(self.centralwidget)
        self.pushSwitch.setObjectName("pushSwitch")
        self.gridLayout_5.addWidget(self.pushSwitch, 0, 2, 1, 1)
        self.pushHelp = QtWidgets.QPushButton(self.centralwidget)
        self.pushHelp.setObjectName("pushHelp")
        self.gridLayout_5.addWidget(self.pushHelp, 0, 3, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_5, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Status.setText(_translate("MainWindow", "Welcome To Your Personal Assistant - Made By Aakarshit Sharma"))
        self.labelAssistant.setText(_translate("MainWindow", "Voice Assistant"))
        self.labelYou.setText(_translate("MainWindow", "You"))
        self.textInput.setText(_translate("MainWindow", "Enter Text if Voice Is Not Used"))
        self.pushSpeak.setText(_translate("MainWindow", "Speak"))
        self.pushExit.setText(_translate("MainWindow", "Exit"))
        self.pushSwitch.setText(_translate("MainWindow", "Switch To Text"))
        self.pushHelp.setText(_translate("MainWindow", "Help"))
