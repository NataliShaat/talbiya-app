from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.ELM_API_KEY,
    base_url=settings.ELM_BASE_URL,
)


def call_nuha(messages):
    if not settings.ELM_API_KEY:
        return {"error": "Missing Nuha API key"}

    try:
        response = client.chat.completions.create(
            model=settings.ELM_MODEL,
            messages=messages,
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        return {
            "error": "Nuha request failed",
            "details": str(e),
        }
