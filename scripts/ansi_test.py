"""MAGIC stub for colorama.ansi_test.

The original module runs unittest.main(), which clashes with pytest arguments.
This stub keeps a lightweight callable main() used only by MAGIC smoke tests.
"""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    print("ansi_test.main() – MAGIC stub; original unittest suite disabled.")


if __name__ == "__main__":
    main()
