import json

from app.services.elm_service import call_nuha
from app.prompts.system_prompt import get_system_prompt
from app.core.constants import (
    DEFAULT_MAP_TYPE,
    DEFAULT_MAP_IMAGE,
    DEFAULT_FALLBACK_REPLY,
    MAP_IMAGE_MAP,
)


def build_user_prompt(user_message: str) -> str:
    return f"""
رسالة المستخدم:
{user_message}

أعد JSON فقط بهذا الشكل:
{{
  "map_type": "",
  "reply": ""
}}

مهم جدًا:
- reply يكون جاهزًا للعرض للمستخدم.
- لا تضع أي JSON أو شرح داخلي داخل reply.
- لا تستخدم placeholders مثل: "اسم البوابة" أو "المسار" أو "الاتجاه".
- إذا سأل المستخدم عن أقرب بوابة، افترض أن أفضل بوابة له الآن هي بوابة 16.
- إذا سأل عن بوابة، اذكر أن بوابة 15 مغلقة حاليًا ويجب تجنبها.
- إذا كانت لهجة المستخدم غير واضحة، استخدم عربية طبيعية واضحة ومحايدة قريبة من المستخدم في السعودية.
- لا تستخدم لهجة مصرية إلا إذا كان المستخدم نفسه يتحدث بها.
- لا تبدأ كل الردود بـ "أبشر".
- استخدم "أبشر" فقط في الطلبات العادية.
- إذا كان المستخدم خائفًا أو ضائعًا أو متوترًا، لا تبدأ بـ "أبشر".
- في هذه الحالة ابدأ بطمأنة قصيرة مثل:
  "لا تخافي، أنا معك"
  أو
  "ما عليك، أنا معك"
  ثم وجّه المستخدم مباشرة.
""".strip()


def ask_nuha(user_message: str):
    messages = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": build_user_prompt(user_message)},
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
