import requests
import json

BASE = "http://127.0.0.1:5000"

data = {
    "name": "George",
    "surname": "Russell",
    "number": 3152732383,
    "email": "grussell@gmx.com",
}

headers = {
    'Accept': 'application/json'
}

response = requests.post(BASE + "/contacts", json=data, headers=headers)
print(response.json())