# tools/emit_metrics_from_summaries.py
import os, time, json, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SUM_DIR = os.path.join(ROOT, "outputs", "summaries")
OUT_DIR = os.path.join(ROOT, "outputs", "metrics")

def parse_tsv(path):
    pass_count = fail_count = 0
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == 0:  # header
                continue
            cols = [c.strip() for c in line.split("\t")]
            if len(cols) >= 2:
                status = cols[1].upper()
                if status == "PASS": pass_count += 1
                elif status == "FAIL": fail_count += 1
    return pass_count, fail_count

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    summaries = glob.glob(os.path.join(SUM_DIR, "phase*_module_*_summary.tsv"))
    total_pass = total_fail = 0
    modules = {}
    for p in summaries:
        mod = os.path.splitext(os.path.basename(p))[0]
        p_count, f_count = parse_tsv(p)
        modules[mod] = {"pass": p_count, "fail": f_count}
        total_pass += p_count
        total_fail += f_count

    metrics = {
        "timestamp": int(time.time()),
        "modules": modules,
        "totals": {"pass": total_pass, "fail": total_fail}
    }
    out = os.path.join(OUT_DIR, f"run_{int(time.time())}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print(f"Wrote metrics: {out}")

if __name__ == "__main__":
    main()
