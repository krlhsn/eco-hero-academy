"""Validated profile model for local Eco-Hero progress."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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
            advisor_uses=data.get("advisor_uses", data.get("ai_advisor_uses", 0)),
            badges=set(data.get("badges", [])),
            quiz_history=data.get("quiz_history", []),
            current_region=data.get("current_region", "Eco-City Standard"),
        )
