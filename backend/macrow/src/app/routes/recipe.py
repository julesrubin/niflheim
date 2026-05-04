"""Recipe CRUD routes.

Five endpoints over a single Firestore collection. iOS today consumes only the
list endpoint, but shipping the full surface unblocks an editor screen without
a follow-up backend step.
"""

import logging

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse

from ..models.recipe import Recipe, RecipeCreate, RecipePatch
from ..services.recipe import RecipeRepository
from ..utils.error import RecipeNotFound, recipe_not_found

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recipes", tags=["recipes"])


def get_recipe_repo(request: Request) -> RecipeRepository:
    return request.app.state.recipe_repo


@router.post("", response_model=Recipe)
async def create_recipe(
    body: RecipeCreate,
    repo: RecipeRepository = Depends(get_recipe_repo),
) -> Recipe:
    return await repo.create(body)


@router.get("", response_model=list[Recipe])
async def list_recipes(
    repo: RecipeRepository = Depends(get_recipe_repo),
) -> list[Recipe]:
    return await repo.list_all()


@router.get("/{recipe_id}", response_model=Recipe)
async def get_recipe(
    recipe_id: str,
    repo: RecipeRepository = Depends(get_recipe_repo),
) -> Recipe | JSONResponse:
    recipe = await repo.get(recipe_id)
    if recipe is None:
        return recipe_not_found(recipe_id)
    return recipe


@router.patch("/{recipe_id}", response_model=Recipe)
async def patch_recipe(
    recipe_id: str,
    body: RecipePatch,
    repo: RecipeRepository = Depends(get_recipe_repo),
) -> Recipe | JSONResponse:
    try:
        return await repo.patch(recipe_id, body)
    except RecipeNotFound:
        return recipe_not_found(recipe_id)


@router.delete("/{recipe_id}", response_model=None)
async def delete_recipe(
    recipe_id: str,
    repo: RecipeRepository = Depends(get_recipe_repo),
) -> Response:
    await repo.delete(recipe_id)
    return Response(status_code=204)
