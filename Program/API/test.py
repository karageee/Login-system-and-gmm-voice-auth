import requests
from requests.api import request
import json

BASE = "http://127.0.0.1:5000/"

data = '{"user_id": "FF1", "voice_loc": "D:/locationA"}'

y = json.loads(data)
print(y)

response = requests.put(BASE + "user/" + y['user_id'])

response = requests.get(BASE + "user/FF2")
print(response.json())