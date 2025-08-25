# writes a simple alert record (stub for Notion)
import json, os, time, sys
ALERTS = "outputs/remediation/alert_log.jsonl"
msg = " ".join(sys.argv[1:]) or "Week11: remediation ready"
os.makedirs(os.path.dirname(ALERTS), exist_ok=True)
with open(ALERTS, "a", encoding="utf-8") as f:
    f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "msg": msg}) + "\n")
print("alert logged")
