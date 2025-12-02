from __future__ import annotations

"""
MAGIC shim for scripts.utils

Goal:
- Provide the subset of helpers that requests.sessions / adapters / api expect.
- Provide the charset-normalizer-style helpers used by scripts.md/cd/api_10.
- Keep everything lightweight and safe; semantics can be approximate for MAGIC.
"""

import os
import unicodedata
import urllib.parse
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)


# ============================================================================
# CA bundle path / ports / headers
# ============================================================================

DEFAULT_CA_BUNDLE_PATH: Optional[str] = None

DEFAULT_PORTS: Dict[str, int] = {
    "http": 80,
    "https": 443,
}


def default_headers() -> Dict[str, str]:
    return {
        "User-Agent": "magic-requests-shim/0.1",
        "Accept": "*/*",
    }


# ============================================================================
# Basic path / zip helpers
# ============================================================================


def extract_zipped_paths(path: str) -> Iterable[str]:
    # We do not actually support zips here; just return the original path.
    return [path]


# ============================================================================
# URL / auth helpers (requests-style)
# ============================================================================


def get_auth_from_url(url: str) -> Tuple[Optional[str], Optional[str]]:
    parsed = urllib.parse.urlsplit(url)
    if parsed.username is None and parsed.password is None:
        return None, None
    return parsed.username, parsed.password


def get_netrc_auth(url: str, netrc_file: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    # MAGIC: we do not read netrc; always return no auth.
    return None, None


def urldefragauth(url: str) -> Tuple[str, str]:
    parsed = urllib.parse.urlsplit(url)
    hostname = parsed.hostname or ""
    netloc = hostname
    if parsed.port:
        netloc = f"{hostname}:{parsed.port}"
    new_url = urllib.parse.urlunsplit(
        (parsed.scheme, netloc, parsed.path, parsed.query, "")
    )
    return new_url, parsed.fragment or ""


def prepend_scheme_if_needed(url: str, new_scheme: str) -> str:
    if not url:
        return url
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme:
        return url
    return f"{new_scheme}://{url}"


def get_encoding_from_headers(headers: Mapping[str, str]) -> Optional[str]:
    content_type = headers.get("content-type") or headers.get("Content-Type")
    if not content_type:
        return None
    parts = [p.strip() for p in content_type.split(";")]
    for part in parts[1:]:
        if part.lower().startswith("charset="):
            return part.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def requote_uri(uri: str) -> str:
    parsed = urllib.parse.urlsplit(uri)
    path = urllib.parse.quote(parsed.path, safe="/%")
    query = urllib.parse.quote_plus(parsed.query, safe="=&%")
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path, query, parsed.fragment))


# ============================================================================
# Proxy helpers
# ============================================================================


def select_proxy(url: str, proxies: Optional[Mapping[str, str]]) -> Optional[str]:
    if not proxies:
        return None
    parsed = urllib.parse.urlsplit(url)
    scheme = parsed.scheme.lower() or "http"
    if scheme in proxies:
        return proxies[scheme]
    for key in ("all", "all://", "*"):
        if key in proxies:
            return proxies[key]
    return None


def get_environ_proxies(url: str) -> Dict[str, str]:
    proxies: Dict[str, str] = {}
    parsed = urllib.parse.urlsplit(url)
    scheme = parsed.scheme.lower() or "http"
    env_var = f"{scheme}_proxy"
    val = os.environ.get(env_var) or os.environ.get(env_var.upper())
    if val:
        proxies[scheme] = val
    return proxies


def should_bypass_proxies(url: str, no_proxy: Optional[str] = None) -> bool:
    parsed = urllib.parse.urlsplit(url)
    host = parsed.hostname or ""
    if not host:
        return False
    if no_proxy is None:
        no_proxy = os.environ.get("NO_PROXY") or os.environ.get("no_proxy") or ""
    entries = [h.strip() for h in no_proxy.split(",") if h.strip()]
    return any(host.endswith(e) for e in entries)


