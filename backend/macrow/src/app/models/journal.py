"""Daily food journal DTOs.

Storage is normalized: a logged item carries only `{id, barcode?, recipe_id?,
quantity, unit, checked}` — exactly one of `barcode` / `recipe_id` is set. The
`food` and `recipe` fields are server-embedded on read by joining to the foods
cache and the recipes collection. Custom (no-barcode, no-recipe) entries and
per-user goals are out of scope for this step.
"""

from enum import StrEnum

from pydantic import Field

from .common import CamelModel
from .food import Food
from .recipe import Recipe


class MealKind(StrEnum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"


class LoggedFood(CamelModel):
    """A single eaten item — either food-backed (barcode + food) or recipe-backed
    (recipe_id + recipe). Exactly one ref is set; both are optional in the DTO so
    the same shape carries both kinds of entries.
    """

    id: str
    quantity: float
    # "g" | "ml" | "portion" | "item"; clients default to food.base_unit when None.
    unit: str | None = None
    checked: bool = False
    barcode: str | None = None
    food: Food | None = None
    recipe_id: str | None = None
    recipe: Recipe | None = None


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


class LoggedRecipeCreate(CamelModel):
    recipe_id: str
    servings: float = Field(gt=0)


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
