f = open("test.raw", "rb")
try:
    byte = f.read(1)
    while byte != "":
        # Do stuff with byte.
        byte += f.read(1)
        if (len(byte)) > 30000:
            print("koniec")
            break


finally:
    pass

import wave
import random
import struct

SAMPLE_LEN = 10000
noise_output = wave.open('noise.wav', 'w')
noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))



for i in range(0, len(byte)):
    print(byte[i], i)
    if int(byte[i]) != ' ':
        value = int(byte[i])#random.randint(-32767, 32767)
        print(type(value))
        packed_value = struct.pack('h', value)
        noise_output.writeframes(packed_value)
        noise_output.writeframes(packed_value)

noise_output.close()