from PyQt5 import QtCore


class threadWelcome(QtCore.QThread):
    signalSpeak = QtCore.pyqtSignal(str)
    signalStatus = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)
        self.parent = parent
        self.voice = parent.voice

    def speak(self, string):
        self.voice.speak(self.parent.comms, string)
        self.signalSpeak.emit(string)

    def setString(self, string):
        self.string = string

    def run(self):
        # self.commands = command_list()
        self.speak(self.string)


class threadTempStatus(QtCore.QThread):
    signalsetStatus = QtCore.pyqtSignal(str)
    signalstartTimer = QtCore.pyqtSignal(int)

    def __init__(self, parent, interval=1000):
        QtCore.QThread.__init__(self, parent)
        self.parent = parent
        self.interval = interval

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(
            lambda: self.signalsetStatus.emit('Personal Voice Assistant'))
        self.signalstartTimer.connect(self.timer.start)

    def setString(self, string):
        self.string = string

    def setDuration(self, interval):
        self.interval = interval

    def tempStatus(self):
        self.start()

    def run(self):
        # print(self.interval)
        self.tempStatus()
        self.signalsetStatus.emit(self.string)
        # self.timer.moveToThread(self)
        self.signalstartTimer.emit(self.interval)

