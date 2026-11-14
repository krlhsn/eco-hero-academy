import unittest
from eco_hero.models import UserProfile


class UserProfileTests(unittest.TestCase):
    def test_round_trip_keeps_sets_and_history(self):
        profile = UserProfile("  Kamrul  ", score=4, highest_score=7,
                              materials_viewed={"plastic", "glass"},
                              badges={"First Step"}, quiz_history=[{"type": "tf", "question": "Q"}])
        restored = UserProfile.from_dict(profile.username, profile.to_dict())
        self.assertEqual(restored.username, "Kamrul")
        self.assertEqual(restored.materials_viewed, {"plastic", "glass"})
        self.assertEqual(restored.badges, {"First Step"})
        self.assertEqual(restored.quiz_history[0]["question"], "Q")

    def test_blank_username_is_rejected(self):
        with self.assertRaises(ValueError):
            UserProfile("  ")

    def test_long_username_is_rejected(self):
        with self.assertRaises(ValueError):
            UserProfile("x" * 25)

    def test_negative_score_is_rejected(self):
        with self.assertRaises(ValueError):
            UserProfile("A", score=-1)

    def test_highest_score_cannot_be_below_current_total(self):
        profile = UserProfile("A", score=8, highest_score=2)
        self.assertEqual(profile.highest_score, 8)

    def test_legacy_ai_advisor_counter_is_supported(self):
        restored = UserProfile.from_dict("Legacy", {"ai_advisor_uses": 3})
        self.assertEqual(restored.advisor_uses, 3)


if __name__ == "__main__":
    unittest.main()
