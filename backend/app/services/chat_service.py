import re
from app.services.elm_service import call_nuha
from app.prompts.system_prompt import get_system_prompt
from app.core.constants import (
    DEFAULT_MAP_TYPE,
    DEFAULT_MAP_IMAGE,
    MAP_IMAGE_MAP,
    SUPPORTED_DIALECTS,
)
def get_calming_phrase(dialect: str, emotion: str, user_message: str = "") -> str:
    lost_markers = ["ضعت", "ضيعت", "ضايع", "ضايعة", "تايه", "تايهة", "خايف", "خايفة"]
    is_lost = any(marker in user_message for marker in lost_markers)

    if dialect == "gulf":
        if is_lost:
            return "أبشر، أنا معك، "

        if emotion == "stressed":
            return "أبشر، "
        if emotion == "confused":
            return "هدي شوي، أنا معك، "
        if emotion == "urgent":
            return "أبشر، "
        if emotion == "tired":
            return "لا تشيل هم "
        if emotion == "scared":
            return "أبشر، أنا معك، "
        return "أبشر، "

    if dialect == "egyptian":
        if is_lost:
            return "ما تقلقش، أنا معاك، "
        if emotion == "confused":
            return "اهدى ، أنا معاك، "
        if emotion == "urgent":
            return "تمام، "
        if emotion == "tired":
            return " بسيطة "
        if emotion == "scared":
            return "ما تخافش، أنا معاك، "
        return ""

    if dialect == "levantine":
        if is_lost:
            return "لا تشيل هم، أنا معك، "
        if emotion == "confused":
            return "اهدى شوي، أنا معك، "
        if emotion == "urgent":
            return "أبشر، "
        if emotion == "tired":
            return "،بسيطة "
        if emotion == "scared":
            return "لا تخاف، أنا معك، "
        return ""

    return ""
def detect_dialect(user_message: str) -> str:
    text = user_message.strip()

    gulf_markers = ["وين", "وش", "أبغى", "ابي", "الحين", "شلون", "مره", "مرة"]
    egyptian_markers = ["فين", "دلوقتي", "عايز", "عايزة", "ازاي", "إزاي"]
    levantine_markers = ["شو", "هلق", "بدي", "وينك", "لك", "بدك"]
    tunisian_markers = ["توّة", "برشة", "شنوة", "نحب"]
    sudanese_markers = ["زول", "هسع", "داير", "شنو"]

    if any(x in text for x in egyptian_markers):
        return "egyptian"
    if any(x in text for x in levantine_markers):
        return "levantine"
    if any(x in text for x in tunisian_markers):
        return "tunisian"
    if any(x in text for x in sudanese_markers):
        return "sudanese"
    if any(x in text for x in gulf_markers):
        return "gulf"

    return "natural"

def detect_emotion(user_message: str) -> str:
    text = user_message.strip()

    scared = ["خايف", "خايفة", "خطر", "طارئة", "طوارئ", "انقذ", "ساعدوني"]
    tired = ["تعبان", "تعبانة", "مرهق", "مرهقة", "أبي أرتاح", "ابي ارتاح", "أحتاج أرتاح"]
    urgent = ["مستعجل", "مستعجلة", "الحين", "الآن", "بسرعة", "سريع", "ألحق"]
    confused = ["ضعت", "ضيعت", "ضايع", "ضايعة", "تايه", "تايهة", "مو عارف", "مو عارفة"]

    if any(x in text for x in scared):
        return "scared"
    if any(x in text for x in tired):
        return "tired"
    if any(x in text for x in urgent):
        return "urgent"
    if any(x in text for x in confused):
        return "confused"

    return "calm"

def detect_map_type(user_message: str) -> str:
    text = user_message.strip()

    if any(word in text for word in ["حمام", "دورة", "دورات المياه", "دورة مياه"]):
        return "bathrooms"

    if any(word in text for word in ["عربة", "كرسي", "متحرك", "كهربائية"]):
        return "cars_wheelchairs"

    if any(word in text for word in ["فندق", "برج الساعة", "هوتيل", "أوتيل"]):
        return "hotels"

    if any(word in text for word in ["بوابة", "باب", "أبواب", "مدخل"]):
        return "doors"

    return "default_haram"

def normalize_reply(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text

def build_generation_prompt(user_message: str, dialect: str, emotion: str, map_type: str) -> str:
    return f"""
بيانات السياق الداخلية:
- dialect: {dialect}
- emotion: {emotion}
- map_type: {map_type}

مهم:
- استخدم هذه البيانات فقط لتشكيل النبرة وطريقة الإجابة.
- لا تذكر هذه البيانات للمستخدم.
- افترض أن النظام يعرف الموقع الحالي للمستخدم وحالة الازدحام والمسارات المتاحة داخل الحرم.
- أجب بناءً على سؤال المستخدم نفسه، وليس بناءً على سيناريوهات ثابتة.
- إذا كان السؤال عن اتجاه أو وصول، أعطِ توجيهًا واضحًا ومباشرًا.
- اجعل الإجابة قصيرة، لطيفة، وإنسانية.

سؤال المستخدم:
{user_message}
""".strip()

def generate_reply_with_nuha(user_message: str, dialect: str, emotion: str, map_type: str) -> str | None:
    messages = [
        {"role": "system", "content": get_system_prompt()},
        {
            "role": "user",
            "content": build_generation_prompt(
                user_message=user_message,
                dialect=dialect,
                emotion=emotion,
                map_type=map_type,
            ),
        },
    ]

    raw_reply = call_nuha(messages)

    if isinstance(raw_reply, dict) and raw_reply.get("error"):
        return None

    if not isinstance(raw_reply, str):
        return None

    cleaned = normalize_reply(raw_reply)
    return cleaned or None

def build_fallback_reply(user_message: str, emotion: str) -> str:
    if emotion in {"confused", "scared"}:
        return "لا تشيل هم، أنا معك. اكتب لي المكان اللي تبي توصله، وأنا أوجهك بأوضح طريقة."
    if emotion == "urgent":
        return "أبشر، اكتب لي وجهتك الآن وأنا أعطيك أسرع توجيه بشكل مباشر."
    return "أبشر، اكتب لي المكان أو الخدمة اللي تحتاجها، وأنا أوجهك بشكل واضح ومباشر."

def process_chat(user_message: str):
    dialect = detect_dialect(user_message)
    emotion = detect_emotion(user_message)
    map_type = detect_map_type(user_message)

    final_reply = generate_reply_with_nuha(
        user_message=user_message,
        dialect=dialect,
        emotion=emotion,
        map_type=map_type,
    )

    if not final_reply:
        final_reply = build_fallback_reply(user_message, emotion)

    map_image = MAP_IMAGE_MAP.get(map_type, DEFAULT_MAP_IMAGE)

    return {
        "map_type": map_type,
        "map_image": map_image,
        "emotion": emotion,
        "dialect": dialect if dialect in SUPPORTED_DIALECTS else "natural",
        "reply": final_reply,
    }
