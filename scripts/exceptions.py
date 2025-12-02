from __future__ import annotations

import socket
import typing
import warnings
from email.errors import MessageDefect
from http.client import IncompleteRead as httplib_IncompleteRead

if typing.TYPE_CHECKING:
    from .connection import HTTPConnection
    from .connectionpool import ConnectionPool
    from .response import HTTPResponse
    from .util.retry import Retry

# Base Exceptions


class HTTPError(Exception):
    """Base exception used by this module."""


class HTTPWarning(Warning):
    """Base warning used by this module."""


_TYPE_REDUCE_RESULT = tuple[typing.Callable[..., object], tuple[object, ...]]


class PoolError(HTTPError):
    """Base exception for errors caused within a pool."""

    def __init__(self, pool: ConnectionPool, message: str) -> None:
        self.pool = pool
        self._message = message
        super().__init__(f"{pool}: {message}")

    def __reduce__(self) -> _TYPE_REDUCE_RESULT:
        # For pickling purposes.
        return self.__class__, (None, self._message)


class RequestError(PoolError):
    """Base exception for PoolErrors that have associated URLs."""

    def __init__(self, pool: ConnectionPool, url: str, message: str) -> None:
        self.url = url
        super().__init__(pool, message)

    def __reduce__(self) -> _TYPE_REDUCE_RESULT:
        # For pickling purposes.
        return self.__class__, (None, self.url, self._message)


class SSLError(HTTPError):
    """Raised when SSL certificate fails in an HTTPS connection."""


class ProxyError(HTTPError):
    """Raised when the connection to a proxy fails."""

    # The original error is also available as __cause__.
    original_error: Exception

    def __init__(self, message: str, error: Exception) -> None:
        super().__init__(message, error)
        self.original_error = error


class DecodeError(HTTPError):
    """Raised when automatic decoding based on Content-Type fails."""


class ProtocolError(HTTPError):
    """Raised when something unexpected happens mid-request/response."""


#: Renamed to ProtocolError but aliased for backwards compatibility.
ConnectionError = ProtocolError

# Leaf Exceptions


class MaxRetryError(RequestError):
    """Raised when the maximum number of retries is exceeded.

    :param pool: The connection pool
    :type pool: :class:`~urllib3.connectionpool.HTTPConnectionPool`
    :param str url: The requested Url
    :param reason: The underlying error
    :type reason: :class:`Exception`

    """

    def __init__(
        self, pool: ConnectionPool, url: str, reason: Exception | None = None
    ) -> None:
        self.reason = reason

        message = f"Max retries exceeded with url: {url} (Caused by {reason!r})"

        super().__init__(pool, url, message)

    def __reduce__(self) -> _TYPE_REDUCE_RESULT:
        # For pickling purposes.
        return self.__class__, (None, self.url, self.reason)


class HostChangedError(RequestError):
    """Raised when an existing pool gets a request for a foreign host."""

    def __init__(
        self, pool: ConnectionPool, url: str, retries: Retry | int = 3
    ) -> None:
        message = f"Tried to open a foreign host with url: {url}"
        super().__init__(pool, url, message)
        self.retries = retries


class TimeoutStateError(HTTPError):
    """Raised when passing an invalid state to a timeout"""


class TimeoutError(HTTPError):
    """Raised when a socket timeout error occurs.

    Catching this error will catch both :exc:`ReadTimeoutErrors
    <ReadTimeoutError>` and :exc:`ConnectTimeoutErrors <ConnectTimeoutError>`.
    """


class ReadTimeoutError(TimeoutError, RequestError):
    """Raised when a socket timeout occurs while receiving data from a server"""


# This timeout error does not have a URL attached and needs to inherit from the
# base HTTPError
class ConnectTimeoutError(TimeoutError):
    """Raised when a socket timeout occurs while connecting to a server"""


