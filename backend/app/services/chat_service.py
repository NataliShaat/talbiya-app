import json
from app.services.elm_service import call_nuha
from app.prompts.system_prompt import get_system_prompt
from app.core.constants import (
    DEFAULT_MAP_TYPE,
    DEFAULT_MAP_IMAGE,
    DEFAULT_EMOTION,
    DEFAULT_DIALECT,
    DEFAULT_FALLBACK_REPLY,
    MAP_IMAGE_MAP,
    SUPPORTED_DIALECTS,
)


def detect_dialect(user_message: str) -> str:
    text = user_message.strip()

    gulf_markers = ["وين", "وش", "أبغى", "ابي", "الحين", "شلون", "مره", "مرة", "كيف اروح", "كيف أروح", "كيف أوصل", "أقرب"]
    egyptian_markers = ["فين", "دلوقتي", "عايز", "عايزة", "ازاي", "إزاي"]
    levantine_markers = ["شو", "هلق", "بدي", "إلك", "وينك"]
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

    return "gulf"


def detect_emotion(user_message: str) -> str:
    text = user_message.strip()

    scared = ["خايف", "خايفة", "خطر", "طارئة", "طوارئ", "انقذ", "ساعدوني"]
    tired = ["تعبان", "تعبانة", "مرهق", "مرهقة", "ابي ارتاح", "أبي أرتاح", "أحتاج أرتاح"]
    urgent = ["متى أتحرك", "متى اتحرك", "مستعجل", "مستعجلة", "الحين", "الآن", "بسرعة", "سريع"]
    confused = ["ضعت", "ضيعت", "ضايع", "ضايعة", "تايه", "تايهة", "مو عارف", "مو عارفة", "كيف أروح", "كيف اروح", "كيف أوصل", "كيف اوصل"]

    if any(x in text for x in scared):
        return "scared"
    if any(x in text for x in tired):
        return "tired"
    if any(x in text for x in urgent):
        return "urgent"
    if any(x in text for x in confused):
        return "confused"

    return "calm"


def detect_intent_and_map(user_message: str):
    text = user_message.strip()

    if "متى أتحرك" in text or "متى اتحرك" in text or "أتحرك" in text or "اتحرك" in text or "انتظر" in text:
        return "when_to_move", "default_haram"

    if "حالة طارئة" in text or "طوارئ" in text or "طارئة" in text or "خطر" in text:
        return "danger_request", "default_haram"

    if "زمزم" in text or "موية" in text or "ماء" in text or "موية زمزم" in text:
        return "water_request", "default_haram"

    if "تعبان" in text or "تعبانة" in text or "أرتاح" in text or "ارتاح" in text or "استراحة" in text or "راحة" in text:
        return "rest_request", "default_haram"

    if "عربة" in text or "كرسي" in text or "متحرك" in text or "كهربائية" in text:
        return "wheelchair_or_cart", "cars_wheelchairs"

    if "حمام" in text or "دورة" in text or "دورات المياه" in text or "دورة مياه" in text:
        return "bathroom_request", "bathrooms"

    if "فندق" in text or "برج الساعة" in text or "هوتيل" in text or "أوتيل" in text:
        return "hotel_request", "hotels"

    if "بوابة" in text or "باب" in text or "أبواب" in text or "مدخل" in text or "كيف أروح" in text or "كيف اروح" in text or "كيف أوصل" in text or "كيف اوصل" in text:
        return "route_guidance", "doors"

    if len(text) < 8:
        return "vague_request", "default_haram"

    return "general_haram", "default_haram"


def get_calming_phrase(dialect: str, emotion: str, user_message: str = "") -> str:
    lost_markers = ["ضعت", "ضيعت", "ضايع", "ضايعة", "تايه", "تايهة", "خايف", "خايفة"]
    is_lost = any(marker in user_message for marker in lost_markers)

    if dialect == "gulf":
        if is_lost:
            return "لا تشيل هم، أنا معك، "
        if emotion == "stressed":
            return "لا تشيل هم، "
        if emotion == "confused":
            return "هدي شوي، أنا معك، "
        if emotion == "urgent":
            return ""
        if emotion == "tired":
            return "الله يقويك، "
        if emotion == "scared":
            return "لا تخاف، أنا معك، "
        return ""

    if dialect == "egyptian":
        if is_lost:
            return "ما تقلقش، أنا معاك، "
        if emotion == "confused":
            return "اهدى بس، أنا معاك، "
        if emotion == "urgent":
            return ""
        if emotion == "tired":
            return "ربنا يقويك، "
        if emotion == "scared":
            return "ما تخافش، أنا معاك، "
        return ""

    if dialect == "levantine":
        if is_lost:
            return "لا تشيل هم، أنا معك، "
        if emotion == "confused":
            return "اهدى شوي، أنا معك، "
        if emotion == "urgent":
            return ""
        if emotion == "tired":
            return "الله يعطيك العافية، "
        if emotion == "scared":
            return "لا تخاف، أنا معك، "
        return ""

    return ""


