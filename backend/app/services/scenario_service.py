def get_prototype_result(intent: str, map_type: str) -> dict:
    if intent == "route_guidance" or map_type == "doors":
        return {
            "destination_name": "بوابة 16",
            "details": "بحسب موقع المستخدم الحالي وتحديثات المنظمين، بوابة 15 وبوابة 7 مغلقتان حالياً بسبب الزحام، وبوابة 16 هي الأقرب والأسرع."
        }

    if intent == "when_to_move":
        return {
            "destination_name": "الانتظار 10 دقائق",
            "details": "بناءً على موقع المستخدم الحالي والزحام حوله الآن، الأفضل الانتظار 10 دقائق ثم التحرك عند فتح البوابات القريبة من المنظمين."
        }

    if intent == "hotel_request" or map_type == "hotels":
        return {
            "destination_name": "برج الساعة",
            "details": "بحسب موقع المستخدم الحالي، برج الساعة هو أقرب فندق له الآن."
        }

    if intent == "wheelchair_or_cart" or map_type == "cars_wheelchairs":
        return {
            "destination_name": "عربة الحرم الكهربائية في منطقة أجياد",
            "details": "بحسب موقع المستخدم الحالي، هذه أقرب خدمة عربات متاحة الآن، وهي في منطقة أجياد وقريبة من بوابة 16."
        }

    if intent == "bathroom_request" or map_type == "bathrooms":
        return {
            "destination_name": "دورة المياه رقم 2 عند بوابة 16",
            "details": "بحسب موقع المستخدم الحالي، هذه أقرب دورة مياه متاحة الآن."
        }

    if intent == "rest_request":
        return {
            "destination_name": "منطقة الراحة الأقرب غير المزدحمة",
            "details": "بحسب موقع المستخدم الحالي والزحام حوله، أقرب منطقة راحة أقل ازدحاماً تقع قرب المسار الجانبي المؤدي إلى بوابة 16."
        }

    if intent == "water_request":
        return {
            "destination_name": "أقرب نقطة زمزم",
            "details": "بحسب موقع المستخدم الحالي، أقرب نقطة زمزم تقع قرب منطقة الخدمة المجاورة لبوابة 16."
        }

    if intent == "danger_request":
        return {
            "destination_name": "أقرب رجال الأمن أو المنظمين",
            "details": "بحسب موقع المستخدم الحالي، يجب التوجه فوراً إلى أقرب رجال أمن أو منظمين موجودين عند المسار القريب من بوابة 16."
        }

    return {
        "destination_name": "الحرم",
        "details": "سؤال عام متعلق بالحرم."
    }