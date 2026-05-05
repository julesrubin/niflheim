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

    quantity is in the unit defined by the embedded ref:
    - food-backed: food.base_unit (g for solids, ml for liquids).
    - recipe-backed: number of servings; client renders "portion" / "portions".
    """

    id: str
    quantity: float
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
    barcode: str = Field(examples=["3017620422003"])
    quantity: float = Field(gt=0, examples=[30.0])


class LoggedRecipeCreate(CamelModel):
    recipe_id: str = Field(examples=["rcp_pasta_carbo"])
    servings: float = Field(gt=0, examples=[1.0])


class LoggedFoodPatch(CamelModel):
    checked: bool | None = Field(default=None, examples=[True])
    quantity: float | None = Field(default=None, gt=0, examples=[45.0])


class BulkDeleteRequest(CamelModel):
    item_ids: list[str] = Field(examples=[["itm_abc", "itm_def"]])


class MoveItemsRequest(CamelModel):
    item_ids: list[str] = Field(examples=[["itm_abc"]])
    to_kind: MealKind
    to_date: str | None = Field(
        default=None,
        description="Target date YYYY-MM-DD; omit to move within the same day.",
        examples=["2026-05-06"],
    )
