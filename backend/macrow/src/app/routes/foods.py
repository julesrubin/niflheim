"""Food catalog routes — barcode lookup + name search.

The `/foods` resource is a shared OFF-backed cache; not user-mutable.
Persistence and the OFF client land in step 7; for now both endpoints
return the standard 501 envelope to publish the OpenAPI surface.
"""

from enum import StrEnum

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from ..config.constants import (
    DEFAULT_SEARCH_LIMIT,
    MAX_SEARCH_LIMIT,
    MIN_SEARCH_QUERY_LENGTH,
)
from ..models.food import Food, FoodSearchResponse
from ..utils.error import not_implemented

router = APIRouter(prefix="/foods", tags=["foods"])


class SearchSource(StrEnum):
    both = "both"
    cache = "cache"
    off = "off"


@router.get("/search", response_model=FoodSearchResponse)
async def search_foods(
    q: str = Query(
        min_length=MIN_SEARCH_QUERY_LENGTH,
        description="Substring match on name + brand.",
    ),
    source: SearchSource = SearchSource.both,
    limit: int = Query(default=DEFAULT_SEARCH_LIMIT, ge=1, le=MAX_SEARCH_LIMIT),
    offset: int = Query(default=0, ge=0),
) -> JSONResponse:
    return not_implemented()


@router.get("/{barcode}", response_model=Food)
async def get_food_by_barcode(barcode: str) -> JSONResponse:
    return not_implemented()
