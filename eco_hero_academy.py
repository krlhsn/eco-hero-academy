"""Eco-Hero Academy: a command-line recycling learning game.

Run with: python eco_hero_academy.py
Uses only the Python standard library.
"""
from __future__ import annotations

import json
import os
import random
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable

ASCII_ART = {
    "welcome": r"""
    ✨🌍♻️🌟
      ECO-HERO ACADEMY
      Level Up Your Recycling!
    🌟♻️🌍✨
    """,
    "challenge_start": r"""
    🧠🚀 ECO-CHALLENGE INITIATED! 🚀🧠
       Prove Your Recycling Prowess!
    """,
    "badge_unlocked": "🏆 BADGE UNLOCKED! 🏆",
    "trophy": r"""
        /|\
       / | \
      /  |  \
     |_______|
    _|_|_|_|_|_
     \       /
      \_____/
    """,
}

REGIONAL_RULES = {
    "Eco-City Standard": {
        "plastic": {
            "tip": "Most plastics (1, 2, 5) can be recycled. Rinse well, no plastic bags. Lids *on* bottles.",
            "fun_fact": "Recycling one ton of plastic saves 7,200 kWh of electricity!",
        },
        "paper": {
            "tip": "Newspapers, magazines, mail, cardboard. Greasy pizza boxes, waxed paper, and shredded paper must go in general waste.",
            "fun_fact": "Recycling a 4-foot stack of newspapers saves one tree!",
        },
        "glass": {
            "tip": "Glass bottles and jars. Rinse, and remove lids (they're often different materials). Labels can stay.",
            "fun_fact": "Glass can be recycled infinitely without losing quality!",
        },
        "electronics": {
            "tip": "E-waste is toxic. Find specific drop-off points or certified recyclers. Never in regular bins!",
            "fun_fact": "E-waste is the fastest-growing waste stream; proper recycling prevents pollution.",
        },
    },
    "Greenburg Initiative": {
        "plastic": {
            "tip": "Only plastics #1 and #2. Rinse thoroughly. Lids *off* bottles and discarded.",
            "fun_fact": "Plastic recycling reduces landfill waste significantly!",
        },
        "paper": {
            "tip": "All clean paper products, including shredded paper (bagged). Greasy cardboard must be composted or binned.",
            "fun_fact": "Recycled paper uses 60% less energy to produce than virgin paper.",
        },
        "glass": {
            "tip": "Clear, brown, and green glass accepted. Rinse and ensure no ceramic or pyrex contaminants. Lids *off*.",
            "fun_fact": "Every ton of recycled glass saves 1,300 pounds of sand!",
        },
        "electronics": {
            "tip": "Special community collection events for e-waste occur monthly. Check city website for dates.",
            "fun_fact": "Many old electronics contain valuable rare earth metals that can be recovered.",
        },
    },
}

