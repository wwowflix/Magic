from __future__ import annotations

"""
MAGIC shim for scripts.argon2

Original module depends on `cryptography.hazmat.bindings._rust` and
Argon2 internals. For MAGIC smoke tests we only need:

- `import scripts.argon2` to succeed
- A tiny, predictable API surface

This shim provides:

- PasswordHasher: simple fake hasher with `hash()` and `verify()`
- VerifyMismatchError: basic exception type

NOTE: This is NOT a real Argon2 implementation and must NOT be used
for real security-sensitive password storage.
"""

from dataclasses import dataclass


class VerifyMismatchError(Exception):
    """Raised when password verification fails."""


@dataclass
class PasswordHasher:
    """
    Minimal stand-in for an Argon2 PasswordHasher.

    Parameters are accepted for API compatibility only.
    """

    time_cost: int = 2
    memory_cost: int = 512
    parallelism: int = 2
    hash_len: int = 16
    salt_len: int = 16

    def hash(self, password: str) -> str:
        """
        Return a deterministic fake hash.

        This is intentionally simple and NOT secure.
        """
        # Very simple marker-based "hash" for MAGIC only.
        return f"argon2$magic$${password}"

    def verify(self, encoded: str, password: str) -> bool:
        """
        Verify that an encoded value matches password.

        Raises VerifyMismatchError on mismatch.
        """
        expected = self.hash(password)
        if encoded != expected:
            raise VerifyMismatchError("Password does not match")
        return True


__all__ = ["PasswordHasher", "VerifyMismatchError"]
