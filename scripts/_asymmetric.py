__doc__ = "MAGIC: header restored; malformed preamble removed."

import abc


class AsymmetricPadding(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """
        A string naming this padding (e.g. "PSS", "PKCS1").
        """
