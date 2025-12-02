from __future__ import annotations

"""
MAGIC Week 0 stub for the third-party `yarl` package.

Goals:
- Allow `import yarl` and `from yarl import URL` to succeed.
- Provide a very small URL type that behaves like a string and exposes
  some common attributes used by HTTP helpers (scheme, host, port, path, query).
- No heavy validation or real networking concerns.

This is enough for scripts/http.py to import and potentially construct URLs
during Week 0.
"""

from typing import Any, Optional
from urllib.parse import urlparse, urlunparse, urlencode


class URL(str):
    """
    Minimal URL implementation compatible enough for light usage.

    It is a subclass of str so existing code that expects a string
    will still work.
    """

    def __new__(cls, value: str, *args: Any, **kwargs: Any) -> "URL":
        return str.__new__(cls, value)

    @property
    def _parts(self):
        # Parse on demand; cheap enough for our Week 0 use.
        return urlparse(str(self))

    @property
    def scheme(self) -> str:
        return self._parts.scheme

    @property
    def host(self) -> str:
        return self._parts.hostname or ""

    @property
    def port(self) -> Optional[int]:
        return self._parts.port

    @property
    def path(self) -> str:
        return self._parts.path

    @property
    def query(self) -> str:
        return self._parts.query

    def with_query(self, params: Any) -> "URL":
        """
        Return a new URL with the given query parameters.

        `params` can be a mapping or sequence of pairs. This is a
        simplified version of the real yarl.URL.with_query.
        """
        parts = self._parts
        query = urlencode(params, doseq=True)
        new_value = urlunparse(
            (
                parts.scheme,
                parts.netloc,
                parts.path,
                parts.params,
                query,
                parts.fragment,
            )
        )
        return URL(new_value)

    def __repr__(self) -> str:
        return f"URL({str(self)!r})"


def URL_build(
    scheme: str = "",
    host: str = "",
    port: Optional[int] = None,
    path: str = "",
    query: Any = None,
) -> URL:
    """
    A tiny helper similar to yarl.URL.build, enough for basic usage.
    """
    netloc = host
    if port is not None:
        netloc = f"{host}:{port}"
    query_str = urlencode(query, doseq=True) if query is not None else ""
    value = urlunparse((scheme, netloc, path, "", query_str, ""))
    return URL(value)


__all__ = ["URL", "URL_build"]