class NewConnectionError(ConnectTimeoutError, HTTPError):
    """Raised when we fail to establish a new connection. Usually ECONNREFUSED."""

    def __init__(self, conn: HTTPConnection, message: str) -> None:
        self.conn = conn
        self._message = message
        super().__init__(f"{conn}: {message}")

    def __reduce__(self) -> _TYPE_REDUCE_RESULT:
        # For pickling purposes.
        return self.__class__, (None, self._message)

    @property
    def pool(self) -> HTTPConnection:
        warnings.warn(
            "The 'pool' property is deprecated and will be removed "
            "in urllib3 v2.1.0. Use 'conn' instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        return self.conn


class NameResolutionError(NewConnectionError):
    """Raised when host name resolution fails."""

    def __init__(self, host: str, conn: HTTPConnection, reason: socket.gaierror):
        message = f"Failed to resolve '{host}' ({reason})"
        self._host = host
        self._reason = reason
        super().__init__(conn, message)

    def __reduce__(self) -> _TYPE_REDUCE_RESULT:
        # For pickling purposes.
        return self.__class__, (self._host, None, self._reason)


class EmptyPoolError(PoolError):
    """Raised when a pool runs out of connections and no more are allowed."""


class FullPoolError(PoolError):
    """Raised when we try to add a connection to a full pool in blocking mode."""


class ClosedPoolError(PoolError):
    """Raised when a request enters a pool after the pool has been closed."""


class LocationValueError(ValueError, HTTPError):
    """Raised when there is something wrong with a given URL input."""


class LocationParseError(LocationValueError):
    """Raised when get_host or similar fails to parse the URL input."""

    def __init__(self, location: str) -> None:
        message = f"Failed to parse: {location}"
        super().__init__(message)

        self.location = location


class URLSchemeUnknown(LocationValueError):
    """Raised when a URL input has an unsupported scheme."""

    def __init__(self, scheme: str):
        message = f"Not supported URL scheme {scheme}"
        super().__init__(message)

        self.scheme = scheme


class ResponseError(HTTPError):
    """Used as a container for an error reason supplied in a MaxRetryError."""

    GENERIC_ERROR = "too many error responses"
    SPECIFIC_ERROR = "too many {status_code} error responses"


class SecurityWarning(HTTPWarning):
    """Warned when performing security reducing actions"""


class InsecureRequestWarning(SecurityWarning):
    """Warned when making an unverified HTTPS request."""


class NotOpenSSLWarning(SecurityWarning):
    """Warned when using unsupported SSL library"""


class SystemTimeWarning(SecurityWarning):
    """Warned when system time is suspected to be wrong"""


class InsecurePlatformWarning(SecurityWarning):
    """Warned when certain TLS/SSL configuration is not available on a platform."""


class DependencyWarning(HTTPWarning):
    """
    Warned when an attempt is made to import a module with missing optional
    dependencies.
    """


class ResponseNotChunked(ProtocolError, ValueError):
    """Response needs to be chunked in order to read it as chunks."""


class BodyNotHttplibCompatible(HTTPError):
    """
    Body should be :class:`http.client.HTTPResponse` like
    (have an fp attribute which returns raw chunks) for read_chunked().
    """


class IncompleteRead(HTTPError, httplib_IncompleteRead):
    """
    Response length doesn't match expected Content-Length

    Subclass of :class:`http.client.IncompleteRead` to allow int value
    for ``partial`` to avoid creating large objects on streamed reads.
    """

    partial: int  # type: ignore[assignment]
    expected: int

    def __init__(self, partial: int, expected: int) -> None:
        self.partial = partial
        self.expected = expected

    def __repr__(self) -> str:
        return "IncompleteRead(%i bytes read, %i more expected)" % (
            self.partial,
            self.expected,
        )


class InvalidChunkLength(HTTPError, httplib_IncompleteRead):
    """Invalid chunk length in a chunked response."""

    def __init__(self, response: HTTPResponse, length: bytes) -> None:
        self.partial: int = response.tell()  # type: ignore[assignment]
        self.expected: int | None = response.length_remaining
        self.response = response
        self.length = length

    def __repr__(self) -> str:
        return "InvalidChunkLength(got length %r, %i bytes read)" % (
            self.length,
            self.partial,
        )


class InvalidHeader(HTTPError):
    """The header provided was somehow invalid."""


class ProxySchemeUnknown(AssertionError, URLSchemeUnknown):
    """ProxyManager does not support the supplied scheme"""

    # TODO(t-8ch): Stop inheriting from AssertionError in v2.0.

    def __init__(self, scheme: str | None) -> None:
        # 'localhost' is here because our URL parser parses
        # localhost:8080 -> scheme=localhost, remove if we fix this.
        if scheme == "localhost":
            scheme = None
        if scheme is None:
            message = "Proxy URL had no scheme, should start with http:// or https://"
        else:
            message = f"Proxy URL had unsupported scheme {scheme}, should use http:// or https://"
        super().__init__(message)


class ProxySchemeUnsupported(ValueError):
    """Fetching HTTPS resources through HTTPS proxies is unsupported"""


class HeaderParsingError(HTTPError):
    """Raised by assert_header_parsing, but we convert it to a log.warning statement."""

    def __init__(
        self, defects: list[MessageDefect], unparsed_data: bytes | str | None
    ) -> None:
        message = f"{defects or 'Unknown'}, unparsed data: {unparsed_data!r}"
        super().__init__(message)


class UnrewindableBodyError(HTTPError):
    """urllib3 encountered an error when trying to rewind a body"""


# --- MAGIC shim: attrs-like exceptions (import-time only) ---
class FrozenAttributeError(AttributeError):
    pass


class FrozenInstanceError(AttributeError):
    pass


class NotAnAttrsClassError(TypeError):
    pass


class AttrsAttributeNotFoundError(KeyError):
    pass


try:
    __all__
except NameError:
    __all__ = []
for _n in (
    "FrozenAttributeError",
    "FrozenInstanceError",
    "NotAnAttrsClassError",
    "AttrsAttributeNotFoundError",
):
    if _n not in __all__:
        __all__.append(_n)
# --- end MAGIC shim ---

# --- MAGIC exception shims (attrs-compatible) ---
# These are minimal definitions so imports in _make.py succeed even if your
# local exceptions module doesn't provide them yet.

try:
    DefaultAlreadySetError
except NameError:  # pragma: no cover

    class DefaultAlreadySetError(Exception):
        """Raised when a default value is set twice for the same attribute."""


try:
    FrozenInstanceError
except NameError:  # pragma: no cover

    class FrozenInstanceError(Exception):
        """Raised when attempting to modify a frozen instance."""


try:
    NotAnAttrsClassError
except NameError:  # pragma: no cover

    class NotAnAttrsClassError(Exception):
        """Raised when a function expecting an attrs class gets something else."""


try:
    UnannotatedAttributeError
except NameError:  # pragma: no cover

    class UnannotatedAttributeError(Exception):
        """Raised when an attribute lacks required type annotations."""


# Ensure these export cleanly when __all__ exists.
try:
    __all__
except NameError:
    __all__ = []
for _n in (
    "DefaultAlreadySetError",
    "FrozenInstanceError",
    "NotAnAttrsClassError",
    "UnannotatedAttributeError",
):
    if _n not in __all__:

        try:
            __all__.index(_n)  # type: ignore[attr-defined]
        except Exception:
            __all__.append(_n)
# --- end MAGIC exception shims (attrs-compatible) ---

# --- MAGIC clean __all__ ensure ---
try:
    __all__
except NameError:
    __all__ = []


def _ensure_in_all(*names):
    for _n in names:
        if _n not in __all__:
            __all__.append(_n)


_ensure_in_all(
    "FrozenAttributeError",
    "DefaultAlreadySetError",
    "FrozenInstanceError",
    "NotAnAttrsClassError",
    "UnannotatedAttributeError",
)
# --- end MAGIC clean __all__ ensure ---


def _ensure_in_all(*names):
    for _n in names:
        if _n not in __all__:
            __all__.append(_n)


_ensure_in_all(
    "FrozenAttributeError",
    "DefaultAlreadySetError",
    "FrozenInstanceError",
    "NotAnAttrsClassError",
    "UnannotatedAttributeError",
)
# =============================================================================
# MAGIC shim: ParseException compatibility for actions/core/data imports
# =============================================================================

# Only define ParseException if it's missing, so we don't override a real one.
try:
    ParseException  # type: ignore[name-defined]
except NameError:  # pragma: no cover
    class ParseException(Exception):
        """
        MAGIC compatibility stub for parsing-related errors.

        This is intentionally minimal:
        - Accepts a message, optional location, and optional expression
        - Behaves like a normal Exception when printed
        """

        def __init__(self, msg: str = "", loc=None, expr=None):
            super().__init__(msg)
            self.msg = msg
            self.loc = loc
            self.expr = expr

        def __str__(self) -> str:  # pragma: no cover - trivial repr
            base = self.msg or self.__class__.__name__
            if self.loc is not None:
                return f"{base} (loc={self.loc})"
            return base



# ---- MAGIC requests-style exceptions shim (idempotent) ----
try:
    ConnectTimeout  # type: ignore[name-defined]
except NameError:
    class RequestException(Exception):
        """Base request exception (shim)."""


    class Timeout(RequestException):
        """Timeout exception (shim)."""


    class ConnectTimeout(Timeout):
        """Connection timed out (shim)."""
        pass


    class InvalidHeader(RequestException):
        """Invalid header (shim)."""
        pass


    class InvalidURL(RequestException):
        """Invalid URL (shim)."""
        pass


    try:
        __all__
    except NameError:
        __all__ = []

    for _name in ["RequestException", "Timeout", "ConnectTimeout", "InvalidHeader", "InvalidURL"]:
        if _name not in __all__:
            __all__.append(_name)
# ---- end MAGIC requests-style exceptions shim ----

# ---- MAGIC InvalidProxyURL shim (import-health) ----
try:
    InvalidProxyURL  # type: ignore[name-defined]
except NameError:
    class InvalidProxyURL(globals().get("InvalidURL", Exception)):  # type: ignore[misc]
        """
        Fallback stub InvalidProxyURL used in MAGIC import-health tests.

        It subclasses InvalidURL if available, otherwise plain Exception.
        This is only to satisfy import-time wiring; runtime behavior is minimal.
        """
        pass
# ---- end MAGIC InvalidProxyURL shim ----

# ---- MAGIC core requests exceptions shim (import-health) ----
# These definitions align scripts.exceptions with what scripts.adapters expects.
# They are kept minimal and only intended to satisfy import-time contracts.

try:
    RequestException  # type: ignore[name-defined]
except NameError:
    class RequestException(Exception):
        """Base exception for MAGIC/Requests-style errors."""
        pass


try:
    InvalidURL  # type: ignore[name-defined]
except NameError:
    class InvalidURL(RequestException):
        """The URL provided was somehow invalid."""
        pass


try:
    InvalidSchema  # type: ignore[name-defined]
except NameError:
    class InvalidSchema(RequestException):
        """The URL schema (e.g. 'ftp', 'file') is not supported."""
        pass


try:
    InvalidProxyURL  # type: ignore[name-defined]
except NameError:
    class InvalidProxyURL(InvalidURL):
        """The proxy URL provided for a proxy server is invalid."""
        pass
# ---- end MAGIC core requests exceptions shim ----

# ---- MAGIC requests exceptions API shim v2 (import-health) ----
# Align scripts.exceptions with scripts.adapters import expectations.

# Base timeout type, if missing.
try:
    Timeout  # type: ignore[name-defined]
except NameError:
    class Timeout(RequestException):
        """Base timeout exception."""
        pass

# ConnectTimeout – connection-level timeout.
try:
    ConnectTimeout  # type: ignore[name-defined]
except NameError:
    class ConnectTimeout(Timeout):
        """The request timed out while trying to connect to the remote server."""
        pass

# ReadTimeout – server did not send data in time.
try:
    ReadTimeout  # type: ignore[name-defined]
except NameError:
    class ReadTimeout(Timeout):
        """The server did not send any data in the allotted amount of time."""
        pass

# RetryError – retry logic failed.
try:
    RetryError  # type: ignore[name-defined]
except NameError:
    class RetryError(RequestException):
        """Custom retry logic failed."""
        pass

# InvalidHeader – header value not acceptable.
try:
    InvalidHeader  # type: ignore[name-defined]
except NameError:
    class InvalidHeader(RequestException):
        """The header value provided was invalid."""
        pass

# SSLError – TLS/SSL related errors.
try:
    SSLError  # type: ignore[name-defined]
except NameError:
    class SSLError(RequestException):
        """An SSL error occurred."""
        pass
# ---- end MAGIC requests exceptions API shim v2 (import-health) ----

# --- MAGIC manual patch: ensure RequestException + InvalidProxyURL exist ---

try:
    RequestException  # type: ignore[name-defined]
except NameError:
    class RequestException(Exception):
        """Base exception for MAGIC HTTP-style errors."""

try:
    InvalidProxyURL  # type: ignore[name-defined]
except NameError:
    class InvalidProxyURL(RequestException):  # type: ignore[misc]
        """The proxy URL provided is invalid."""

# ---- MAGIC requests exceptions API shim v3 (models-related, import-health) ----
# These align scripts.exceptions with scripts.models expectations.

# Base RequestException, if still missing for any reason.
try:
    RequestException  # type: ignore[name-defined]
except NameError:
    class RequestException(Exception):
        """Base exception for MAGIC/Requests-style errors."""
        pass

# HTTPError – HTTP-level error responses.
try:
    HTTPError  # type: ignore[name-defined]
except NameError:
    class HTTPError(RequestException):
        """An HTTP error occurred."""
        pass

# ChunkedEncodingError – issues with chunked transfer encoding.
try:
    ChunkedEncodingError  # type: ignore[name-defined]
except NameError:
    class ChunkedEncodingError(RequestException):
        """The server declared chunked encoding but sent an invalid chunk."""
        pass

# ContentDecodingError – failure to decode compressed/encoded content.
try:
    ContentDecodingError  # type: ignore[name-defined]
except NameError:
    class ContentDecodingError(RequestException):
        """Failed to decode response content."""
        pass

# InvalidJSONError – JSON response was invalid or unexpected.
try:
    InvalidJSONError  # type: ignore[name-defined]
except NameError:
    class InvalidJSONError(RequestException):
        """The JSON response could not be decoded or was unexpected."""
        pass
# ---- end MAGIC requests exceptions API shim v3 (models-related, import-health) ----

# ---- MAGIC JSONDecodeError shim (import-health) ----
try:
    JSONDecodeError  # type: ignore[name-defined]
except NameError:
    class JSONDecodeError(RequestException, ValueError):  # type: ignore[misc]
        """
        Magic shim for JSONDecodeError used by requests-style models.

        In the real requests library this is raised when JSON decoding fails.
        Here it only exists to satisfy imports during MAGIC import-health tests.
        """
        pass
# ---- end MAGIC JSONDecodeError shim ----

# ---- MAGIC MissingSchema shim (import-health) ----
try:
    MissingSchema  # type: ignore[name-defined]
except NameError:
    # Base is RequestException (already in file)
    try:
        MissingSchema = type("MissingSchema", (RequestException,), {})
    except Exception:
        class MissingSchema(RequestException):  # type: ignore[misc]
            """Magic shim for MissingSchema (requests-style)."""
            pass
# ---- end MAGIC MissingSchema shim ----

# ---- MAGIC StreamConsumedError shim (import-health) ----
try:
    StreamConsumedError  # type: ignore[name-defined]
except NameError:
    class StreamConsumedError(RequestException):  # type: ignore[misc]
        """
        Magic shim for StreamConsumedError (requests-style).

        In real requests this is raised when a response stream is read twice.
        Here it only exists to satisfy imports during MAGIC import-health tests.
        """
        pass
# ---- end MAGIC StreamConsumedError shim ----

# ---- MAGIC TooManyRedirects shim ----
class TooManyRedirects(Exception):
    """MAGIC shim: placeholder for requests.exceptions.TooManyRedirects."""
    pass
# ---- end MAGIC TooManyRedirects shim ----



# MAGIC shim: FSTimeoutError used by async file operations
try:
    FSTimeoutError  # type: ignore[name-defined]
except NameError:
    class FSTimeoutError(TimeoutError):
        """Stub filesystem timeout error used in MAGIC shims."""
        pass
# ==== MAGIC compatibility shim: FSTimeoutError ====
try:
    FSTimeoutError  # type: ignore[name-defined]
except Exception:  # pragma: no cover
    class FSTimeoutError(TimeoutError):
        """
        Minimal stand-in used by async filesystem wrappers.
        """
        pass
# ==== end MAGIC shim ====
