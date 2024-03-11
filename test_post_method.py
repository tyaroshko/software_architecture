import requests

for i in range(10):
    message = "message_" + str(i)
    post_response = requests.post("http://127.0.0.1:5000/", json={"text": message})
    print("POST Response:", post_response.json()["status"])