# General recycling guide. These are educational examples,
# not universal disposal instructions; local programs may differ.
RECYCLING_GUIDE = {
    "plastic": {
        "tip": "Most plastics (bottles, jugs, tubs) can be recycled if clean and have the symbol. Remember to rinse them!",
        "what_not_to_recycle": "Plastic bags, plastic film, Styrofoam, plastic cutlery, toys, or medical waste. These jam machines!",
        "fun_fact": "Plastic can take hundreds of years to decompose in a landfill.",
    },
    "paper": {
        "tip": "Newspapers, magazines, mail, cardboard boxes (flattened), paperboard. Keep them dry!",
        "what_not_to_recycle": "Greasy pizza boxes, paper towels, tissues, coffee cups (often lined with plastic), shredded paper (unless bagged according to local rules).",
        "fun_fact": "Recycling one ton of paper saves 17 trees, 7,000 gallons of water, and 3 cubic yards of landfill space.",
    },
    "glass": {
        "tip": "Glass bottles and jars (food and beverage). Rinse them out. No need to remove labels.",
        "what_not_to_recycle": "Ceramics, Pyrex, window glass, mirrors, light bulbs, drinking glasses. These have different melting points or compositions.",
        "fun_fact": "Glass can be recycled endlessly without losing quality, making it a truly sustainable material!",
    },
    "metal": {
        "tip": "Aluminum cans, steel/tin cans (food and beverage). Rinse them out. Aerosol cans are often accepted if empty.",
        "what_not_to_recycle": "Scrap metal, aluminum foil (unless balled up and very clean), hazardous waste containers, electronics.",
        "fun_fact": "Recycling aluminum saves 95% of the energy compared to making it from raw materials. Enough to power a TV for 3 hours!",
    },
    "electronics": {
        "tip": "Old phones, computers, batteries, TVs. These are 'e-waste' and contain hazardous materials. Never put in regular bins!",
        "what_not_to_recycle": "Anything electronic that's not specifically handled by an e-waste program.",
        "fun_fact": "E-waste is the fastest-growing waste stream in the world. Proper recycling prevents toxic substances like lead and mercury from polluting our environment.",
    },
    "food": {
        "tip": "Compost food waste if possible – it creates nutrient-rich soil! Check if your area has food waste collection.",
        "what_not_to_recycle": "Food scraps should never go into your recycling bin for paper, plastic, glass, or metal. They contaminate recyclables.",
        "fun_fact": "Composting food waste reduces methane gas emissions from landfills, a powerful greenhouse gas.",
    },
    "cardboard": {
        "tip": "Corrugated cardboard boxes (delivery boxes, moving boxes). Flatten them and keep them dry.",
        "what_not_to_recycle": "Greasy pizza boxes, wet cardboard, cardboard with heavy wax coatings.",
        "fun_fact": "Recycling cardboard uses 75% less energy than making new cardboard from virgin pulp.",
    },
    "batteries": {
        "tip": "Most batteries (AA, AAA, C, D, 9V, button cells, rechargeable) should be recycled at special collection points. Never throw in trash!",
        "what_not_to_recycle": "Car batteries (different program), damaged or leaking batteries (handle with extreme care).",
        "fun_fact": "Many batteries contain valuable metals that can be recovered, and harmful chemicals that should not end up in landfills.",
    },
    "clothing": {
        "tip": "Donate usable clothing to charities. For unwearable textiles, check for textile recycling programs in your area.",
        "what_not_to_recycle": "Wet, moldy, or heavily soiled clothing usually cannot be recycled.",
        "fun_fact": "The fashion industry is a major polluter; recycling and reusing clothing reduces its environmental impact.",
    },
}

QUIZ_QUESTIONS = [
    {"type": "tf", "question": "True or False: Greasy pizza boxes can always be recycled with other paper.", "answer": False, "explanation": "Grease contaminates paper, making it non-recyclable. Compost or trash the greasy part!"},
    {"type": "tf", "question": "True or False: All plastics with a recycling symbol are accepted in every curbside recycling program.", "answer": False, "explanation": "Recycling rules vary by location! Always check your local guidelines."},
    {"type": "tf", "question": "True or False: You should rinse glass jars before recycling them.", "answer": True, "explanation": "Rinsing removes food residue that can attract pests and contaminate other recyclables."},
    {"type": "tf", "question": "True or False: Old cell phones can be safely thrown in the regular trash.", "answer": False, "explanation": "E-waste like cell phones contains toxic materials and valuable components; it requires special recycling."},
    {"type": "tf", "question": "True or False: Plastic bags should be put in your curbside recycling bin.", "answer": False, "explanation": "Plastic bags jam recycling machinery. Many grocery stores have special drop-offs for them."},
    {"type": "tf", "question": "True or False: Ceramics and Pyrex dishes can be recycled with glass bottles.", "answer": False, "explanation": "Ceramics and Pyrex have different melting points and compositions than glass bottles, contaminating the batch."},
    {"type": "mc", "question": "Which of these materials is generally NOT accepted in curbside recycling bins?", "options": ["A. Aluminum cans", "B. Glass bottles", "C. Styrofoam cups", "D. Cardboard boxes"], "answer": "C", "explanation": "Styrofoam is notoriously difficult to recycle and rarely accepted in curbside programs."},
    {"type": "mc", "question": "What is the best way to dispose of old batteries?", "options": ["A. Throw them in the trash", "B. Place them in the recycling bin with plastics", "C. Take them to a special battery collection point", "D. Flush them down the toilet"], "answer": "C", "explanation": "Batteries contain hazardous materials and should be recycled at designated collection points."},
    {"type": "mc", "question": "Before recycling plastic bottles, what is the most important step?", "options": ["A. Remove the label", "B. Rinse them out", "C. Flatten them completely", "D. Put the lid back on tightly"], "answer": "B", "explanation": "Rinsing removes food and liquid residue, preventing contamination and odors."},
    {"type": "mc", "question": "Which material can be recycled endlessly without losing quality?", "options": ["A. Plastic", "B. Paper", "C. Glass", "D. Textiles"], "answer": "C", "explanation": "Glass is unique in its ability to be recycled repeatedly without degradation."},
    {"type": "mc", "question": "What is 'e-waste'?", "options": ["A. Everyday trash", "B. Electronic waste like old computers and phones", "C. Organic food scraps", "D. Excess paper waste"], "answer": "B", "explanation": "E-waste refers to discarded electronic devices, which require special handling due to hazardous components."},
]

