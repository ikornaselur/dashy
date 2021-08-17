from typing import Any

import pytest


@pytest.fixture(autouse=True)
def no_http_requests(monkeypatch: Any) -> None:
    def urlopen_mock(
        self: Any, method: str, url: str, *args: Any, **kwargs: Any
    ) -> None:
        raise RuntimeError(
            f"The test was about to {method} {self.scheme}://{self.host}{url}"
        )

    monkeypatch.setattr(
        "urllib3.connectionpool.HTTPConnectionPool.urlopen", urlopen_mock
    )
