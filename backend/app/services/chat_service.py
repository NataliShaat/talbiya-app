import json

from app.services.elm_service import call_nuha
from app.prompts.system_prompt import get_system_prompt
from app.core.constants import (
    DEFAULT_MAP_TYPE,
    DEFAULT_MAP_IMAGE,
    DEFAULT_FALLBACK_REPLY,
    MAP_IMAGE_MAP,
)

def ask_nuha(user_message: str):
    messages = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": user_message},
    ]

    raw_reply = call_nuha(messages)

    if isinstance(raw_reply, dict) and raw_reply.get("error"):
        return None

    if not isinstance(raw_reply, str):
        return None

    try:
        parsed = json.loads(raw_reply)

        map_type = parsed.get("map_type", DEFAULT_MAP_TYPE)
        reply = parsed.get("reply", "").strip()

        if map_type not in MAP_IMAGE_MAP:
            map_type = DEFAULT_MAP_TYPE

        if not reply:
            reply = DEFAULT_FALLBACK_REPLY

        return {
            "map_type": map_type,
            "reply": reply,
        }

    except Exception:
        return None


def process_chat(user_message: str):
    nuha_result = ask_nuha(user_message)

    if nuha_result:
        map_type = nuha_result["map_type"]
        reply = nuha_result["reply"]
    else:
        map_type = DEFAULT_MAP_TYPE
        reply = DEFAULT_FALLBACK_REPLY

    map_image = MAP_IMAGE_MAP.get(map_type, DEFAULT_MAP_IMAGE)

    return {
        "map_type": map_type,
        "map_image": map_image,
        "reply": reply,
    }
