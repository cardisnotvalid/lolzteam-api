from __future__ import annotations

from typing import TypeVar, Generic, Union, Dict, Any
from types import TracebackType

from niquests._typing import (
    MultiPartFilesType,
    MultiPartFilesAltType,
    BodyType,
    AsyncBodyType,
    QueryParameterType
)
import niquests
from niquests import Request, PreparedRequest, Response


_T = TypeVar("_T")

_NiquestsClientT = TypeVar(
    "_NiquestsClientT", bound=Union[niquests.Session, niquests.AsyncSession]
)


class BaseClient(Generic[_NiquestsClientT]):
    __slots__ = ("_version", "_base_url", "_client")

    _version: str
    _base_url: str
    _client: _NiquestsClientT

    def __init__(self, *, version: str, base_url: str) -> None:
        self._version = version
        self._base_url = base_url

    def _build_request(
        self,
        method: str,
        url: str,
        *,
        files: MultiPartFilesType | MultiPartFilesAltType | None = None,
        data: BodyType | AsyncBodyType | None = None,
        params: QueryParameterType | None = None,
    ) -> PreparedRequest:
        req = Request(
            method=method,
            url=url,
            headers=self.default_headers,
            files=files,
            data=data,
            params=params,
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
        return {
            "Accept": "application/json",
            "User-Agent": self.user_agent,
            **self.auth_headers,
        }


class SyncAPIClient(BaseClient[niquests.Session]):
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

    def request(
        self,
        method: str,
        url: str,
        *,
        files: MultiPartFilesType | MultiPartFilesAltType | None = None,
        data: BodyType | AsyncBodyType | None = None,
        params: QueryParameterType | None = None,
    ) -> Dict[str, Any]:
        prepped = self._build_request(
            method=method,
            url=url,
            files=files,
            data=data,
            params=params
        )
        response = self._client.send(prepped)
        self._check_response(response)
        return response.json()

    def get(
        self,
        url: str,
        *,
        params: QueryParameterType | None = None
    ) -> Dict[str, Any]:
        return self.request("GET", url, params=params)

    def post(
        self,
        url: str,
        *,
        files: MultiPartFilesType | MultiPartFilesAltType | None = None,
        data: BodyType | AsyncBodyType | None = None,
        params: QueryParameterType | None = None,
    ) -> Dict[str, Any]:
        return self.request("POST", url, files=files, data=data, params=params)

    def delete(
        self,
        url: str,
        *,
        params: QueryParameterType | None = None
    ) -> Dict[str, Any]:
        return self.request("DELETE", url, params=params)

    def put(
        self,
        url: str,
        *,
        data: BodyType | AsyncBodyType | None = None,
        params: QueryParameterType | None = None,
    ) -> Dict[str, Any]:
        return self.request("PUT", url, data=data, params=params)
