"""Open Food Facts client.

Async httpx wrapper over two OFF surfaces:
- product by barcode → `/api/v2/product/{code}` on world.openfoodfacts.org
- name search        → `/search` on search.openfoodfacts.org (search-a-licious,
                       Elasticsearch-backed). v2 /api/search is filter-only and
                       v1 /cgi/search.pl is the legacy MongoDB scan.

The official `openfoodfacts` PyPI package is sync-only; using it from an async
route would block the event loop. Direct httpx calls keep the
`asyncio.gather(cache, off)` pattern in /foods/search async-native.

Rate limits as of 2026 (per IP): 100 req/min product, 10 req/min v1 search.
search-a-licious has no published quota. We don't enforce client-side
throttling — single-user load is well under, and 429 / 5xx map to
OffUnavailable so the route falls back gracefully.
"""

import json
import logging
import re

import httpx

from ..config.constants import OFF_PRODUCT_FIELDS
from ..models.common import NutriScore, ServingUnit
from ..models.food import Food
from ..utils.error import OffUnavailable

logger = logging.getLogger(__name__)

# search-a-licious doesn't return these even when asked for, so we trim them
# from the fields= request to avoid noise.
_SEARCH_FIELDS = (
    ",".join(
        f
        for f in OFF_PRODUCT_FIELDS.split(",")
        if f not in {"product_quantity_unit", "serving_size", "origin_countries"}
    )
    + ",countries_tags"
)


class OffClient:
    def __init__(
        self,
        base_url: str,
        search_base_url: str,
        user_agent: str,
        timeout: float,
        language: str = "fr",
    ) -> None:
        common = {"headers": {"User-Agent": user_agent}, "timeout": timeout}
        self._product_client = httpx.AsyncClient(base_url=base_url, **common)
        self._search_client = httpx.AsyncClient(base_url=search_base_url, **common)
        self._lc = language

    async def get_product(self, barcode: str) -> Food | None:
        """Fetch one product by barcode.

        Returns None when OFF reports the product is missing OR when the
        nutrition data is too incomplete to be useful (we'd rather hide the
        product than log a 0-calorie banana).
        """
        try:
            r = await self._product_client.get(
                f"/api/v2/product/{barcode}",
                params={"lc": self._lc, "fields": OFF_PRODUCT_FIELDS},
            )
        except httpx.HTTPError as exc:
            logger.warning("OFF product fetch failed: %s", exc)
            raise OffUnavailable() from exc

        if r.status_code == 429 or r.status_code >= 500:
            logger.warning("OFF returned %s for barcode %s", r.status_code, barcode)
            raise OffUnavailable()
        if r.status_code != 200:
            # 4xx other than 429 means OFF rejected us (bad UA, auth, malformed
            # request) — not the same as "product missing", which OFF signals via
            # 200 + status:0 below.
            logger.warning(
                "OFF returned unexpected %s for barcode %s",
                r.status_code,
                barcode,
            )
            raise OffUnavailable()

        try:
            data = r.json()
        except json.JSONDecodeError as exc:
            logger.warning("OFF product response was not JSON: %s", exc)
            raise OffUnavailable() from exc
        if data.get("status") != 1 or "product" not in data:
            return None
        return _parse_off_product(data["product"])

    async def search(self, q: str, page_size: int = 50) -> list[Food]:
        """Free-text search via search-a-licious. Skips products with
        incomplete nutrition data."""
        try:
            r = await self._search_client.get(
                "/search",
                params={
                    "q": q,
                    "langs": self._lc,
                    "page_size": page_size,
                    "page": 1,
                    "fields": _SEARCH_FIELDS,
                },
            )
        except httpx.HTTPError as exc:
            logger.warning("OFF search failed: %s", exc)
            raise OffUnavailable() from exc

        if r.status_code == 429 or r.status_code >= 500:
            raise OffUnavailable()
        if r.status_code != 200:
            logger.warning(
                "OFF search returned unexpected %s for q=%r", r.status_code, q
            )
            raise OffUnavailable()

        try:
            hits = r.json().get("hits", [])
        except json.JSONDecodeError as exc:
            logger.warning("OFF search response was not JSON: %s", exc)
            raise OffUnavailable() from exc
        out: list[Food] = []
        for hit in hits:
            food = _parse_off_product(_normalize_search_hit(hit))
            if food is not None:
                out.append(food)
        return out

    async def aclose(self) -> None:
        await self._product_client.aclose()
        await self._search_client.aclose()


