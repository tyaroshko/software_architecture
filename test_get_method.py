import requests
import json

try:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    }
    response = requests.get("http://localhost:5000/", headers=headers)
    print(response)
    print("GET Response:", response.json())
except json.decoder.JSONDecodeError:
    print("No JSON data returned from the server.")
