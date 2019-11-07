import sys
import webbrowser
import Threads
import speech_recognition_assistance as spa
import VoiceAssistantDriver as va
import ui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLineEdit, QDialog, QPushButton
from PyQt5 import QtCore
import time

name = ''


class NameDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(300, 100)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(25, 0, 250, 30)
        self.lineEdit.setText('Type in Your Name')
        self.button = QPushButton(self)
        self.button.setText('Confirm')
        self.button.setGeometry(25, 40, 250, 30)
        self.lineEdit.returnPressed.connect(self.pressed)
        self.button.clicked.connect(self.pressed)
        self.name = ''
        self.exec_()

    def pressed(self):
        self.name = self.lineEdit.text()
        self.close()


class MainWindow(QMainWindow):

    def __init__(self, comms_means, pVoice):
        super().__init__()

        self.comms = comms_means
        self.setWindowTitle('Voice Assistant - Made By Aakarshit Sharma')
        self.nameDialog = NameDialog()
        self.comms.name = self.nameDialog.name
        self.welcome = f'Welcome {self.nameDialog.name} to your Voice'
        self.welcome += ' Assistant.'
        self.voice = pVoice
        self.spa = spa
        self.ui = ui.Ui_MainWindow()
        self.GuiFunc = Threads.GuiFunctions(self)
        self.VFunc = Threads.VoiceFunctions(self)
        self.threadWelcome = Threads.threadWelcome(self)
        self.threadTempStatus = Threads.threadTempStatus(self)
        self.threadMain = Threads.threadMain(self)
        self.init_ui()

        self.status_temp_running = False

    def init_ui(self):
        self.ui.setupUi(self)
        self.ui.Status.setText(self.welcome)
        self.ui.pushExit.clicked.connect(sys.exit)
        self.ui.pushHelp.clicked.connect(self.run_help)
        self.ui.pushSpeak.clicked.connect(self.threadMain.start)

        self.VFunc.signalSetStatus.connect(self.GuiFunc.setStatus)
        self.VFunc.signalTempStatus.connect(self.GuiFunc.setTempStatus)
        self.VFunc.signalAppendAssistHistory.connect(self.GuiFunc.appendAssistHistory)
        self.VFunc.signalAppendUserHistory.connect(self.GuiFunc.appendUserHistory)
        self.VFunc.signalDefaultStatus.connect(self.GuiFunc.setDefaultStatus)

        self.threadWelcome.finished.connect(self.threadMain.start)

        self.threadTempStatus.signalDefaultStatus.connect(self.GuiFunc.setDefaultStatus)

    def run_help(self):
        webbrowser.open('www.github.com/Aakarshit-Sharma19/Voice_Assist')
        self.GuiFunc.setTempStatus('Opened Help', 2000)

    def run_welcome(self):
        string = self.GuiFunc.getStatus() + ' How may I help you?'
        self.threadWelcome.setString(string)
        self.threadWelcome.start()
        time.sleep(1)
        self.GuiFunc.setTempStatus(string + ' (Initializing)', 10000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    comms = va.comms()
    voice = va.voicesynthesizer()
    MainWindow1 = MainWindow(comms, voice)
    MainWindow1.showNormal()
    MainWindow1.run_welcome()
    sys.exit(app.exec_())
