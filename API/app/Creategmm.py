import os
import voices
import pandas as pd

end = []

for i in range(12,20):
    print(i)
    source_dat = "./API/app/voice_database/"

    for voice in os.listdir(source_dat):
        for test in os.listdir(source_dat+voice):
            voices.add_user(voice, i)

    source_test = "./API/app/Test_data/Voice/"

    result = []

    for voice in os.listdir(source_test):
        for test in os.listdir(source_test+voice):
            result.append(str(voices.recognize(voice, source_test+voice+"/"+test)))

    correct = 0
    for res in result:
        if res == "True":
            correct = correct + 1

    print("the amount of accuracy "+ str((correct/48)*100) + "%")
    end.append(str((correct/48)*100) + "%")

pd.DataFrame(end).to_excel("test.xlsx")

#this is to test the accruracy for the gmm