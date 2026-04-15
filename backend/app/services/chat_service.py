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

المطلوب:
- افهم هل السؤال يطابق أحد السيناريوهات المعروفة.
- إذا طابقها، أجب بشكل محدد ومباشر.
- إذا لم يطابقها، أجب بحرية وكأن لديك بيانات آنية عن الحرم.
- لا تستخدم placeholders أبدًا.
- لا تكتب أي شرح داخلي.
- reply يجب أن يكون طبيعيًا جدًا وجاهزًا للعرض للمستخدم.
- أخرج JSON فقط بهذا الشكل:
{{
  "map_type": "",
  "reply": ""
}}
""".strip()


def extract_json_object(text: str):
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        candidate = text[start:end + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            return None

    return None


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

    parsed = extract_json_object(raw_reply)
    if not parsed:
        return None

    map_type = parsed.get("map_type", DEFAULT_MAP_TYPE)
    reply = str(parsed.get("reply", "")).strip()

    if map_type not in MAP_IMAGE_MAP:
        map_type = DEFAULT_MAP_TYPE

    if not reply:
        reply = DEFAULT_FALLBACK_REPLY

    return {
        "map_type": map_type,
        "reply": reply,
    }


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
