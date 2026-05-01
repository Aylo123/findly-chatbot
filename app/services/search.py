import json
from rapidfuzz import fuzz


def load_data():
    with open("app/data/knowledge.json", encoding="utf-8") as f:
        return json.load(f)


def detect_intent(query: str):
    data = load_data()
    query = query.lower().strip()

    best_score = 0
    best_item = None

    for item in data:
        for pattern in item["patterns"]:
            pattern = pattern.lower().strip()

            score = fuzz.token_set_ratio(query, pattern)

            if pattern in query:
                score += 20

            if score > best_score:
                best_score = score
                best_item = item

    if best_score > 65:
        return best_item["response"]

    return " Уучлаарай, Мэдээлэл олдсонгүй 🫂"