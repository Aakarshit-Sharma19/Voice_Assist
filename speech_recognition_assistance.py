import pyaudio
import wave
import speech_recognition as sr

# pyaudio Initialization
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "sound.wav"


# Speech Recognition Initialization
r = sr.Recognizer()


def mic(vlc_obj=None):
    print('Listening')
    playfile = vlc_obj
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* Speak")

    frames = []
    playfile('cortana_open.mp3')
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("**Converting to Audio")
    stream.stop_stream()
    playfile('cortana_close.mp3')
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def speech_synth():
    try:
        recorded = sr.AudioFile('sound.wav')
        with recorded as source:
            audio = r.record(source)
        string = r.recognize_google(audio)
        return string
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return -1


def listen():
    mic()
    return speech_synth()


if __name__ == '__main__':
    pass
