# MAGIC: CI import-safe stub for pip runner.
# Importing this module must be a no-op for smoke tests.
if __name__ != "__main__":
    __pip_runner_import_safe__ = True  # sentinel for tests if needed
else:
    # When executed as a script, behave like the original:
    import runpy
if __name__ == "__main__":
        runpy.run_module("pip", run_name="__main__", alter_sys=True)

else:
    def main(*_a, **_k): return 0
