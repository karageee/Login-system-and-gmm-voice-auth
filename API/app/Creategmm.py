import os
import voices

source = "./API/app/voice_database/"

for voice in os.listdir(source):
    for test in os.listdir(source+voice):
        voices.add_user(voice)