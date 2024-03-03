import requests
import json

BASE = "http://127.0.0.1:5000"

data = {
    "name": "Seb",
    "surname": "Vet",
    "number": 4152737383,
    "email": "seb@vettel.com",
    "folderid": 3
}

headers = {
    'Accept': 'application/json'
}

response = requests.put(BASE + "/contacts/1", json=data, headers=headers)
print(response.json())