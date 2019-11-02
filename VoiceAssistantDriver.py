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


class voicesynthesizer(object):
    def __init__(self):
        self.file = "sound.mp3"

    def playfile(self, file):
        self.play = vlc.MediaPlayer(file)
        self.play.set_rate(1.25)
        self.play.play()
        sleep(1.2)
        self.duration = self.play.get_length() / 1000
        sleep(self.duration)

    def speak(self, co, string):
        if co.internet:
            try:
                tts = gt(string)
                tts.save(self.file)
                self.playfile(self.file)
            except(gtts.tts.gTTSError):
                co.noInternet()
                print('\n\nInternet Connection Error.')
                print('Only text operations are available\n')





if __name__ == "__main__":
    # Program Start
    welcome = '\n\n\n\n***********************WELCOME'
    welcome += '***************************\n\n\n'
    print(welcome)

    co = comms()

    name = input("Please Enter Your Name: ")
    
    lang = 'en'
    main()
