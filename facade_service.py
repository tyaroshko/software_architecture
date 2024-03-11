from uuid import uuid4
from fastapi import FastAPI
from pydantic import BaseModel
import random
import logging
import requests

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOGGING_SERVICE_URLS = [
    "http://localhost:5002",
    "http://localhost:5003",
    "http://localhost:5004",
]
MESSAGES_SERVICE_URL = "http://localhost:5001"


class Message(BaseModel):
    text: str


@app.get("/")
async def root():
    logging_service_url = random.choice(LOGGING_SERVICE_URLS)
    logging_response = requests.get(logging_service_url)
    print(f"LOG: GET TO {logging_service_url}, RESPONSE: {logging_response.json()}")
    if logging_response.status_code == 200:
        logger.info("SUCCESSFUL RESPONSE FROM LOGGING SERVICE")
    else:
        logger.critical("ERROR IN GET REQUEST TO LOGGING SERVICE")

    messages_response = requests.get(MESSAGES_SERVICE_URL)
    if messages_response.status_code == 200:
        logger.info("SUCCESSFUL RESPONSE FROM MESSAGES SERVICE")
    else:
        logger.critical("ERROR IN GET REQUEST TO MESSAGES SERVICE")
    logging_response = logging_response.json()["messages"]
    messages_response = messages_response.json()["message"]
    return f"[{logging_response}]" + " " + messages_response


@app.post("/")
async def root(message: Message):
    print(f"LOG from FACADE: POST with body: {message}")
    UUID = str(uuid4())
    payload = {"UUID": UUID, "message": message.text}
    print(payload)
    response = requests.post(
        random.choice(LOGGING_SERVICE_URLS),
        headers={"Content-Type": "application/json"},
        json=payload,
    )
    if response.status_code == 200:
        logger.info(
            f'MESSAGE with TEXT "{message.text}" LOGGED SUCCESSFULLY with UUID {UUID}'
        )
    else:
        logger.critical("POST: ERROR from the LOGGING SERVICE")
    return {"status": "success"}
