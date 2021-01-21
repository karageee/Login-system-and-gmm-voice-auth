import os
from scipy.io.wavfile import read
import voices

source = "./API/app/Test_data/Voice/"


with open("records.txt", "a") as f:
    for voice in os.listdir(source):
        for test in os.listdir(source+voice):
            print(str(voices.recognize(voice, source+voice+"/"+test)) +" (" + voice + ")", file=f)

#this is to test the accruracy for the gmm