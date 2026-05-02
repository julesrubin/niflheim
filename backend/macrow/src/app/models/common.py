from enum import StrEnum

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        from_attributes=True,
    )


class ServingUnit(StrEnum):
    g = "g"
    ml = "ml"


class NutriScore(StrEnum):
    a = "A"
    b = "B"
    c = "C"
    d = "D"
    e = "E"


class ApiError(CamelModel):
    code: str
    message: str
    details: dict | None = None


class ApiErrorResponse(CamelModel):
    error: ApiError
