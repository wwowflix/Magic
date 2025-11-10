from __future__ import annotations

# --- MAGIC urls shim (URL) ---
from urllib.parse import urlsplit, urlunsplit, urljoin


class URL(str):
    def __new__(cls, value: str | None = None):
        return str.__new__(cls, value or "")

    # Components
    @property
    def parts(self):
        return urlsplit(str(self))

    @property
    def scheme(self) -> str:
        return self.parts.scheme

    @property
    def netloc(self) -> str:
        return self.parts.netloc

    @property
    def path(self) -> str:
        return self.parts.path

    @property
    def query(self) -> str:
        return self.parts.query

    @property
    def fragment(self) -> str:
        return self.parts.fragment

    # Builders
    def with_path(self, path: str) -> "URL":
        p = self.parts
        return URL(urlunsplit((p.scheme, p.netloc, path or "", p.query, p.fragment)))

    def with_query(self, query: str) -> "URL":
        p = self.parts
        return URL(urlunsplit((p.scheme, p.netloc, p.path, query or "", p.fragment)))

    def with_fragment(self, fragment: str) -> "URL":
        p = self.parts
        return URL(urlunsplit((p.scheme, p.netloc, p.path, p.query, fragment or "")))

    def join(self, other: str | "URL") -> "URL":
        return URL(urljoin(str(self), str(other)))


try:
    __all__
except NameError:
    __all__ = []
if "URL" not in __all__:
    __all__.append("URL")
# --- end MAGIC urls shim (URL) ---
