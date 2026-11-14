"""Pure game rules: material guides, rule-based advice, quizzes and badges."""
from __future__ import annotations

import random
from typing import Any, Iterable

from .data import BADGES, QUIZ_QUESTIONS, RECYCLING_GUIDE, REGIONAL_RULES
from .models import UserProfile


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
