import tempfile
import unittest
from pathlib import Path
from eco_hero.cli import EcoHeroApp
from eco_hero.models import UserProfile
from eco_hero.storage import ProfileStore


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = ProfileStore(Path(self.temp.name) / "profiles.json")
        self.outputs = []

    def tearDown(self):
        self.temp.cleanup()

    def app_with(self, answers):
        queue = iter(answers)
        return EcoHeroApp(self.store, input_fn=lambda _prompt: next(queue), output_fn=self.outputs.append)

    def test_exit_from_welcome_menu(self):
        app = self.app_with(["2"])
        app.run()
        self.assertFalse(app.running)
        self.assertTrue(any("Goodbye" in line for line in self.outputs))

    def test_create_profile_and_save(self):
        app = self.app_with(["1", "2", "EcoFox", "6", "2"])
        app.run()
        loaded = self.store.load("EcoFox")
        self.assertIsNotNone(loaded)
        self.assertTrue(any("created" in line for line in self.outputs))

    def test_invalid_main_menu_choice_is_reported(self):
        app = EcoHeroApp(self.store, input_fn=lambda _p: "9", output_fn=self.outputs.append)
        app.current_user = UserProfile("Eco")
        app._main_menu()
        self.assertTrue(any("Invalid choice" in line for line in self.outputs))

    def test_general_guide_option_can_be_selected(self):
        app = self.app_with(["5"])
        app.current_user = UserProfile("Eco")
        answers = iter(["3"])
        app.input = lambda _p: next(answers)
        app._change_region()
        self.assertEqual(app.current_user.current_region, "General Guide")


if __name__ == "__main__":
    unittest.main()
