"""Recipe DTOs.

Recipes are user-authored multi-ingredient compositions. Ingredients reference
the foods cache by barcode + quantity (in the food's base unit — g for solids,
ml for liquids). Custom (no-barcode) ingredients are deferred, matching the
`/journal` constraint.

Per-serving macros (calories, protein, carbs, fat) are NOT stored — they're
server-derived on read by joining ingredients to the foods cache and dividing
by servings. Food is the single source of truth; a recipe inherits whatever
macros the cache currently reports for its ingredients, so updates propagate
automatically and the recipe doc can never drift.
"""

from pydantic import Field

from .common import CamelModel


class RecipeIngredient(CamelModel):
    barcode: str = Field(examples=["3017620422003"])
    quantity: float = Field(gt=0, examples=[120.0])


class Recipe(CamelModel):
    id: str = Field(examples=["rcp_pasta_carbo"])
    name: str = Field(examples=["Pâtes carbonara"])
    servings: int = Field(default=2, ge=1, examples=[2])
    duration_minutes: int | None = Field(default=None, ge=0, examples=[20])
    difficulty: str = Field(default="Facile", examples=["Facile"])
    emoji: str = Field(default="", examples=[""])
    thumb_bg: str = Field(default="", examples=["#F4E1C1"])
    ingredients: list[RecipeIngredient] = Field(default_factory=list)
    cooked: bool = False

    # Server-computed from ingredients × Food.macro / 100, divided by servings.
    # Defaults are placeholders — the route layer overwrites these via
    # services.recipe.compute_macros after the recipe is fetched.
    calories_per_serving: int = 0
    protein_per_serving: float = 0.0
    carbs_per_serving: float = 0.0
    fat_per_serving: float = 0.0

    # False when one or more ingredient barcodes are missing from the foods
    # cache; the macros above exclude that ingredient's contribution. Lets the
    # client render "approx" or warn the user to scan the missing ingredient.
    nutrition_complete: bool = True


class RecipeCreate(CamelModel):
    name: str = Field(examples=["Pâtes carbonara"])
    servings: int = Field(default=2, ge=1, examples=[2])
    duration_minutes: int | None = Field(default=None, ge=0, examples=[20])
    difficulty: str = Field(default="Facile", examples=["Facile"])
    emoji: str = Field(default="", examples=[""])
    thumb_bg: str = Field(default="", examples=["#F4E1C1"])
    ingredients: list[RecipeIngredient] = Field(default_factory=list)
    cooked: bool = False


class RecipePatch(CamelModel):
    name: str | None = None
    servings: int | None = Field(default=None, ge=1)
    duration_minutes: int | None = Field(default=None, ge=0)
    difficulty: str | None = None
    emoji: str | None = None
    thumb_bg: str | None = None
    ingredients: list[RecipeIngredient] | None = None
    cooked: bool | None = None
