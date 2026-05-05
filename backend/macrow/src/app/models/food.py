from pydantic import Field

from .common import CamelModel, NutriScore, ServingUnit


class Food(CamelModel):
    """An Open Food Facts product, keyed by barcode.

    All macro values (calories, protein, carbs, fat, fiber, sugar, salt) are
    expressed per 100 of `base_unit` — per 100 g for solids, per 100 ml for
    liquids. Clients compute per-serving values as `value * serving_size / 100`
    when `serving_size` is set.
    """

    barcode: str = Field(examples=["3017620422003"])

    name: str | None = Field(default=None, examples=["Nutella"])
    brand: str | None = Field(default=None, examples=["Ferrero"])

    base_unit: ServingUnit
    calories: float = Field(examples=[539.0])
    protein: float = Field(examples=[6.3])
    carbs: float = Field(examples=[57.5])
    fat: float = Field(examples=[30.9])
    fiber: float | None = Field(default=None, examples=[3.4])
    sugar: float | None = Field(default=None, examples=[56.3])
    salt: float | None = Field(default=None, examples=[0.107])

    serving_size: float | None = Field(default=None, examples=[15.0])

    nutri_score: NutriScore | None = None
    origin: str | None = Field(default=None, examples=["France"])
    image_url: str | None = None


class SourceBreakdown(CamelModel):
    cache: int
    off: int


class FoodSearchResponse(CamelModel):
    items: list[Food]
    total: int
    source_breakdown: SourceBreakdown
