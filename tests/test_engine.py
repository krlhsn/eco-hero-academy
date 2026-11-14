import random
import unittest
from eco_hero.data import BADGES, QUIZ_QUESTIONS, RECYCLING_GUIDE
from eco_hero.engine import (
    advisor_answer, build_quiz_round, check_and_unlock_badges, get_material_guide,
    grade_answer, record_advisor_use, record_challenge_result, record_material_view,
)
from eco_hero.models import UserProfile


class GuideTests(unittest.TestCase):
    def test_material_lookup_is_case_insensitive(self):
        self.assertEqual(get_material_guide(" PLASTIC ")["tip"], RECYCLING_GUIDE["plastic"]["tip"])

    def test_unknown_material_returns_none(self):
        self.assertIsNone(get_material_guide("moon dust"))

    def test_demo_region_overrides_material_tip(self):
        guide = get_material_guide("plastic", "Greenburg Initiative")
        self.assertIn("Only plastics #1 and #2", guide["tip"])
        self.assertIn("Demonstration preset", guide["source"])

    def test_general_region_uses_original_guide(self):
        guide = get_material_guide("paper", "General Guide")
        self.assertIn("Keep them dry", guide["tip"])
        self.assertIn("what_not_to_recycle", guide)


class AdvisorTests(unittest.TestCase):
    def test_known_questions_return_topic_specific_answers(self):
        self.assertIn("jam machinery", advisor_answer("What about plastic bags?"))
        self.assertIn("battery collection", advisor_answer("Where do batteries go?"))
        self.assertIn("Composting", advisor_answer("Tell me about composting"))

    def test_empty_question_is_handled(self):
        self.assertIn("Enter a recycling question", advisor_answer("  "))

    def test_unknown_question_explains_supported_topics(self):
        self.assertIn("I can help with common recycling topics", advisor_answer("Can you explain quantum gravity?"))


class QuizTests(unittest.TestCase):
    def test_round_has_requested_number_of_unique_questions(self):
        questions = build_quiz_round(rng=random.Random(1), size=5)
        self.assertEqual(len(questions), 5)
        self.assertEqual(len({q["question"] for q in questions}), 5)

    def test_round_revisits_up_to_two_missed_questions(self):
        history = QUIZ_QUESTIONS[:4]
        questions = build_quiz_round(history, rng=random.Random(5), size=5)
        question_texts = {q["question"] for q in questions}
        self.assertEqual(len(question_texts.intersection(q["question"] for q in history)), 2)

    def test_too_small_bank_is_rejected(self):
        with self.assertRaises(ValueError):
            build_quiz_round(question_bank=QUIZ_QUESTIONS[:2], size=5)

    def test_true_false_grading_accepts_common_forms(self):
        q = QUIZ_QUESTIONS[2]
        self.assertTrue(grade_answer(q, "T"))
        self.assertTrue(grade_answer(q, "true"))
        self.assertFalse(grade_answer(q, "F"))

    def test_multiple_choice_grading_is_case_insensitive(self):
        q = next(q for q in QUIZ_QUESTIONS if q["type"] == "mc")
        self.assertTrue(grade_answer(q, q["answer"].lower()))
        self.assertFalse(grade_answer(q, "Z"))


class AchievementTests(unittest.TestCase):
    def test_material_master_unlocks_after_five_distinct_materials(self):
        profile = UserProfile("Eco")
        for material in list(RECYCLING_GUIDE)[:5]:
            record_material_view(profile, material)
        self.assertIn("Material Master", profile.badges)

    def test_knowledge_seeker_unlocks_after_three_advisor_uses(self):
        profile = UserProfile("Eco")
        for _ in range(3):
            record_advisor_use(profile)
        self.assertIn("Knowledge Seeker", profile.badges)

    def test_perfect_round_unlocks_conqueror(self):
        profile = UserProfile("Eco")
        new = record_challenge_result(profile, 5, 5)
        self.assertIn("Challenge Conqueror", new)
        self.assertEqual(profile.score, 5)

    def test_non_perfect_round_does_not_unlock_conqueror(self):
        profile = UserProfile("Eco")
        record_challenge_result(profile, 4, 5)
        self.assertNotIn("Challenge Conqueror", profile.badges)

    def test_score_threshold_badges_unlock(self):
        profile = UserProfile("Eco")
        record_challenge_result(profile, 5, 5)
        record_challenge_result(profile, 5, 5)
        self.assertIn("Recycling Rookie", profile.badges)
        self.assertIn("Green Guardian", profile.badges)

    def test_invalid_challenge_result_is_rejected(self):
        with self.assertRaises(ValueError):
            record_challenge_result(UserProfile("Eco"), 6, 5)


if __name__ == "__main__":
    unittest.main()
