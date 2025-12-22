# -*- coding: utf-8 -*-
"""MAGIC bridge: expose Trio's ABC types under scripts.abc."""

from __future__ import annotations

from trio.abc import (
    AsyncResource,
    HalfCloseableStream,
    ReceiveStream,
    SendStream,
)

__all__ = [
    "AsyncResource",
    "HalfCloseableStream",
    "ReceiveStream",
    "SendStream",
]# === MAGIC Week 0 ABC shim (appended) ===
# Provide Listener / HalfCloseableStream symbols for high-level socket helpers.

try:
    from trio.abc import (
        HalfCloseableStream as _TrioHalfCloseableStream,
        Listener as _TrioListener,
    )  # type: ignore[attr-defined]
except Exception:  # pragma: no cover - ultra-defensive fallback
    class _TrioHalfCloseableStream:  # type: ignore[too-many-ancestors]
        """Fallback base class for HalfCloseableStream shim."""
        pass

    class _TrioListener:  # type: ignore[too-many-ancestors]
        """Fallback base class for Listener shim."""
        pass

# Only define if they aren't already present in this module
if "HalfCloseableStream" not in globals():
    class HalfCloseableStream(_TrioHalfCloseableStream):  # type: ignore[misc]
        """MAGIC shim: minimal interface for type compatibility."""
        pass

if "Listener" not in globals():
    class Listener(_TrioListener):  # type: ignore[misc]
        """MAGIC shim: minimal interface for type compatibility."""
        pass
from typing import Generic, TypeVar

_T_Stream = TypeVar("_T_Stream")

try:
    from trio.abc import Listener as _RealListener  # type: ignore[attr-defined]
except Exception:  # pragma: no cover - ultra-defensive fallback
    class _RealListener:  # type: ignore[too-many-ancestors]
        """Fallback base for generic Listener shim."""
        pass


# Redefine Listener as a generic class so that Listener[T] works
class Listener(_RealListener, Generic[_T_Stream]):  # type: ignore[misc]
    """MAGIC shim: generic Listener[T] for high-level socket helpers."""
    pass

# Ensure it's exported
if "Listener" not in globals().get("__all__", []):
    try:
        __all__.append("Listener")
    except Exception:
        __all__ = [
            "AsyncResource",
            "HalfCloseableStream",
            "ReceiveStream",
            "SendStream",
            "Listener",
        ]
# === MAGIC Week 0 ABC shim – Clock / Instrument ===
# Provide Clock / Instrument symbols so scripts._trio_test can import them.

from typing import Protocol

try:
    from trio.abc import Clock as _TrioClock, Instrument as _TrioInstrument  # type: ignore[attr-defined]
except Exception:  # pragma: no cover - ultra-defensive fallback
    class _TrioClock:  # type: ignore[too-many-ancestors]
        """Fallback base for Clock shim."""
        def current_time(self) -> float:  # minimal trio-like API
            raise NotImplementedError

        def sleep_until(self, deadline: float) -> None:
            raise NotImplementedError

    class _TrioInstrument:  # type: ignore[too-many-ancestors]
        """Fallback base for Instrument shim."""
        pass


class Clock(_TrioClock):  # type: ignore[misc]
    """MAGIC shim: trio.abc.Clock-compatible type for test helpers."""
    pass


class Instrument(_TrioInstrument):  # type: ignore[misc]
    """MAGIC shim: trio.abc.Instrument-compatible type for test helpers."""
    pass


# Ensure exports list contains both
try:
    __all__.extend(["Clock", "Instrument"])
except Exception:
    try:
        __all__ = [
            "AsyncResource",
            "HalfCloseableStream",
            "ReceiveStream",
            "SendStream",
            "Listener",
            "Clock",
            "Instrument",
        ]
    except NameError:
        __all__ = ["Clock", "Instrument"]
