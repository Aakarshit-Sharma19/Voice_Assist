# Created By Aakarshit Sharma
from time import sleep
from gtts import gTTS as gt
import speech_recognition_assistance as spa
from weather import Weather, Unit
import vlc


class functions:
    def pronounce(self):
        if co.comms_means != 1:
            co.internet = 1
            txt = input("Enter what you want to speak >")
            speak(txt)
            co.internet = 2
        else:
            speak('Sorry, but Voice Recognition is On. No Text Input Available')




class comms(object):
    def __init__(self):
        self.comms_means = int(
            input('For Voice communication press 1 else type any other number for text\n'))
        self.internet = self.comms_means




#Program Start
welcome = '\n\n\n\n***********************WELCOME***************************\n\n\n'
print(welcome)

co = comms()


name = input("Please Enter Your Name: ")
file = "sound.mp3"
lang = 'en'
# lang = input("Select Your Language (en,hi):")


def INPUT(text):
    if co.internet == 1:
        return spa.main_func()
    else:
        return input(text)


def init():
    if lang == 'en':
        lang_speak = f'Welcome {name} to your personal voice assistant.\nHow may i help you {name}'
    elif lang == 'hi':
        lang_speak = f'आवाज सहायक में आपका स्वागत है।मैं आपकी मदद कैसे कर सकती हूं {name} जी'
    begin(lang_speak)


def begin(string):
    print("Initializing\n")
    speak(string)


def speak(string):
    print('****************', string)
    if co.internet is 1:
        try:
            tts = gt(string)
            tts.save(file)
            play = vlc.MediaPlayer(file)
            play.play()
            sleep(0.8)
            duration = play.get_length() / 1000
            sleep(duration)
            print(duration)
        except:
            comms_means = 2
            co.internet = 2
            print('\n\nInternet Connection Error.\nOnly text assistance is available\n')


def main():
    '''The Main Function'''
    init()
    f = functions()
    intr = {
        'NAME': f'{name}',
        'BARK': 'Dog barks',
        'HELLO': f' Hi {name}',
    }
    func = {
        'EXIT': exit,
        'SPEAK': f.pronounce
    }
    while True:
        print('values:', co.comms_means, co.internet)
        said_text = INPUT("> ")
        if said_text == -1:
            speak("No valid input detected")
            continue
        said_text = said_text.upper()
        command = said_text.split()
        print('****************', 'You said', str(command))
        reply = intr.get(command[0])
        task = func.get(command[0])

        if command[0] == 'SWITCH':
            if said_text == 'SWITCH TO TEXT':
                speak('SWITCHING TO TEXT!')
                co.internet = 2
                co.comms_means = 2
            else:
                speak('switch to what?')

        elif reply == None and task == None:
            speak("Didn't Catch That")
            continue

        elif reply != None:
            speak(reply)

        elif task != None:
            task()


if __name__ == "__main__":
    main()
