"""Daily food journal DTOs.

Storage is normalized: a logged item carries only `{id, barcode, quantity, unit,
checked}`. The `food` field on `LoggedFood` is server-embedded on read by joining
to the foods cache. Custom (no-barcode) entries and per-user goals are out of
scope for this step.
"""

from enum import StrEnum

from pydantic import Field

from .common import CamelModel
from .food import Food


class MealKind(StrEnum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"


class LoggedFood(CamelModel):
    """A single eaten item. `food` is embedded on read; never persisted."""

    id: str
    barcode: str
    quantity: float
    # "g" | "ml" | "portion" | "item"; clients default to food.base_unit when None.
    unit: str | None = None
    checked: bool = False
    food: Food


class Meal(CamelModel):
    kind: MealKind
    items: list[LoggedFood]


class DailyJournal(CamelModel):
    date: str  # YYYY-MM-DD
    meals: list[Meal]  # always 4, ordered breakfast → lunch → dinner → snack


class LoggedFoodCreate(CamelModel):
    barcode: str
    quantity: float = Field(gt=0)
    unit: str | None = None


class LoggedFoodPatch(CamelModel):
    checked: bool | None = None
    quantity: float | None = Field(default=None, gt=0)
    unit: str | None = None


class BulkDeleteRequest(CamelModel):
    item_ids: list[str]


class MoveItemsRequest(CamelModel):
    item_ids: list[str]
    to_kind: MealKind
    to_date: str | None = None  # None = same-day move
