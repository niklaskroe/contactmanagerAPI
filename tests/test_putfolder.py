import requests
import json

BASE = "http://127.0.0.1:5000"

data = {
    "name": "AlphaTauri"
}

headers = {
    'Accept': 'application/json'
}

response = requests.put(BASE + "/folders/9", json=data, headers=headers)
print(response.json())