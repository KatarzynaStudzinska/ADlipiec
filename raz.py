# from naoqi import ALProxy
# tts = ALProxy("ALTextToSpeech", "192.168.210.109", 9559)
# tts.say(" ")

import argparse
from naoqi import ALProxy, ALBehavior
import time
import speech_recognition as sr
import os

tts = audio = record = aup = None


def main(robot_IP, robot_PORT = 9559):
    global tts, audio, record, aup
    # ----------> Connect to robot <----------
    sd = ALProxy("ALSoundDetection", robot_IP, robot_PORT)
    tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
    audio = ALProxy("ALAudioDevice", robot_IP, robot_PORT)
    record = ALProxy("ALAudioRecorder", robot_IP, robot_PORT)
    aup = ALProxy("ALAudioPlayer", robot_IP, robot_PORT)
    mem = ALProxy('ALMemory', robot_IP, robot_PORT)
    print(mem.getDataListName())
    # ----------> recording <----------
    print 'start recording...'

    sd.setParameter("Sensibility", 0.9)
    audio.openAudioInputs()
    record_path = '/home/nao/audio/wista.wav'

    # noise_output = wave.open('sample.wav', 'w')
    # noise_output.setparams((1, 4, 16000, 0, 'NONE', 'not compressed'))
    #(nchannels, sampwidth, framerate, nframes, comptype, compname)
    # kanaly, szerokosc probki, czestotliwosc wyswietlania klatek, ilosc ramek

    # noise_output = wave.open('file.wav', 'w')
    record.startMicrophonesRecording('wista.wav', 'wav', 16000, (1, 0, 0, 0))

    print("start!!!")
    time.sleep(35)
    print("stop!!!")
    record.stopMicrophonesRecording()

    # record_to_read = aup.playFile('/home/nao/audio/wista.wav', 0.1, 0)
    #
    r = sr.Recognizer()
    with sr.AudioFile('audio/wista.wav') as source:#sr.Microphone()
        try:
            audio = r.record(source)# read the entire audio file
            print("You said " + r.recognize_sphinx(audio))
        except sr.UnknownValueError:
            tts.say("sorry")#"I don't understand you, sorry! ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.210.109", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()

main(args.ip, args.port)

#192.168.210.109
