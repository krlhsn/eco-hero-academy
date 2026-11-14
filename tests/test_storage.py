import json
import tempfile
import unittest
from pathlib import Path
from eco_hero.models import UserProfile
from eco_hero.storage import ProfileStore, StorageError


class ProfileStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "nested" / "profiles.json"
        self.store = ProfileStore(self.path)

    def tearDown(self):
        self.temp.cleanup()

    def test_save_and_load_profile(self):
        profile = UserProfile("EcoFox", score=3, challenge_rounds_played=2)
        self.store.save(profile)
        loaded = self.store.load("EcoFox")
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.score, 3)
        self.assertEqual(loaded.challenge_rounds_played, 2)

    def test_missing_profile_returns_none(self):
        self.assertIsNone(self.store.load("Nobody"))

    def test_save_preserves_other_profiles(self):
        self.store.save(UserProfile("One", score=2))
        self.store.save(UserProfile("Two", score=4))
        self.assertEqual(len(self.store.all_profiles()), 2)

    def test_leaderboard_sorts_by_personal_best(self):
        self.store.save(UserProfile("Low", score=2, highest_score=2))
        self.store.save(UserProfile("High", score=5, highest_score=9))
        self.assertEqual(self.store.leaderboard()[0].username, "High")

    def test_corrupt_file_is_not_overwritten(self):
        self.path.parent.mkdir(parents=True)
        self.path.write_text("{broken", encoding="utf-8")
        with self.assertRaises(StorageError):
            self.store.save(UserProfile("Safe"))
        self.assertEqual(self.path.read_text(encoding="utf-8"), "{broken")

    def test_invalid_json_shape_is_rejected(self):
        self.path.parent.mkdir(parents=True)
        self.path.write_text("[]", encoding="utf-8")
        with self.assertRaises(StorageError):
            self.store.all_profiles()

    def test_persisted_json_is_valid(self):
        self.store.save(UserProfile("JSON"))
        self.assertEqual(json.loads(self.path.read_text(encoding="utf-8"))["JSON"]["score"], 0)


if __name__ == "__main__":
    unittest.main()
