"""Shared FastAPI dependencies — pull long-lived clients off app.state.

Each repository / client is opened once in lifespan; routes consume them via
Depends(get_*) so the call shape stays the same whether we're running locally
against ADC or in production against the Cloud Run runtime SA.
"""

from fastapi import Request

from ..services.food import FoodRepository
from ..services.journal import JournalRepository
from ..services.off import OffClient
from ..services.recipe import RecipeRepository
from ..services.user import UserRepository


def get_off(request: Request) -> OffClient:
    return request.app.state.off_client


def get_food_repo(request: Request) -> FoodRepository:
    return request.app.state.food_repo


def get_journal_repo(request: Request) -> JournalRepository:
    return request.app.state.journal_repo


def get_recipe_repo(request: Request) -> RecipeRepository:
    return request.app.state.recipe_repo


def get_user_repo(request: Request) -> UserRepository:
    return request.app.state.user_repo
