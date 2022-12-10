from typing import Optional
from pydantic import BaseModel


class BroadcastBase(BaseModel):
    type: str


class MessageBroadcast(BroadcastBase):
    username: str
    message_text: str
    id: Optional[int]


class DeleteBroadcast(BroadcastBase):
    username: str
    id: int
