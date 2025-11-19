from __future__ import annotations

"""
MAGIC shim for scripts.api

Two roles:

1. Small "requests-style" public API:
   - request(), get(), post(), put(), delete(), head(), options(), patch()
   - session() → creates a requests-like Session from scripts.sessions

2. Minimal "platformdirs-style" API:
   - PlatformDirsABC base class that android.py can import.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

from . import sessions as _sessions


def request(method: str, url: str, **kwargs: Any):
    s = _sessions.Session()
    return s.request(method=method, url=url, **kwargs)


def get(url: str, **kwargs: Any):
    return request("GET", url, **kwargs)


def post(url: str, **kwargs: Any):
    return request("POST", url, **kwargs)


def put(url: str, **kwargs: Any):
    return request("PUT", url, **kwargs)


def delete(url: str, **kwargs: Any):
    return request("DELETE", url, **kwargs)


def head(url: str, **kwargs: Any):
    return request("HEAD", url, **kwargs)


def options(url: str, **kwargs: Any):
    return request("OPTIONS", url, **kwargs)


def patch(url: str, **kwargs: Any):
    return request("PATCH", url, **kwargs)


def session() -> "_sessions.Session":
    return _sessions.Session()


@dataclass
class PlatformDirsABC(ABC):
    appname: Optional[str] = None
    appauthor: Optional[str] = None
    roaming: bool = False
    ensure_exists: bool = False

    @abstractmethod
    def user_data_dir(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def site_data_dir(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def user_config_dir(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def site_config_dir(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def user_cache_dir(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def user_state_dir(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def user_log_dir(self) -> str:
        raise NotImplementedError


__all__ = [
    "request",
    "get",
    "post",
    "put",
    "delete",
    "head",
    "options",
    "patch",
    "session",
    "PlatformDirsABC",
]
