import json
import random
import logging
import os
from datetime import datetime
from rapidfuzz import fuzz

# ── Logging setup ──────────────────────────────────────────────
logging.basicConfig(
    filename="app/data/unmatched_queries.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    encoding="utf-8",
)

# ── Cache: load data once at startup ───────────────────────────
_DATA_CACHE: list | None = None

def load_data() -> list:
    global _DATA_CACHE
    if _DATA_CACHE is None:
        path = os.path.join(os.path.dirname(__file__), "../data/knowledge.json")
        with open(path, encoding="utf-8") as f:
            _DATA_CACHE = json.load(f)
    return _DATA_CACHE


def reload_data() -> None:
    """Call this if knowledge.json is updated at runtime."""
    global _DATA_CACHE
    _DATA_CACHE = None
    load_data()


# ── Core matching ───────────────────────────────────────────────
def smart_match(query: str) -> str:
    data = load_data()
    query_clean = query.lower().strip()

    best_score = 0
    best_item = None

    for item in data:
        # Normalize: support both "patterns" and legacy "keywords" keys
        patterns = item.get("patterns") or item.get("keywords") or []

        for pattern in patterns:
            pattern_clean = pattern.lower().strip()

            # Fuzzy similarity
            score = fuzz.token_set_ratio(query_clean, pattern_clean)

            # Bonus: pattern is a substring of the query
            if pattern_clean in query_clean:
                score += 20

            # Bonus: query is a substring of the pattern (very short queries)
            if query_clean in pattern_clean and len(query_clean) >= 3:
                score += 10

            if score > best_score:
                best_score = score
                best_item = item

    # ── Match found ─────────────────────────────────────────────
    if best_score >= 65 and best_item:
        responses = best_item.get("responses") or best_item.get("response")
        if isinstance(responses, list):
            return random.choice(responses)
        return responses

    # ── No match: log for knowledge-base improvement ────────────
    logging.info("UNMATCHED | score=%d | query=%s", best_score, query)
    return (
        "❌ Уучлаарай, таны асуултыг ойлгосонгүй.\n\n"
        "Та дараах байдлаар холбогдоно уу:\n"
        "📞 7507-3000\n"
        "Эсвэл асуултаа дахин өөрөөр бичиж үзнэ үү."
    )