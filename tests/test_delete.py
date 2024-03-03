import requests
import json

BASE = "http://127.0.0.1:5000"

response = requests.delete(BASE + "/contacts/14")
print(response.json())