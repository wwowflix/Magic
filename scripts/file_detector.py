from __future__ import annotations

"""
MAGIC Week 0 shim for scripts.file_detector.

Goal
----
- Allow `importlib.import_module("scripts.file_detector")` to succeed.
- Avoid importing selenium or any browser drivers at import time.
- Provide minimal stand-in classes with the same kind of names that
  real code would expect, without real behaviour.
"""

from typing import Any


class FileDetector:
    """
    Minimal stand-in for Selenium's FileDetector.

    Week 0: this does essentially nothing and always returns None.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return None


class UselessFileDetector(FileDetector):
    """
    A detector that always returns None.
    """
    pass


class LocalFileDetector(FileDetector):
    """
    A detector that pretends every given path is acceptable and
    simply returns it unchanged.
    """

    def __call__(self, file_path: str, *args: Any, **kwargs: Any) -> str | None:
        return file_path


class ZipExtensionFileDetector(FileDetector):
    """
    Very minimal detector that accepts only paths ending with one of
    the provided extensions.
    """

    def __init__(self, *extensions: str) -> None:
        super().__init__()
        self.extensions = tuple(extensions)

    def __call__(self, file_path: str, *args: Any, **kwargs: Any) -> str | None:
        if any(file_path.endswith(ext) for ext in self.extensions):
            return file_path
        return None


__all__ = [
    "FileDetector",
    "UselessFileDetector",
    "LocalFileDetector",
    "ZipExtensionFileDetector",
]
