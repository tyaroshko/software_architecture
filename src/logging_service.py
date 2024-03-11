from fastapi import FastAPI
import hazelcast
from pydantic import BaseModel

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LogEntity(BaseModel):
    UUID: str
    message: str


app = FastAPI()

hazelcast_client = hazelcast.HazelcastClient()
log_messages = hazelcast_client.get_map("log_messages").blocking()


@app.get("/")
async def root():
    print(f"LOG from LOGGING: GET")
    messages = []
    for entry in log_messages.entry_set():
        print(entry)
        message = {"id": entry[0], "message": entry[1]}
        messages.append(message)
    return {"messages": messages}


@app.post("/")
async def root(log_message: LogEntity):
    print(f"LOG from LOGGING: POST with body: {log_message.message}")
    uuid = log_message.UUID
    msg = log_message.message
    log_messages.put(uuid, msg)
    return {"status": "success"}
