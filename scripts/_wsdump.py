from __future__ import annotations

"""
MAGIC shim for websocket-client's wsdump CLI entrypoint.

The real script is meant to be run as a standalone program; inside
MAGIC we only require that importing ``scripts._wsdump`` does not
raise any exceptions.
"""


def main(argv: list[str] | None = None) -> int:
    """
    No-op entry point used in tests.

    Returns 0 to indicate a successful, but effectively empty, run.
    """
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI behaviour
    raise SystemExit(main())
