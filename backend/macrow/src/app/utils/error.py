"""Error helpers — produce the `{ "error": { code, message, details } }` envelope."""

from fastapi.responses import JSONResponse

from ..models.common import ApiError, ApiErrorResponse


class OffUnavailable(Exception):
    """Raised by services.off when OFF returns 5xx, 429, or fails transport."""


class JournalItemNotFound(Exception):
    """Raised by services.journal when a logged-food item can't be located in any meal."""


def error_response(
    status_code: int,
    code: str,
    message: str,
    details: dict | None = None,
) -> JSONResponse:
    """Build a JSONResponse carrying the standard error envelope."""
    return JSONResponse(
        status_code=status_code,
        content=ApiErrorResponse(
            error=ApiError(code=code, message=message, details=details)
        ).model_dump(by_alias=True),
    )


def not_implemented(message: str = "Not yet implemented.") -> JSONResponse:
    return error_response(501, "NOT_IMPLEMENTED", message)


def barcode_not_found(barcode: str) -> JSONResponse:
    return error_response(
        404,
        "BARCODE_NOT_FOUND",
        f"Barcode {barcode!r} is unknown to Open Food Facts.",
        {"barcode": barcode},
    )


def off_unavailable() -> JSONResponse:
    return error_response(
        502,
        "OFF_UNAVAILABLE",
        "Open Food Facts is temporarily unavailable.",
    )


def invalid_date(value: str) -> JSONResponse:
    return error_response(
        400,
        "INVALID_DATE",
        f"Date {value!r} must be formatted as YYYY-MM-DD.",
        {"date": value},
    )


def invalid_meal_kind(value: str, allowed: tuple[str, ...]) -> JSONResponse:
    return error_response(
        400,
        "INVALID_MEAL_KIND",
        f"Meal kind {value!r} must be one of {list(allowed)}.",
        {"kind": value, "allowed": list(allowed)},
    )


def journal_item_not_found(item_id: str) -> JSONResponse:
    return error_response(
        404,
        "JOURNAL_ITEM_NOT_FOUND",
        f"No logged-food item with id {item_id!r} on this day.",
        {"itemId": item_id},
    )
