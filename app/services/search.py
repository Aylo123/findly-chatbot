import json
from rapidfuzz import fuzz
import random


def load_data():
    with open("app/data/knowledge.json", encoding="utf-8") as f:
        return json.load(f)


def smart_match(query: str):
    data = load_data()
    query = query.lower().strip()

    best_score = 0
    best_item = None

    for item in data:
        for pattern in item.get("patterns", []):
            pattern = pattern.lower().strip()

            score = fuzz.token_set_ratio(query, pattern)

            if pattern in query:
                score += 20

            if score > best_score:
                best_score = score
                best_item = item

    if best_score > 65 and best_item:
        # 🔥 dynamic response support
        if "responses" in best_item:
            return random.choice(best_item["responses"])
        return best_item["response"]

    return "❌ Уучлаарай, мэдээлэл олдсонгүй"