def build_reply(dialect: str, intent: str, map_type: str, emotion: str, user_message: str) -> str:
    calm = get_calming_phrase(dialect, emotion, user_message)

    replies = {
        "gulf": {
            "when_to_move": "بحسب موقعك الحين والزحام حولك، انتظر 10 دقايق وبعدها تحرك، المنظمين بيفتحون البوابات القريبة منك.",
            "danger_request": f"{calm}هل تحتاج كرسي متحرك أو مساعدة طبية؟ وإذا أنت في خطر الحين، توجه مباشرة لأقرب رجال أمن أو منظمين قريبين منك عند المسار القريب من بوابة 16.",
            "route_guidance": f"{calm}بحسب موقعك الحين وتحديثات المنظمين، بوابة 15 وبوابة 7 مغلقتان حالياً بسبب الزحام، وبوابة 16 هي الأقرب والأسرع.",
            "hotel_request": "بحسب موقعك الحين، أقرب فندق لك هو برج الساعة.",
            "wheelchair_or_cart": "بحسب موقعك الحين، أقرب خدمة عربات لك هي عربة الحرم الكهربائية في منطقة أجياد.",
            "bathroom_request": f"{calm}بحسب موقعك الحين، أقرب دورة مياه لك هي دورة المياه رقم 2 عند بوابة 16.",
            "rest_request": f"{calm}بحسب موقعك الحين، أقرب منطقة راحة أقل زحمة قرب المسار الجانبي المؤدي إلى بوابة 16. وإذا تبي، أقدر أوجّهك بعد لأقرب زمزم.",
            "water_request": "بحسب موقعك الحين، أقرب زمزم لك عند منطقة الخدمة القريبة من بوابة 16.",
            "vague_request": f"{calm}عطني تفاصيل أكثر عشان أوجّهك صح، وين تبي تروح بالضبط؟",
            "general_haram": "أنا معك في الحرم، قل لي وش تحتاج بالضبط؟",
        },
        "egyptian": {
            "when_to_move": "بناءً على مكانك دلوقتي والزحمة حواليك، استنى 10 دقايق وبعدها اتحرك، والمنظمين هيفتحوا البوابات القريبة منك.",
            "danger_request": f"{calm}محتاج كرسي متحرك أو مساعدة طبية؟ ولو إنت في خطر دلوقتي، اتجه فوراً لأقرب رجال أمن أو منظمين قريبين منك عند المسار القريب من بوابة 16.",
            "route_guidance": f"{calm}بناءً على مكانك دلوقتي وتحديثات المنظمين، بوابة 15 وبوابة 7 مقفولين حالياً بسبب الزحمة، وبوابة 16 هي الأقرب والأسرع.",
            "hotel_request": "بناءً على مكانك دلوقتي، أقرب فندق ليك هو برج الساعة.",
            "wheelchair_or_cart": "بناءً على مكانك دلوقتي، أقرب خدمة عربات ليك هي عربة الحرم الكهربائية في منطقة أجياد.",
            "bathroom_request": f"{calm}بناءً على مكانك دلوقتي، أقرب حمام ليك هو دورة المياه رقم 2 عند بوابة 16.",
            "rest_request": f"{calm}بناءً على مكانك دلوقتي، أقرب مكان راحة أقل زحمة قرب المسار الجانبي المؤدي إلى بوابة 16. ولو تحب، أقدر أوجهك كمان لأقرب زمزم.",
            "water_request": "بناءً على مكانك دلوقتي، أقرب زمزم ليك عند منطقة الخدمة القريبة من بوابة 16.",
            "vague_request": f"{calm}قولّي تفاصيل أكتر عشان أوجّهك صح، إنت عايز تروح فين بالظبط؟",
            "general_haram": "أنا معاك جوه الحرم، قولّي محتاج إيه بالظبط؟",
        },
        "levantine": {
            "when_to_move": "بحسب موقعك هلق والزحمة حواليك، استنى 10 دقايق وبعدها تحرك، والمنظمين رح يفتحوا البوابات القريبة منك.",
            "danger_request": f"{calm}بدك كرسي متحرك أو مساعدة طبية؟ وإذا إنت بخطر هلق، توجّه فوراً لأقرب رجال أمن أو منظمين قريبين منك عند المسار القريب من بوابة 16.",
            "route_guidance": f"{calm}بحسب موقعك هلق وتحديثات المنظمين، بوابة 15 وبوابة 7 مسكّرتين حالياً بسبب الزحمة، وبوابة 16 هي الأقرب والأسرع.",
            "hotel_request": "بحسب موقعك هلق، أقرب فندق إلك هو برج الساعة.",
            "wheelchair_or_cart": "بحسب موقعك هلق، أقرب خدمة عربات إلك هي عربة الحرم الكهربائية في منطقة أجياد.",
            "bathroom_request": f"{calm}بحسب موقعك هلق، أقرب حمّام إلك هو دورة المياه رقم 2 عند بوابة 16.",
            "rest_request": f"{calm}بحسب موقعك هلق، أقرب منطقة راحة أقل زحمة قرب المسار الجانبي المؤدي إلى بوابة 16. وإذا بدك، بقدر دلّك كمان على أقرب زمزم.",
            "water_request": "بحسب موقعك هلق، أقرب زمزم إلك عند منطقة الخدمة القريبة من بوابة 16.",
            "vague_request": f"{calm}اعطيني تفاصيل أكتر لحتى أوجّهك صح، لوين بدك تروح بالضبط؟",
            "general_haram": "أنا معك داخل الحرم، احكيلي شو تحتاج بالضبط؟",
        },
    }

    dialect_replies = replies.get(dialect, replies["gulf"])
    return dialect_replies.get(intent, DEFAULT_FALLBACK_REPLY)


