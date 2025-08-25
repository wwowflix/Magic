# ranks failures by recency + frequency (stub)
import json, time, os
def prioritize(fails_json, out_path):
    if not os.path.exists(fails_json):
        return []
    data = json.loads(open(fails_json, 'r', encoding='utf-8').read() or '[]')
    ranked = sorted(data, key=lambda x: (x.get('count',0), x.get('last_ts','')), reverse=True)
    open(out_path, 'w', encoding='utf-8').write(json.dumps(ranked[:50], ensure_ascii=False, indent=2))
    return ranked
if __name__ == "__main__":
    os.makedirs("outputs/remediation", exist_ok=True)
    out = "outputs/remediation/prioritized_failures.json"
    print(len(prioritize("outputs/fail/fail_summary.json", out)))
