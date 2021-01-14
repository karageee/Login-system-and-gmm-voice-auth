import os
import voices

source = "./API/app/Test_data/Voice/"

with open("records.txt", "a") as f:
    for voice in os.listdir(source):
        for test in os.listdir(source+voice):
            print(voices.recognize(voice, source+voice+"/"+test), file=f)

#this is to test the accruracy for the gmm