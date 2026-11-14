"""Atomic JSON persistence for local profiles and the local leaderboard."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .models import UserProfile


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
