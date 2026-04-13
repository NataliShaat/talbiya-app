from fastapi import APIRouter # type: ignore
from app.models.request_models import ChatRequest
from app.services.chat_service import process_chat

router = APIRouter()


@router.post("/chat")
def chat_endpoint(request: ChatRequest):
    result = process_chat(request.message)
    return {
        "user_message": request.message,
        "data": result
    }