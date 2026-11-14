"""Interactive terminal interface for Eco-Hero Academy."""
from __future__ import annotations

from typing import Callable

from .data import ASCII_ART, BADGES, REGIONS
from .engine import (
    advisor_answer, build_quiz_round, get_material_guide, grade_answer,
    record_advisor_use, record_challenge_result, record_material_view,
)
from .models import UserProfile
from .storage import ProfileStore, StorageError

Input = Callable[[str], str]
Output = Callable[[str], None]


class EcoHeroApp:
    def __init__(self, store: ProfileStore | None = None, input_fn: Input = input, output_fn: Output = print) -> None:
        self.store = store or ProfileStore()
        self.input = input_fn
        self.output = output_fn
        self.current_user: UserProfile | None = None
        self.running = True

    def run(self) -> None:
        self.output(ASCII_ART["welcome"])
        while self.running:
            if self.current_user is None:
                self._profile_menu()
            else:
                self._main_menu()

    def _profile_menu(self) -> None:
        self.output("\n--- Welcome, Eco-Hero! ---")
        self.output("1. Manage Profiles (Load/Create/Leaderboard)")
        self.output("2. Exit Application")
        choice = self.input("Enter your choice: ").strip()
        if choice == "1":
            self._manage_profiles()
        elif choice == "2":
            self.output("Thank you for being an Eco-Hero! Protecting our planet starts with you. Goodbye!")
            self.running = False
        else:
            self.output("Invalid choice. Please enter 1 or 2.")

    def _manage_profiles(self) -> None:
        while self.running and self.current_user is None:
            self.output("\n--- Profile Management ---")
            self.output("1. Load Existing Profile")
            self.output("2. Create New Profile")
            self.output("3. View Leaderboard")
            self.output("4. Back to Main Menu")
            choice = self.input("Enter your choice: ").strip()
            try:
                if choice == "1":
                    username = self.input("Enter username to load: ").strip()
                    self.current_user = self.store.load(username)
                    if self.current_user:
                        self.output(f"Welcome back, {username}! Loading your progress...")
                        self._announce_badges([])
                    else:
                        self.output("Profile not found. Please try again or create a new one.")
                elif choice == "2":
                    username = self.input("Enter a new username: ").strip()
                    if self.store.load(username):
                        self.output("A profile with that username already exists. Choose another name or load it.")
                        continue
                    self.current_user = UserProfile(username)
                    self.store.save(self.current_user)
                    self.output(f"Profile '{username}' created!")
                elif choice == "3":
                    self._show_leaderboard()
                elif choice == "4":
                    return
                else:
                    self.output("Invalid choice. Please enter 1, 2, 3, or 4.")
            except (ValueError, StorageError) as exc:
                self.output(f"Could not complete that profile action: {exc}")

    def _main_menu(self) -> None:
        assert self.current_user is not None
        profile = self.current_user
        self.output(f"\n--- Main Menu (Eco-Hero: {profile.username}) ---")
        for line in (
            "1. Get Recycling Tip", "2. Take the Eco-Challenge!",
            "3. Ask Eco Advisor", "4. View My Profile & Badges",
            "5. Change My Recycling Region", "6. Save & Log Out",
            "7. Exit Application (without saving)",
        ):
            self.output(line)
        choice = self.input("Enter your choice: ").strip()
        actions = {
            "1": self._get_tip, "2": self._challenge, "3": self._advisor,
            "4": self._show_profile, "5": self._change_region,
            "6": self._save_and_logout, "7": self._exit_without_saving,
        }
        action = actions.get(choice)
        if action:
            action()
        else:
            self.output("Invalid choice. Please enter a number from 1 to 7.")

    def _announce_badges(self, names: list[str]) -> None:
        for name in names:
            self.output(ASCII_ART["badge_unlocked"])
            self.output(f"{name}: {BADGES[name]['desc']}")
            self.output(ASCII_ART["trophy"])

    def _get_tip(self) -> None:
        profile = self.current_user
        assert profile is not None
        material = self.input("Enter a material (e.g., plastic, glass, electronics, batteries, clothing): ").strip().casefold()
        guide = get_material_guide(material, profile.current_region)
        if guide is None:
            self.output("Sorry, we don't have detailed information on that material. Try another!")
            return
        self._announce_badges(record_material_view(profile, material))
        self.output(f"\n--- {material.title()} Recycling Guide ({profile.current_region}) ---")
        self.output(f"Tip: {guide['tip']}")
        if "what_not_to_recycle" in guide:
            self.output(f"What NOT to recycle: {guide['what_not_to_recycle']}")
        self.output(f"Fun fact: {guide['fun_fact']}")
        self.output(f"Content note: {guide['source']}. Verify local instructions before disposal.")

    def _challenge(self) -> None:
        profile = self.current_user
        assert profile is not None
        self.output(ASCII_ART["challenge_start"])
        questions = build_quiz_round(profile.quiz_history)
        profile.quiz_history = []
        correct = 0
        for index, question in enumerate(questions, start=1):
            self.output(f"\n--- Question {index}/{len(questions)} ---")
            self.output(question["question"])
            if question["type"] == "tf":
                while True:
                    answer = self.input("Enter 'T' for True or 'F' for False: ").strip().upper()
                    if answer in {"T", "F"}:
                        break
                    self.output("Invalid input. Please enter T or F.")
            else:
                for option in question["options"]:
                    self.output(option)
                while True:
                    answer = self.input("Enter your choice (A, B, C, D): ").strip().upper()
                    if answer in {"A", "B", "C", "D"}:
                        break
                    self.output("Invalid input. Please enter A, B, C, or D.")
            if grade_answer(question, answer):
                self.output("Correct! You're an Eco-Hero!")
                correct += 1
            else:
                self.output("Incorrect. Don't worry, every mistake is a learning opportunity!")
                self.output(f"Explanation: {question['explanation']}")
                profile.quiz_history.append(question)
        new_badges = record_challenge_result(profile, correct, len(questions))
        self._announce_badges(new_badges)
        self.output("\n--- Challenge Summary ---")
        self.output(f"You got {correct} out of {len(questions)} questions correct!")
        self.output(f"Your total score: {profile.score}")
        self.output(f"Rounds played: {profile.challenge_rounds_played}")

    def _advisor(self) -> None:
        profile = self.current_user
        assert profile is not None
        self._announce_badges(record_advisor_use(profile))
        self.output("\n--- Eco Advisor ---")
        self.output("Ask about common recycling questions. Type 'back' to return to the main menu.")
        while True:
            question = self.input("Your question: ").strip()
            if question.casefold() == "back":
                self.output("Returning to main menu.")
                return
            self.output(f"Advisor: {advisor_answer(question)}")

    def _show_profile(self) -> None:
        profile = self.current_user
        assert profile is not None
        self.output("\n--- Your Eco-Hero Profile ---")
        self.output(f"Username: {profile.username}")
        self.output(f"Current Score: {profile.score}")
        self.output(f"Highest Score: {profile.highest_score}")
        self.output(f"Eco-Challenge Rounds Played: {profile.challenge_rounds_played}")
        self.output(f"Materials Viewed: {len(profile.materials_viewed)}")
        self.output(f"Eco Advisor Uses: {profile.advisor_uses}")
        self.output(f"Current Region Setting: {profile.current_region}")
        self.output("\n--- Your Badges ---")
        if not profile.badges:
            self.output("No badges unlocked yet! Keep learning and challenging yourself!")
        for badge in sorted(profile.badges):
            self.output(f"- {badge}: {BADGES[badge]['desc']}")

    def _show_leaderboard(self) -> None:
        try:
            entries = self.store.leaderboard(10)
        except StorageError as exc:
            self.output(f"Could not load leaderboard: {exc}")
            return
        self.output("\n--- Eco-Hero Leaderboard (this device) ---")
        if not entries:
            self.output("No profiles found yet. Be the first Eco-Hero!")
            return
        self.output(f"{'Rank':<5}{'Username':<25}{'High Score':<12}{'Rounds':<8}")
        self.output("-" * 50)
        for index, entry in enumerate(entries, start=1):
            self.output(f"{index:<5}{entry.username:<25}{entry.highest_score:<12}{entry.challenge_rounds_played:<8}")

    def _change_region(self) -> None:
        profile = self.current_user
        assert profile is not None
        self.output("\n--- Select a Recycling Guide Preset ---")
        self.output("The named presets below are fictional demo scenarios, not real municipal rules.")
        for index, region in enumerate(REGIONS, start=1):
            self.output(f"{index}. {region}")
        while True:
            answer = self.input(f"Enter number (1-{len(REGIONS)}): ").strip()
            try:
                choice = int(answer)
            except ValueError:
                self.output("Invalid input. Please enter a number.")
                continue
            if 1 <= choice <= len(REGIONS):
                profile.current_region = REGIONS[choice - 1]
                self.output(f"Guide preset is now: {profile.current_region}")
                return
            self.output("Invalid number. Please choose one from the list.")

    def _save_and_logout(self) -> None:
        assert self.current_user is not None
        try:
            self.store.save(self.current_user)
        except StorageError as exc:
            self.output(f"Could not save profile: {exc}")
            return
        self.output(f"Profile '{self.current_user.username}' saved. Logged out.")
        self.current_user = None

    def _exit_without_saving(self) -> None:
        self.output("Exiting without saving the current session's progress.")
        self.output("Thank you for being an Eco-Hero. Goodbye!")
        self.current_user = None
        self.running = False


def main() -> None:
    EcoHeroApp().run()
