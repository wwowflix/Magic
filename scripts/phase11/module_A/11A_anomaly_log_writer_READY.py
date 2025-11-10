# -*- coding: utf-8 -*-
# MAGIC_SOFT_IMPORT_WRAP v1
import os, warnings
_MAGIC_SOFT = os.environ.get("MAGIC_ALLOW_SOFT_IMPORT", "1") == "1"
try:
    # MAGIC_CLEAN_V1
    from pathlib import Path
    import os, sys, datetime

    # Robust project root
    _ROOT = Path(__file__).resolve()
    _tmp = _ROOT
    for _ in range(6):
        if (_tmp / ".git").exists() or (_tmp / "outputs").exists():
            _ROOT = _tmp
            break
        _tmp = _tmp.parent
    else:
        _ROOT = Path(__file__).resolve().parents[4]

    LOG_DIR = _ROOT / "outputs" / "logs"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE = LOG_DIR / "11A_anomaly_log_writer_report.txt"

    def find_anomalies():
        """Very light checks that can never hard-fail the orchestrator."""
        anomalies = []
        phase11 = _ROOT / "scripts" / "phase11"
        if not phase11.exists():
            anomalies.append(("info", f"phase11 folder not found: {phase11}"))
            return anomalies
        # Example anomalies: zero-byte files or strict utf-8 decode trouble
        for p in phase11.rglob("*.py"):
            try:
                data = p.read_text(encoding="utf-8", errors="strict")
                if len(data) == 0:
                    anomalies.append(("zero-byte", str(p)))
            except Exception as e:
                anomalies.append(("decode-error", f"{p} | {e}"))
        return anomalies

    def main():
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
        anomalies = find_anomalies()
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            ts = datetime.datetime.now().isoformat(timespec="seconds")
            f.write(f"[{ts}] anomalies={len(anomalies)}\n")
            for kind, msg in anomalies[:200]:
                f.write(f"{kind} | {msg}\n")
        print("OK")

    if __name__ == "__main__":
        main()

except Exception as _e:
    if _MAGIC_SOFT:
        warnings.warn(f"soft-import: {_e.__class__.__name__}: {_e}")
    else:
        raise
