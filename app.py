# Made by Aakarshit Sharma
import sys

from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen, QGridLayout, QMessageBox, QLabel
from PyQt5.QtWidgets import QLineEdit, QDialog, QPushButton

import ChatbotCore as cc
import Form
import VoiceEngine as VoiceEng

comms = VoiceEng.TypeComm()
voice = VoiceEng.VoiceCore(comms)
name = ''


class NameDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.resize(300, 100)
        self.grid = QGridLayout()
        self.lineEdit = QLineEdit()
        self.grid_layout = QGridLayout(self)
        self.grid_layout.addWidget(QLabel('<h2 style="font-family: sans-serif">'
                                          '<center>Welcome to the Voice Assisted Chatbot<center/><h2/>'))
        self.grid_layout.addWidget(
            QLabel('<center> Type in Your Name<center/>'))
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
            close_confirm.setInformativeText(
                'No name entered. Do you want to close the app')
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
    showed = pyqtSignal()

    def __init__(self):
        super().__init__(QPixmap('images/splash.png'))
        self.timer = QTimer(app)
        self.timer.setSingleShot(True)
        self.showMessage(
            f'<center style="font-family: sans-serif;"><h2>Welcome {name} to your voice assisted chatbot</h2><center/>',
            alignment=Qt.AlignHCenter, color=Qt.white)
        app.processEvents()

    def close(self):
        super().close()
        print('splash closed')
        MainWindow1.run()

    def show(self):
        super().show()
        self.showed.connect(self.initialize)
        app.processEvents()
        self.showed.emit()

    def initialize(self):
        print('Splash Showed')
        app.processEvents()

        def welcome_text():
            self.clearMessage()
            self.setPixmap(QPixmap('images/splash_text.png'))
            self.repaint()
            message = f'<h2>Welcome {name} to your voice assisted chatbot.</h2>\n'
            message += 'To Switch to Voice, internet n is needed'
            self.showMessage(message, Qt.AlignTop, color=Qt.white)
            self.timer.timeout.connect(self.close)
            self.timer.start(2000)
            comms.switch_to_text()
            # app.processEvents()
            print('TEXT ONLY MODE')

        def welcome_voice():
            if voice.synthesize_speech(f'Welcome {name} to your voice assisted chatbot'):
                voice.speak()
                self.close()
            else:
                welcome_text()

        if comms.comm_status():
            self.timer.timeout.connect(welcome_voice)
            self.timer.start(125)

        else:
            welcome_text()


# Main App

class MainWindow(QMainWindow):
    signal_append_user_history = pyqtSignal(str)
    signal_append_chatbot_history = pyqtSignal(str)
    signal_set_status = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ui = Form.Ui_MainWindow()
        self.ui.setupUi(self)

        self.core = cc.core(self, voice, name)
        self.open_url = lambda url: QDesktopServices.openUrl(
            QUrl(url, QUrl.TolerantMode))

        # self.ui.pushInput.clicked.connect(self.get_Input)

        # Connecting Signals
        self.ui.pushSwitchToText.clicked.connect(self.switch_comm)
        self.ui.pushHelp.clicked.connect(lambda: self.open_url("www.google.com"))
        self.ui.pushAbout.clicked.connect(lambda: self.open_url("https://github.com/Aakarshit-Sharma19/Voice_Assist"))
        self.ui.text_input.returnPressed.connect(self.accept_input)
        # The True Value only works if comm_status returns True thus listens only if returns voice input is set
        self.ui.pushAcceptInput.clicked.connect(lambda: self.accept_input(True))
        self.signal_append_user_history.connect(self.append_user_history)
        self.signal_append_chatbot_history.connect(self.append_chatbot_history)
        self.signal_set_status.connect(self.ui.status.setText)

        self.core.started.connect(self.pushAcceptInput_set_Stop_action)
        self.core.finished.connect(lambda: self.ui.pushAcceptInput.setText('Listen'))
        # Setting text_input to '' for using voice as the app only listens when ui.text_input is ''
        if not comms.comm_status():
            self.ui.text_input.setText('')

        self.input_string = ''

    def pushAcceptInput_set_Stop_action(self):
        self.ui.pushAcceptInput.setText('Stop')
        self.ui.pushAcceptInput.clicked.connect(self.core.quit)

    def pushAcceptInput_set_Default_action(self):
        self.ui.pushAcceptInput.setText('Listen')
        self.ui.pushAcceptInput.clicked.connect(lambda: self.accept_input(True))

    def append_chatbot_history(self, string):
        self.ui.history.append(
            "<h3>Chatbot said: {}</h3>  ".format(string))
        self.ui.history.setAlignment(Qt.AlignLeft)

    def append_user_history(self, string):
        self.ui.history.append(
            "<h3>You Said: {}</h3>".format(string))
        self.ui.history.setAlignment(Qt.AlignRight)

    def accept_input(self, is_listening=False):
        if comms.comm_status():
            if is_listening:
                self.core.start()
            else:
                self.input_string = self.ui.text_input.text()
                self.signal_append_user_history.emit(self.input_string)
                self.ui.text_input.setText('')

        elif not comms.comm_status():
            self.input_string = self.ui.text_input.text()
            self.signal_append_user_history.emit(self.input_string)
            self.ui.text_input.setText('')

        app.processEvents()
        self.core.process(self.input_string)

    def run(self):
        self.showMaximized()

    def switch_comm(self):
        if comms.comm_status():
            comms.switch_to_text()
            self.ui.pushSwitchToText.setText("Text -> Voice")
            self.ui.pushAcceptInput.setText('Enter')
        else:
            comms.switch_to_voice()
            self.ui.pushSwitchToText.setText("Voice -> Text")
            self.ui.pushAcceptInput.setText('Listen')
            self.ui.text_input.setText('')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Name_dialog = NameDialog()
    splash = Splash()
    MainWindow1 = MainWindow()
    splash.show()
    sys.exit(app.exec_())
