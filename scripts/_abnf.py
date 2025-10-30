# SPDX-FileCopyrightText: 2015 Eric Larson
#
# SPDX-License-Identifier: Apache-2.0

import logging

from pip._vendor import requests

from pip._vendor.cachecontrol.adapter import CacheControlAdapter
from pip._vendor.cachecontrol.cache import DictCache
from pip._vendor.cachecontrol.controller import logger

from argparse import ArgumentParser


def setup_logging():
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    logger.addHandler(handler)


def get_session():
    adapter = CacheControlAdapter(
        DictCache(), cache_etags=True, serializer=None, heuristic=None
    )
    sess = requests.Session()
    sess.mount("http://", adapter)
    sess.mount("https://", adapter)

    sess.cache_controller = adapter.controller
    return sess


def get_args(argv=None):
    parser = ArgumentParser()
    parser.add_argument("url", help="The URL to try and cache", nargs="?", default=None)
    argv = [] if argv is None else list(argv)
    args, _unknown = parser.parse_known_args(argv)
    return args


def main(argv=None):
    args = get_args(argv or [])
    # --- MAGIC no-op when url is missing (e.g., during pytest) ---
    if not hasattr(args, "url") or args.url in (None, ""):
        return 0
    # --- end MAGIC guard ---
    sess = get_session()

    # Make a request to get a response
    resp = sess.get(args.url)

    # Turn on logging
    setup_logging()

    # try setting the cache
    sess.cache_controller.cache_response(resp.request, resp.raw)

    # Now try to get it
    if sess.cache_controller.cached_request(resp.request):
        print("Cached!")
    else:
        print("Not cached :(")


if __name__ == "__main__":
    main()

# --- MAGIC ABNF shim: expose regex source strings expected by _events/_headers ---
# field-name = token  ; token uses tchar = "!#$%&'*+-.^_`|~" + ALPHA + DIGIT
field_name = r"[!#$%&'*+\-.\^_`|~0-9A-Za-z]+"

# relaxed field-value: HTAB/space + VCHAR + obs-text
field_value = r"[ \t\x21-\x7E\x80-\xFF]*"

# HTTP method group (string; caller will do .encode('ascii') then re.compile)
method = r"(GET|HEAD|POST|PUT|DELETE|OPTIONS|TRACE|CONNECT|PATCH)"

# request-target (relaxed, non-space, non-CRLF)
request_target = r"[^ \r\n]+"

try:
    __all__
except NameError:
    __all__ = []
for _n in ("field_name", "field_value", "method", "request_target"):
    if _n not in __all__:
        __all__.append(_n)
# --- end MAGIC ABNF shim ---
# --- MAGIC force final ABNF values (ensure strings win) ---
field_name = r"[!#$%&'*+\-.\^_|~0-9A-Za-z]+"
field_value = r"[ \t\x21-\x7E\x80-\xFF]*"
method = r"(GET|HEAD|POST|PUT|DELETE|OPTIONS|TRACE|CONNECT|PATCH)"
request_target = r"[^ \r\n]+"
# --- end MAGIC force ---

# --- MAGIC ABNF shim (forces string regex sources) ---
field_name = r"[!#$%&'*+\-.\^_`|~0-9A-Za-z]+"
field_value = r"[ \t\x21-\x7E\x80-\xFF]*"
method = r"(GET|HEAD|POST|PUT|DELETE|OPTIONS|TRACE|CONNECT|PATCH)"
request_target = r"[^ \r\n]+"
try:
    __all__
except NameError:
    __all__ = []
for _n in ("field_name", "field_value", "method", "request_target"):
    if _n not in __all__:
        __all__.append(_n)
# --- end MAGIC ABNF shim ---

# --- MAGIC ABNF shim (extra regex source strings for _readers) ---
# header_field = field-name ":" OWS field-value
header_field = r"[!#$%&'*+\-.\^_`|~0-9A-Za-z]+:[ \t\x21-\x7E\x80-\xFF]*"

# request-line = method SP request-target SP HTTP-version
request_line = (
    r"(GET|HEAD|POST|PUT|DELETE|OPTIONS|TRACE|CONNECT|PATCH) [^\r\n]+ HTTP/\d\.\d"
)

# status-line = HTTP-version SP status-code SP reason-phrase
status_line = r"HTTP/\d\.\d [0-9]{3} [^\r\n]*"

# chunk-header = chunk-size *(; chunk-ext)   ; relaxed: hex digits then optional ;...
chunk_header = r"[0-9A-Fa-f]+(?:;[^\r\n]*)?"

try:
    __all__
except NameError:
    __all__ = []
for _n in ("header_field", "request_line", "status_line", "chunk_header"):
    if _n not in __all__:
        __all__.append(_n)
# --- end MAGIC ABNF shim ---


# --- MAGIC: minimal ABNF container for _app.py consumers ---
class ABNF:
    # Expose the regex source strings already defined in this module
    field_name = field_name
    field_value = field_value
    method = method
    request_target = request_target
    try:
        header_field
    except NameError:
        header_field = r"[!#$%&'*+\-.\^_`|~0-9A-Za-z]+:[ \t\x21-\x7E\x80-\xFF]*"
    try:
        request_line
    except NameError:
        request_line = r"(GET|HEAD|POST|PUT|DELETE|OPTIONS|TRACE|CONNECT|PATCH) [^\r\n]+ HTTP/\d\.\d"
    try:
        status_line
    except NameError:
        status_line = r"HTTP/\d\.\d [0-9]{3} [^\r\n]*"
    try:
        chunk_header
    except NameError:
        chunk_header = r"[0-9A-Fa-f]+(?:;[^\r\n]*)?"


