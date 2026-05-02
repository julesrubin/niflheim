from datetime import datetime

from .common import CamelModel, NutriScore, ServingUnit


class Food(CamelModel):
    barcode: str

    name: str
    brand: str

    base_unit: ServingUnit
    calories_per_100: float
    protein_per_100: float
    carbs_per_100: float
    fat_per_100: float
    fiber_per_100: float | None = None
    sugar_per_100: float | None = None
    salt_per_100: float | None = None

    serving_size: float | None = None

    nutri_score: NutriScore | None = None
    origin: str | None = None
    image_url: str | None = None

    cached_at: datetime
    refreshed_at: datetime


class SourceBreakdown(CamelModel):
    cache: int
    off: int


class FoodSearchResponse(CamelModel):
    items: list[Food]
    total: int
    source_breakdown: SourceBreakdown
