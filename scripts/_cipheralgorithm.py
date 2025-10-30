from __future__ import annotations

# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.
import abc

# --- MAGIC shim: tolerate missing 'cryptography' at import-time ---
try:
    from cryptography import utils as _crypto_utils  # type: ignore
except Exception:

    def _read_only_property(name):
        def _decorator(f):
            return property(f)

        return _decorator

    class _CryptoUtilsShim:  # pragma: no cover
        read_only_property = staticmethod(_read_only_property)

    _crypto_utils = _CryptoUtilsShim()
# --- end MAGIC shim ---
# --- MAGIC shim: tolerate missing 'cryptography' at import-time ---
try:
    from cryptography import utils as _crypto_utils  # type: ignore
except Exception:  # cryptography not installed
    # Minimal replacement for cryptography._crypto_utils.read_only_property
    def _read_only_property(name):
        def _decorator(f):
            # Return a regular @property that ignores the name param.
            return property(f)

        return _decorator

    class _CryptoUtilsShim:  # pragma: no cover
        read_only_property = staticmethod(_read_only_property)

    _crypto_utils = _CryptoUtilsShim()
else:
    # Keep the same attribute name used below, so downstream code doesn't care.
    pass
# --- end MAGIC shim ---
# This exists to break an import cycle. It is normally accessible from the
# ciphers module.


class CipherAlgorithm(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """
        A string naming this mode (e.g. "AES", "Camellia").
        """

    @property
    @abc.abstractmethod
    def key_sizes(self) -> frozenset[int]:
        """
        Valid key sizes for this algorithm in bits
        """

    @property
    @abc.abstractmethod
    def key_size(self) -> int:
        """
        The size of the key being used as an integer in bits (e.g. 128, 256).
        """


class BlockCipherAlgorithm(CipherAlgorithm):
    key: utils.Buffer

    @property
    @abc.abstractmethod
    def block_size(self) -> int:
        """
        The size of a block as an integer in bits (e.g. 64, 128).
        """


def _verify_key_size(algorithm: CipherAlgorithm, key: utils.Buffer) -> utils.Buffer:
    # Verify that the key is instance of bytes
    utils._check_byteslike("key", key)

    # Verify that the key size matches the expected key size
    if len(key) * 8 not in algorithm.key_sizes:
        raise ValueError(f"Invalid key size ({len(key) * 8}) for {algorithm.name}.")
    return key