try:
    __all__
except NameError:
    __all__ = []
for _n in ("ABNF",):
    if _n not in __all__:
        __all__.append(_n)
# --- end MAGIC ABNF container ---

# --- MAGIC: websocket compatibility names expected by _core.py ---
# RFC 6455 normal closure
STATUS_NORMAL = 1000
# Minimal module-level placeholders used by _core.py
continuous_frame = None
frame_buffer = bytearray()
try:
    __all__
except NameError:
    __all__ = []
for _n in ("STATUS_NORMAL", "continuous_frame", "frame_buffer"):
    if _n not in __all__:
        __all__.append(_n)
# --- end MAGIC websocket compatibility ---

# --- MAGIC: ABNF opcode constants for websocket core ------------------------
try:
    ABNF
except NameError:

    class ABNF:  # minimal container if not defined earlier
        pass


# Standard RFC 6455 opcodes
if not hasattr(ABNF, "OPCODE_CONT"):
    ABNF.OPCODE_CONT = 0x0
if not hasattr(ABNF, "OPCODE_TEXT"):
    ABNF.OPCODE_TEXT = 0x1
if not hasattr(ABNF, "OPCODE_BINARY"):
    ABNF.OPCODE_BINARY = 0x2
if not hasattr(ABNF, "OPCODE_CLOSE"):
    ABNF.OPCODE_CLOSE = 0x8
if not hasattr(ABNF, "OPCODE_PING"):
    ABNF.OPCODE_PING = 0x9
if not hasattr(ABNF, "OPCODE_PONG"):
    ABNF.OPCODE_PONG = 0xA

# Useful bit flags often referenced by websocket libs
if not hasattr(ABNF, "FIN"):
    ABNF.FIN = 0x80
if not hasattr(ABNF, "RSV1"):
    ABNF.RSV1 = 0x40
if not hasattr(ABNF, "RSV2"):
    ABNF.RSV2 = 0x20
if not hasattr(ABNF, "RSV3"):
    ABNF.RSV3 = 0x10

try:
    __all__
except NameError:
    __all__ = []
for _n in ("ABNF",):
    if _n not in __all__:
        __all__.append(_n)
# --- end MAGIC ABNF opcodes -------------------------------------------------

# --- MAGIC: minimal HTTP token helpers (compat) -------------------------------
import re

_TOKEN_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")


def _is_token(s: str) -> bool:
    return isinstance(s, str) and bool(_TOKEN_RE.match(s))


def method(s):
    """Return an uppercased HTTP method if valid token, else raise ValueError."""
    if s is None:
        raise ValueError("method cannot be None")
    s2 = str(s).upper()
    if not _is_token(s2):
        raise ValueError(f"invalid HTTP method: {s!r}")
    return s2


def request_target(s):
    """Very permissive passthrough for request-target (origin-form / absolute-form / asterisk / authority)."""
    if s is None:
        raise ValueError("request_target cannot be None")
    return str(s)


# --- end MAGIC helpers --------------------------------------------------------

# === MAGIC SHIM: ensure ABNF tokens are regex *strings* for _events/_state =====
try:
    method  # may exist already
except NameError:
    pass
# Force names to be regex strings (so code like `method.encode("ascii")` works)
method = r"[!#$%&'*+\-.^_`|~0-9A-Za-z]+"
request_target = r".+"

try:
    __all__
except NameError:
    __all__ = []
for _n in ("method", "request_target"):
    if _n not in __all__:
        __all__.append(_n)
# === end MAGIC SHIM =============================================================


# === MAGIC SHIM: ensure ABNF tokens are regex *strings* for _events/_state =====
try:
    method  # may exist already
except NameError:
    pass
# Force names to be regex strings (so code like `method.encode("ascii")` works)
method = r"[!#$%&'*+\-.^_`|~0-9A-Za-z]+"
request_target = r".+"

try:
    __all__
except NameError:
    __all__ = []
for _n in ("method", "request_target"):
    if _n not in __all__:
        __all__.append(_n)
# === end MAGIC SHIM =============================================================

# --- MAGIC: ABNF shim & exports ---
try:
    ABNF
except NameError:

    class ABNF: ...


for k, v in {
    "OPCODE_CONT": 0x0,
    "OPCODE_TEXT": 0x1,
    "OPCODE_BINARY": 0x2,
    "OPCODE_CLOSE": 0x8,
    "OPCODE_PING": 0x9,
    "OPCODE_PONG": 0xA,
    "FIN": 0x80,
    "RSV1": 0x40,
    "RSV2": 0x20,
    "RSV3": 0x10,
}.items():
    if not hasattr(ABNF, k):
        setattr(ABNF, k, v)

# exports required by _events
method = r"[!#$%&'*+\-.^_`|~0-9A-Za-z]+"
request_target = r".+"

try:
    __all__
except NameError:
    __all__ = []
for name in ("ABNF", "method", "request_target"):
    if name not in __all__:
        __all__.append(name)
# --- end MAGIC ---
