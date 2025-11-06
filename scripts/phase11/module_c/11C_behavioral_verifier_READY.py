#!/usr/bin/env python3
from __future__ import annotations
import json, math, os
from pathlib import Path
from statistics import median
from typing import Dict, List, Tuple

LOG_ROOTS = [Path("outputs/logs")]
BASELINE_PATH = Path("tools/behaviour/11C_baseline.json")
FEATURE_KEYS = ["duration_ms", "exit_code", "warn_count", "out_len"]
EMA_ALPHA = 0.2
WARN_Z = 2.5
FAIL_Z = 4.0
MIN_OBS_BEFORE_STRICT = 5

def _ensure_dirs() -> None:
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)

def _load_baseline() -> Dict:
    if BASELINE_PATH.exists():
        try:
            return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def _save_baseline(b: Dict) -> None:
    _ensure_dirs()
    BASELINE_PATH.write_text(json.dumps(b, indent=2, sort_keys=True), encoding="utf-8")

def _gather_metric_paths():
    paths = []
    for root in LOG_ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*.metrics.json"):
            paths.append(p)
        for p in root.rglob("*.json"):
            if p.name.endswith(".metrics.json"):
                continue
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                if any(k in data for k in FEATURE_KEYS):
                    paths.append(p)
            except Exception:
                pass
    seen, out = set(), []
    for p in paths:
        if p not in seen:
            seen.add(p); out.append(p)
    return out

def _extract_features(data: Dict):
    feats = {}
    for k in FEATURE_KEYS:
        v = data.get(k, None)
        if isinstance(v, (int, float)):
            feats[k] = float(v)
    return feats

def _ema_update(mean, var, x, alpha):
    if (mean is None) or (var is None) or math.isnan(mean) or math.isnan(var):
        return x, 0.0
    new_mean = (1 - alpha) * mean + alpha * x
    diff = x - new_mean
    new_var = (1 - alpha) * var + alpha * (diff * diff)
    return new_mean, max(new_var, 0.0)

def _robust_z(x, mean, var, fallback_samples):
    sd = math.sqrt(var) if (var is not None and var > 1e-12) else 0.0
    if sd <= 1e-6 and fallback_samples:
        med = median(fallback_samples)
        mad = median([abs(u - med) for u in fallback_samples]) or 1.0
        sd = 1.4826 * mad
        mean = med
    if sd <= 1e-6:
        return 0.0
    return (x - mean) / sd

def main() -> int:
    metric_paths = _gather_metric_paths()
    if not metric_paths:
        print("11C\tbehavioral_check\tWARN\tno metrics found under outputs/logs")
        return 0

    baseline = _load_baseline()
    for k in FEATURE_KEYS:
        baseline.setdefault(k, {"mean": float("nan"), "var": float("nan"), "n": 0, "recent": []})

    latest_file = max(metric_paths, key=lambda p: p.stat().st_mtime)
    try:
        latest = json.loads(latest_file.read_text(encoding="utf-8"))
    except Exception:
        print("11C\tbehavioral_check\tWARN\tlatest metrics unreadable")
        return 0

    feats = _extract_features(latest)
    if not feats:
        print("11C\tbehavioral_check\tWARN\tno recognized feature keys in latest metrics")
        return 0

    status, reasons, strict_ready = "PASS", [], True
    for k, x in feats.items():
        slot = baseline[k]
        z = _robust_z(x, slot.get("mean", float("nan")), slot.get("var", float("nan")), slot.get("recent", []))
        if abs(z) >= FAIL_Z and slot.get("n", 0) >= MIN_OBS_BEFORE_STRICT:
            status = "FAIL"; reasons.append(f"{k} z={z:.2f}")
        elif abs(z) >= WARN_Z:
            if status != "FAIL":
                status = "WARN"
            reasons.append(f"{k} z={z:.2f}")
        if slot.get("n", 0) < MIN_OBS_BEFORE_STRICT:
            strict_ready = False

        new_mean, new_var = _ema_update(slot.get("mean", float("nan")), slot.get("var", float("nan")), x, EMA_ALPHA)
        slot["mean"], slot["var"] = new_mean, new_var
        slot["n"] = int(slot.get("n", 0)) + 1
        recent = slot.get("recent", [])
        recent.append(x)
        if len(recent) > 50:
            recent = recent[-50:]
        slot["recent"] = recent
        baseline[k] = slot

    if status == "FAIL" and not strict_ready:
        status = "WARN"; reasons.append("warmup")

    _save_baseline(baseline)
    note = "ok" if not reasons else "; ".join(reasons)
    print(f"11C\tbehavioral_check\t{status}\t{note}")
    return 2 if status == "FAIL" else 0

if __name__ == "__main__":
    raise SystemExit(main())
