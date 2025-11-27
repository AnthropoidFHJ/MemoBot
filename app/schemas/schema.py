from pydantic import BaseModel
from typing import List, Literal

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    user_id: int
    session_id: str
    message: str

class ChatResponse(BaseModel):
    user_id: int
    session_id: str
    messages: List[ChatMessage]

class SessionHistory(BaseModel):
    user_id: int
    session_id: str
    history: List[ChatMessage]