def ask_nuha_fast(user_message: str):
    messages = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": user_message}
    ]

    raw_reply = call_nuha(messages)
    if isinstance(raw_reply, dict) and raw_reply.get("error"):
        return None

    try:
        parsed = json.loads(raw_reply)
        return {
            "map_type": parsed.get("map_type", DEFAULT_MAP_TYPE),
            "intent": parsed.get("intent", "general_haram"),
            "emotion": parsed.get("emotion", DEFAULT_EMOTION),
            "dialect": parsed.get("dialect", DEFAULT_DIALECT),
        }
    except Exception:
        return None


def process_chat(user_message: str):
    dialect = detect_dialect(user_message)
    emotion = detect_emotion(user_message)
    intent, map_type = detect_intent_and_map(user_message)

    nuha_result = ask_nuha_fast(user_message)
    if nuha_result:
        if nuha_result["intent"] and nuha_result["intent"] != "general_haram":
            intent = nuha_result["intent"]
        if nuha_result["map_type"] and nuha_result["map_type"] != DEFAULT_MAP_TYPE:
            map_type = nuha_result["map_type"]
        if nuha_result["emotion"]:
            emotion = nuha_result["emotion"]
        if nuha_result["dialect"] in SUPPORTED_DIALECTS:
            dialect = nuha_result["dialect"]

    # Force obvious Gulf back to Gulf
    gulf_markers = ["وين", "وش", "أبغى", "ابي", "الحين", "شلون", "مره", "مرة", "كيف اروح", "كيف أروح", "كيف أوصل", "أقرب"]
    if any(marker in user_message for marker in gulf_markers):
        dialect = "gulf"

    # Force lost tone
    lost_markers = ["ضعت", "ضيعت", "ضايع", "ضايعة", "تايه", "تايهة", "خايف", "خايفة"]
    if any(marker in user_message for marker in lost_markers) and emotion == "calm":
        emotion = "confused"

    final_reply = build_reply(
        dialect=dialect,
        intent=intent,
        map_type=map_type,
        emotion=emotion,
        user_message=user_message,
    )

    map_image = MAP_IMAGE_MAP.get(map_type, DEFAULT_MAP_IMAGE)

    return {
        "map_type": map_type,
        "map_image": map_image,
        "intent": intent,
        "emotion": emotion,
        "dialect": dialect,
        "reply": final_reply,
    }