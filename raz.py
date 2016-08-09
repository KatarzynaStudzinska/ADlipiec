# from naoqi import ALProxy
# tts = ALProxy("ALTextToSpeech", "192.168.210.109", 9559)
# tts.say(" ")

import argparse
from naoqi import ALProxy, ALBehavior
import time
import speech_recognition as sr
import wave

tts = audio = record = aup = None

class D:

    def __init__(self):
        pass

    def p(self):
        pass

def main(robot_IP, robot_PORT = 9559):
    global tts, audio, record, aup
    # ----------> Connect to robot <----------
    tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
    audio = ALProxy("ALAudioDevice", robot_IP, robot_PORT)
    record = ALProxy("ALAudioRecorder", robot_IP, robot_PORT)
    aup = ALProxy("ALAudioPlayer", robot_IP, robot_PORT)
    # ----------> recording <----------
    print 'start recording...'

    audio.openAudioInputs()
    record_path = '/home/nao/record.wav'

    # moze trzeba zrobic cos takiego?
    noise_output = wave.open('sample.wav', 'w')
    noise_output.setparams((1, 4, 48000, 0, 'NONE', 'not compressed'))
    #(nchannels, sampwidth, framerate, nframes, comptype, compname)
    # kanaly, szerokosc probki, czestotliwosc wyswietlania klatek, ilosc ramek

    #trzeba cos wyczarowac, by to sie rzeczywiscie zapisywalo. sie nie zapisuje.

    record.startMicrophonesRecording('sample.wav', 'wav', 48000, (0, 0, 0, 1))#(1, 1, 1, 1))
    print " start!!!"
    time.sleep(3)
    record.stopMicrophonesRecording()

    noise_output.close()
    #
    # import winsound
    #
    # winsound.PlaySound('man.wav', winsound.SND_FILENAME)

    time.sleep(3)
    fileID = aup.playFile('sample.wav', 0.7, 0)

    r = sr.Recognizer()
    with sr.AudioFile('sample.wav') as source:#sr.Microphone()
        try:
            audio = r.record(source)  # read the entire audio file
            print("You said" + r.recognize_google(audio))
        except sr.UnknownValueError:
            tts.say("I don't understand you, sorry! ")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.210.109", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()

main(args.ip, args.port)
#192.168.210.109

# czesc kodu, ktora czyni, ze nao sie nie meczy


# import sys
# from naoqi import ALProxy
#
# def main(robotIP):
#     PORT = 9559
#
#     try:
#         motionProxy = ALProxy("ALMotion", robotIP, PORT)
#     except Exception, e:
#         print "Could not create proxy to ALMotion"
#         print "Error was: ", e
#
#     try:
#         postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
#     except Exception, e:
#         print "Could not create proxy to ALRobotPosture"
#         print "Error was: ", e
#
#     # Send NAO to Pose Init
#     postureProxy.goToPosture("StandInit", 0.5)
#
#     motionProxy.rest()
#
#     # print motion state
#     print motionProxy.getSummary()
#
#
# if __name__ == "__main__":
#     robotIp = "192.168.210.109"
#
#     if len(sys.argv) <= 1:
#         print "Usage python almotion_rest.py robotIP (optional default: 127.0.0.1)"
#     else:
#         robotIp = sys.argv[1]
#
#     main(robotIp)