BADGES = {
    "First Step": {"desc": "Completed your first Eco-Challenge round.", "threshold": {"challenge_rounds": 1}},
    "Recycling Rookie": {"desc": "Scored 3 points in Eco-Challenge.", "threshold": {"challenge_score": 3}},
    "Material Master": {"desc": "Viewed tips for 5 different materials.", "threshold": {"materials_viewed": 5}},
    "Eco-Enthusiast": {"desc": "Played 5 Eco-Challenge rounds.", "threshold": {"challenge_rounds": 5}},
    "Challenge Conqueror": {"desc": "Achieved a perfect score in a 5-question challenge round.", "threshold": {"perfect_challenge": True}},
    "Knowledge Seeker": {"desc": "Used the built-in Eco Advisor 3 times.", "threshold": {"advisor_uses": 3}},
    "Green Guardian": {"desc": "Scored 10 points in Eco-Challenge.", "threshold": {"challenge_score": 10}},
}

# These two named presets are fictional examples retained from the 2025 demo.
REGIONS = tuple(REGIONAL_RULES) + ("General Guide",)
MATERIALS = tuple(RECYCLING_GUIDE)

@dataclass
class UserProfile:
    username: str
    score: int = 0
    highest_score: int = 0
    challenge_rounds_played: int = 0
    materials_viewed: set[str] = field(default_factory=set)
    advisor_uses: int = 0
    badges: set[str] = field(default_factory=set)
    quiz_history: list[dict[str, Any]] = field(default_factory=list)
    current_region: str = "Eco-City Standard"

    def __post_init__(self) -> None:
        self.username = self.username.strip()
        if not self.username:
            raise ValueError("Username cannot be empty.")
        if len(self.username) > 24:
            raise ValueError("Username must be 24 characters or fewer.")
        if any(ord(ch) < 32 for ch in self.username):
            raise ValueError("Username contains unsupported control characters.")
        for name in ("score", "highest_score", "challenge_rounds_played", "advisor_uses"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"{name} must be a non-negative integer.")
        if self.highest_score < self.score:
            self.highest_score = self.score
        self.materials_viewed = set(self.materials_viewed)
        self.badges = set(self.badges)
        self.quiz_history = list(self.quiz_history)

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "highest_score": self.highest_score,
            "challenge_rounds_played": self.challenge_rounds_played,
            "materials_viewed": sorted(self.materials_viewed),
            "advisor_uses": self.advisor_uses,
            "badges": sorted(self.badges),
            "quiz_history": self.quiz_history,
            "current_region": self.current_region,
        }

    @classmethod
    def from_dict(cls, username: str, data: dict[str, Any]) -> "UserProfile":
        if not isinstance(data, dict):
            raise ValueError("Saved profile must be a JSON object.")
        return cls(
            username=username,
            score=data.get("score", 0),
            highest_score=data.get("highest_score", data.get("score", 0)),
            challenge_rounds_played=data.get("challenge_rounds_played", 0),
            materials_viewed=set(data.get("materials_viewed", [])),
            advisor_uses=data.get("advisor_uses", 0),
            badges=set(data.get("badges", [])),
            quiz_history=data.get("quiz_history", []),
            current_region=data.get("current_region", "Eco-City Standard"),
        )

class StorageError(RuntimeError):
    """Raised when profile data cannot safely be read or written."""


