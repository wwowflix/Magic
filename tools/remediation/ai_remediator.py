import os, json, time, re
from pathlib import Path

OUT_DIR = Path(os.environ.get("MAGIC_ROOT",".")) / "outputs" / "remediation" / "ai_suggestions"

def _now(): return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def apply_remediation_ai(script_path: str, error_text: str = "", provider: str = None):
    """
    Returns dict with suggested_patch (text), explanation (str), provider (str).
    Safe fallback uses simple heuristics so it works offline.
    """
    provider = (provider or os.environ.get("AI_PROVIDER","RULES")).upper()
    p = Path(script_path)

    try:
        src = p.read_text(encoding="utf-8")
    except Exception:
        src = ""

    suggestion = {
        "ts": _now(),
        "script": p.name,
        "provider": provider,
        "error_excerpt": error_text[:4000] if error_text else "",
        "explanation": "",
        "suggested_patch": "",
    }

    # --- safe RULES fallback (no external calls) ---
    new_src = src
    notes = []

    # fix: ensure file ends with newline (harmless, creates a real diff)
    if not new_src.endswith("\n"):
        new_src = new_src + "\n"
        notes.append("added trailing newline at EOF")

    # fix: common 'print x' -> 'print(x)' for py3 if seen
    if re.search(r"(?m)^\s*print\s+[^(\n]", new_src):
        new_src = re.sub(r"(?m)^\s*print\s+(.+)$", lambda m: f"print({m.group(1)})", new_src)
        notes.append("normalized print statements to py3 style")

    # fix: strip BOM or non-printable at file start
    if new_src.startswith("\ufeff"):
        new_src = new_src.lstrip("\ufeff")
        notes.append("removed UTF-8 BOM")

    # if indentation error hinted, replace tabs with 4 spaces (safe-ish)
    if "IndentationError" in (error_text or "") or "\t" in new_src:
        if "\t" in new_src:
            new_src = new_src.replace("\t", "    ")
            notes.append("replaced tabs with 4 spaces")

    explanation = " | ".join(notes) if notes else "no-op (baseline normalization)"

    # If we had a real provider, we would call it here and override new_src + explanation.
    # For safety and offline execution, we keep RULES fallback by default.

    suggestion["explanation"] = explanation
    suggestion["suggested_patch"] = new_src

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    logf = OUT_DIR / f"{p.stem}.jsonl"
    with open(logf, "a", encoding="utf-8") as f:
        f.write(json.dumps(suggestion, ensure_ascii=False) + "\n")

    return suggestion
