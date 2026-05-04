"""Recipe DTOs.

Recipes are user-authored multi-ingredient compositions. iOS today carries only
`caloriesPerServing` (no protein/carbs/fat breakdown); the model leaves room for
those when iOS gains them.

Ingredients reference the foods cache by barcode + quantity (in the food's base
unit — g for solids, ml for liquids). Custom (no-barcode) ingredients are
deferred, matching the `/journal` constraint.
"""

from pydantic import Field

from .common import CamelModel


class RecipeIngredient(CamelModel):
    barcode: str
    quantity: float = Field(gt=0)


class Recipe(CamelModel):
    id: str
    name: str
    servings: int = Field(default=2, ge=1)
    duration_minutes: int | None = Field(default=None, ge=0)
    difficulty: str = "Facile"
    emoji: str = ""
    thumb_bg: str = ""
    ingredients: list[RecipeIngredient] = []
    cooked: bool = False
    calories_per_serving: int = Field(default=0, ge=0)


class RecipeCreate(CamelModel):
    name: str
    servings: int = Field(default=2, ge=1)
    duration_minutes: int | None = Field(default=None, ge=0)
    difficulty: str = "Facile"
    emoji: str = ""
    thumb_bg: str = ""
    ingredients: list[RecipeIngredient] = []
    cooked: bool = False
    calories_per_serving: int = Field(default=0, ge=0)


class RecipePatch(CamelModel):
    name: str | None = None
    servings: int | None = Field(default=None, ge=1)
    duration_minutes: int | None = Field(default=None, ge=0)
    difficulty: str | None = None
    emoji: str | None = None
    thumb_bg: str | None = None
    ingredients: list[RecipeIngredient] | None = None
    cooked: bool | None = None
    calories_per_serving: int | None = Field(default=None, ge=0)
