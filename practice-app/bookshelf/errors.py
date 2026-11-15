"""Every error has the same shape, so tests can always check it the same way:

    {"error": {"code": "OUT_OF_STOCK", "message": "...", "request_id": "...", "details": ...}}

`code` is stable (tests can rely on it); `message` is for people and may change.
"""

from __future__ import annotations

import logging
from http import HTTPStatus
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

log = logging.getLogger("bookshelf")


class ApiError(Exception):
    def __init__(
        self,
        status: int,
        code: str,
        message: str,
        details: Any = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.details = details
        self.headers = headers


def not_found(what: str) -> ApiError:
    code = what.upper().replace(" ", "_") + "_NOT_FOUND"
    return ApiError(404, code, f"{what.capitalize()} not found.")


def error_response(
    request: Request,
    status: int,
    code: str,
    message: str,
    details: Any = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    body: dict[str, Any] = {
        "code": code,
        "message": message,
        "request_id": getattr(request.state, "request_id", None),
    }
    if details is not None:
        body["details"] = details
    return JSONResponse({"error": body}, status_code=status, headers=headers)


WEB_SKIP = ("/api", "/docs", "/openapi.json", "/static")


def web_page(request: Request, status: int, message: str):
    """Web pages get an HTML error page; the API keeps its JSON errors."""
    render = getattr(request.app.state, "render_error", None)
    if render is None or request.url.path.startswith(WEB_SKIP):
        return None
    return render(request, status, message)


def field_name(location: tuple) -> str:
    parts = [str(part) for part in location if part not in ("body", "query", "path")]
    return ".".join(parts) or "body"


def install(app: FastAPI) -> None:
    @app.exception_handler(ApiError)
    async def _api_error(request: Request, exc: ApiError):
        page = web_page(request, exc.status, exc.message)
        if page is not None:
            return page
        return error_response(request, exc.status, exc.code, exc.message, exc.details, exc.headers)

    @app.exception_handler(RequestValidationError)
    async def _validation(request: Request, exc: RequestValidationError) -> JSONResponse:
        # The input value is left out on purpose: it may be a password.
        details = [
            {"field": field_name(tuple(error["loc"])), "message": error["msg"]}
            for error in exc.errors()
        ]
        return error_response(
            request, 422, "VALIDATION_ERROR", "Some fields are missing or not valid.", details
        )

    @app.exception_handler(StarletteHTTPException)
    async def _http(request: Request, exc: StarletteHTTPException):
        phrase = HTTPStatus(exc.status_code).phrase
        if exc.status_code == 404:
            page = web_page(request, 404, "We could not find that page.")
            if page is not None:
                return page
        code = phrase.upper().replace(" ", "_").replace("-", "_")
        message = exc.detail if isinstance(exc.detail, str) else phrase
        return error_response(request, exc.status_code, code, message, headers=exc.headers)

    @app.exception_handler(Exception)
    async def _unexpected(request: Request, exc: Exception):
        log.exception("Unexpected error (request %s)", getattr(request.state, "request_id", "-"))
        response = web_page(request, 500, "Something went wrong on the server. Try again.")
        if response is None:
            response = error_response(
                request, 500, "INTERNAL_ERROR", "Something went wrong on the server."
            )
        request_id = getattr(request.state, "request_id", None)
        if request_id:
            response.headers["X-Request-ID"] = request_id
        return response
