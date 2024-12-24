from __future__ import annotations

import os
from typing import Dict

from ._version import __version__
from ._base_client import SyncAPIClient
from ._mixin import SyncAllMixin


class Lolzteam(SyncAPIClient, SyncAllMixin):
    __slots__ = ("_api_key",)

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        if not api_key:
            api_key = os.environ.get("LOLZTEAM_API_KEY")
        if not api_key:
            raise TypeError("The `api_key` client option must be set either "
                            "by passing `api_key` to the client or by "
                            "setting the `LOLZTEAM_API_KEY` environment "
                            "variable")
        self._api_key = api_key

        if not base_url:
            base_url = "https://api.zelenka.guru"

        super().__init__(version=__version__, base_url=base_url)

    @property
    def auth_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self._api_key}"}
