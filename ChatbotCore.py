import datetime
import re
from urllib import parse

import requests
from PyQt5.QtCore import QThread
from bs4 import BeautifulSoup


def extract_title(url):
    p = parse.urlparse(url, 'http')
    netloc = p.netloc or p.path
    path = p.path if p.netloc else ''
    if not netloc.startswith('www.'):
        netloc = 'www.' + netloc
    p = parse.ParseResult('https', netloc, path, *p[3:])
    url = p.geturl()
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.title.string


class core(QThread):
    def __init__(self, main_window, voice, name):
        super().__init__()
        self.main_window = main_window
        self.name = name
        self.voice = voice
        self.input_string = ''

    def process(self, string):

        response = ''
        string = string.lower()

        # Checking Conditions
        if 'tell me about' in string or 'search about' in string or 'search' in string:
            string = string.replace('tell me about', '')
            string = string.replace('search about', '')
            string = string.replace('search', '')

            # response = 'Searching for {}'.format(string)

            string = '+'.join(string.split())
            url = 'http://www.google.com/search?q=' + string
            response = extract_title(url)

            self.respond(response)
            print(url)
            self.main_window.open_url(url)

        elif 'time' in string:
            response = 'The time is {}'.format(datetime.datetime.now().strftime('%I %M %p'))  # %d %B, %Y'))
            self.respond(response)

        elif 'hello' in string:
            response = 'Hello {}'.format(self.name)
            self.respond(response)

        elif 'open' in string:
            reg_ex = re.search('open (.+)', string)
            self.main_window.open_url('www.' + reg_ex.group(1))
            response = 'Opening ' + reg_ex.group(1)
            self.respond(response)

        elif 'weather' in string:
            reg_ex = re.search('weather in (.+)', string)

        elif 'switch to text' in string:
            self.voice.comms_object.switch_to_text()
            self.respond('Switching to text')

        elif 'bye' in string or 'exit' in string:
            self.respond('bye {}'.format(self.name))
            self.main_window.close()
            return False
        return True

    # VoiceEngine.VoiceSynth().synthesize_speech(VoiceEngine.TypeComm(), string, True)

    def respond(self, response):

        if self.voice.comms_object.comm_status():
            # Below condition shows that if there is a internet error and the synthesize_speech function returns false
            # then the internet status is set to false
            if not self.voice.synthesize_speech(response):
                self.main_window.switch_comm()
                self.main_window.signal_set_status.emit('Internet Error')
            else:
                self.main_window.signal_set_status.emit('Speaking...')
                self.main_window.signal_append_chatbot_history.emit(response)
                self.voice.speak()
                self.main_window.signal_set_status.emit('')
        else:
            self.main_window.signal_append_chatbot_history.emit(response)

    def run(self):
        while self.voice.comms_object.comm_status():

            self.main_window.signal_set_status.emit('Listening')
            self.main_window.input_string = self.voice.listen()
            self.main_window.signal_set_status.emit('Thinking...')
            if self.main_window.input_string == -1:
                self.respond('Didn\'t catch That')
            if self.main_window.input_string == -2:
                self.main_window.switch_comm()
                self.signal_set_status.setText('Internet Error.Text Only')
                break
            self.main_window.signal_append_user_history.emit(self.main_window.input_string)
            if not self.process(self.main_window.input_string):
                break


if __name__ == '__main__':
    # process('time', 1, 2, 3)
    pass
