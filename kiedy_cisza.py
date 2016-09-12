from scipy import io
from matplotlib import pyplot as plt
from math import copysign
from numpy import std
import speech_recognition as sr
import struct
import wave
sign = lambda x: copysign(1, x)


def check_zero_transition(list_of_transition, IZTC):
    for i in range(1, min(10, len(list_of_transition))):
        if list_of_transition[-i] < IZTC:
            return False
    return True

if __name__ == "__main__":
    rate, values = io.wavfile.read("hotdog.wav")
    print(len(values))
    plt.plot(values)
    # plt.show()

    energy_in_silence = []
    silence_zero_transition = []

    energy = 0
    zero_transition = 0

    #PRZEJECHANIE WALCEM CALEGO PLIKU

    for i in range(1, 45500):
        energy += abs(values[i][0])
        zero_transition += abs((sign(values[i][0]) - sign(values[i - 1][0]))/2)
        if i%455 == 0:
            # print(i)
            energy_in_silence.append(energy)
            silence_zero_transition.append(zero_transition)
            zero_transition = 0
            energy = 0


    #WYZNACZANIE PROGOW
    #dla pierwszysz 100ms tj dla ciszy

    IMN = sum(energy_in_silence) / len(energy_in_silence)
    IMX = max(energy_in_silence)
    ITC = sum(silence_zero_transition) / len(silence_zero_transition)
    Qitc = std(silence_zero_transition)

    I1 = 0.03*(IMX - IMN) + IMN
    I2 = 4*IMN

    ITL = min(I1, I2)   #dolna granica zwiazana z energia
    ITU = 5*ITL         #gorna granica zwiazana z energia

    IZTC = min(25, ITC + 2*Qitc) #granica zwizana z przejsciami przez zero

    #ANALIZA RESZTY PLIKU
    #proba wykrycia pierwszego fragmentu gadanego

    energy_per10 = []
    zero_transition_per10 = []
    signal = []
    rising = True
    signal_to_play = []
    interrupt = False
    ITL_couter = 0
    ile = 0

    for i in range(45500, len(values)):
        energy += abs(values[i][0])
        zero_transition += abs((sign(values[i][0]) - sign(values[i - 1][0]))/2)
        if not rising:
            signal_to_play.append(values[i][0])
        if i % 455 == 0:
            # energy_per10 .append(energy) #ewentualnie moze byc potrzebne gdy zrobimy jeszcze chapanie kawalka sygnalu z tylu
            zero_transition_per10.append(zero_transition)

            if rising:
                if energy > ITL and rising:
                    signal.append(energy)
                if energy < ITL and rising:
                    signal = []
                if energy > ITU and rising:
                    rising = False
            else:
                signal.append(energy)
                if energy < ITL:
                    ITL_couter += 1
                    zero_correction = check_zero_transition(zero_transition_per10, IZTC)
                    if ITL_couter == 19: #15:#  if ITL_couter == 10:#
                        interrupt = True
                else:
                    ITL_couter = 0
            zero_transition = 0
            energy = 0

        if interrupt:
            nazwa = 'odciete' + str(ile) +'.wav'
            noise_output = wave.open(nazwa, 'w')
            noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))

            for i in signal_to_play:
                    value = i
                    packed_value = struct.pack('h', value)
                    noise_output.writeframes(packed_value)
                    noise_output.writeframes(packed_value)

            noise_output.close()
            signal_to_play = []
            interrupt = False
            rising = True
            ile += 1
            r = sr.Recognizer()
            with sr.AudioFile(nazwa) as source:#sr.Microphone()
                try:
                    audio = r.record(source)# read the entire audio file
                    print("You said " + r.recognize_sphinx(audio))
                except sr.UnknownValueError:
                    print("sphinx :<   ")#"I don't understand you, sorry! ")
                try:
                    audio = r.record(source)# read the entire audio file
                    print("You said " + r.recognize_google(audio))
                except sr.UnknownValueError:
                    print("gugle :<   ")#"I don't understand you, sorry! ")

        if ile > 5:
            break







