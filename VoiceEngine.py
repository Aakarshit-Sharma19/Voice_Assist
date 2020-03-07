# Made by Aakarshit Sharma
import urllib.request
from platform import system

import gtts
import speech_recognition as sr
from gtts import gTTS as Gt


def media_player(file):
    if system() == 'Windows':
        import winsound
        winsound.PlaySound(file, winsound.SND_FILENAME)

    else:
        from pydub import AudioSegment
        from pydub.playback import play
        sound = None
        if 'mp3' in file:
            sound = AudioSegment.from_mp3(file)
        elif 'wav' in file:
            sound = AudioSegment.from_wav(file)
        if sound:
            play(sound)


class TypeComm():
    def __init__(self):
        self.useVoice = True
        self.internet = True
        self.name = ''
        try:
            urllib.request.urlopen('https://www.google.com')  # Python 3.x
            self.internet = True
        except:
            self.internet = False

    def internet_active(self):
        self.internet = True

    def no_internet(self):
        self.switch_to_text()
        self.internet = False

    def switch_to_voice(self):
        if self.internet:
            self.useVoice = True

    def switch_to_text(self):
        self.useVoice = False

    def comm_status(self):
        return self.useVoice and self.internet

    def internet_status(self):
        return self.internet


class VoiceCore():
    def __init__(self, comms_object):
        self.file = "sounds/sound.mp3"
        self.comms_object = comms_object

    def speak(self):
        media_player(self.file)

    def synthesize_speech(self, string, speak=False):
        co = self.comms_object
        if co.comm_status():
            try:
                tts = Gt(string)
                tts.save(self.file)
                if speak:
                    self.speak()
                return True
            except gtts.tts.gTTSError:
                co.no_internet()
                return False

    def listen(self):
        return speech_to_text()


# Speech Recognition Initialization
r = sr.Recognizer()


def speech_to_text():
    try:
        with sr.Microphone() as source:
            print('Say something...')
            media_player('sounds/CortanaOpen.mp3')
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
            print('Processing your voice')
            media_player('sounds/CortanaClose.mp3')
        string = r.recognize_google(audio)
        return string
    except sr.UnknownValueError:
        return -1
    except sr.RequestError:
        return -2


if __name__ == '__main__':
    def test_sst():
        x = speech_to_text()
        print(x)
        return x


    VoiceCore(TypeComm()).synthesize_speech(test_sst(), True)
