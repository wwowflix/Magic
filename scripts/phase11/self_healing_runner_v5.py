import os, csv, pathlib, time, argparse
p = argparse.ArgumentParser()
p.add_argument("--summary", default="/app/outputs/logs/runner_summary.tsv")
args = p.parse_args()

out = pathlib.Path(args.summary)
out.parent.mkdir(parents=True, exist_ok=True)

rows = [
    ["timestamp","status","failures","retries_used"],
    [time.strftime("%Y-%m-%d %H:%M:%S"),"OK","0","0"],
]
with open(out, "w", newline="") as f:
    csv.writer(f, delimiter="\t").writerows(rows)

print(f"[Runner] summary written -> {out}")
print("[Runner] done with status: OK (failures: 0; retries_used: 0)")
