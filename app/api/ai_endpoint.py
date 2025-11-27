from fastapi import APIRouter, HTTPException
from app.schemas.schema import ChatRequest, ChatResponse, SessionHistory
from app.services.ai_service import AIService
from app.utils.history import HistoryStore

router = APIRouter()

_ai = AIService()
_store = HistoryStore()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    try:
        await _store.append_message(req.user_id, req.session_id, {"role": "user", "content": req.message})
        history = await _store.get_history(req.user_id, req.session_id)
        reply = await _ai.generate_reply(req.user_id, req.session_id, req.message, history)
        await _store.append_message(req.user_id, req.session_id, {"role": "assistant", "content": reply})

        messages = await _store.get_history(req.user_id, req.session_id)

        return ChatResponse(user_id=req.user_id, session_id=req.session_id, messages=messages, reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=SessionHistory)
async def get_history(user_id: int, session_id: str):
    history = await _store.get_history(user_id, session_id)
    return SessionHistory(user_id=user_id, session_id=session_id, history=history)