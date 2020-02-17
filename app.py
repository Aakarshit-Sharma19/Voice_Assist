# Made by Aakarshit Sharma
import sys
import time
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen, QGridLayout, QMessageBox, QLabel
from PyQt5.QtWidgets import QLineEdit, QDialog, QPushButton

import TTSEngine as Tts
import ui

voice = Tts.VoiceSynth()
comms = Tts.comms()
name = ''


class NameDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.resize(300, 100)
        self.grid = QGridLayout()
        self.lineEdit = QLineEdit()
        self.grid_layout = QGridLayout(self)
        self.grid_layout.addWidget(QLabel('Type in Your Name'))
        self.grid_layout.addWidget(self.lineEdit)
        self.button_use_text = QPushButton()
        self.button_use_voice = QPushButton()
        self.grid_layout.addWidget(self.button_use_text)
        self.grid_layout.addWidget(self.button_use_voice)
        self.button_use_text.setText('Continue with text')
        self.button_use_voice.setText('Continue with voice')
        self.lineEdit.returnPressed.connect(self.button_use_voice.click)
        self.button_use_text.clicked.connect(lambda: self.pressed(False))
        self.button_use_voice.clicked.connect(lambda: self.pressed(True))

        self.exec_()

    def accept(self):
        if self.lineEdit.text() == '':
            self.reject(True)
        else:
            super().accept()

    def reject(self, no_input=False):
        close_confirm = QMessageBox()
        if no_input:
            close_confirm.setInformativeText('No name entered. Do you want to close the app')
        else:
            close_confirm.setInformativeText('Do You want to close the app')
        close_confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        close_confirm.setDefaultButton(QMessageBox.No)
        ret = close_confirm.exec_()
        if ret == QMessageBox.Yes:
            super().reject()
            app.exit(0)
            sys.exit()

    def pressed(self, use_voice):
        global comms
        global name
        self.accept()
        name = self.lineEdit.text()
        if use_voice:
            comms.switch_to_voice()
        else:
            comms.switch_to_text()


class Splash(QSplashScreen):
    closed = pyqtSignal()

    def __init__(self):
        super().__init__(QPixmap('images/splash.png'))
        self.showMessage(f'Welcome {name} to your voice assisted chatbot', alignment=5, color=QColor(255, 255, 255))

    def close(self):
        super().close()
        self.closed.emit()

    def initialize(self):
        self.show()
        print('Splash Showed')
        app.processEvents()
        if voice.synth_speech(comms, f'Welcome {name} to your voice assisted chatbot') and comms.comm_status():
            voice.speak()
            self.close()
        else:
            self.clearMessage()
            message = f'Welcome {name} to your voice assisted chatbot.\n'
            message += ' TEXT ONLY MODE\nTip: To Switch to Voice, internet connection is needed'
            self.showMessage(message, alignment=5, color=QColor(255, 255, 255))
            app.processEvents()
            timer = QTimer(app)
            timer.timeout.connect(self.close)
            timer.setSingleShot(True)
            timer.start(2000)

            comms.switch_to_text()
            # app.processEvents()
            print('TEXT ONLY MODE')
        print('Splash Closed')


class MainWindow(QMainWindow):
    signal_listen = pyqtSignal()
    # signal_switch_to_text = pyqtSignal()
    # signal_switch_to_voice = pyqtSignal()
    signal_entered_text = pyqtSignal()

    def append_chatbot_history(self, string):
        self.ui.history.append('Chatbot said: {}'.format(string))

    def append_user_history(self, string):
        self.ui.history.append('You Said: {}'.format(string))

    def __init__(self):
        super().__init__()
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushInput.clicked.connect(self.get_Input)
        self.ui.pushSwitchToText.clicked.connect(MainWindow.switch_comm)

    # def get_Input(self):
        # if comms.comm_status:


    @staticmethod
    def switch_comm():
        if comms.comm_status():
            comms.switch_to_text()
        else:
            comms.switch_to_voice()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setColorSpec(255)
    Name_dialog = NameDialog()
    splash = Splash()
    splash.initialize()
    MainWindow1 = MainWindow()
    splash.closed.connect(MainWindow1.showMaximized)
    sys.exit(app.exec_())

# class MainWindow(QMainWindow):
#
#     def __init__(self, comms_means, pVoice):
#         super().__init__()
#
#         self.comms = comms_means
#         self.setWindowTitle('Voice Assistant - Made By Aakarshit Sharma')
#         self.nameDialog = NameDialog()
#         self.comms.name = self.nameDialog.name
#         self.welcome = f'Welcome {self.nameDialog.name} to your Voice'
#         self.welcome += ' Assistant.'
#         self.voice = pVoice
#         self.spa = spa
#         self.ui = ui.Ui_MainWindow()
#         self.GuiFunc = Threads.GuiFunctions(self)
#         self.VFunc = Threads.VoiceFunctions(self)
#         self.threadWelcome = Threads.threadWelcome(self)
#         self.threadTempStatus = Threads.threadTempStatus(self)
#         self.threadMain = Threads.threadMain(self)
#         self.init_ui()
#
#         self.status_temp_running = False
#
#     def init_ui(self):
#         self.ui.setupUi(self)
#         self.ui.Status.setText(self.welcome)
#         self.ui.pushExit.clicked.connect(sys.exit)
#         self.ui.pushHelp.clicked.connect(self.run_help)
#         self.ui.pushSpeak.clicked.connect(self.threadMain.start)
#
#         self.VFunc.signalSetStatus.connect(self.GuiFunc.setStatus)
#         self.VFunc.signalTempStatus.connect(self.GuiFunc.setTempStatus)
#         self.VFunc.signalAppendAssistHistory.connect(self.GuiFunc.appendAssistHistory)
#         self.VFunc.signalAppendUserHistory.connect(self.GuiFunc.appendUserHistory)
#         self.VFunc.signalDefaultStatus.connect(self.GuiFunc.setDefaultStatus)
#
#         self.threadWelcome.finished.connect(self.threadMain.start)
#
#         self.threadTempStatus.signalDefaultStatus.connect(self.GuiFunc.setDefaultStatus)
#
#     def run_help(self):
#         webbrowser.open('www.github.com/Aakarshit-Sharma19/Voice_Assist')
#         self.GuiFunc.setTempStatus('Opened Help', 2000)
#
#     def run_welcome(self):
#         string = self.GuiFunc.getStatus() + ' How may I help you?'
#         self.threadWelcome.setString(string)
#         self.threadWelcome.start()
#         time.sleep(1)
#         self.GuiFunc.setTempStatus(string + ' (Initializing)', 10000)
