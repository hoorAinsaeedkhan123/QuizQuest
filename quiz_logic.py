"""Pure-Python quiz logic (no GUI), kept separate so it can be unit tested."""

import json
import random
from pathlib import Path

REQUIRED_QUESTION_KEYS = ("category", "question", "options", "answer", "explanation")
QUESTIONS_PER_ROUND = 10
POINTS_PER_QUESTION = 10
MAX_SAVED_SCORES = 10


def load_json(path, default):
    """Read JSON from `path`; return `default` if it is missing or unreadable."""
    try:
        with Path(path).open("r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


def save_json(path, data):
    """Write JSON atomically so a crash cannot leave a half-written file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    temp.replace(path)


def is_valid_question(q):
    """A question needs all keys, 2+ unique options, and an answer among them."""
    if not isinstance(q, dict) or any(k not in q for k in REQUIRED_QUESTION_KEYS):
        return False
    options = q["options"]
    return (
        isinstance(options, list)
        and len(options) >= 2
        and len(set(options)) == len(options)
        and q["answer"] in options
        and all(isinstance(q[k], str) and q[k].strip()
                for k in ("category", "question", "explanation"))
    )


def clean_questions(raw):
    """Keep only valid questions so one bad entry cannot crash the app."""
    return [q for q in raw if is_valid_question(q)] if isinstance(raw, list) else []


def is_valid_score(item):
    return (
        isinstance(item, dict)
        and all(k in item for k in ("name", "category", "score", "total", "percent", "date"))
        and isinstance(item["score"], int)
        and isinstance(item["total"], int)
        and item["total"] > 0
    )


def clean_scores(raw):
    return [s for s in raw if is_valid_score(s)] if isinstance(raw, list) else []


def pick_round(questions, category, rng=random):
    """Choose up to 10 random questions and shuffle each one's options."""
    pool = questions if category == "All" else [q for q in questions if q["category"] == category]
    chosen = rng.sample(pool, min(QUESTIONS_PER_ROUND, len(pool)))
    round_questions = []
    for q in chosen:
        copy = dict(q)
        copy["options"] = rng.sample(q["options"], len(q["options"]))
        round_questions.append(copy)
    return round_questions


def add_score(scores, entry):
    """Add a score and keep the best ones, ranked by percentage, then points."""
    ranked = sorted(scores + [entry], key=lambda s: (s["percent"], s["score"]), reverse=True)
    return ranked[:MAX_SAVED_SCORES]


def make_score_entry(name, category, score, total, date):
    return {
        "name": name, "category": category, "score": score, "total": total,
        "percent": round(score / total * 100), "date": date,
    }