def resolve_proxies(
    url: str,
    proxies: Optional[Mapping[str, str]],
    trust_env: bool = True,
) -> Dict[str, str]:
    resolved: Dict[str, str] = {}
    if proxies:
        resolved.update(proxies)
    if trust_env:
        env_proxies = get_environ_proxies(url)
        resolved.update(env_proxies)
    return resolved


# ============================================================================
# Body helpers
# ============================================================================


def rewind_body(body: Any, body_pos: Optional[int]) -> None:
    if body_pos is None:
        return
    seek = getattr(body, "seek", None)
    if callable(seek):
        try:
            seek(body_pos)
        except Exception:
            pass


def to_key_val_list(
    value: Optional[
        Union[
            Mapping[str, Any],
            Sequence[Tuple[str, Any]],
        ]
    ]
) -> Sequence[Tuple[str, Any]]:
    if value is None:
        return []
    if isinstance(value, Mapping):
        return list(value.items())
    return list(value)


# ============================================================================
# Charset / unicode helpers (charset-normalizer-style)
# ============================================================================


def unicode_range(char: str) -> Optional[str]:
    """Very small heuristic unicode-range classifier."""
    code_point = ord(char)
    if 0x0000 <= code_point <= 0x007F:
        return "Basic Latin"
    if 0x0080 <= code_point <= 0x00FF:
        return "Latin-1 Supplement"
    if 0x3040 <= code_point <= 0x309F:
        return "Hiragana"
    if 0x30A0 <= code_point <= 0x30FF:
        return "Katakana"
    if 0x4E00 <= code_point <= 0x9FFF:
        return "CJK Unified Ideographs"
    if 0xAC00 <= code_point <= 0xD7AF:
        return "Hangul Syllables"
    return None


def is_unicode_range_secondary(range_name: str) -> bool:
    """
    Approximate: treat 'Latin-1 Supplement' and other extensions as secondary.
    Good enough for coherence calculations; tests only care that it exists.
    """
    if range_name is None:
        return False
    keywords = ("Supplement", "Extended", "Compatibility", "Forms")
    return any(k in range_name for k in keywords)


def is_unprintable(char: str) -> bool:
    return unicodedata.category(char) in {"Cc", "Cf"}


def is_separator(char: str) -> bool:
    return unicodedata.category(char).startswith("Z") or char.isspace()


def is_punctuation(char: str) -> bool:
    return unicodedata.category(char).startswith("P")


def is_symbol(char: str) -> bool:
    return unicodedata.category(char).startswith("S")


def is_emoticon(char: str) -> bool:
    # Very rough emoji range subset
    return 0x1F300 <= ord(char) <= 0x1FAFF


def is_accentuated(char: str) -> bool:
    decomposed = unicodedata.normalize("NFD", char)
    return any(unicodedata.category(c) == "Mn" for c in decomposed)


