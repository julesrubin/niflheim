from .common import CamelModel, NutriScore, ServingUnit


class Food(CamelModel):
    """An Open Food Facts product, keyed by barcode.

    All macro values (calories, protein, carbs, fat, fiber, sugar, salt) are
    expressed per 100 of `base_unit` — per 100 g for solids, per 100 ml for
    liquids. Clients compute per-serving values as `value * serving_size / 100`
    when `serving_size` is set.
    """

    barcode: str

    name: str
    brand: str

    base_unit: ServingUnit
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: float | None = None
    sugar: float | None = None
    salt: float | None = None

    serving_size: float | None = None

    nutri_score: NutriScore | None = None
    origin: str | None = None
    image_url: str | None = None


class SourceBreakdown(CamelModel):
    cache: int
    off: int


class FoodSearchResponse(CamelModel):
    items: list[Food]
    total: int
    source_breakdown: SourceBreakdown
