import json
from rapidfuzz import fuzz


# 📦 Data load
def load_data():
    with open("app/data/knowledge.json", encoding="utf-8") as f:
        return json.load(f)


def smart_match(query: str):
    data = load_data()
    query = query.lower().strip()

    # 🔥 1. CONTAINS MATCH (хамгийн түрүүнд)
    for item in data:
        for keyword in item["keywords"]:
            keyword_clean = keyword.lower().strip()

            # keyword query дотор байвал шууд буцаана
            if keyword_clean in query:
                return item["response"]

    # 🔥 2. EXACT MATCH (backup)
    for item in data:
        for keyword in item["keywords"]:
            if keyword.lower().strip() == query:
                return item["response"]

    # 🔥 3. FUZZY MATCH
    best_score = 0
    best_item = None

    for item in data:
        for keyword in item["keywords"]:
            keyword_lower = keyword.lower().strip()

            score = fuzz.token_sort_ratio(query, keyword_lower)

            # урт keyword bonus
            score += len(keyword_lower)

            # keyword query дотор байвал bonus
            if keyword_lower in query:
                score += 20

            if score > best_score:
                best_score = score
                best_item = item

    # 🔥 4. Threshold багасгасан (80 → 70)
    if best_score > 70 and best_item:
        return best_item["response"]

    return "❌ Мэдээлэл олдсонгүй"