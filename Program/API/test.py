import requests
from requests.api import request

BASE = "http://127.0.0.1:5000/"

data = [{"user_id": "FF1", "voice_loc": "D:/locationA"},
        {"user_id": "FF2", "voice_loc": "D:/locationB"},
        {"user_id": "FF3", "voice_loc": "D:/locationC"}]

for i in range (len(data)):
    response = requests.post(BASE + "user/" + str(i), data[i])
    print(response.json())

input()
response = requests.get(BASE + "user/2")
print(response.json())