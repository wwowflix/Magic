import sys  # noqa: I001
import os
import re
import importlib
import pathlib
import json
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]  # E:\MAGIC
SCRIPTS = ROOT / "scripts"
OUT = ROOT / "outputs" / "reports" / "readiness"
OUT.mkdir(parents=True, exist_ok=True)
ts = time.strftime("%Y%m%d_%H%M%S")
tsv = OUT / f"root_numpy_shadow_report_{ts}.tsv"

# Heuristics: known risky names & private NumPy APIs
RISKY_BASENAMES = {
    # numpy core-ish names commonly cloned/ported:
    "_asarray",
    "multiarray",
    "overrides",
    "_add_newdocs",
    "_array_function",
    "fromnumeric",
    "_methods",
    "numeric",
    "_dtype",
    "_ufunc_config",
}
PRIVATE_PATTERNS = [
    r"\bnumpy\.core\._multiarray_umath\b",
    r"\bnumpy\.compat\b",
    r"\bnumpy\._core\.function_base\b",
    r"\bnumpy\.core\.function_base\b",
]
RELATIVE_PRIVATE = [
    r"from\s+\.\s+import\s+_multiarray_umath",
]


def env_snapshot():
    info = {}
    try:
        import numpy as np

        info["numpy_version"] = getattr(np, "__version__", "?")
        info["numpy_file"] = getattr(np, "__file__", "?")
    except Exception as e:
        info["numpy_error"] = repr(e)

    info["python_version"] = sys.version.replace("\n", ")
    info["sys_path_head"] = sys.path[:5]
    info["PYTHONPATH"] = os.environ.get("PYTHONPATH", "")
    return info


def scan_repo():
    rows = []
    # 1) Shadowing detection: names in scripts/ that collide with NumPy-ish names
    for p in SCRIPTS.glob("**/*.py"):
        base = p.stem
        if base in RISKY_BASENAMES:
            rows.append(
                (
                    "SHADOW_NAME",
                    str(p.relative_to(ROOT)),
                    "High",
                    f"Local module '{base}' likely shadows NumPy internals",
                )
            )

        # 2) grep for private imports/patterns
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for pat in PRIVATE_PATTERNS:
            if re.search(pat, text):
                rows.append(
                    (
                        "PRIVATE_NUMPY_API",
                        str(p.relative_to(ROOT)),
                        "High",
                        f"Matches pattern: {pat}",
                    )
                )

        for pat in RELATIVE_PRIVATE:
            if re.search(pat, text):
                rows.append(
                    (
                        "RELATIVE_PRIVATE_IMPORT",
                        str(p.relative_to(ROOT)),
                        "High",
                        f"Relative import of private C-ext: {pat}",
                    )
                )

    # 3) Runtime import reality: which module are we actually importing?
    def origin(name):
        try:
            m = importlib.import_module(name)
            return (
                getattr(m, "__file__", "<built-in/extension>") or "<built-in/extension>"
            )
        except Exception as e:
            return f"<import error: {e!r}>"

    runtime = [
        ("RUNTIME_IMPORT", "numpy", origin("numpy")),
        ("RUNTIME_IMPORT", "numpy.core", origin("numpy.core")),
        (
            "RUNTIME_IMPORT",
            "numpy.core._multiarray_umath",
            origin("numpy.core._multiarray_umath"),
        ),
        (
            "RUNTIME_IMPORT",
            "numpy._core.function_base",
            origin("numpy._core.function_base"),
        ),
        (
            "RUNTIME_IMPORT",
            "numpy.core.function_base",
            origin("numpy.core.function_base"),
        ),
    ]

    return rows, runtime


def write_tsv(env, rows, runtime):
    with open(tsv, "w", encoding="utf-8", newline="") as f:
        f.write("Kind\tPath/Name\tSeverity\tDetail\n")
        # env header
        f.write(f"ENV\tpython\tinfo\t{env.get('python_version','?')}\n")
        f.write(
            f"ENV\tnumpy_version\tinfo\t{env.get('numpy_version', env.get('numpy_error','?'))}\n"  # noqa: E501
        )
        f.write(f"ENV\tnumpy_file\tinfo\t{env.get('numpy_file','?')}\n")
        f.write(f"ENV\tPYTHONPATH\tinfo\t{env.get('PYTHONPATH','')}\n")
        f.write(
            f"ENV\tsys.path[0:5]\tinfo\t{json.dumps(env.get('sys_path_head', []))}\n"
        )

        # findings
        for k, p, sev, d in rows:
            f.write(f"{k}\t{p}\t{sev}\t{d}\n")
        for k, name, detail in runtime:
            f.write(f"{k}\t{name}\tinfo\t{detail}\n")
    return str(tsv)


if __name__ == "__main__":
    env = env_snapshot()
    rows, runtime = scan_repo()
    path = write_tsv(env, rows, runtime)
    print(f"Saved: {path}")
