# Made by Aakarshit Sharma
from PyQt5 import QtCore
import sys
import webbrowser

class GuiFunctions:

    def __init__(self, parent):
        self.parent = parent
        self.comms = parent.comms

    def StatusTempRunning(self):
        return self.parent.status_temp_running

    def setStatus(self, string):
        self.parent.ui.Status.setText(string)

    def getStatus(self):
        if self.StatusTempRunning() == False:
            return self.parent.ui.Status.text()

    def setDefaultStatus(self):
        self.setStatus('Personal Voice Assistant')

    def setTempStatus(self, string='', interval=-1):
        self.parent.threadTempStatus.setParam(string, interval)
        if self.parent.threadTempStatus.isRunning() is False:
            self.parent.threadTempStatus.quit()
        self.parent.threadTempStatus.start()

    def appendAssistHistory(self, string):
        self.parent.ui.historyAssistant.append(string)

    def appendUserHistory(self, string):
        self.parent.ui.historyYou.append(string)


class VoiceFunctions(QtCore.QObject):
    signalSetStatus = QtCore.pyqtSignal(str)
    signalAppendAssistHistory = QtCore.pyqtSignal(str)
    signalAppendUserHistory = QtCore.pyqtSignal(str)
    signalTempStatus = QtCore.pyqtSignal(str, int)
    signalDefaultStatus = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.comms = self.parent.comms
        self.spa = self.parent.spa
        self.voice = self.parent.voice
        self.said_text = None

    def speak(self, string):
        self.signalSetStatus.emit('Voice Assistant:' + string)
        status = self.parent.voice.speaks(self.comms, string)
        self.signalDefaultStatus.emit()
        if status == -1:
            self.signalTempStatus.emit(
                'No Internet! Only text based Assistance is Available', 3000)
        self.signalDefaultStatus.emit()
        self.signalAppendAssistHistory.emit(string)

    def listen(self):

        self.signalSetStatus.emit('Listening')
        self.spa.mic(self.voice.playfile)
        self.said_text = self.spa.speech_synth()
        if self.said_text is not None:
            self.signalAppendUserHistory.emit(self.said_text)
        else:
            self.signalTempStatus.emit('No internet available, Only Text Input Available.', 2000)
            self.comms.noInternet()
        return self.said_text


class threadWelcome(QtCore.QThread):

    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)
        self.parent = parent
        self.voice = self.parent.voice
        self.guiFunctions = self.parent.GuiFunc
        self.speak = self.parent.VFunc.speak

    def setString(self, string):
        self.string = string

    def run(self):
        print('Welcome to Voice Assistant')
        self.speak(self.string)


class threadTempStatus(QtCore.QThread):
    signalstartTimer = QtCore.pyqtSignal(int)
    signalDefaultStatus = QtCore.pyqtSignal()

    def __init__(self, parent, interval=1000):
        QtCore.QThread.__init__(self, parent)
        self.parent = parent
        self.interval = interval
        self.setStatus = self.parent.GuiFunc.setStatus
        self.string = ''

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(
            self.defaultstausfortemp)
        self.signalstartTimer.connect(self.timer.start)

    def setParam(self, string='', interval=-1):
        if string != '':
            self.string = string
        if interval != -1:
            self.interval = interval

    def setDuration(self, interval):
        self.interval = interval

    def defaultstausfortemp(self):
        self.parent.status_temp_running = False
        self.signalDefaultStatus.emit()

    def tempStatus(self):
        self.start()

    def run(self):
        # print(self.interval)
        # self.tempStatus()
        self.setStatus(self.string)
        self.parent.status_temp_running = True
        # self.timer.moveToThread(self)
        self.signalstartTimer.emit(self.interval)


class threadMain(QtCore.QThread):

    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)
        self.parent = parent
        self.listen = self.parent.VFunc.listen
        self.speak = self.parent.VFunc.speak

        self.replies = {
            'NAME': f'{self.parent.comms.name}',
            'BARK': 'Dog barks',
            'HELLO': f' Hi {self.parent.comms.name}',
        }
        self.functions = {
            # 'SEARCH': self.search,
            'BYE': self.bye
        }

    def bye(self):
        self.speak('bye' + self.replies['NAME'] + '!')
        self.parent.thread
        sys.exit(0)

    def run(self):
        print('Main running')
        while True:
            self.said_text = self.listen()
            print(self.said_text)
            if self.said_text is None:
                self.speak("Didn't get a voice!")
                continue

            self.said_text = self.said_text.upper()
            command = self.said_text.split()
            reply = self.replies.get(command[0])
            task = self.functions.get(command[0])
            if command[0] == 'SWITCH':
                if self.said_text == 'SWITCH TO TEXT':
                    self.speak('SWITCHING TO TEXT!')
                    self.parent.comms.switchToText()
                else:
                    self.speak('switch to what?')
            elif reply is None and task is None:
                webbrowser.open("https://google.com/search?q=%s" % self.said_text)
                self.speak('Searching on Google')
                # self.speak("Didn't Catch That! What can i do for you?")
                # continue
            elif reply is not None:
                self.speak(reply)

            elif task is not None:
                task()
