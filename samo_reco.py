import speech_recognition as sr
from os import environ, path
DATADIR = "C:/Users/Katarzyna/PycharmProjects/SpeechToText"



r = sr.Recognizer()
#ALAudioRecorderProxy as source???

stream = open(path.join(DATADIR, 'hello.raw'), 'rb')
with sr.AudioFile("record_hey.wav") as source:
    audio = r.record(source)# read the entire audio file
    print(r.recognize_sphinx(audio))
    try:
        print(r.recognize_google(audio))
    except sr.UnknownValueError:
        print("niet tym razem")