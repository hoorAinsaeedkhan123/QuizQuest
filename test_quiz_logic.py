import json
import random
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from quiz_logic import (add_score, clean_questions, clean_scores, is_valid_question,
                        load_json, make_score_entry, pick_round, save_json)

QUESTIONS = json.loads((ROOT / "data" / "questions.json").read_text(encoding="utf-8"))


class TestQuestionBank(unittest.TestCase):
    def test_all_questions_valid(self):
        for q in QUESTIONS:
            self.assertTrue(is_valid_question(q), q["question"])

    def test_no_duplicate_questions(self):
        texts = [q["question"] for q in QUESTIONS]
        self.assertEqual(len(texts), len(set(texts)))

    def test_every_category_fills_a_round(self):
        counts = {}
        for q in QUESTIONS:
            counts[q["category"]] = counts.get(q["category"], 0) + 1
        for category, n in counts.items():
            self.assertGreaterEqual(n, 10, category)


class TestLogic(unittest.TestCase):
    def test_pick_round_size_category_and_answer_kept(self):
        for category in ("All", "Python"):
            r = pick_round(QUESTIONS, category, random.Random(1))
            self.assertEqual(len(r), 10)
            for q in r:
                self.assertIn(q["answer"], q["options"])
                if category != "All":
                    self.assertEqual(q["category"], category)

    def test_pick_round_does_not_mutate_bank(self):
        before = json.dumps(QUESTIONS)
        pick_round(QUESTIONS, "All", random.Random(2))
        self.assertEqual(before, json.dumps(QUESTIONS))

    def test_clean_questions_drops_bad_entries(self):
        bad = [{"category": "x"}, "oops", dict(QUESTIONS[0], answer="nope")]
        self.assertEqual(clean_questions(bad + [QUESTIONS[0]]), [QUESTIONS[0]])
        self.assertEqual(clean_questions({"not": "a list"}), [])

    def test_scores_ranked_by_percent_and_capped(self):
        scores = []
        for i in range(15):
            scores = add_score(scores, make_score_entry("a", "All", i * 10 % 100, 100, "d"))
        self.assertEqual(len(scores), 10)
        percents = [s["percent"] for s in scores]
        self.assertEqual(percents, sorted(percents, reverse=True))
        # a perfect 5-question round (50/50) must outrank 60/100
        ranked = add_score([make_score_entry("a", "All", 60, 100, "d")],
                           make_score_entry("b", "Py", 50, 50, "d"))
        self.assertEqual(ranked[0]["name"], "b")

    def test_clean_scores_ignores_garbage(self):
        self.assertEqual(clean_scores([{"name": "x"}, 5]), [])

    def test_json_roundtrip_and_fallbacks(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "sub" / "s.json"
            self.assertEqual(load_json(p, []), [])
            save_json(p, [{"a": 1}])
            self.assertEqual(load_json(p, []), [{"a": 1}])
            p.write_text("{broken", encoding="utf-8")
            self.assertEqual(load_json(p, "fallback"), "fallback")


if __name__ == "__main__":
    unittest.main()
