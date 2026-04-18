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
        "عايز", "عاوزه", "ازاي", "فين", "دلوقتي", "ليه", "مفيش", "كده", "إيه", "ايه"
    ]
    gulf_markers = [
        "وش", "شلون", "وين", "أبغى", "ابغى", "الحين", "مرة", "تكفى", "أبي", "ودي"
    ]
    levantine_markers = [
        "شو", "وين", "هلق", "بدي", "لسا", "كتير", "هيك", "ليش", "ازايك", "اروح"
    ]
    tunisian_markers = [
        "شنو", "برشة", "توا", "علاش", "وينو", "نحب"
    ]
    sudanese_markers = [
        "عايز", "داير", "هسي", "شنو", "مالو"
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
    return best if scores[best] > 0 else "neutral"


def detect_user_state(user_message: str) -> str:
    text = user_message.strip()

    distress_patterns = [
        r"\bضعت\b",
        r"\bضايع\b",
        r"\bضايعة\b",
        r"\bخايف\b",
        r"\bخايفة\b",
        r"\bمتوتر\b",
        r"\bمتوترة\b",
        r"\bمرعوب\b",
        r"\bمرعوبة\b",
        r"\bما أعرف وين\b",
        r"\bمو عارف وين\b",
        r"\bمستعجل\b",
        r"\bحالة طارئة\b",
        r"\bالحق\b",
        r"\bساعدني بسرعة\b",
    ]

    for pattern in distress_patterns:
        if re.search(pattern, text):
            return "distressed"

    return "normal"


def build_control_prompt(user_message: str, detected_dialect: str, user_state: str) -> str:
    return f"""
رسالة المستخدم الأصلية:
{user_message}

تحكم إلزامي:
- detected_dialect = {detected_dialect}
- user_state = {user_state}

قواعد إلزامية:
- الرد النهائي يجب أن يكون بنفس لهجة المستخدم إذا كانت لهجته واضحة.
- إذا كانت detected_dialect = levantine فالرد لازم يكون شامي طبيعي.
- إذا كانت detected_dialect = egyptian فالرد لازم يكون مصري طبيعي.
- إذا كانت detected_dialect = gulf فالرد لازم يكون خليجي طبيعي.
- إذا كانت detected_dialect = tunisian فالرد لازم يكون تونسي طبيعي.
- إذا كانت detected_dialect = sudanese فالرد لازم يكون سوداني طبيعي.
- إذا كانت detected_dialect = neutral فاستخدم عربية بسيطة طبيعية.

- إذا كانت user_state = normal:
  لا تستخدم أي جملة تطمين.
  ادخل مباشرة في الجواب.
  لا تقل: "أنا معك" ولا "لا تخاف" ولا "ما عليك".
- إذا كانت user_state = distressed:
  استخدم تطمينًا قصيرًا جدًا وبنفس لهجة المستخدم، ثم أعطِ توجيهًا مباشرًا فورًا.

- تعامل وكأنك تعرف موقع المستخدم الحالي بدقة داخل الحرم.
- أعطِ توجيهًا عمليًا محسوسًا، وليس وصفًا عامًا.
- لا تجعل الرد يبدو رسميًا أو ميكانيكيًا.
- لا تستخدم كلمة "العزيز" أو "عزيزي".
- لا تعتمد على الخريطة وحدها؛ يجب أن يكون النص نفسه مفيدًا.
- لا تكتب أي شرح داخلي.
- أخرج JSON فقط بهذا الشكل:
{{ "map_type": "", "reply": "" }}
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
    detected_dialect = detect_dialect(user_message)
    user_state = detect_user_state(user_message)

    messages = [
        {"role": "system", "content": get_system_prompt()},
        {
            "role": "user",
            "content": build_control_prompt(
                user_message=user_message,
                detected_dialect=detected_dialect,
                user_state=user_state,
            ),
        },
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
