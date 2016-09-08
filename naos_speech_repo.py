import argparse
import time

from naoqi import ALProxy
from naoqi import ALModule
from naoqi import ALBroker

SpeechReco=None
memory=None

class SpeechRecoModule(ALModule):
    #""" A module to use speech recognition """
    def __init__(self, name):
        ALModule.__init__(self, name)
        try:
            self.asr = ALProxy("ALSpeechRecognition")
        except Exception as e:
            self.asr = None
        self.memory = ALProxy("ALMemory")

    def onLoad(self):
        from threading import Lock
        self.bIsRunning = False
        self.mutex = Lock()
        self.hasPushed = False
        self.hasSubscribed = False
        self.BIND_PYTHON("SpeechReco", "onWordRecognized")

    def onUnload(self):
        from threading import Lock
        self.mutex.acquire()
        try:
            if (self.bIsRunning):
                if (self.hasSubscribed):
                    self.memory.unsubscribeToEvent("WordRecognized", "SpeechReco")
                if (self.hasPushed and self.asr):
                    self.asr.popContexts()
        except RuntimeError, e:
            self.mutex.release()
            raise e
        self.bIsRunning = False;
        self.mutex.release()

    def onInput_onStart(self):
        from threading import Lock
        self.mutex.acquire()
        if(self.bIsRunning):
            self.mutex.release()
            return
        self.bIsRunning = True
        try:
            if self.asr:
                self.asr.setVisualExpression(True)
                self.asr.pushContexts()
            self.hasPushed = True
            if self.asr:
                self.asr.setVocabulary( ['yes','no'], True )
            self.subscribe("Test_ASR")
            self.memory.subscribeToEvent("WordRecognized", "SpeechReco", "onWordRecognized")
            self.hasSubscribed = True
            self.unsubscribe("Test_ASR")
        except RuntimeError, e:
            self.mutex.release()
            self.onUnload()
            raise e
        self.mutex.release()

    def onWordRecognized(self, key, value, message):
        print 'word recognized'
        if(len(value) > 1 and value[1] >= 0.5):
            print 'recognized the word :', value[0]
        else:
            print 'unsifficient threshold'

def main(robotIP,PORT):
    callSpeechReco(robotIP,PORT)

def callSpeechReco(robotIP,PORT):
    myBroker=ALBroker("myBroker","0.0.0.0",0,robotIP,PORT)
    global SpeechReco
    SpeechReco=SpeechRecoModule("SpeechReco")
    SpeechReco.onLoad()
    SpeechReco.onInput_onStart()
    time.sleep(10)
    SpeechReco.onUnload()

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--ip",type=str,default="192.168.210.109",help="Robot ip address")
    parser.add_argument("--port",type=int,default=9559,help="Robot port number")

    args=parser.parse_args()
    main(args.ip,args.port)    