from __future__ import annotations
import sys, types

def s(msg: str) -> None:
    """Safe print for Windows cp1252 consoles."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", "replace").decode("ascii"))

def main() -> None:
    try:
        import fontTools.ttLib.tables.otTables as otTables  # type: ignore
    except Exception as e:
        s(f"[warn] fontTools not importable: {e}")
        sys.exit(0)

    try:
        if not hasattr(otTables, "FeatureParamsCharacterVariants"):
            class FeatureParamsCharacterVariants:  # noqa: N801
                pass
            otTables.FeatureParamsCharacterVariants = FeatureParamsCharacterVariants
            s("[ok] injected FeatureParamsCharacterVariants")
        else:
            s("[info] FeatureParamsCharacterVariants already present")
    except Exception as e:
        s(f"[warn] failed to inject shim: {e}")

    sys.exit(0)

if __name__ == "__main__":
    main()
