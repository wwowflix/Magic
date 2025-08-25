# minimal "auto-fix" stub: logs a remediation metrics entry
import json, os, time
METRICS = "outputs/remediation/remediate_metrics.json"
def append_metric(applied: int, attempted: int):
    os.makedirs(os.path.dirname(METRICS), exist_ok=True)
    try:
        arr = json.loads(open(METRICS, 'r', encoding='utf-8').read() or "[]")
    except:
        arr = []
    arr.append({
        "attempted": attempted,
        "applied": applied,
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    })
    open(METRICS, 'w', encoding='utf-8').write(json.dumps(arr, ensure_ascii=False, indent=2))
if __name__ == "__main__":
    append_metric(applied=1, attempted=1)
    print("remediation recorded")
