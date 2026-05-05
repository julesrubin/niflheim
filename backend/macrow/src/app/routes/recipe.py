"""Recipe CRUD routes.

Five endpoints over a single Firestore collection. Per-serving macros are
server-derived on every read — see `services.recipe.compute_macros`. Each
write endpoint joins ingredient foods after the storage call so the response
already carries the freshly-computed totals.
"""

import logging

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from ..models.recipe import Recipe, RecipeCreate, RecipePatch
from ..services.food import FoodRepository
from ..services.recipe import RecipeRepository, compute_macros
from ..utils.error import ERR_404, RecipeNotFound, recipe_not_found
from .deps import get_food_repo, get_recipe_repo

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recipes", tags=["recipes"])


async def _decorate(recipe: Recipe, foods: FoodRepository) -> Recipe:
    food_map = await foods.get_many([i.barcode for i in recipe.ingredients])
    return compute_macros(recipe, food_map)


async def _decorate_many(recipes: list[Recipe], foods: FoodRepository) -> list[Recipe]:
    barcodes = list({i.barcode for r in recipes for i in r.ingredients})
    food_map = await foods.get_many(barcodes)
    return [compute_macros(r, food_map) for r in recipes]


@router.post("", response_model=Recipe, status_code=201, summary="Create a recipe")
async def create_recipe(
    body: RecipeCreate,
    repo: RecipeRepository = Depends(get_recipe_repo),
    foods: FoodRepository = Depends(get_food_repo),
) -> Recipe:
    recipe = await repo.create(body)
    return await _decorate(recipe, foods)


@router.get("", response_model=list[Recipe], summary="List all recipes")
async def list_recipes(
    repo: RecipeRepository = Depends(get_recipe_repo),
    foods: FoodRepository = Depends(get_food_repo),
) -> list[Recipe]:
    recipes = await repo.list_all()
    return await _decorate_many(recipes, foods)


@router.get(
    "/{recipe_id}",
    response_model=Recipe,
    responses={**ERR_404},
    summary="Get a recipe by id",
)
async def get_recipe(
    recipe_id: str,
    repo: RecipeRepository = Depends(get_recipe_repo),
    foods: FoodRepository = Depends(get_food_repo),
) -> Recipe | JSONResponse:
    recipe = await repo.get(recipe_id)
    if recipe is None:
        return recipe_not_found(recipe_id)
    return await _decorate(recipe, foods)


@router.patch(
    "/{recipe_id}",
    response_model=Recipe,
    responses={**ERR_404},
    summary="Update a recipe",
)
async def patch_recipe(
    recipe_id: str,
    body: RecipePatch,
    repo: RecipeRepository = Depends(get_recipe_repo),
    foods: FoodRepository = Depends(get_food_repo),
) -> Recipe | JSONResponse:
    try:
        recipe = await repo.patch(recipe_id, body)
    except RecipeNotFound:
        return recipe_not_found(recipe_id)
    return await _decorate(recipe, foods)


@router.delete(
    "/{recipe_id}",
    response_model=None,
    status_code=204,
    summary="Delete a recipe",
)
async def delete_recipe(
    recipe_id: str,
    repo: RecipeRepository = Depends(get_recipe_repo),
) -> Response:
    await repo.delete(recipe_id)
    return Response(status_code=204)
