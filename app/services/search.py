import json
from rapidfuzz import fuzz

# Data load
def load_data():
    with open("app/data/knowledge.json", encoding="utf-8") as f:
        return json.load(f)


def smart_match(query: str):
    data = load_data()
    query = query.lower().strip()

    # 🔥 1. EXACT MATCH (хамгийн түрүүнд шалгана)
    for item in data:
        for keyword in item["keywords"]:
            if keyword.lower() == query:
                return item["response"]

    # 🔥 2. FUZZY MATCH + PRIORITY
    best_score = 0
    best_item = None

    for item in data:
        for keyword in item["keywords"]:
            keyword_lower = keyword.lower()

            # үндсэн оноо
            score = fuzz.token_sort_ratio(query, keyword_lower)

            # 🔥 урт keyword-д бонус (илүү нарийвчлалтай)
            score += len(keyword_lower)

            # 🔥 keyword query дотор байвал нэмэлт оноо
            if keyword_lower in query:
                score += 20

            if score > best_score:
                best_score = score
                best_item = item

    # 🔥 threshold
    if best_score > 80 and best_item:
        return best_item["response"]

    return "❌ Мэдээлэл олдсонгүй"