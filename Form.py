# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(732, 623)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.history = QtWidgets.QTextBrowser(self.centralwidget)
        self.history.setObjectName("history")
        self.gridLayout.addWidget(self.history, 1, 0, 1, 1)
        self.text_input = QtWidgets.QLineEdit(self.centralwidget)
        self.text_input.setObjectName("text_input")
        self.gridLayout.addWidget(self.text_input, 2, 0, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.pushHelp = QtWidgets.QPushButton(self.centralwidget)
        self.pushHelp.setObjectName("pushHelp")
        self.gridLayout_5.addWidget(self.pushHelp, 0, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(390, 27, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 0, 1, 1, 1)
        self.pushAcceptInput = QtWidgets.QPushButton(self.centralwidget)
        self.pushAcceptInput.setObjectName("pushAcceptInput")
        self.gridLayout_5.addWidget(self.pushAcceptInput, 0, 2, 1, 1)
        self.pushAbout = QtWidgets.QPushButton(self.centralwidget)
        self.pushAbout.setObjectName("pushAbout")
        self.gridLayout_5.addWidget(self.pushAbout, 0, 5, 1, 1)
        self.pushSwitchToText = QtWidgets.QPushButton(self.centralwidget)
        self.pushSwitchToText.setObjectName("pushSwitchToText")
        self.gridLayout_5.addWidget(self.pushSwitchToText, 0, 3, 1, 1)
        self.status = QtWidgets.QLabel(self.centralwidget)
        self.status.setMinimumSize(QtCore.QSize(200, 0))
        self.status.setText("")
        self.status.setObjectName("status")
        self.gridLayout_5.addWidget(self.status, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_5, 3, 0, 1, 1)
        self.layoutHistory = QtWidgets.QGridLayout()
        self.layoutHistory.setObjectName("layoutHistory")
        self.labelAssistant = QtWidgets.QLabel(self.centralwidget)
        self.labelAssistant.setMinimumSize(QtCore.QSize(0, 0))
        self.labelAssistant.setObjectName("labelAssistant")
        self.layoutHistory.addWidget(self.labelAssistant, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.layoutHistory, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.text_input.setText(_translate("MainWindow", "Type In what you want to say"))
        self.pushHelp.setText(_translate("MainWindow", "Help"))
        self.pushAcceptInput.setText(_translate("MainWindow", "Listen"))
        self.pushAbout.setText(_translate("MainWindow", "About"))
        self.pushSwitchToText.setText(_translate("MainWindow", "Switch To Text"))
        self.labelAssistant.setText(_translate("MainWindow",
                                               "<center style=\"font-family: sans-serif; font-size: large;\"><strong>Voice Assistant<strong/><center/>\n"
                                               ""))