class ProfileStore:
    def __init__(self, path: str | Path = "eco_hero_profiles.json") -> None:
        self.path = Path(path)

    def _read_all(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        try:
            raw = self.path.read_text(encoding="utf-8")
            if not raw.strip():
                return {}
            data = json.loads(raw)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise StorageError(
                f"Could not read {self.path}. The file was left untouched; make a backup before repairing it."
            ) from exc
        if not isinstance(data, dict):
            raise StorageError(f"Profile file {self.path} must contain a JSON object.")
        return data

    def _write_all(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_name: str | None = None
        try:
            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=self.path.parent,
                prefix=f".{self.path.name}.", suffix=".tmp", delete=False
            ) as stream:
                temp_name = stream.name
                json.dump(data, stream, indent=2, ensure_ascii=False)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp_name, self.path)
        except OSError as exc:
            if temp_name:
                try:
                    os.unlink(temp_name)
                except OSError:
                    pass
            raise StorageError(f"Could not save profiles to {self.path}.") from exc

    def save(self, profile: UserProfile) -> None:
        data = self._read_all()
        data[profile.username] = profile.to_dict()
        self._write_all(data)

    def load(self, username: str) -> UserProfile | None:
        data = self._read_all()
        stored = data.get(username)
        if stored is None:
            return None
        try:
            return UserProfile.from_dict(username, stored)
        except (TypeError, ValueError) as exc:
            raise StorageError(f"Saved profile '{username}' is invalid.") from exc

    def all_profiles(self) -> list[UserProfile]:
        data = self._read_all()
        profiles: list[UserProfile] = []
        for username, item in data.items():
            try:
                profiles.append(UserProfile.from_dict(username, item))
            except (TypeError, ValueError) as exc:
                raise StorageError(f"Saved profile '{username}' is invalid.") from exc
        return profiles

    def leaderboard(self, limit: int = 10) -> list[UserProfile]:
        if limit < 1:
            raise ValueError("Leaderboard limit must be at least one.")
        profiles = self.all_profiles()
        return sorted(
            profiles,
            key=lambda p: (p.highest_score, p.challenge_rounds_played, p.username.casefold()),
            reverse=True,
        )[:limit]

def get_material_guide(material: str, region: str = "General Guide") -> dict[str, str] | None:
    """Return a copy of the guide, preferring a selected demo preset when present."""
    key = material.strip().casefold()
    canonical = next((name for name in RECYCLING_GUIDE if name.casefold() == key), None)
    if canonical is None:
        return None
    if region in REGIONAL_RULES and canonical in REGIONAL_RULES[region]:
        result = dict(REGIONAL_RULES[region][canonical])
        result["source"] = f"Demonstration preset: {region}"
        result["what_not_to_recycle"] = RECYCLING_GUIDE[canonical]["what_not_to_recycle"]
        return result
    result = dict(RECYCLING_GUIDE[canonical])
    result["source"] = "General guide from the original project"
    return result


_ADVISOR_RULES = (
    (("plastic bag", "plastic bags", "plastic film", "film packaging"), "Plastic bags and film typically cannot go into curbside recycling bins because they can jam machinery. Check whether a dedicated drop-off programme is available locally."),
    (("dirty", "greasy", "food residue", "contaminated"), "Food residue can contaminate recyclable material. Check local guidance for cleaning requirements; some items may need composting or general-waste disposal."),
    (("compost", "food waste", "food scraps"), "Composting can turn suitable food scraps and yard waste into a soil amendment. Check which materials and collection options your local programme accepts."),
    (("battery", "batteries", "old battery"), "Use a designated battery collection or recycling programme. Do not place loose batteries in ordinary recycling unless local instructions explicitly say to do so; damaged batteries need special handling advice."),
    (("electronics", "e-waste", "old phone", "computer disposal"), "Use an appropriate electronic-waste collection or certified recycling programme. Do not put electronics in ordinary recycling bins."),
    (("light bulb", "light bulbs", "fluorescent", "bulbs"), "Light-bulb disposal depends on bulb type and local rules. Fluorescent lamps may contain mercury and should go through an appropriate collection route."),
    (("shredded paper",), "Shredded paper is accepted differently across programmes. Some facilities require it to be bagged or collected separately; check local instructions."),
    (("lid", "lids", "cap", "caps"), "Whether bottle lids should be on or off varies by material and facility. Follow your local programme's instructions rather than assuming one universal rule."),
    (("what can i recycle", "what should i recycle", "recyclable items"), "Commonly collected materials can include clean paper and cardboard, selected plastic containers, glass bottles and jars, and metal cans. Acceptance varies; check your local programme."),
    (("why recycle", "benefits of recycling"), "Recycling can conserve material resources and reduce the need for some virgin raw materials. Its benefits depend on material, collection quality, transport and processing."),
)


