import sys
import webbrowser
import Threads
import speech_recognition_assistance as spa
import VoiceAssistantDriver as va
import ui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLineEdit, QDialog, QPushButton
from PyQt5 import QtCore


name = ''


class nameDialog(QDialog):
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


class command_list:
    def __init__(self):
        self.intr = {
            'NAME': f'{name}',
            'BARK': 'Dog barks',
            'HELLO': f' Hi {name}',
        }
        self.func = {
            'BYE': exit
        }


class MainWindow(QMainWindow):
    def __init__(self, comms_means, voice):
        super().__init__()
        self.comms = comms_means
        self.setWindowTitle('Voice Assistant - Made By Aakarshit Sharma')
        self.nameDialog = nameDialog()
        self.comms.name = self.nameDialog.name
        self.welcome = f'Welcome {self.nameDialog.name} to your Voice'
        self.welcome += ' Assistant.'
        self.voice = voice
        self.initUI()

    def initUI(self):
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Status.setText(self.welcome)
        self.ui.pushExit.clicked.connect(sys.exit)
        self.ui.pushHelp.clicked.connect(self.run_help)

        self.threadWelcome = Threads.threadWelcome(self)
        self.threadWelcome.signalSpeak.connect(self.appendAssistHistory)

        self.threadTempStatus = Threads.threadTempStatus(self)
        self.threadTempStatus.signalsetStatus.connect(self.setStatus)

    def setStatus(self, string):
        self.ui.Status.setText(string)

    def getStatus(self):
        return self.ui.Status.text()

    def speak(self, comms, string):
        self.tempStatus('Speaking', 500)
        self.voice.speak(comms, string)
        self.appendAssistHistory(string)

    def appendAssistHistory(self, string):
        self.ui.historyAssistant.append(string)

    def appendYourHistory(self, string):
        self.ui.historyYou.append(string)

    def run_help(self):
        webbrowser.open('www.github.com/Aakarshit-Sharma19/Voice_Assist')
        self.tempStatus('Opened Help')

    def run_welcome(self):
        string = self.getStatus()+' How may I help you?'
        self.threadWelcome.setString(string)
        self.threadTempStatus.setString(string)
        self.threadTempStatus.setDuration(5000)
        self.threadWelcome.start()
        self.threadTempStatus.start()


def INPUT(co, text):
    if co.internet:
        return spa.listen()


# def main(main):
#     '''The Main Function'''
#     thread = QtCore.QThread(MainWindow1)
#     thread.start()
#     # commands = command_list()

#     # main.speak(comms, main.getStatus()+' How may I help you?')
#     # while True:
#     #     said_text = spa.listen()
#     #     if said_text is None:
#     #         voice.speak("No valid input detected")
#     #         continue
#     #     said_text = said_text.upper()
#     #     command = said_text.split()
#     #     print('****************', 'You said', str(command))
#     #     reply = intr.get(command[0])
#     #     task = func.get(command[0])

#     #     if command[0] == 'SWITCH':
#     #         if said_text == 'SWITCH TO TEXT':
#     #             speak('SWITCHING TO TEXT!')
#     #             co.internet = 2
#     #             co.comms_means = 2
#     #         else:
#     #             speak('switch to what?')

#     #     elif reply is None and task is None:
#     #         speak("Didn't Catch That")
#     #         continue

#     #     elif reply is not None:
#     #         speak(reply)

#     #     elif task is not None:
#     #         task()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    comms = va.comms()
    voice = va.voicesynthesizer()
    MainWindow1 = MainWindow(comms, voice)
    MainWindow1.showNormal()
    MainWindow1.run_welcome()
    sys.exit(app.exec_())
    # main(MainWindow1)


# class Thread(QtCore.QThread):
#     signal = QtCore.pyqtSignal(str)
#     signal2 = QtCore.pyqtSignal(list)
#     def __init__(self, parent=None):
#         QtCore.QThread.__init__(self, parent)

#     def run(self):
#         self.signal.emit("start")
#         for i in range(0, 1000000000):
#             pass
#         self.signal.emit("finish")
#         self.signal2.emit([1, 2, 3, 4])

# class Child_Form(QtWidgets.QWidget):
#     def __init__(self, Parent_Form):
#         [...]
#     def busyFunc(self):
#         self.thread = Thread(self)
#         self.thread.signal.connect(lambda text: self.textEdit.append(text))
#         self.thread.signal2.connect(lambda l: print(l))
#         self.thread.start()

# class Parent_Form(QtWidgets.QWidget):
#     def __init__(self):
#         [...]
#     def openChild(self):
#         self.hide()
#         self.Child.show()
#         self.Child.busyFunc()
