import os
import voices
import pandas as pd

source = "./API/app/Test_data/Voice/"

result = []

with open("records.txt", "a") as f:
    for voice in os.listdir(source):
        for test in os.listdir(source+voice):
            result.append(str(voices.recognize(voice, source+voice+"/"+test)))

df = DataFrame(result)
print(df)
correct = 0
for res in result:
    if res == "True":
        correct = correct + 1

print("the amount of accuracy "+ str((correct/48)*100) + "%")

#this is to test the accruracy for the gmm