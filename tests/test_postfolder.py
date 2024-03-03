import requests
import json

BASE = "http://127.0.0.1:5000"

data = {
    "name": "AlphaTauri"
}

headers = {
    'Accept': 'application/json'
}

response = requests.post(BASE + "/folders", json=data, headers=headers)
print(response.json())