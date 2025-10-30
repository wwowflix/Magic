# UTF-8 no BOM
# Minimal DefaultTable shim so relative imports like `from . import DefaultTable` work in smoke tests.


class DefaultTable:
    """Lightweight table base for smoke-time imports."""

    def __init__(self, tag=None):
        self.tag = tag

    def decompile(self, data, ttFont=None):
        # Accept bytes but do nothing – smoke tests care only that import succeeds.
        self._raw = data

    def compile(self, ttFont=None):
        # Return empty bytes to be safe if something calls compile()
        return b""

    def toXML(self, writer, ttFont=None):
        # Optional: keep quiet in smoke
        pass

    def fromXML(self, name, attrs, content, ttFont=None):
        pass


__all__ = ["DefaultTable"]
