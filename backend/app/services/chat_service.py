import json
import re
from app.services.elm_service import call_nuha
from app.prompts.system_prompt import get_system_prompt
from app.core.constants import (
    DEFAULT_MAP_TYPE,
    DEFAULT_MAP_IMAGE,
    DEFAULT_FALLBACK_REPLY,
    MAP_IMAGE_MAP,
)

def detect_dialect(user_message: str) -> str:
    text = user_message.strip()

    egyptian_markers = [
        "عايز", "عاوزه", "ازاي", "فين", "دلوقتي", "ليه", "لو سمحت",
        "محتاج", "مفيش", "كده", "إيه", "ايه"
    ]
    gulf_markers = [
        "وش", "شلون", "وين", "أبغى", "ابغى", "الحين", "مرة", "تكفى",
        "لو سمحت", "أبي", "ودي"
    ]
    levantine_markers = [
        "شو", "وين", "هلق", "بدي", "لسا", "كتير", "هيك", "ليش"
    ]
    tunisian_markers = [
        "شنو", "برشة", "توا", "علاش", "وينو", "نحب"
    ]
    sudanese_markers = [
        "عايز", "داير", "هسي", "وين", "مالو", "شنو"
    ]

    def count_markers(markers):
        return sum(1 for m in markers if re.search(rf"\b{re.escape(m)}\b", text))

    scores = {
        "egyptian": count_markers(egyptian_markers),
        "gulf": count_markers(gulf_markers),
        "levantine": count_markers(levantine_markers),
        "tunisian": count_markers(tunisian_markers),
        "sudanese": count_markers(sudanese_markers),
    }

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "natural"


def ask_nuha(user_message: str):
    detected_dialect = detect_dialect(user_message)

    dialect_instruction = f"""
Detected user dialect: {detected_dialect}

STRICT RULES:
- Your final reply MUST use the same dialect as the user.
- Do not switch to another dialect.
- Do not default to neutral Arabic if a dialect is detected.
- If detected_dialect is "egyptian", reply in Egyptian Arabic.
- If detected_dialect is "gulf", reply in Gulf Arabic.
- If detected_dialect is "levantine", reply in Levantine Arabic.
- If detected_dialect is "tunisian", reply in Tunisian Arabic.
- If detected_dialect is "sudanese", reply in Sudanese Arabic.
- If detected_dialect is "natural", use simple clear Arabic suitable for Saudi users.
"""

    messages = [
        {"role": "system", "content": get_system_prompt() + "\n\n" + dialect_instruction},
        {
            "role": "user",
            "content": f"User original message:\n{user_message}\n\nReply in the same dialect exactly."
        },
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
            "detected_dialect": detected_dialect,
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
