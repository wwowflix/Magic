from __future__ import annotations

"""
MAGIC stub for cryptography-style OID helpers.

The real `cryptography.x509.oid` module defines lots of ObjectIdentifiers and
mapping dictionaries. For MAGIC, we only need this module to import cleanly and
provide the expected names. We do NOT need real cryptographic behaviour.
"""


class ObjectIdentifier(str):
    """Minimal stand-in for cryptography's ObjectIdentifier."""

    def __new__(cls, value: str):
        return str.__new__(cls, value)

    def __repr__(self) -> str:
        return f"ObjectIdentifier({str(self)!r})"


# --- Stub OID groups ---------------------------------------------------------


class ExtensionOID:
    """Stub ExtensionOID container."""

    SUBJECT_DIRECTORY_ATTRIBUTES = ObjectIdentifier("2.5.29.9")
    SUBJECT_KEY_IDENTIFIER = ObjectIdentifier("2.5.29.14")
    KEY_USAGE = ObjectIdentifier("2.5.29.15")


class OCSPExtensionOID:
    """Stub OCSPExtensionOID container."""

    NONCE = ObjectIdentifier("1.3.6.1.5.5.7.48.1.2")


class CRLEntryExtensionOID:
    """Stub CRLEntryExtensionOID container."""

    CERTIFICATE_ISSUER = ObjectIdentifier("2.5.29.29")


class NameOID:
    """Stub NameOID container."""

    COMMON_NAME = ObjectIdentifier("2.5.4.3")
    COUNTRY_NAME = ObjectIdentifier("2.5.4.6")
    ORGANIZATION_NAME = ObjectIdentifier("2.5.4.10")


class SignatureAlgorithmOID:
    """Stub SignatureAlgorithmOID container."""

    RSA_WITH_MD5 = ObjectIdentifier("1.2.840.113549.1.1.4")
    RSA_WITH_SHA1 = ObjectIdentifier("1.2.840.113549.1.1.5")
    RSA_WITH_SHA256 = ObjectIdentifier("1.2.840.113549.1.1.11")
    ED25519 = ObjectIdentifier("1.3.101.112")


# This mapping exists in the real module. For MAGIC we only need a dict with
# valid keys; the values are never used by our tests.
_SIG_OIDS_TO_HASH: dict[ObjectIdentifier, object | None] = {
    SignatureAlgorithmOID.RSA_WITH_MD5: None,
    SignatureAlgorithmOID.RSA_WITH_SHA1: None,
    SignatureAlgorithmOID.RSA_WITH_SHA256: None,
    SignatureAlgorithmOID.ED25519: None,
}
