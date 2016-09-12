from pydub import AudioSegment
from pydub.utils import make_chunks

myaudio = AudioSegment.from_file("artofwar.wav" , "wav")
chunk_length_ms = 100000 # pydub calculates in millisec
chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec

#Export all of the individual chunks as wav files
licz = 0
for i, chunk in enumerate(chunks):
    chunk_name = "art{0}.wav".format(i)
    print "exporting", chunk_name
    chunk.export(chunk_name, format="wav")
    licz +=2
    if licz > 0:
        break