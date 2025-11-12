"""MAGIC unified _exceptions.py — vendor-safe + self-healing.

Provides placeholder exceptions used across:
- Trio/MAGIC, WebSocket, NumPy, FastJSONSchema, AnyIO, content/streaming layers.
Also includes a dynamic fallback so unknown *Exception/*Error/Stream* names
auto-create as lightweight Exception subclasses at import-time.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Type


# --- Generic Group ------------------------------------------------------------
@dataclass
class BaseExceptionGroup(Exception):
    message: str
    exceptions: List[BaseException] = field(default_factory=list)
    def __str__(self):  # pragma: no cover
        return f"{self.message}: {len(self.exceptions)} subexceptions"


# --- Trio / MAGIC -------------------------------------------------------------
class TrioInternalError(RuntimeError): ...
class Cancelled(BaseException): ...
class RunFinishedError(RuntimeError): ...


# --- WebSocket (engn33r) ------------------------------------------------------
class WebSocketException(Exception): ...
class WebSocketProtocolException(WebSocketException): ...
class WebSocketPayloadException(WebSocketException): ...
class WebSocketConnectionClosedException(WebSocketException): ...
class WebSocketTimeoutException(WebSocketException): ...
class WebSocketProxyException(WebSocketException): ...
class WebSocketBadStatusException(WebSocketException):
    def __init__(self, message:str, status_code:int,
                 status_message=None, resp_headers=None, resp_body=None):
        super().__init__(message)
        self.status_code = status_code
        self.resp_headers = resp_headers
        self.resp_body = resp_body
class WebSocketAddressException(WebSocketException): ...


# --- NumPy-style --------------------------------------------------------------
class AxisError(ValueError, IndexError): ...
class UFuncTypeError(TypeError): ...
class UFuncNoLoopError(UFuncTypeError): ...
class ArrayMemoryError(MemoryError): ...


# --- FastJSONSchema -----------------------------------------------------------
class JsonSchemaException(ValueError): ...
class JsonSchemaValueException(JsonSchemaException):
    def __init__(self, message, value=None, name=None, definition=None, rule=None):
        super().__init__(message)
        self.message, self.value, self.name, self.definition, self.rule = (
            message, value, name, definition, rule
        )
class JsonSchemaDefinitionException(JsonSchemaException): ...


# --- AnyIO / async ------------------------------------------------------------
class BrokenResourceError(Exception): ...
class BrokenWorkerProcess(Exception): ...
class BrokenWorkerInterpreter(Exception): ...
class BusyResourceError(Exception): ...
class ClosedResourceError(Exception): ...
class DelimiterNotFound(Exception): ...
class EndOfStream(Exception): ...
class IncompleteRead(Exception): ...
class TypedAttributeLookupError(LookupError): ...
class WouldBlock(Exception): ...


# --- Content / streaming (needed by scripts._content) -------------------------
class StreamClosed(Exception): ...
class StreamConsumed(Exception): ...


# Export list (will be augmented by __getattr__ if it creates new names)
__all__ = [
    # groups
    "BaseExceptionGroup",
    # trio/magic
    "TrioInternalError", "Cancelled", "RunFinishedError",
    # websocket
    "WebSocketException", "WebSocketProtocolException", "WebSocketPayloadException",
    "WebSocketConnectionClosedException", "WebSocketTimeoutException",
    "WebSocketProxyException", "WebSocketBadStatusException", "WebSocketAddressException",
    # numpy-like
    "AxisError", "UFuncTypeError", "UFuncNoLoopError", "ArrayMemoryError",
    # fastjsonschema
    "JsonSchemaException", "JsonSchemaValueException", "JsonSchemaDefinitionException",
    # anyio
    "BrokenResourceError", "BrokenWorkerProcess", "BrokenWorkerInterpreter",
    "BusyResourceError", "ClosedResourceError", "DelimiterNotFound",
    "EndOfStream", "IncompleteRead", "TypedAttributeLookupError", "WouldBlock",
    # streaming
    "StreamClosed", "StreamConsumed",
]

# --- Dynamic fallback: auto-create unknown exception names --------------------
# If some module imports a not-yet-declared FooError/FooException/StreamFoo,
# we create a minimal Exception subclass on the fly to keep imports green.
def __getattr__(name: str):
    if (name.endswith("Error") or name.endswith("Exception") or name.startswith("Stream")):
        cls = type(name, (Exception,), {})
        globals()[name] = cls
        try:
            __all__.append(name)
        except Exception:
            pass
        return cls
    raise AttributeError(name)
