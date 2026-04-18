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
        "شو", "وين", "هلق", "بدي", "لسا", "كتير", "هيك", "ليش", "ضعت", "اروح"
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
        r"\bوين أروح\b",
        r"\bوين اروح\b",
        r"\bما أعرف أروح وين\b",
        r"\bمحتاج مساعدة بسرعة\b",
        r"\bحالة طارئة\b",
    ]

    for pattern in distress_patterns:
        if re.search(pattern, text):
            return "distressed"

    return "normal"


def build_control_prompt(user_message: str, detected_dialect: str, user_state: str) -> str:
    return f"""
رسالة المستخدم الأصلية:
{user_message}

المتغيرات:
- detected_dialect = {detected_dialect}
- user_state = {user_state}

تعليمات إلزامية:
- إذا كانت لهجة المستخدم واضحة، فالرد النهائي يجب أن يكون بنفس لهجته بشكل واضح.
- إذا كانت detected_dialect = levantine فالرد يكون شامي طبيعي.
- إذا كانت detected_dialect = egyptian فالرد يكون مصري طبيعي.
- إذا كانت detected_dialect = gulf فالرد يكون خليجي طبيعي.
- إذا كانت detected_dialect = tunisian فالرد يكون تونسي طبيعي.
- إذا كانت detected_dialect = sudanese فالرد يكون سوداني طبيعي.
- إذا كانت detected_dialect = neutral فاستخدم عربية طبيعية واضحة.
- إذا كان سؤال المستخدم خارج السيناريوهات المحددة لكنه ما زال عن مكان أو معلم أو خدمة داخل الحرم:
  اعتبره سؤال موقع عام داخل الحرم.
  تصرّف وكأنك تعرف مكان المستخدم الحالي ومكان الوجهة الآن.
  أعطِ توجيهًا عمليًا واضحًا بناءً على موقعه الحالي.
  لا تقل: "لا أستطيع تحديد موقعك" ولا "تحقق من الخريطة".
  لا تجعل الرد عامًا أو وصفيًا فقط.
  اذكر أقرب اتجاه واضح مثل: أمامك، على يمينك، على يسارك، بعد الممر، عند المخرج، بجانب الرواق.
  اختر map_type الأقرب للسؤال:
  - إذا كان السؤال عن بوابة أو مخرج فاستخدم "doors"
  - إذا كان عن دورات المياه فاستخدم "bathrooms"
  - إذا كان عن فندق فاستخدم "hotels"
  - إذا كان عن عربات أو كراسي متحركة فاستخدم "cars_wheelchairs"
  - إذا كان عن أي موقع عام داخل الحرم مثل المسعى أو الكعبة أو الأروقة أو المصليات أو الساحات أو نقاط التجمع فاستخدم "default_haram"
- إذا كانت user_state = normal:
  ادخل مباشرة في الجواب.
  لا تستخدم تطمينًا عاطفيًا.
  لا تقل "أنا معك" أو "لا تخاف" إلا عند الحاجة الحقيقية.

- إذا كانت user_state = distressed:
  استخدم تطمينًا قصيرًا جدًا وبنفس لهجة المستخدم.
  ثم أعطِ خطوة مكانية واضحة وفورية.
  لا تعطِ كلامًا عامًّا مثل: "الطريق اللي قدامك هو الصح".
  لا تطلب من المستخدم أن يشرح كثيرًا قبل أن تعطيه خطوة أولى.
  وجّه المستخدم فورًا إلى مكان آمن وواضح مثل:
  - الممر الرئيسي
  - نقطة تجمع واضحة
  - أقرب بوابة مناسبة
  - أقرب نقطة مساعدة
  ويجب أن تبدو وكأنك تعرف موقعه الحالي فعلًا.

- الرد لازم يكون مفيدًا حتى بدون النظر إلى الخريطة.
- لا تستخدم placeholders.
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


def normalize_direction_wording(reply: str) -> str:
    replacements = {
        " انعط ": " انعطف ",
        "انعط ": "انعطف ",
        " انعط،": " انعطف،",
        " انعط.": " انعطف.",
        " انعط على": " انعطف على",
        "وبعدين انعط": "وبعدين انعطف",
        "ثم انعط": "ثم انعطف",
    }

    for wrong, correct in replacements.items():
        reply = reply.replace(wrong, correct)

    return reply


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
    reply = normalize_direction_wording(reply)

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
