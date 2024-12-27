from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from niquests import PreparedRequest, Response


class LolzteamException(Exception):
    pass


class APIError(LolzteamException):
    message: str
    request: PreparedRequest | None
    body: object | None

    def __init__(
        self,
        message: str,
        request: PreparedRequest | None,
        *,
        body: object | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.request = request
        self.body = body


class APIStatusError(APIError):
    response: Response
    status_code: int | None

    def __init__(
        self,
        message: str,
        *,
        response: Response,
        body: object | None = None
    ) -> None:
        super().__init__(message, response.request, body=body)
        self.response = response
        self.status_code = response.status_code


class RateLimitError(APIStatusError):
    status_code = 429
