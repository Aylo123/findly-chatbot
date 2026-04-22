from fastapi import APIRouter
from app.services.search import smart_match
router = APIRouter()

@router.get("/chat")
def chat(message: str):
    return {"response": smart_match(message)}