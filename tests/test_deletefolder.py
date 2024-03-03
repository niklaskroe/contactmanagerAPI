import requests
import json

BASE = "http://127.0.0.1:5000"

response = requests.delete(BASE + "/folders/1")
print(response.json())