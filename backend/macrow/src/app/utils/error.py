"""Error helpers — produce the `{ "error": { code, message, details } }` envelope."""

from fastapi.responses import JSONResponse

from ..models.common import ApiError, ApiErrorResponse


class OffUnavailable(Exception):
    """Raised by services.off when OFF returns 5xx, 429, or fails transport."""


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
