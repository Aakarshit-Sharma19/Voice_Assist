# Made by Aakarshit Sharma
from time import sleep
import gtts
from gtts import gTTS as Gt
from speech_recognizer import mediaplayer


class comms(object):
    def __init__(self):
        self.useVoice = True
        self.internet = True
        self.name = ''

    def internet_active(self):
        self.internet = True

    def no_internet(self):
        self.switch_to_text()
        self.internet = False

    def switch_to_voice(self):
        if self.internet == True:
            self.useVoice = True

    def switch_to_text(self):
        self.useVoice = False

    def comm_status(self):
        return self.useVoice and self.internet


class VoiceSynth(object):
    def __init__(self):
        self.file = "sounds/sound.mp3"
        self.play = None
        self.duration = 0.0

    def speak(self):
        mediaplayer(self.file)

    def synth_speech(self, co, string):
        if co.comm_status():
            try:
                tts = Gt(string)
                tts.save(self.file)
                return True
            except gtts.tts.gTTSError:
                co.no_internet()
                return False


if __name__ == '__main__':
    co = comms()
    co.name = 'Aakarshit Sharma'
    voice_synthesizer = VoiceSynth()
    voice_synthesizer.synth_speech(co, co.name)
