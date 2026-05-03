"""Food catalog routes — barcode lookup + name search.

The `/foods` resource is a shared OFF-backed cache; not user-mutable.
Cache hits are served straight from Firestore; misses fall through to the
Open Food Facts API and are lazily cached on the way back.
"""

import asyncio
import logging
from enum import StrEnum

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from ..config.constants import (
    DEFAULT_SEARCH_LIMIT,
    MAX_SEARCH_LIMIT,
    MIN_SEARCH_QUERY_LENGTH,
    OFF_SEARCH_PAGE_SIZE,
)
from ..models.food import Food, FoodSearchResponse, SourceBreakdown
from ..services.food import FoodRepository, resolve_food
from ..services.off import OffClient
from ..utils.error import OffUnavailable, barcode_not_found, off_unavailable

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/foods", tags=["foods"])


class SearchSource(StrEnum):
    both = "both"
    cache = "cache"
    off = "off"


def get_off(request: Request) -> OffClient:
    return request.app.state.off_client


def get_repo(request: Request) -> FoodRepository:
    return request.app.state.food_repo


@router.get("/search", response_model=FoodSearchResponse)
async def search_foods(
    q: str = Query(
        min_length=MIN_SEARCH_QUERY_LENGTH,
        description="Substring match on name + brand.",
    ),
    source: SearchSource = SearchSource.both,
    limit: int = Query(default=DEFAULT_SEARCH_LIMIT, ge=1, le=MAX_SEARCH_LIMIT),
    offset: int = Query(default=0, ge=0),
    off: OffClient = Depends(get_off),
    repo: FoodRepository = Depends(get_repo),
) -> FoodSearchResponse | JSONResponse:
    cache_results: list[Food] = []
    off_results: list[Food] = []

    cache_task = (
        repo.search_by_name_prefix(q, limit + offset)
        if source != SearchSource.off
        else None
    )
    off_task = (
        off.search(q, page_size=OFF_SEARCH_PAGE_SIZE)
        if source != SearchSource.cache
        else None
    )

    tasks = [t for t in (cache_task, off_task) if t is not None]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    idx = 0
    if cache_task is not None:
        r = results[idx]
        idx += 1
        if isinstance(r, BaseException):
            logger.warning("Cache search failed: %s", r)
        else:
            cache_results = r
    if off_task is not None:
        r = results[idx]
        if isinstance(r, OffUnavailable):
            if source == SearchSource.off:
                return off_unavailable()
            logger.warning("OFF search failed; degrading to cache-only")
        elif isinstance(r, BaseException):
            logger.warning("OFF search raised unexpectedly: %s", r)
            if source == SearchSource.off:
                return off_unavailable()
        else:
            off_results = r

    # Merge: cache rows first (we trust them), OFF rows fill the rest.
    # Dedupe by barcode — cache wins on collision.
    cache_barcodes = {f.barcode for f in cache_results}
    merged: list[Food] = list(cache_results)
    for f in off_results:
        if f.barcode not in cache_barcodes:
            merged.append(f)

    page = merged[offset : offset + limit]
    cache_in_page = sum(1 for f in page if f.barcode in cache_barcodes)
    return FoodSearchResponse(
        items=page,
        total=len(merged),
        source_breakdown=SourceBreakdown(
            cache=cache_in_page,
            off=len(page) - cache_in_page,
        ),
    )


@router.get("/{barcode}", response_model=Food)
async def get_food_by_barcode(
    barcode: str,
    off: OffClient = Depends(get_off),
    repo: FoodRepository = Depends(get_repo),
) -> Food | JSONResponse:
    try:
        product = await resolve_food(barcode, repo, off)
    except OffUnavailable:
        return off_unavailable()
    if product is None:
        return barcode_not_found(barcode)
    return product
