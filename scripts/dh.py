"""
MAGIC Week 0: safe stub for scripts.dh (Diffie–Hellman bindings).

Goal:
- Let "import scripts.dh" succeed even without the cryptography package.
- Provide minimal placeholder classes/functions that look like a DH API.
- Do NOT perform any real cryptographic operations. This is NOT secure.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class DHParameters:
    """Very small placeholder for DH parameter object."""
    key_size: int = 2048

    def generate_private_key(self) -> "DHPrivateKey":
        # Week 0: return a dummy private key object
        return DHPrivateKey(parameters=self)


@dataclass
class DHPrivateKey:
    """Very small placeholder for DH private key."""
    parameters: DHParameters

    def public_key(self) -> "DHPublicKey":
        return DHPublicKey(parameters=self.parameters)


@dataclass
class DHPublicKey:
    """Very small placeholder for DH public key."""
    parameters: DHParameters


def generate_parameters(generator: int, key_size: int, backend: Any | None = None) -> DHParameters:
    """
    Week 0 stub for cryptography.hazmat.primitives.asymmetric.dh.generate_parameters.
    We ignore generator/backend and just return a DHParameters stub.
    """
    return DHParameters(key_size=key_size)


def generate_private_key(parameters: DHParameters, backend: Any | None = None) -> DHPrivateKey:
    """
    Week 0 stub for cryptography.hazmat.primitives.asymmetric.dh.generate_private_key.
    """
    return DHPrivateKey(parameters=parameters)


__all__ = [
    "DHParameters",
    "DHPublicKey",
    "DHPrivateKey",
    "generate_parameters",
    "generate_private_key",
]
