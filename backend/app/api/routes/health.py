from fastapi import APIRouter # type: ignore
from app.core.config import settings

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "talbiyah-backend",
        "nuha_model": settings.ELM_MODEL,
        "dialect_model": settings.DIALECT_MODEL_ID,
        "anthropic_ready": bool(settings.ANTHROPIC_API_KEY),
    }