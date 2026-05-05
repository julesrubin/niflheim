"""Single-user profile + goals DTOs.

Goals are global per-user: editing them retroactively shifts totals on every
historical /journal day. Stats fields (streakDays, scannedCount, etc.) are
deferred — they're derivable from /journal+/foods or tied to integrations
not yet wired.
"""

from pydantic import EmailStr, Field, field_validator

from .common import CamelModel


def _empty_to_none(v: object) -> object:
    """Coerce '' to None — historical user docs serialized email='' as the
    empty-string default, and that doesn't validate as EmailStr on re-read."""
    return None if v == "" else v


class User(CamelModel):
    name: str = Field(default="", examples=["Jules"])
    email: EmailStr | None = Field(default=None, examples=["jules@example.com"])
    age: int = Field(default=0, examples=[28])
    weight_kg: int = Field(default=0, examples=[78])
    height_cm: int = Field(default=0, examples=[180])
    regime: str = Field(default="", examples=["high-protein"])

    calorie_goal: int = Field(default=2600, examples=[2600])
    protein_goal: float = Field(default=130.0, examples=[130.0])
    carbs_goal: float = Field(default=320.0, examples=[320.0])
    fat_goal: float = Field(default=80.0, examples=[80.0])

    _empty_email_to_none = field_validator("email", mode="before")(_empty_to_none)


class UserPatch(CamelModel):
    """Partial update — only set fields are written."""

    name: str | None = Field(default=None, examples=["Jules"])
    email: EmailStr | None = Field(default=None, examples=["jules@example.com"])
    age: int | None = Field(default=None, ge=0, examples=[28])
    weight_kg: int | None = Field(default=None, ge=0, examples=[78])
    height_cm: int | None = Field(default=None, ge=0, examples=[180])
    regime: str | None = Field(default=None, examples=["high-protein"])

    calorie_goal: int | None = Field(default=None, ge=0, examples=[2600])
    protein_goal: float | None = Field(default=None, ge=0, examples=[130.0])
    carbs_goal: float | None = Field(default=None, ge=0, examples=[320.0])
    fat_goal: float | None = Field(default=None, ge=0, examples=[80.0])

    _empty_email_to_none = field_validator("email", mode="before")(_empty_to_none)
