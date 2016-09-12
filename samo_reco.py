import speech_recognition as sr
from os import environ, path
DATADIR = "C:/Users/Katarzyna/PycharmProjects/SpeechToText"



r = sr.Recognizer()
#ALAudioRecorderProxy as source???

with sr.AudioFile("chunk1.wav") as source:
    audio = r.record(source)# read the entire audio file
    # print("sphinx", r.recognize_sphinx(audio))
    try:
        print("gugle", r.recognize_google(audio))
    except sr.UnknownValueError:
        print("nie tym razem")