# ─── parsing ────────────────────────────────────────────────────────────────

_SERVING_RE = re.compile(r"(\d+(?:[.,]\d+)?)")


def _normalize_search_hit(hit: dict) -> dict:
    """Reshape a search-a-licious hit into the v2 product schema.

    Only two fields differ from /api/v2/product:
    - `brands` is a list of strings instead of a comma-joined string
    - `countries_tags` is a list of `en:france`-style tags rather than the
      `origin_countries` comma-joined string

    Search hits also lack `product_quantity_unit` and `serving_size`, which
    the parser already treats as optional.
    """
    out = dict(hit)
    brands = hit.get("brands")
    if isinstance(brands, list):
        out["brands"] = ", ".join(brands)
    tags = hit.get("countries_tags")
    if isinstance(tags, list) and tags:
        out["origin_countries"] = ", ".join(_pretty_country(t) for t in tags)
    return out


def _pretty_country(tag: str) -> str:
    """`en:france` → `France`, `en:united-kingdom` → `United Kingdom`."""
    body = tag.split(":", 1)[-1] if ":" in tag else tag
    return body.replace("-", " ").title()


def _parse_off_product(p: dict) -> Food | None:
    """Map an OFF product dict to a Food, or None if unusable."""
    barcode = p.get("code")
    if not barcode:
        return None

    nutriments = p.get("nutriments") or {}
    try:
        calories = float(nutriments["energy-kcal_100g"])
        protein = float(nutriments["proteins_100g"])
        carbs = float(nutriments["carbohydrates_100g"])
        fat = float(nutriments["fat_100g"])
    except (KeyError, TypeError, ValueError):
        return None

    name = p.get("product_name_fr") or p.get("product_name") or None
    brands = (p.get("brands") or "").strip()
    brand = brands.split(",")[0].strip() if brands else None

    unit_raw = (p.get("product_quantity_unit") or "g").lower()
    base_unit = ServingUnit.ml if unit_raw in ("ml", "l") else ServingUnit.g

    return Food(
        barcode=str(barcode),
        name=name,
        brand=brand,
        base_unit=base_unit,
        calories=calories,
        protein=protein,
        carbs=carbs,
        fat=fat,
        fiber=_optional_float(nutriments.get("fiber_100g")),
        sugar=_optional_float(nutriments.get("sugars_100g")),
        salt=_optional_float(nutriments.get("salt_100g")),
        serving_size=_parse_serving_size(p.get("serving_size")),
        nutri_score=_parse_nutri_score(p.get("nutrition_grades")),
        origin=_first_csv(p.get("origin_countries")),
        image_url=p.get("image_url"),
    )


def _optional_float(v: object) -> float | None:
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def _parse_serving_size(s: object) -> float | None:
    """Extract the leading number from strings like '25 g' or '250ml'."""
    if not isinstance(s, str):
        return None
    m = _SERVING_RE.search(s)
    if not m:
        return None
    return float(m.group(1).replace(",", "."))


def _parse_nutri_score(s: object) -> NutriScore | None:
    if not isinstance(s, str):
        return None
    s = s.strip().upper()
    try:
        return NutriScore(s)
    except ValueError:
        return None


def _first_csv(s: object) -> str | None:
    if not isinstance(s, str) or not s.strip():
        return None
    return s.split(",")[0].strip() or None
