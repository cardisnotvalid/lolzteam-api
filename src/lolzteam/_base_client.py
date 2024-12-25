from __future__ import annotations

from types import TracebackType
from typing import TYPE_CHECKING, TypeVar, Dict, Union, Generic

import niquests

if TYPE_CHECKING:
    from niquests._typing import (
        BodyType,
        AsyncBodyType,
        QueryParameterType,
        MultiPartFilesType,
        MultiPartFilesAltType,
    )
    from niquests import PreparedRequest, Response

    from ._types import JsonType


_T = TypeVar("_T")

_NiquestsSessionT = TypeVar(
    "_NiquestsSessionT",
    bound=Union[niquests.Session, niquests.AsyncSession]
)


class Route:
    __slots__ = ("method", "url", "files", "data", "params")

    def __init__(
        self,
        method: str,
        url: str,
        *,
        files: MultiPartFilesType | MultiPartFilesAltType | None = None,
        data: BodyType | AsyncBodyType | None = None,
        params: QueryParameterType | None = None,
    ) -> None:
        self.method = method
        self.url = url
        self.files = files
        self.data = data
        self.params = params

    def __repr__(self) -> str:
        slots = []
        for slot in self.__slots__:
            slots.append(f"{slot}={repr(getattr(self, slot))}")
        return f"Route({', '.join(slots)})"


class BaseClient(Generic[_NiquestsSessionT]):
    __slots__ = ("_version", "_base_url", "_client")

    _version: str
    _base_url: str
    _client: _NiquestsSessionT

    def __init__(self, *, version: str, base_url: str) -> None:
        self._version = version
        self._base_url = base_url

    def _build_request(self, route: Route) -> PreparedRequest:
        headers = self.default_headers

        if route.files:
            headers["Content-Type"] = "multipart/form-data"
        if route.data:
            headers["Content-Type"] = "application/json"

        req = niquests.Request(
            method=route.method,
            url=route.url,
            headers=headers,
            files=route.files,
            data=route.data,
            params=route.params,
            base_url=self._base_url,
        )
        return self._client.prepare_request(req)

    # TODO: создать базоый класс для ошибок api
    def _check_response(self, response: Response) -> None:
        if not response.ok:
            errors = response.json().get("errors", [])
            msg = "; ".join(errors)
            raise niquests.RequestException(msg)

    @property
    def user_agent(self) -> str:
        return f"{self.__class__.__name__}/Python {self._version}"

    @property
    def auth_headers(self) -> Dict[str, str]:
        return {}

    @property
    def default_headers(self) -> Dict[str, str]:
        return {"User-Agent": self.user_agent, **self.auth_headers}


class SyncAPIClient(BaseClient[niquests.Session]):
    _client: niquests.Session    

    def __init__(self, *, version: str, base_url: str) -> None:
        super().__init__(version=version, base_url=base_url)
        
        self._client = niquests.Session(base_url=base_url)

    def close(self) -> None:
        if hasattr(self, "_client"):
            self._client.close()

    def __enter__(self: _T) -> _T:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def request(self, route: Route) -> JsonType:
        prepped = self._build_request(route)
        response = self._client.send(prepped)
        self._check_response(response)
        return response.json()

    def get(
        self,
        path: str,
        *,
        params: QueryParameterType | None = None
    ) -> JsonType:
        return self.request(Route("GET", path, params=params))

    def post(
        self,
        path: str,
        *,
        files: MultiPartFilesType | MultiPartFilesAltType | None = None,
        data: BodyType | AsyncBodyType | None = None,
        params: QueryParameterType | None = None,
    ) -> JsonType:
        return self.request(
            Route("POST", path, files=files, data=data, params=params)
        )

    def delete(
        self,
        path: str,
        *,
        params: QueryParameterType | None = None
    ) -> JsonType:
        return self.request(Route("DELETE", path, params=params))

    def put(
        self,
        path: str,
        *,
        data: BodyType | AsyncBodyType | None = None,
        params: QueryParameterType | None = None,
    ) -> JsonType:
        return self.request(Route("PUT", path, data=data, params=params))
