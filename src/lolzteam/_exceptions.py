from __future__ import annotations

from typing import Literal


class LolzteamException(Exception):
    pass


class APIError(LolzteamException):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class APIStatusError(APIError):
    status_code: int
    message: str

    def __init__(self, message: str | None = None) -> None:
        super().__init__(f"{message or self.message}")


class BadRequestError(APIStatusError):
    status_code: Literal[400] = 400
    message = "Bad Request"


class PermissionDeniedError(APIStatusError):
    status_code: Literal[403] = 403
    message = "Forbidden"


class RateLimitError(APIStatusError):
    status_code: Literal[429] = 429
    message = "Too Many Requests"
