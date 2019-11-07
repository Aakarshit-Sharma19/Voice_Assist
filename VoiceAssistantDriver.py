# Made by Aakarshit Sharma
from time import sleep
import gtts
from gtts import gTTS as gt
import vlc


class comms(object):
    def __init__(self):
        self.useVoice = True
        self.internet = True
        self.name = ''

    def noInternet(self):
        self.switchToText()

    def switchToText(self):
        self.useVoice = False
        self.internet = False

    def commsStatus(self):
        if self.useVoice and self.internet:
            return True
        else:
            return False


class voicesynthesizer(object):
    def __init__(self):
        self.file = "sound.mp3"
        self.play = None
        self.duration = 0.0

    def playfile(self, file):
        self.play = vlc.MediaPlayer(file)
        self.play.set_rate(1.25)
        self.play.play()
        sleep(1.2)
        self.duration = self.play.get_length() / 1000
        sleep(self.duration)

    def speaks(self, co, string):
        if co.commsStatus():
            try:
                tts = gt(string)
                tts.save(self.file)
                self.playfile(self.file)
                return None
            except gtts.tts.gTTSError:
                co.noInternet()
                return -1
