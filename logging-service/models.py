from pydantic import BaseModel


class Message(BaseModel):
    uuid: str
    message: str
