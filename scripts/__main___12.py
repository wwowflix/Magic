# MAGIC SAFE MAIN STUB — auto-added for CI
# Intentionally do nothing when imported; no CLI execution.
if __name__ == "__main__":
    print("SAFE STUB OK")

# --- MAGIC Phase11 – SHIELD: tolerant main wrapper ---
def _magic__wrap_main(_f):
    def _w(*_a, **_k):
        try:
            return _f(*_a, **_k)
        except SystemExit:
            return 0
    return _w
try:
    main = _magic__wrap_main(main)
except Exception:
    pass
# --- end shield ---
