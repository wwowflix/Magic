import argparse, json, subprocess, sys, time, os, pathlib, re

ROOT = pathlib.Path(r"D:\MAGIC")
LOGS = ROOT / "outputs" / "logs"
LOGS.mkdir(parents=True, exist_ok=True)


def ensure_placeholder(path: pathlib.Path):
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("if __name__ == '__main__':\n    pass\n", encoding="utf-8")


def run_one(
    pyexe: str, file: pathlib.Path, logs_dir: pathlib.Path, timeout=20, attempts=2
):
    logs_dir.mkdir(parents=True, exist_ok=True)
    outp = logs_dir / (file.stem + "_out.txt")
    errp = logs_dir / (file.stem + "_err.txt")
    last_rc = 1
    for i in range(1, attempts + 1):
        with outp.open("a", encoding="utf-8") as out, errp.open(
            "a", encoding="utf-8"
        ) as err:
            out.write(f"=== attempt {i} @ {time.strftime('%F %T')} ===\n")
            err.write(f"=== attempt {i} @ {time.strftime('%F %T')} ===\n")
            try:
                rc = subprocess.run(
                    [pyexe, str(file)], stdout=out, stderr=err, timeout=timeout
                ).returncode
            except subprocess.TimeoutExpired:
                rc = 124
                err.write("[runner] timeout\n")
        last_rc = rc
        if rc == 0:
            break
    return last_rc, outp, errp


def write_summary(dirpath: pathlib.Path, rows):
    tsv = dirpath / "summary.tsv"
    dirpath.mkdir(parents=True, exist_ok=True)
    with tsv.open("w", encoding="utf-8") as f:
        f.write("script\tstatus\trc\tstdout\tstderr\n")
        for r in rows:
            f.write("\t".join(map(str, r)) + "\n")
    return tsv


def merge_summaries(root: pathlib.Path):
    master = root / "outputs" / "phase_master_summary.tsv"
    with master.open("w", encoding="utf-8") as fout:
        fout.write("phase\tmodule\tscript\tstatus\trc\tstdout\tstderr\n")
        for p in (root / "outputs" / "logs").glob("phase*_*"):
            m = re.match(r"phase(\d+)_(.*)", p.name)
            if not m:
                continue
            phase, module = m.group(1), m.group(2)
            s = p / "summary.tsv"
            if not s.exists():
                continue
            lines = s.read_text(encoding="utf-8").splitlines()[1:]
            for ln in lines:
                fout.write(f"{phase}\t{module}\t{ln}\n")
    return master


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=str(ROOT / "phase_manifest.json"))
    ap.add_argument("--phases", nargs="*", type=int, help="subset of phases")
    ap.add_argument("--timeout", type=int, default=20)
    args = ap.parse_args()

    py = str((ROOT / "venv" / "Scripts" / "python.exe"))
    if not os.path.exists(py):
        py = sys.executable

    data = json.loads(pathlib.Path(args.manifest).read_text(encoding="utf-8"))
    # optional phase filter
    if args.phases:
        data = [d for d in data if d.get("PhaseNumber") in set(args.phases)]

    # group by phase/module
    groups = {}
    for d in data:
        phase = d.get("PhaseNumber")
        module = d.get("Module") or "_"
        file = ROOT / d["FinalFilename"]
        groups.setdefault((phase, module), []).append(file)

    # process groups
    for (phase, module), files in sorted(groups.items()):
        outdir = LOGS / f"phase{phase}_{module}"
        rows = []
        for f in files:
            ensure_placeholder(f)
            rc, outp, errp = run_one(py, f, outdir, timeout=args.timeout, attempts=2)
            status = "PASS" if rc == 0 else "FAIL"
            rows.append(
                (
                    str(f.relative_to(ROOT)),
                    status,
                    rc,
                    str(outp.relative_to(ROOT)),
                    str(errp.relative_to(ROOT)),
                )
            )
        tsv = write_summary(outdir, rows)
        print(f"[summary] {tsv}")

    m = merge_summaries(ROOT)
    print(f"[master] {m}")


if __name__ == "__main__":
    sys.exit(main())
