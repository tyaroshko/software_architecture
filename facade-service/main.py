from fastapi import FastAPI
from models import Message 
import uuid
import requests

app = FastAPI()

@app.get("/")
async def root():
    print(f"LOG from FACADE: GET")
    logging_output = requests.get(f"http://logging:8000/").json()
    messages_output = requests.get(f"http://messages:8000/").json()
    # data =  {"messages": logging_output["messages"] + " " + messages_output["messages"]}
    data = {"logging": logging_output["messages"], "messages": messages_output["messages"]}
    return data


@app.post("/")
async def root(message: Message):
    print(f"LOG from FACADE: POST with body: {message}")
    message = message.text
    cur_uuid = str(uuid.uuid4())
    requests.post(
        f"http://logging:8000/",
        headers={"Content-type": "application/json"},
        json={"uuid": cur_uuid, "message": message},
    )
