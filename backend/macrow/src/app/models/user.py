"""Single-user profile + goals DTOs.

Goals are global per-user: editing them retroactively shifts totals on every
historical /journal day. Stats fields (streakDays, scannedCount, etc.) are
deferred — they're derivable from /journal+/foods or tied to integrations
not yet wired.
"""

from pydantic import Field

from .common import CamelModel


class User(CamelModel):
    name: str = ""
    email: str = ""
    age: int = 0
    weight_kg: int = 0
    height_cm: int = 0
    regime: str = ""

    calorie_goal: int = 2600
    protein_goal: float = 130.0
    carbs_goal: float = 320.0
    fat_goal: float = 80.0


class UserPatch(CamelModel):
    """Partial update — only set fields are written."""

    name: str | None = None
    email: str | None = None
    age: int | None = Field(default=None, ge=0)
    weight_kg: int | None = Field(default=None, ge=0)
    height_cm: int | None = Field(default=None, ge=0)
    regime: str | None = None

    calorie_goal: int | None = Field(default=None, ge=0)
    protein_goal: float | None = Field(default=None, ge=0)
    carbs_goal: float | None = Field(default=None, ge=0)
    fat_goal: float | None = Field(default=None, ge=0)