def advisor_answer(question: str) -> str:
    """Return a helpful response to a common recycling question."""
    normalized = " ".join(question.casefold().split())
    if not normalized:
        return "Enter a recycling question, or type 'back' to return to the menu."
    for keywords, answer in _ADVISOR_RULES:
        if any(keyword in normalized for keyword in keywords):
            return answer
    for material in RECYCLING_GUIDE:
        if material in normalized:
            guide = get_material_guide(material)
            assert guide is not None
            return f"{material.title()}: {guide['tip']} Local acceptance and preparation rules can differ, so verify with your collection provider."
    return (
        "I can help with common recycling topics such as plastic bags, dirty containers, "
        "composting, batteries, electronics, light bulbs, shredded paper, lids and general recycling. "
        "Try one of those topics or open a material guide."
    )


def build_quiz_round(
    quiz_history: Iterable[dict[str, Any]] = (),
    *,
    question_bank: list[dict[str, Any]] | None = None,
    rng: random.Random | None = None,
    size: int = 5,
) -> list[dict[str, Any]]:
    """Build a round with up to two previously missed questions, then fresh ones."""
    bank = question_bank if question_bank is not None else QUIZ_QUESTIONS
    if size < 1:
        raise ValueError("Round size must be at least one.")
    if len(bank) < size:
        raise ValueError("Question bank must contain at least as many questions as the round size.")
    generator = rng or random.Random()
    by_id = {(q["type"], q["question"]): q for q in bank}
    missed: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for item in quiz_history:
        if not isinstance(item, dict):
            continue
        key = (item.get("type"), item.get("question"))
        if key in by_id and key not in seen:
            missed.append(by_id[key])
            seen.add(key)
    generator.shuffle(missed)
    chosen = missed[: min(2, size)]
    chosen_ids = {(q["type"], q["question"]) for q in chosen}
    fresh = [q for q in bank if (q["type"], q["question"]) not in chosen_ids]
    generator.shuffle(fresh)
    chosen.extend(fresh[: size - len(chosen)])
    generator.shuffle(chosen)
    return [dict(q) for q in chosen]


def grade_answer(question: dict[str, Any], answer: str | bool) -> bool:
    """Check a normalized True/False or A-D answer."""
    if question.get("type") == "tf":
        if isinstance(answer, bool):
            normalized: bool | str = answer
        else:
            value = str(answer).strip().casefold()
            if value in {"t", "true"}:
                normalized = True
            elif value in {"f", "false"}:
                normalized = False
            else:
                return False
        return normalized is question.get("answer")
    if question.get("type") == "mc":
        return str(answer).strip().upper() == str(question.get("answer", "")).upper()
    return False


def record_challenge_result(profile: UserProfile, correct: int, total: int = 5) -> list[str]:
    """Update cumulative score and return newly unlocked badges."""
    if total < 1 or correct < 0 or correct > total:
        raise ValueError("Challenge result must satisfy 0 <= correct <= total and total >= 1.")
    profile.score += correct
    profile.challenge_rounds_played += 1
    profile.highest_score = max(profile.highest_score, profile.score)
    new_badges = check_and_unlock_badges(profile)
    if correct == total and total == 5 and "Challenge Conqueror" not in profile.badges:
        profile.badges.add("Challenge Conqueror")
        new_badges.append("Challenge Conqueror")
    return new_badges


def check_and_unlock_badges(profile: UserProfile) -> list[str]:
    newly_unlocked: list[str] = []
    for name, info in BADGES.items():
        if name in profile.badges:
            continue
        threshold = info["threshold"]
        unlocked = True
        if "challenge_rounds" in threshold:
            unlocked = unlocked and profile.challenge_rounds_played >= threshold["challenge_rounds"]
        if "challenge_score" in threshold:
            unlocked = unlocked and profile.score >= threshold["challenge_score"]
        if "materials_viewed" in threshold:
            unlocked = unlocked and len(profile.materials_viewed) >= threshold["materials_viewed"]
        if "advisor_uses" in threshold:
            unlocked = unlocked and profile.advisor_uses >= threshold["advisor_uses"]
        if threshold.get("perfect_challenge"):
            unlocked = False  # Earned only by a perfect five-question round.
        if unlocked:
            profile.badges.add(name)
            newly_unlocked.append(name)
    return newly_unlocked


def record_material_view(profile: UserProfile, material: str) -> list[str]:
    guide = get_material_guide(material, profile.current_region)
    if guide is None:
        return []
    profile.materials_viewed.add(material.strip().casefold())
    return check_and_unlock_badges(profile)


def record_advisor_use(profile: UserProfile) -> list[str]:
    profile.advisor_uses += 1
    return check_and_unlock_badges(profile)

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

if __name__ == "__main__":
    main()
