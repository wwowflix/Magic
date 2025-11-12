# --- MAGIC shim: AsyncGenerators (import-safe no-op) ---
try:
    AsyncGenerators  # type: ignore[name-defined]
except NameError:
    class AsyncGenerators:  # minimal no-op to satisfy attrs.Factory
        def __init__(self) -> None:
            pass