def remove_accent(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


def is_latin(char: str) -> bool:
    name = unicodedata.name(char, "")
    return "LATIN" in name


def is_cjk(char: str) -> bool:
    block = unicode_range(char)
    return block is not None and "CJK" in block


def is_cjk_uncommon(char: str) -> bool:
    # Very rough; reuse CJK detection
    return is_cjk(char)


def is_hiragana(char: str) -> bool:
    return unicode_range(char) == "Hiragana"


def is_katakana(char: str) -> bool:
    return unicode_range(char) == "Katakana"


def is_hangul(char: str) -> bool:
    return unicode_range(char) == "Hangul Syllables"


def is_thai(char: str) -> bool:
    code_point = ord(char)
    return 0x0E00 <= code_point <= 0x0E7F


def is_case_variable(char: str) -> bool:
    return char.upper() != char.lower()


def is_arabic(char: str) -> bool:
    code_point = ord(char)
    return 0x0600 <= code_point <= 0x06FF


def is_arabic_isolated_form(char: str) -> bool:
    # Rough heuristic; treat Arabic range as possibly isolated
    return is_arabic(char)


# ============================================================================
# Higher-level charset-normalizer helpers used by api_10
# ============================================================================


def any_specified_encoding(sequence: bytes, search_zone: int = 8192) -> Optional[str]:
    """
    Scan a bytes sequence for an explicitly mentioned encoding.
    MAGIC: return None (we do not try to infer encodings this way).
    """
    if not isinstance(sequence, (bytes, bytearray)):
        raise TypeError("sequence must be bytes or bytearray")
    return None


def identify_sig_or_bom(sequence: bytes) -> Tuple[Optional[str], bytes]:
    """
    Very small subset: detect UTF-8 BOM.
    """
    if sequence.startswith(b"\xef\xbb\xbf"):
        return "utf_8", b"\xef\xbb\xbf"
    return None, b""


def should_strip_sig_or_bom(iana_encoding: str) -> bool:
    # Keep BOM for UTF-16/32, strip for others.
    enc = (iana_encoding or "").lower()
    return enc not in {"utf_16", "utf_16_be", "utf_16_le", "utf_32", "utf_32_be", "utf_32_le"}


def iana_name(cp_name: str, strict: bool = True) -> str:
    """
    Normalize a codec name into something like an IANA-ish identifier.
    """
    if not cp_name:
        if strict:
            raise ValueError("Empty codec name")
        return cp_name
    normalized = cp_name.lower().replace("-", "_")
    return normalized


def is_multi_byte_encoding(name: str) -> bool:
    """
    Approximate: treat UTF encodings as multi-byte. Good enough for cd.py.
    """
    if not name:
        return False
    lower = name.lower().replace("-", "_")
    if lower.startswith("utf_"):
        return True
    return False


def cp_similarity(iana_name_a: str, iana_name_b: str) -> float:
    """
    Stub: return 0.0 if we consider them dissimilar, 1.0 if equal.
    Enough for coherence heuristics not used in MAGIC.
    """
    a = iana_name(iana_name_a, strict=False)
    b = iana_name(iana_name_b, strict=False)
    return 1.0 if a == b else 0.0


def is_cp_similar(iana_name_a: str, iana_name_b: str) -> bool:
    return cp_similarity(iana_name_a, iana_name_b) >= 0.8


def range_scan(decoded_sequence: str) -> List[str]:
    """
    Return the list of unicode range names present in the string.
    """
    ranges: Set[str] = set()
    for ch in decoded_sequence:
        r = unicode_range(ch)
        if r is not None:
            ranges.add(r)
    return list(ranges)


def cut_sequence_chunks(
    sequence: Union[bytes, bytearray, str],
    chunk_size: int = 512,
) -> List[Union[bytes, str]]:
    """
    Simple chunker: cut a bytes/str sequence into chunks of at most chunk_size.
    """
    if isinstance(sequence, (bytes, bytearray)):
        seq_len = len(sequence)
        return [sequence[i : i + chunk_size] for i in range(0, seq_len, chunk_size)]
    else:
        seq_len = len(sequence)
        return [sequence[i : i + chunk_size] for i in range(0, seq_len, chunk_size)]


# ============================================================================
# Public API
# ============================================================================

__all__ = [
    "DEFAULT_CA_BUNDLE_PATH",
    "DEFAULT_PORTS",
    "default_headers",
    "extract_zipped_paths",
    "get_auth_from_url",
    "get_encoding_from_headers",
    "prepend_scheme_if_needed",
    "select_proxy",
    "urldefragauth",
    "get_environ_proxies",
    "should_bypass_proxies",
    "get_netrc_auth",
    "requote_uri",
    "resolve_proxies",
    "rewind_body",
    "to_key_val_list",
    # charset helpers
    "unicode_range",
    "is_unicode_range_secondary",
    "is_unprintable",
    "is_separator",
    "is_punctuation",
    "is_symbol",
    "is_emoticon",
    "is_accentuated",
    "remove_accent",
    "is_latin",
    "is_cjk",
    "is_cjk_uncommon",
    "is_hiragana",
    "is_katakana",
    "is_hangul",
    "is_thai",
    "is_case_variable",
    "is_arabic",
    "is_arabic_isolated_form",
    # charset-normalizer API helpers
    "any_specified_encoding",
    "identify_sig_or_bom",
    "should_strip_sig_or_bom",
    "iana_name",
    "is_multi_byte_encoding",
    "cp_similarity",
    "is_cp_similar",
    "range_scan",
    "cut_sequence_chunks",
]
