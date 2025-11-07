# -*- coding: utf-8 -*-
"""Minimal MultipartStream shim used by scripts._content."""

from __future__ import annotations
from typing import Iterable, Iterator, Mapping, Optional, Union

__all__ = ["MultipartStream"]

CRLF = b"\r\n"

def _to_bytes(chunk: Union[str, bytes]) -> bytes:
    return chunk.encode("utf-8") if isinstance(chunk, str) else chunk

class MultipartStream:
    """
    Tiny helper to build multipart/form-data bodies.

    Example:
        mp = MultipartStream(boundary="----MAGICBOUNDARY")
        body = b"".join(mp.iter_bytes([
            ({"name": "field1"}, b"value"),
            ({"name": "file", "filename": "a.txt"}, b"hello"),
        ]))
        headers = {"content-type": mp.content_type}
    """

    def __init__(self, boundary: Union[str, bytes]) -> None:
        self.boundary: bytes = _to_bytes(boundary)

    @property
    def content_type(self) -> str:
        return f'multipart/form-data; boundary={self.boundary.decode("utf-8", "ignore")}'

    def iter_bytes(
        self,
        parts: Iterable[
            tuple[
                Optional[Mapping[str, str]],
                Union[bytes, str, Iterable[Union[bytes, str]]],
                Optional[Mapping[str, str]]
            ] |
            tuple[Optional[Mapping[str, str]], Union[bytes, str, Iterable[Union[bytes, str]]]]
        ],
    ) -> Iterator[bytes]:
        b = self.boundary
        for part in parts:
            if len(part) == 2:
                params, payload = part  # type: ignore[misc]
                extra = None
            else:
                params, payload, extra = part  # type: ignore[misc]

            yield b"--" + b + CRLF
            disp = ["form-data"]
            if params:
                for k, v in params.items():
                    disp.append(f'{k}="{v}"')
            yield _to_bytes("Content-Disposition: " + "; ".join(disp)) + CRLF

            if extra:
                for k, v in extra.items():
                    yield _to_bytes(f"{k}: {v}") + CRLF

            yield CRLF
            if isinstance(payload, (bytes, str)):
                yield _to_bytes(payload) + CRLF
            else:
                for chunk in payload:
                    yield _to_bytes(chunk)
                yield CRLF

        yield b"--" + b + b"--" + CRLF
