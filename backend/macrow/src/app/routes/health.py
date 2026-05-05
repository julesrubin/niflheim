from fastapi import APIRouter

from ..models.common import CamelModel

router = APIRouter(tags=["health"])


class HealthResponse(CamelModel):
    status: str


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Liveness probe (auth-exempt)",
)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")
