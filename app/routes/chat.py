from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from app.services.search import smart_match

router = APIRouter()


# ── Request / Response schemas ──────────────────────────────────
class ChatRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def message_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Асуулт хоосон байж болохгүй.")
        if len(v) > 500:
            raise ValueError("Асуулт хэт урт байна (500 тэмдэгтээс бага байх ёстой).")
        return v


class ChatResponse(BaseModel):
    response: str


# ── Route ───────────────────────────────────────────────────────
@router.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest):
    """
    Main chat endpoint.
    Accepts a JSON body: { "message": "..." }
    Returns:  { "response": "..." }
    """
    try:
        answer = smart_match(body.message)
        return ChatResponse(response=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Серверийн алдаа: {str(e)}")


# ── GET kept for backwards-compatibility (redirects to POST logic) ──
@router.get("/chat", response_model=ChatResponse)
def chat_get(message: str = ""):
    """Legacy GET support — prefer POST for new clients."""
    if not message.strip():
        return ChatResponse(response="Асуулт хоосон байна.")
    try:
        return ChatResponse(response=smart_match(message))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))